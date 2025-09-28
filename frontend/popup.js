/**
 * Main Layout JavaScript
 * Handles sidebar interactions, input management, and navigation
 */

// DOM Elements
const sidebar = document.getElementById("sidebar")
const collapseBtn = document.getElementById("collapseBtn")
const textInput = document.getElementById("textInput")
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

  // CHANGE: File upload handling - open upload page instead of direct file input
  const uploadBtn = document.querySelector('.upload-btn')
  uploadBtn.addEventListener("click", handleUploadButtonClick)

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

function handleUploadButtonClick(event){
  event.preventDefault() //prevents default file input behavior

  console.log("Opening upload Page...")

  chrome.windows.create({
    url: chrome.runtime.getURL('upload.html'),
    type: 'popup',
    width: 520,
    height: 520,
    focused: true
  }, (window) =>{
    if (chrome.runtime.lastError){
      console.error("Error opening upload window",  chrome.runtime.lastError)
    } else{
      console.log("Upload Window Opened:", window.id)
    }
  })
}

if (chrome.runtime && chrome.runtime.onMessage){
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action == 'imageSelected'){
      console.log("Recieved image from Upload Page:", message.fileName)

      //process the uploaded image
      processUploadedImage(message)

      //send a response back to the upload page
      sendResponse ({status: 'success'})
    }
  })
}

function processUploadedImage(imageData){

  const fileName = document.getElementById("fileName")
  fileName.textContent = imageData.fileName

  //Store the image Data to use in HandleSubmit
  window.uploadedImageData = {
    fileName: imageData.fileName,
    base64Data: imageData.base64Data,
    fileType: imageData.fileType,
    fileSize: imageData.fileSize
  }

  //clear the text after image upload
  textInput.value = ""

  console.log("Image Processed:", imageData.fileName, "Size:", imageData.fileSize)

  //for enable/disable submit button
  validateInputs()
}

// Validates the Inputs
function validateInputs(){
  const hasText = textInput.value.trim().length > 0
  const hasImage = window.uploadedImageData !== undefined && window.uploadedImageData !== null

  submitBtn.disabled = !(hasText || hasImage)
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
        // if (linksHtml) {
        //     addHtmlMessage("assistant-html", linksHtml)
        // }
        
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


// Modified Submit Function - handles initial submission and switches to chat mode
// Function uses window.uploadedImageData populated by the upload page
async function handleSubmit() {
    const textValue = textInput.value.trim()
    // const imageFile = imageInput.files[0] // REMOVED: No longer used
    const contextValue = contextInput.value.trim()

    const fullContext = `Question: ${textValue}. Additional Context: ${contextValue}`;

    console.log("Starting initial submission...")
    console.log("Full context:", fullContext)

    const formData = new FormData()
    formData.append("context", fullContext)

    // Show loading UI
    showLoadingState()

    try {
        let imageData = "TEXT_PLACEHOLDER"

        // CHECK IF IMAGE DATA WAS RECEIVED FROM THE UPLOAD POPUP
        if (window.uploadedImageData && window.uploadedImageData.base64Data) {
            imageData = window.uploadedImageData.base64Data
            console.log("Using Uploaded Image:", window.uploadedImageData.fileName)
        }

        formData.append("image", imageData) // Placeholder for image data

        const response = await fetch(`${API_URL}/links`, {
            method: "POST",
            body: formData
        })

        if (!response.ok) {
            throw new Error(`API error: ${response.statusText}`)
        }
        console.log("Initial submission response received")

        const result = await response.json()
        console.log("Initial API Response:", result)
        
        // Extract response data
        // const summaryText = result.text || "No summary provided."
        // const linksHtml = result.html_links
        // const cleanSummary = summaryText.replace("##ADK_RESPONSE_END##", "").trim()

        // Process the response - YOUR BACKEND RETURNS: {"links": [...], "status": "success"}
        if (result.links && Array.isArray(result.links)) {
            console.log("Processing", result.links.length, "links")
            
            // Create formatted message
            let formattedMessage = `I found ${result.links.length} helpful resources for you:\n\n`
            
            result.links.forEach((linkObject, index) => {
                console.log(`Processing link ${index + 1}:`, {
                    title: linkObject.title?.substring(0, 50) + "...",
                    url: linkObject.url,
                    relevance: linkObject.relevance_score
                })
                
                const title = linkObject.title || "No title available"
                const url = linkObject.url || "No URL available"
                const snippet = linkObject.snippet || "No description available"
                const relevanceScore = linkObject.relevance_score || 0
                
                formattedMessage += `${index + 1}. ${title}\n`
                
                if (url !== 'N/A' && url !== 'No URL available') {
                    formattedMessage += `   🔗 ${url}\n`
                }
                
                formattedMessage += `   📝 ${snippet}\n`
                formattedMessage += `   📊 Relevance: ${Math.round(relevanceScore * 100)}%\n\n`
            })
            
            // Switch to chat mode and show results
            switchToChatMode()
            addChatMessage("assistant", formattedMessage)
            showVideoPlayer()
            
        } else {
            console.error("No links found in response or invalid format")
            switchToChatMode()
            addChatMessage("assistant", "I couldn't find any relevant resources. Try rephrasing your question!")
            showVideoPlayer()
        }

        // Switch to chat mode
        //switchToChatMode()
        
        // Add initial assistant response
        //addChatMessage("assistant", )
        
        // Add HTML links if available
        // if (linksHtml) {
        //     addHtmlMessage("assistant-html", linksHtml)
        // }
        
        // Show video player (simulate completion)
        //showVideoPlayer()
    } catch (error) {
        console.error("Error during initial submission:", error)
        resetToPlaceholder()
    }
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
    downloadVideoReliable()
    // const a = document.createElement('a')
    // a.href = mathVideo.src
    // a.download = 'math-solution.mp4'
    // a.click()
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

async function downloadVideoReliable() {
    const mathVideo = document.getElementById("mathVideo")
    const downloadBtn = document.getElementById("downloadBtn")
    
    try {
        console.log("Starting video download...")
        downloadBtn.disabled = true
        downloadBtn.textContent = "⬇️ Downloading..."
        
        // Fetch the video as blob
        const response = await fetch(mathVideo.src)
        if (!response.ok) {
            throw new Error(`Failed to fetch video: ${response.statusText}`)
        }
        
        const blob = await response.blob()
        console.log("Video blob size:", blob.size, "bytes")
        
        // Create download link
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = 'math-solution.mp4'
        a.style.display = 'none'
        
        // Add to DOM, click, then remove
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        
        // Clean up the blob URL
        setTimeout(() => URL.revokeObjectURL(url), 100)
        
        console.log("Video download initiated successfully")
        
    } catch (error) {
        console.error("Download failed:", error)
        alert("Download failed. Please try again.")
    } finally {
        downloadBtn.disabled = false
        downloadBtn.textContent = "⬇️ Download"
    }
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
  window.uploadedImageData = null
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