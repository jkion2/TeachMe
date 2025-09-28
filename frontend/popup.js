/**
 * Main Layout JavaScript
 * Handles sidebar interactions, input management, and navigation
 */

// DOM Elements
const sidebar = document.getElementById("sidebar")
const collapseBtn = document.getElementById("collapseBtn")
const textInput = document.getElementById("textInput")
const imageInput = document.getElementById("imageInput")
const contextInput = document.getElementById("contextInput")
const submitBtn = document.getElementById("submitBtn")
const fileName = document.getElementById("fileName")

// State Management
let isCollapsed = false
const API_URL = "http://127.0.0.1:8000"

// Initialize Event Listeners
document.addEventListener("DOMContentLoaded", () => {
  setupEventListeners()
  console.log("Main layout initialized")
})

function setupEventListeners() {
  // Sidebar collapse/expand
  collapseBtn.addEventListener("click", toggleSidebar)

  // File upload handling
  imageInput.addEventListener("change", handleFileUpload)

  // Submit button
  submitBtn.addEventListener("click", handleSubmit)

  // Input validation
  textInput.addEventListener("input", validateInputs)
  contextInput.addEventListener("input", validateInputs)

  // Chat functionality
  const chatSendBtn = document.getElementById("chatSendBtn")
  const chatInput = document.getElementById("chatInput")
  chatSendBtn.addEventListener("click", handleChatSend)

  chatInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault()
        handleChatSend()
    }
  })
  // Auto-resize chat input
  chatInput.addEventListener("input", autoResizeChatInput)
}

// Fixed chat send function with proper API integration
async function handleChatSend() {
    const chatInput = document.getElementById("chatInput")
    const message = chatInput.value.trim()
    
    if (!message) return
    
    // Add user message to chat
    addChatMessage("user", message)
    
    // Clear input and disable send button
    chatInput.value = ""
    const chatSendBtn = document.getElementById("chatSendBtn")
    chatSendBtn.disabled = true
    
    try {
        console.log("Sending chat message to API:", message)
        
        // Make API call
        const response = await fetch(`${API_URL}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                context: message, // Use the chat message as context
                image: "TEXT_PLACEHOLDER"
            })
        })

        if (!response.ok) {
            throw new Error(`API error: ${response.statusText}`)
        }

        const result = await response.json()
        console.log("Chat API Response:", result)
        
        // Extract and clean the response
        const summaryText = result.text || "No summary provided."
        const linksHtml = result.html_links
        const cleanSummary = summaryText.replace("##ADK_RESPONSE_END##", "").trim()
        
        // Add assistant response to chat
        addChatMessage("assistant", cleanSummary)
        
        // Add HTML links if available
        if (linksHtml) {
            addHtmlMessage("assistant-html", linksHtml)
        }
        
    } catch (error) {
        console.error("Error during chat API call:", error)
        addChatMessage("assistant", "Sorry, I encountered an error. Please try again.")
    } finally {
        // Re-enable send button
        chatSendBtn.disabled = false
    }
}

function autoResizeChatInput() {
    const chatInput = document.getElementById("chatInput")
    chatInput.style.height = "auto"
    chatInput.style.height = Math.min(chatInput.scrollHeight, 100) + "px"
}

// Sidebar Functions
function toggleSidebar() {
  isCollapsed = !isCollapsed
  sidebar.classList.toggle("collapsed")
  collapseBtn.textContent = isCollapsed ? "→" : "←"
  console.log("Sidebar toggled:", isCollapsed ? "collapsed" : "expanded")
}

// File Upload Functions
function handleFileUpload(event) {
  const file = event.target.files[0]
  if (file) {
    fileName.textContent = file.name
    // Clear text input when image is uploaded
    textInput.value = ""
    console.log("Image uploaded:", file.name)
    validateInputs()
  }
}

// Input Validation
function validateInputs() {
  const hasText = textInput.value.trim().length > 0
  const hasImage = imageInput.files.length > 0

  // Enable submit if either text or image is provided
  submitBtn.disabled = !(hasText || hasImage)
}

// Modified Submit Function - handles initial submission and switches to chat mode
async function handleSubmit() {
  const textValue = textInput.value.trim()
  const imageFile = imageInput.files[0]
  const contextValue = contextInput.value.trim()

  const fullContext = `Question: ${textValue}. Additional Context: ${contextValue}`;

  console.log("Starting initial submission...")
  console.log("Full context:", fullContext)

  // Show loading UI
  showLoadingState()

  try {
    let imageData = "TEXT_PLACEHOLDER"
    const formData = new FormData()
    formData.append("context", fullContext)
    if (imageFile) {
        formData.append('image', imageFile);
    }

    // 4. Make the API call using FormData
    const response = await fetch(`${API_URL}/links`, {
        method: "POST",
        body: formData // Pass the FormData object directly
    })

    // --- (Rest of your success/error handling logic) ---
    console.log("API Response Status:", response.status, response.statusText);
    if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`)
    }

    const result = await response.json();
    console.log("API Response Data:", result);

    if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`)
    }
    // Switch to chat mode
    switchToChatMode()

    let formattedMessage = ""
    if (Array.isArray(result) && result.length > 0) {
            console.log("Processing array of", result.length, "links")
            
            // Start with a header
            formattedMessage = `I found ${result.length} helpful resources for you:\n\n`
            
            // STEP 3: Loop through each link object and extract the data
            result.forEach((linkObject, index) => {
                console.log(`Processing link ${index + 1}:`, linkObject)
                
                // Extract the specific properties we want
                const title = linkObject.title || "No title available"
                const url = linkObject.url || "No URL available"
                const snippet = linkObject.snippet || "No description available"
                const relevanceScore = linkObject.relevance_score || 0
                
                console.log(`Link ${index + 1} extracted data:`, {
                    title: title,
                    url: url,
                    snippet: snippet.substring(0, 50) + "...",
                    relevance: relevanceScore
                })
                
                // STEP 4: Format each link nicely as a string
                formattedMessage += `${index + 1}. ${title}\n`
                
                // Only show URL if it's not 'N/A'
                if (url !== 'N/A') {
                    formattedMessage += `   🔗 ${url}\n`
                }
                
                formattedMessage += `   📝 ${snippet}\n`
                formattedMessage += `   📊 Relevance: ${Math.round(relevanceScore * 100)}%\n\n`
            })
            
        } else {
            console.log("No links found or result is not an array")
            formattedMessage = "I couldn't find any relevant resources for your question. Try rephrasing it!"
        }
        
        // STEP 5: Log the final formatted message
        console.log("Final formatted message:")
        console.log("Message length:", formattedMessage.length)
        console.log("Message preview:", formattedMessage.substring(0, 200) + "...")
  
    // Add initial assistant response
    console.log("Adding chat message with formatted string")
    addChatMessage("assistant", formattedMessage)
    
    // // Add HTML links if available
    // if (linksHtml) {
    //     addHtmlMessage("assistant-html", linksHtml)
    // }
    
    // Show video player (simulate completion)
    showVideoPlayer()

  } catch (error) {
    console.error("Error during initial submission:", error)
    resetToPlaceholder()
  }
}


function convertImageToBase64(file){
  return new Promise((resolve, reject)=> {
    const reader = new fileReader()
    reader.onload = () => {
      const base64 = reader.result.split(',')[1]
      resolve(base64)
    }
    reader.oneerror = reject
    reader.readDataasURL(file)
  })
}

// UI State Management Functions
function showLoadingState() {
  const placeholderContent = document.getElementById("placeholderContent")
  const videoContainer = document.getElementById("videoContainer")
  const videoLoading = document.getElementById("videoLoading")
  const videoPlayer = document.getElementById("videoPlayer")

  // Show loading state
  placeholderContent.style.display = "none"
  videoContainer.style.display = "flex"
  videoLoading.style.display = "flex"
  videoPlayer.style.display = "none"

  // Disable submit button
  submitBtn.disabled = true
  submitBtn.textContent = "Processing..."

  // Expand sidebar if collapsed
  if (sidebar.classList.contains("collapsed")) {
    toggleSidebar()
  }
}

function showVideoPlayer() {
  const videoLoading = document.getElementById("videoLoading")
  const videoPlayer = document.getElementById("videoPlayer")

  // Hide loading, show video player
  videoLoading.style.display = "none"
  videoPlayer.style.display = "flex"

  // Initialize video controls
  initializeVideoControls()

  // Reset submit button
  submitBtn.disabled = false
  submitBtn.textContent = "Submit"
}

function switchToChatMode() {
  const inputSection = document.querySelector('.input-section')
  const chatSection = document.getElementById("chatSection")

  // Hide input section, show chat section
  if (inputSection) inputSection.style.display = "none"
  if (chatSection) chatSection.style.display = "flex"
    
  console.log("Switched to chat mode")
}

function switchToInputMode() {
  const inputSection = document.querySelector('.input-section')
  const chatSection = document.getElementById("chatSection")

  // Show input section, hide chat section
  if (inputSection) inputSection.style.display = "block"
  if (chatSection) chatSection.style.display = "none"
    
  // Clear chat messages
  clearChatMessages()
    
  console.log("Switched to input mode")
}

function addChatMessage(sender, message) {
    const chatMessages = document.getElementById("chatMessages")
    const messageDiv = document.createElement("div")
    messageDiv.className = `chat-message ${sender}`
    messageDiv.textContent = message
    chatMessages.appendChild(messageDiv)
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight
}

/**
 * Adds HTML content to chat (for search result links)
 */
// function addHtmlMessage(sender, htmlContent) {
//     const chatMessages = document.getElementById("chatMessages");
//     const messageDiv = document.createElement("div");
//     messageDiv.className = `chat-message ${sender}`;
    
//     // Render HTML content
//     messageDiv.innerHTML = htmlContent;
//     chatMessages.appendChild(messageDiv);
//     chatMessages.scrollTop = chatMessages.scrollHeight;
// }

function clearChatMessages() {
    const chatMessages = document.getElementById("chatMessages")
    chatMessages.innerHTML = ""
}

// Video Control Functions
function initializeVideoControls() {
  const mathVideo = document.getElementById("mathVideo")
  const playPauseBtn = document.getElementById("playPauseBtn")
  const downloadBtn = document.getElementById("downloadBtn")
  const newQuestionBtn = document.getElementById("newQuestionBtn")

  // Set video source dynamically
  mathVideo.src = chrome.runtime.getURL("demo-math-video.mp4")
  
  console.log("Video URL:", mathVideo.src)
  mathVideo.load()

  // Play/Pause functionality
  playPauseBtn.addEventListener("click", () => {
    if (mathVideo.paused) {
      mathVideo.play()
      playPauseBtn.textContent = "⏸️ Pause"
    } else {
      mathVideo.pause()
      playPauseBtn.textContent = "▶️ Play"
    }
  })

  // Download functionality
  downloadBtn.addEventListener("click", () => {
    const a = document.createElement('a')
    a.href = mathVideo.src
    a.download = 'math-solution.mp4'
    a.click()
  })

  // New Question functionality
  newQuestionBtn.addEventListener("click", () => {
    resetToPlaceholder()
  })

  // Auto-update play/pause button
  mathVideo.addEventListener("play", () => {
    playPauseBtn.textContent = "⏸️ Pause"
  })

  mathVideo.addEventListener("pause", () => {
    playPauseBtn.textContent = "▶️ Play"
  })

  // Error handling
  mathVideo.addEventListener("error", (e) => {
    console.error("Video error:", e)
  })

  // Auto-play when ready
  mathVideo.play().catch((e) => {
    console.log("Auto-play prevented:", e)
  })
}

function resetToPlaceholder() {
  const placeholderContent = document.getElementById("placeholderContent")
  const videoContainer = document.getElementById("videoContainer")

  // Hide video container, show placeholder
  videoContainer.style.display = "none"
  placeholderContent.style.display = "flex"

  // Switch back to input mode
  switchToInputMode()

  // Clear inputs
  clearInputs()

  console.log("Reset to placeholder state")
}

// Utility Functions
function clearInputs() {
  textInput.value = ""
  contextInput.value = ""
  imageInput.value = ""
  fileName.textContent = ""
  validateInputs()
}

// Export functions for potential use by other modules
window.MathLearnMain = {
  toggleSidebar,
  handleSubmit,
  clearInputs,
  resetToPlaceholder
}