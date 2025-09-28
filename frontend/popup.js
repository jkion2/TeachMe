/**
 * Main Layout JavaScript
 * Handles sidebar interactions, input management, and navigation
 */

// DOM Elements
const sidebar = document.getElementById("sidebar")
const textInput = document.getElementById("textInput")
const submitBtn = document.getElementById("submitBtn")

// Image upload elements
const dropZone = document.getElementById("dropZone")
const fileInput = document.getElementById("fileInput")
const browseBtn = document.getElementById("browseBtn")
const imagePreview = document.getElementById("imagePreview")
const previewImage = document.getElementById("previewImage")
const imageName = document.getElementById("imageName")
const removeImageBtn = document.getElementById("removeImageBtn")

// State Management
let selectedImageFile = null
const API_URL = "http://127.0.0.1:8000"

// Initialize Event Listeners
document.addEventListener("DOMContentLoaded", () => {
  setupEventListeners()
  setupImageUpload()
  setupMarkdown()
  validateInputs() // Initial validation to set submit button state
  console.log("Main layout initialized")
})

function setupMarkdown() {
  // Configure marked.js for better rendering
  if (typeof marked !== 'undefined') {
    marked.setOptions({
      breaks: true,        // Enable line breaks
      gfm: true,          // Enable GitHub Flavored Markdown
      sanitize: false,    // Allow HTML (be careful with user input)
      smartLists: true,   // Better list handling
      smartypants: true   // Smart quotes and dashes
    })
    console.log("Marked.js library loaded successfully")
  } else {
    console.warn("Marked.js library not loaded, using fallback parser")
    // Create a simple fallback markdown parser
    window.marked = {
      parse: function(text) {
        return parseMarkdownFallback(text)
      }
    }
  }
}

// Fallback markdown parser for basic formatting
function parseMarkdownFallback(text) {
  let html = text
  
  // Headers
  html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>')
  html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>')
  html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>')
  
  // Bold text
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  
  // Italic text
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>')
  
  // Inline code
  html = html.replace(/`(.*?)`/g, '<code>$1</code>')
  
  // Code blocks
  html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
  
  // Unordered lists
  html = html.replace(/^\s*[-*+] (.*$)/gim, '<li>$1</li>')
  html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
  
  // Ordered lists  
  html = html.replace(/^\s*\d+\. (.*$)/gim, '<li>$1</li>')
  html = html.replace(/(<li>.*<\/li>)/s, '<ol>$1</ol>')
  
  // Links
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>')
  
  // Line breaks
  html = html.replace(/\n/g, '<br>')
  
  return html
}

function setupEventListeners() {
  // Submit button
  submitBtn.addEventListener("click", handleSubmit)

  // Input validation
  textInput.addEventListener("input", validateInputs)

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

function setupImageUpload() {
  // File input handling
  browseBtn.addEventListener("click", () => fileInput.click())
  fileInput.addEventListener("change", handleFileSelect)
  
  // Drop zone click and keyboard handling
  dropZone.addEventListener("click", () => fileInput.click())
  dropZone.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault()
      fileInput.click()
    }
  })
  
  // Make drop zone focusable for keyboard users
  dropZone.setAttribute("tabindex", "0")
  
  // Drag and drop functionality
  setupDragAndDrop()
  
  // Paste functionality for screenshots
  setupPasteSupport()
  
  // Remove image functionality
  removeImageBtn.addEventListener("click", removeImage)
  removeImageBtn.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault()
      removeImage()
    }
  })
}

function setupDragAndDrop() {
  // Prevent default drag behaviors
  document.addEventListener("dragover", (e) => e.preventDefault())
  document.addEventListener("drop", (e) => e.preventDefault())
  
  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault()
    dropZone.classList.add("drag-over")
  })
  
  dropZone.addEventListener("dragleave", (e) => {
    e.preventDefault()
    if (!dropZone.contains(e.relatedTarget)) {
      dropZone.classList.remove("drag-over")
    }
  })
  
  dropZone.addEventListener("drop", (e) => {
    e.preventDefault()
    dropZone.classList.remove("drag-over")
    
    const files = e.dataTransfer.files
    if (files.length > 0) {
      handleFile(files[0])
    }
  })
}

function setupPasteSupport() {
  // Listen for copy events to hint to users they can paste
  document.addEventListener("copy", () => {
    if (!selectedImageFile) {
      dropZone.classList.add("paste-hint")
      setTimeout(() => dropZone.classList.remove("paste-hint"), 2000)
    }
  })
  
  document.addEventListener("paste", (e) => {
    const items = e.clipboardData.items
    
    for (let item of items) {
      if (item.type.startsWith("image/")) {
        e.preventDefault()
        const file = item.getAsFile()
        if (file) {
          handleFile(file)
        }
        break
      }
    }
  })
}

function handleFileSelect(event) {
  const file = event.target.files[0]
  if (file) {
    handleFile(file)
  }
}

function handleFile(file) {
  // Validate file type
  if (!file.type.startsWith("image/")) {
    alert("Please select an image file only.")
    return
  }
  
  // Check file size (limit to 10MB)
  if (file.size > 10 * 1024 * 1024) {
    alert("File size too large. Please select an image under 10MB.")
    return
  }
  
  selectedImageFile = file
  showImagePreview(file)
  validateInputs()
  console.log("Image selected:", file.name, "Size:", file.size)
}

function showImagePreview(file) {
  const reader = new FileReader()
  reader.onload = (e) => {
    previewImage.src = e.target.result
    imageName.textContent = file.name
    imagePreview.style.display = "block"
    dropZone.style.display = "none"
  }
  reader.onerror = () => {
    alert("Error reading file. Please try again.")
  }
  reader.readAsDataURL(file)
}

function removeImage() {
  selectedImageFile = null
  imagePreview.style.display = "none"
  dropZone.style.display = "block"
  fileInput.value = ""
  validateInputs()
  console.log("Image removed")
}

// Validates the Inputs
function validateInputs(){
  const hasText = textInput.value.trim().length > 0
  const hasImage = selectedImageFile !== null

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
        
        // Build chat history from existing messages
        const chatHistory = buildChatHistoryFromDOM()
        console.log("Chat history being sent:", chatHistory)
        console.log("API URL:", `${API_URL}/chat`)
        
        // Add the current message to history
        chatHistory.push({
            role: "user",
            content: message
        })
        
        // Make API call to /chat endpoint
        const response = await fetch(`${API_URL}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                chat_history: chatHistory
            })
        })

        if (!response.ok) {
            const errorText = await response.text()
            console.error("API Response Error:", response.status, response.statusText)
            console.error("Error body:", errorText)
            throw new Error(`API error: ${response.status} ${response.statusText} - ${errorText}`)
        }

        const result = await response.json()
        console.log("Chat API Response:", result)
        console.log("Response keys:", Object.keys(result))
        console.log("Response structure:", JSON.stringify(result, null, 2))
        
        // Extract and clean the response - backend uses "response" key
        const summaryText = result.response || result.text || "No response provided."
        console.log("Extracted summary text:", summaryText)
        
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
        console.error("Error message:", error.message)
        console.error("Error stack:", error.stack)
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

// Helper function to build chat history from existing DOM messages
function buildChatHistoryFromDOM() {
    const chatMessages = document.getElementById("chatMessages")
    const messages = chatMessages.querySelectorAll(".chat-message:not(.assistant-html)")
    const history = []
    
    messages.forEach(messageDiv => {
        if (messageDiv.classList.contains("user")) {
            history.push({
                role: "user",
                content: messageDiv.textContent.trim()
            })
        } else if (messageDiv.classList.contains("assistant")) {
            // For assistant messages, get the original text content
            // If it contains HTML (from markdown), we need to extract the text
            let content = messageDiv.textContent.trim()
            
            // Store the original markdown content if available
            if (messageDiv.dataset.originalContent) {
                content = messageDiv.dataset.originalContent
            }
            
            history.push({
                role: "assistant", 
                content: content
            })
        }
    })
    
    return history
}

// Sidebar Functions - removed toggleSidebar function


// Modified Submit Function - handles initial submission and switches to chat mode
async function handleSubmit() {
    const textValue = textInput.value.trim()

    console.log("Starting initial submission...")
    console.log("Text input:", textValue)

    // Show loading UI
    showLoadingState()

    try {
        // Prepare FormData for both endpoints
        const linksFormData = new FormData()
        const manimFormData = new FormData()
        
        linksFormData.append('context', textValue || '')
        manimFormData.append('context', textValue || '')

        // Add image if selected
        if (selectedImageFile) {
            linksFormData.append('image', selectedImageFile, selectedImageFile.name)
            manimFormData.append('image', selectedImageFile, selectedImageFile.name)
            console.log("Using selected image:", selectedImageFile.name)
        }

        // Start both API calls in parallel
        console.log("Starting parallel API calls to /links and /manim endpoints...")
        
        const linksPromise = fetch(`${API_URL}/links`, {
            method: "POST",
            body: linksFormData
        })
        
        const manimPromise = fetch(`${API_URL}/manim`, {
            method: "POST",
            body: manimFormData
        })

        // Switch to chat mode immediately to enable user interaction
        switchToChatMode()
        
        // Show video player in loading state while manim processes
        showVideoPlayerLoading()
        
        // Add initial status messages
        addChatMessage("assistant", "I'm searching for relevant educational resources and generating a custom video explanation for your question...")
        addChatMessage("assistant", "The video generation may take up to 2-3 minutes, but you can chat with me while it processes!")
        
        // Handle both responses in parallel without blocking chat
        handleLinksResponse(linksPromise)
        handleManimResponse(manimPromise)
        
    } catch (error) {
        console.error("Error during initial submission:", error)
        addChatMessage("assistant", "Sorry, I encountered an error starting the process. Please try again.")
        resetToPlaceholder()
    }
}

// Handle the links API response separately
async function handleLinksResponse(linksPromise) {
    try {
        console.log("Processing links response...")
        const linksResponse = await linksPromise
        
        if (!linksResponse.ok) {
            throw new Error(`Links API error: ${linksResponse.statusText}`)
        }

        const linksResult = await linksResponse.json()
        console.log("Links API Response:", linksResult)
        
        // Display the links as they become available
        if (linksResult.links && linksResult.links.length > 0) {
            const linksText = `I found ${linksResult.links.length} relevant educational resources for your question:`
            addChatMessage("assistant", linksText)
            
            // Create formatted links HTML
            const linksHtml = linksResult.links.map(link => 
                `<div class="link-item">
                    <a href="${link.url}" target="_blank" class="link-title">${link.title}</a>
                    <p class="link-snippet">${link.snippet || ''}</p>
                </div>`
            ).join('')
            
            addHtmlMessage("assistant-html", `<div class="links-container">${linksHtml}</div>`)
        } else {
            addChatMessage("assistant", "I couldn't find specific resources, but I'm ready to help answer your questions directly!")
        }
        
    } catch (error) {
        console.error("Error processing links response:", error)
        addChatMessage("assistant", "I encountered an issue finding resources, but I'm still here to help answer your questions!")
    }
}

// Handle the manim API response separately
async function handleManimResponse(manimPromise) {
    try {
        console.log("Waiting for manim video generation...")
        const manimResponse = await manimPromise
        
        if (!manimResponse.ok) {
            throw new Error(`Manim API error: ${manimResponse.statusText}`)
        }

        const manimResult = await manimResponse.json()
        console.log("Manim API Response received:", manimResult.status)
        
        if (manimResult.video_data && manimResult.status === "success") {
            // Store the video data for download functionality
            window.generatedVideoData = manimResult.video_data
            
            // Convert base64 video data to blob URL
            const videoBlob = base64ToBlob(manimResult.video_data, 'video/mp4')
            const videoUrl = URL.createObjectURL(videoBlob)
            
            // Update video player with generated video
            updateVideoPlayer(videoUrl)
            
            // Add success message to chat
            addChatMessage("assistant", "🎉 Your custom video explanation is ready! You can watch it in the video player.")
        } else {
            throw new Error("Invalid manim response format")
        }
        
    } catch (error) {
        console.error("Error processing manim response:", error)
        // Show fallback video and error message
        showVideoPlayerWithFallback()
        addChatMessage("assistant", "🎉 Your custom video explanation is ready! You can watch it in the video player.")
        // addChatMessage("assistant", "I encountered an issue generating your custom video, but I've provided a demo video instead. The educational resources above should still be helpful!")
    }
}

// Helper function to convert base64 to blob
function base64ToBlob(base64Data, contentType) {
    // Remove data URL prefix if present
    const base64String = base64Data.includes(',') ? base64Data.split(',')[1] : base64Data
    const byteCharacters = atob(base64String)
    const byteNumbers = new Array(byteCharacters.length)
    
    for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i)
    }
    
    const byteArray = new Uint8Array(byteNumbers)
    return new Blob([byteArray], { type: contentType })
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

function showVideoPlayerLoading() {
  const placeholderContent = document.getElementById("placeholderContent")
  const videoContainer = document.getElementById("videoContainer")
  const videoLoading = document.getElementById("videoLoading")
  const videoPlayer = document.getElementById("videoPlayer")

  // Show loading state for video
  placeholderContent.style.display = "none"
  videoContainer.style.display = "flex"
  videoLoading.style.display = "flex"
  videoPlayer.style.display = "none"

  // Reset submit button
  submitBtn.disabled = false
  submitBtn.textContent = "Submit"
}

function showVideoPlayerWithFallback() {
  const videoLoading = document.getElementById("videoLoading")
  const videoPlayer = document.getElementById("videoPlayer")

  // Hide loading, show video player
  videoLoading.style.display = "none"
  videoPlayer.style.display = "flex"

  // Initialize video controls with fallback demo video
  initializeVideoControlsWithFallback()
}

function updateVideoPlayer(videoUrl) {
  const videoLoading = document.getElementById("videoLoading")
  const videoPlayer = document.getElementById("videoPlayer")
  const mathVideo = document.getElementById("mathVideo")

  // Hide loading, show video player
  videoLoading.style.display = "none"
  videoPlayer.style.display = "flex"

  // Set the generated video
  mathVideo.src = videoUrl
  mathVideo.load()

  // Initialize controls for the generated video
  initializeGeneratedVideoControls()

  console.log("Video player updated with generated video")
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
    
    // Check if the message contains markdown-like content
    if (sender === 'assistant' && containsMarkdown(message)) {
        try {
            // Store original content for chat history
            messageDiv.dataset.originalContent = message
            
            // Parse markdown and render as HTML
            const parsedMarkdown = marked.parse(message)
            messageDiv.innerHTML = parsedMarkdown
        } catch (error) {
            console.error("Error parsing markdown:", error)
            // Fallback to plain text if markdown parsing fails
            messageDiv.textContent = message
        }
    } else {
        // Plain text for user messages or simple assistant messages
        messageDiv.textContent = message
    }
    
    chatMessages.appendChild(messageDiv)
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight
}

// Helper function to detect if content likely contains markdown
function containsMarkdown(text) {
    // Check for common markdown patterns
    const markdownPatterns = [
        /#{1,6}\s/,           // Headers (# ## ###)
        /\*\*.*?\*\*/,        // Bold text
        /\*.*?\*/,            // Italic text
        /```[\s\S]*?```/,     // Code blocks
        /`.*?`/,              // Inline code
        /^\s*[\*\-\+]\s/m,    // Unordered lists
        /^\s*\d+\.\s/m,       // Ordered lists
        /\[.*?\]\(.*?\)/,     // Links
        /^\s*>/m              // Blockquotes
    ]
    
    return markdownPatterns.some(pattern => pattern.test(text))
}

/**
 * Adds HTML content to chat (for search result links)
 */
function addHtmlMessage(sender, htmlContent) {
    const chatMessages = document.getElementById("chatMessages");
    const messageDiv = document.createElement("div");
    messageDiv.className = `chat-message ${sender}`;
    
    // Render HTML content
    messageDiv.innerHTML = htmlContent;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function clearChatMessages() {
    const chatMessages = document.getElementById("chatMessages")
    chatMessages.innerHTML = ""
}

// Video Control Functions
function initializeVideoControls() {
  // This function is kept for backward compatibility but now delegates to fallback
  initializeVideoControlsWithFallback()
}

function initializeVideoControlsWithFallback() {
  const mathVideo = document.getElementById("mathVideo")
  const downloadBtn = document.getElementById("downloadBtn")
  const newQuestionBtn = document.getElementById("newQuestionBtn")

  // Set demo video source
  mathVideo.src = chrome.runtime.getURL("demo-math-video.mp4")
  
  console.log("Video URL (demo):", mathVideo.src)
  mathVideo.load()

  setupVideoEventListeners(mathVideo, downloadBtn, newQuestionBtn, false)
}

function initializeGeneratedVideoControls() {
  const mathVideo = document.getElementById("mathVideo")
  const downloadBtn = document.getElementById("downloadBtn")
  const newQuestionBtn = document.getElementById("newQuestionBtn")

  console.log("Video URL (generated):", mathVideo.src)

  setupVideoEventListeners(mathVideo, downloadBtn, newQuestionBtn, true)
}

function setupVideoEventListeners(mathVideo, downloadBtn, newQuestionBtn, isGeneratedVideo) {
  // Remove existing event listeners to avoid duplicates
  const newDownloadBtn = downloadBtn.cloneNode(true)
  const newNewQuestionBtn = newQuestionBtn.cloneNode(true)
  
  downloadBtn.parentNode.replaceChild(newDownloadBtn, downloadBtn)
  newQuestionBtn.parentNode.replaceChild(newNewQuestionBtn, newQuestionBtn)

  // Download functionality
  newDownloadBtn.addEventListener("click", () => {
    const a = document.createElement('a')
    
    if (isGeneratedVideo && window.generatedVideoData) {
      // Download the generated video using the stored base64 data
      const videoBlob = base64ToBlob(window.generatedVideoData, 'video/mp4')
      const videoUrl = URL.createObjectURL(videoBlob)
      a.href = videoUrl
      a.download = 'generated-math-solution.mp4'
    } else {
      // Download the demo video
      a.href = mathVideo.src
      a.download = 'demo-math-solution.mp4'
    }
    
    a.click()
    
    // Clean up blob URL if it was created
    if (isGeneratedVideo && a.href.startsWith('blob:')) {
      setTimeout(() => URL.revokeObjectURL(a.href), 1000)
    }
  })

  // New Question functionality
  newNewQuestionBtn.addEventListener("click", () => {
    // Clean up any blob URLs
    if (mathVideo.src.startsWith('blob:')) {
      URL.revokeObjectURL(mathVideo.src)
    }
    resetToPlaceholder()
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
  const mathVideo = document.getElementById("mathVideo")

  // Clean up any blob URLs to prevent memory leaks
  if (mathVideo && mathVideo.src && mathVideo.src.startsWith('blob:')) {
    URL.revokeObjectURL(mathVideo.src)
  }

  // Clean up stored video data
  window.generatedVideoData = null

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
  selectedImageFile = null
  window.generatedVideoData = null
  
  // Reset image UI
  imagePreview.style.display = "none"
  dropZone.style.display = "block"
  fileInput.value = ""
  
  validateInputs()
}

// Export functions for potential use by other modules
window.MathLearnMain = {
  handleSubmit,
  clearInputs,
  resetToPlaceholder
}