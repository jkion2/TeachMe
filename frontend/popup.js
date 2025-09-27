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
const toggleHistoryBtn = document.getElementById("toggleHistoryBtn")
const fileName = document.getElementById("fileName")

// State Management
let isCollapsed = false
let historyVisible = false

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

  // History toggle
  toggleHistoryBtn.addEventListener("click", toggleHistory)

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

function handleChatSend() {
    const chatInput = document.getElementById("chatInput")
    const message = chatInput.value.trim()
    
    if (!message) return
    
    // Add user message
    addChatMessage("user", message)
    
    // Clear input
    chatInput.value = ""
    
    // Simulate assistant response (replace with actual API call)
    setTimeout(() => {
        addChatMessage("assistant", "This is a simulated response. In production, this would connect to your FastAPI backend for actual AI responses.")
    }, 1000)
    
    console.log("Chat message sent:", message)
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

// Submit Function
function handleSubmit() {
  const textValue = textInput.value.trim()
  const imageFile = imageInput.files[0]
  const contextValue = contextInput.value.trim()

  // Log submission data
  console.log("Submit clicked")
  console.log("Text input:", textValue)
  console.log("Image file:", imageFile ? imageFile.name : "None")
  console.log("Context:", contextValue)

  if(sidebar.classList.contains("collapsed")) {
    toggleSidebar()
  }

  // Hide the placeholder content
  const placeholderContent = document.getElementById("placeholderContent")
  const videoContainer = document.getElementById("videoContainer")
  const videoLoading = document.getElementById("videoLoading")
  const videoPlayer = document.getElementById("videoPlayer")

  // Show video container and loading state
  placeholderContent.style.display = "none"
  videoContainer.style.display = "flex"
  videoLoading.style.display = "flex"
  videoPlayer.style.display = "none"

  // Simulate loading state
  submitBtn.disabled = true
  submitBtn.textContent = "Processing..."

  // Simulate video generation/loading delay (3 seconds)
  setTimeout(() => {
    // Hide loading, show video player
    videoLoading.style.display = "none"
    videoPlayer.style.display = "flex"

    // Initialize video controls
    initializeVideoControls()

    // Switch to chat mode
    switchToChartMode()

    // Reset submit button
    submitBtn.disabled = false
    submitBtn.textContent = "Submit"

    console.log("Video loaded and ready to play")
  }, 3000)
}

function switchToChartMode() {
  // `input-section` in HTML uses a class, not an id. Query by class to avoid null.
  const inputSection = document.querySelector('.input-section')
  const chatSection = document.getElementById("chatSection")

  // Hide input section, show chat section (guard nulls)
  if (inputSection) inputSection.style.display = "none"
  if (chatSection) chatSection.style.display = "flex"
    
    // Add initial message to chat
    addChatMessage("assistant", "I've generated your math explanation video! Feel free to ask any follow-up questions about the solution.")
    
    console.log("Switched to chat mode")
}

function switchToInputMode() {
  const inputSection = document.querySelector('.input-section')
  const chatSection = document.getElementById("chatSection")

  // Show input section, hide chat section (guard nulls)
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

  // 🔥 FIX: Set video source dynamically
  mathVideo.src = chrome.runtime.getURL("demo-math-video.mp4")
  
  // Debug: Log the video URL
  console.log("Video URL:", mathVideo.src)

  // Load the video
  mathVideo.load()

  // Play/Pause functionality
  playPauseBtn.addEventListener("click", () => {
    if (mathVideo.paused) {
      mathVideo.play()
      playPauseBtn.textContent = "⏸️ Pause"
      console.log("[v0] Video playing")
    } else {
      mathVideo.pause()
      playPauseBtn.textContent = "▶️ Play"
      console.log("[v0] Video paused")
    }
  })

  // Download functionality
  downloadBtn.addEventListener("click", () => {
    console.log("[v0] Download button clicked")
    const a = document.createElement('a')
    a.href = mathVideo.src
    a.download = 'math-solution.mp4'
    a.click()
  })

  // New Question functionality
  newQuestionBtn.addEventListener("click", () => {
    console.log("[v0] New question button clicked")
    resetToPlaceholder()
  })

  // Auto-update play/pause button based on video state
  mathVideo.addEventListener("play", () => {
    playPauseBtn.textContent = "⏸️ Pause"
  })

  mathVideo.addEventListener("pause", () => {
    playPauseBtn.textContent = "▶️ Play"
  })

  // Debug: Add error handling
  mathVideo.addEventListener("error", (e) => {
    console.error("[v0] Video error:", e)
    console.error("Video error details:", mathVideo.error)
  })

  mathVideo.addEventListener("canplay", () => {
    console.log("[v0] Video can play")
  })

  // Auto-play the video when it loads
  mathVideo.play().catch((e) => {
    console.log("[v0] Auto-play prevented by browser:", e)
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

  console.log("[v0] Reset to placeholder state")
}

// History Functions
// ...existing code...
function toggleHistory() {
  historyVisible = !historyVisible
  toggleHistoryBtn.textContent = historyVisible ? "📚 Hide History" : "📚 Show History"
  console.log("History toggle clicked:", historyVisible ? "show" : "hide")

  const contentArea = document.getElementById("contentArea")
  if (!contentArea) return

  // If showing, create iframe (only once)
  if (historyVisible) {
    if (!document.getElementById("mathlearn-history-iframe")) {
      // hide main placeholders/video if present
      const placeholder = document.getElementById("placeholderContent")
      const videoContainer = document.getElementById("videoContainer")
      if (placeholder) placeholder.style.display = "none"
      if (videoContainer) videoContainer.style.display = "none"

      const iframe = document.createElement("iframe")
      iframe.id = "mathlearn-history-iframe"
      iframe.src = chrome.runtime.getURL("history.html")
      iframe.style.width = "100%"
      iframe.style.height = "100%"
      iframe.style.border = "0"
      iframe.style.flex = "1"
      // ensure iframe fills the content area
      contentArea.appendChild(iframe)
      console.log("History iframe appended:", iframe.src)
    }
  } else {
    // hide/remove iframe and restore main view
    const existing = document.getElementById("mathlearn-history-iframe")
    if (existing) existing.remove()

    const placeholder = document.getElementById("placeholderContent")
    const videoContainer = document.getElementById("videoContainer")
    if (placeholder) placeholder.style.display = "flex"
    if (videoContainer) videoContainer.style.display = "none"
    console.log("History iframe removed")
  }
}

// ...existing code...
// Listen for messages from the history iframe
window.addEventListener("message", (event) => {
  // Optional: check event.origin if you want to restrict allowed senders
  const msg = event.data
  if (!msg || msg.action !== "hide-history") return

  const iframe = document.getElementById("mathlearn-history-iframe")
  if (iframe) iframe.remove()

  historyVisible = false
  if (toggleHistoryBtn) toggleHistoryBtn.textContent = "📚 Show History"

  // Restore placeholder / hide video container if needed
  const placeholder = document.getElementById("placeholderContent")
  const videoContainer = document.getElementById("videoContainer")
  if (placeholder) placeholder.style.display = "flex"
  if (videoContainer) videoContainer.style.display = "none"

  console.log("History hidden via iframe message")
})



 /* Youtube Upload Button Functionality */
/**
 * NOTE: Before this will work you MUST:
 * 1) Enable the YouTube Data API v3 in Google Cloud Console for a project.
 * 2) Configure OAuth consent screen (external/internal) and publish it (for testing choose Internal or add test users).
 * 3) Create an OAuth 2.0 Client ID of type "Chrome App" or "Web application" and get the CLIENT_ID.
 *    For chrome.identity.getAuthToken, add the redirect URI: https://<YOUR-EXTENSION-ID>.chromiumapp.org/ (Chrome will show it).
 * 4) Add the CLIENT_ID and scopes to manifest.json under "oauth2" and add "identity" permission:
 *    "permissions": ["activeTab","storage","identity"],
 *    "oauth2": { "client_id": "<YOUR_CLIENT_ID>.apps.googleusercontent.com", "scopes": ["https://www.googleapis.com/auth/youtube.upload"] }
 * 5) Add the YouTube upload scope to web_accessible_resources if needed (not required for token).
 *
 * Security note: Keep client_id private for production; do not embed client_secret in an extension.
 */

async function getYoutubeAccessToken(interactive = true) {
  return new Promise((resolve, reject) => {
    try {
      // chrome.identity.getAuthToken is the recommended flow for extensions.
      chrome.identity.getAuthToken({ interactive }, (token) => {
        if (chrome.runtime.lastError) {
          return reject(new Error(chrome.runtime.lastError.message))
        }
        if (!token) return reject(new Error('No auth token obtained'))
        resolve(token)
      })
    } catch (err) {
      reject(err)
    }
  })
}

/**
 * Start a resumable upload session for YouTube:
 * POST to https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status
 * Authorization: Bearer <ACCESS_TOKEN>
 * Body: JSON with snippet and status (title, description, tags, privacyStatus)
 * The response Location header is the upload URL.
 */
async function startResumableSession(accessToken, metadata = {}) {
  const url = 'https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status'
  const body = {
    snippet: {
      title: metadata.title || 'MathLearn Demo Video',
      description: metadata.description || 'Generated by MathLearn',
      tags: metadata.tags || ['mathlearn', 'demo'],
      categoryId: metadata.categoryId || '27', // education/science categories vary
    },
    status: {
      privacyStatus: metadata.privacyStatus || 'private',
    },
  }

  const res = await fetch(url, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${accessToken}`,
      'Content-Type': 'application/json; charset=UTF-8',
      'X-Upload-Content-Length': metadata.size || '0', // optional hint
      'X-Upload-Content-Type': metadata.contentType || 'video/*',
    },
    body: JSON.stringify(body),
  })

  if (!res.ok) {
    const txt = await res.text()
    throw new Error(`Resumable session request failed: ${res.status} ${txt}`)
  }

  const uploadUrl = res.headers.get('Location')
  if (!uploadUrl) throw new Error('No upload URL returned by YouTube resumable session')
  return uploadUrl
}

/**
 * Upload the actual video bytes to the session URL using PUT.
 * For small videos you can PUT the whole blob at once. For large files use chunked uploads.
 */
async function uploadBlobToUrl(uploadUrl, blob, onProgress) {
  // Use XMLHttpRequest if you want progress events; fetch does not provide upload progress yet.
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest()
    xhr.open('PUT', uploadUrl, true)
    xhr.setRequestHeader('Content-Type', blob.type || 'application/octet-stream')

    xhr.upload.onprogress = (e) => {
      if (e.lengthComputable && typeof onProgress === 'function') {
        onProgress((e.loaded / e.total) * 100)
      }
    }

    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        try {
          const json = JSON.parse(xhr.responseText || '{}')
          resolve(json)
        } catch (err) {
          resolve(xhr.responseText)
        }
      } else {
        reject(new Error(`Upload failed: ${xhr.status} ${xhr.statusText} - ${xhr.responseText}`))
      }
    }

    xhr.onerror = () => reject(new Error('Network error during upload'))
    xhr.send(blob)
  })
}

/**
 * Top-level helper to upload the video currently loaded in the player.
 * This function:
 *  - grabs the video source blob (fetches the src)
 *  - obtains an access token via chrome.identity
 *  - starts resumable session and uploads blob
 */
async function uploadCurrentVideoToYouTube() {
  try {
    const mathVideo = document.getElementById('mathVideo')
    if (!mathVideo) throw new Error('Video element not found')
    // Determine effective source URL; either <source> element or video.src
    const sourceEl = mathVideo.querySelector('source')
    const videoUrl = (sourceEl && sourceEl.src) || mathVideo.currentSrc || mathVideo.src
    if (!videoUrl) throw new Error('No video source available to upload')

    console.log('[youtube] Fetching video blob from', videoUrl)
    // fetch the video bytes from the extension URL or remote URL
    const fetched = await fetch(videoUrl)
    if (!fetched.ok) throw new Error(`Failed to fetch video: ${fetched.status}`)
    const blob = await fetched.blob()
    console.log('[youtube] Blob length', blob.size, 'type', blob.type)

    // Get OAuth token (interactive)
    const token = await getYoutubeAccessToken(true)
    console.log('[youtube] Got access token (masked):', token && token.slice(0, 8) + '...')

    // Build metadata (customize as needed or prompt user)
    const metadata = {
      title: 'MathLearn Demo — ' + new Date().toISOString().split('T')[0],
      description: 'Demo upload from MathLearn extension (replace with real generated video).',
      tags: ['mathlearn', 'demo', 'manim'],
      privacyStatus: 'private',
      size: blob.size,
      contentType: blob.type,
    }

    // Start resumable session
    const uploadUrl = await startResumableSession(token, metadata)
    console.log('[youtube] Resumable upload URL:', uploadUrl)

    // Upload blob (with basic progress handler)
    const result = await uploadBlobToUrl(uploadUrl, blob, (percent) => {
      console.log(`[youtube] upload progress: ${percent.toFixed(1)}%`)
      // Optionally update UI progress bar
    })

    console.log('[youtube] Upload result:', result)
    alert('Upload completed (check YouTube Studio).')

  } catch (err) {
    console.error('[youtube] Upload failed:', err)
    alert('YouTube upload failed: ' + err.message)
  }
}

// Hook the UI button
document.addEventListener('DOMContentLoaded', () => {
  const uploadBtn = document.getElementById('uploadYoutubeBtn')
  if (uploadBtn) {
    uploadBtn.addEventListener('click', (e) => {
      e.preventDefault()
      console.log('[youtube] Upload button clicked')
      uploadCurrentVideoToYouTube()
    })
  }
})


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
  toggleHistory,
  clearInputs,
  resetToPlaceholder, // Added new function to exports
}