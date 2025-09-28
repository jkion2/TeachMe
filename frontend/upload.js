// DOM Elements
const dropZone = document.getElementById('dropZone')
const fileInput = document.getElementById('fileInput')
const browseBtn = document.getElementById('browseBtn')
const closeBtn = document.getElementById('closeBtn')
const previewSection = document.getElementById('previewSection')
const previewImage = document.getElementById('previewImage')
const fileName = document.getElementById('fileName')
const useImageBtn = document.getElementById('useImageBtn')
const removeImageBtn = document.getElementById('removeImageBtn')

let selectedFile = null

// Initialize when page loads
document.addEventListener('DOMContentLoaded', setupUploadPage)

function setupUploadPage() {
    setupEventListeners()
    setupDragAndDrop()
    setupPasteSupport()
    console.log("Upload page initialized")
}

function setupEventListeners() {
    browseBtn.addEventListener('click', () => fileInput.click())
    fileInput.addEventListener('change', handleFileSelect)
    closeBtn.addEventListener('click', closeUploadPage)
    useImageBtn.addEventListener('click', useSelectedImage)
    removeImageBtn.addEventListener('click', removeImage)
    
    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeUploadPage()
        }
    })
}

function setupDragAndDrop() {
    // Prevent default drag behaviors on document
    document.addEventListener('dragover', (e) => e.preventDefault())
    document.addEventListener('drop', (e) => e.preventDefault())
    
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault()
        dropZone.classList.add('drag-over')
    })
    
    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault()
        // Only remove class if leaving the drop zone entirely
        if (!dropZone.contains(e.relatedTarget)) {
            dropZone.classList.remove('drag-over')
        }
    })
    
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault()
        dropZone.classList.remove('drag-over')
        
        const files = e.dataTransfer.files
        if (files.length > 0) {
            handleFile(files[0])
        }
    })
}

function setupPasteSupport() {
    document.addEventListener('paste', (e) => {
        const items = e.clipboardData.items
        
        for (let item of items) {
            if (item.type.startsWith('image/')) {
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
    if (!file.type.startsWith('image/')) {
        alert('Please select an image file only.')
        return
    }
    
    // Check file size (limit to 10MB)
    if (file.size > 10 * 1024 * 1024) {
        alert('File size too large. Please select an image under 10MB.')
        return
    }
    
    selectedFile = file
    showPreview(file)
    console.log("File selected:", file.name, "Size:", file.size)
}

function showPreview(file) {
    const reader = new FileReader()
    reader.onload = (e) => {
        previewImage.src = e.target.result
        fileName.textContent = file.name
        previewSection.style.display = 'flex'
        dropZone.style.display = 'none'
    }
    reader.onerror = () => {
        alert('Error reading file. Please try again.')
    }
    reader.readAsDataURL(file)
}

function removeImage() {
    selectedFile = null
    previewSection.style.display = 'none'
    dropZone.style.display = 'flex'
    fileInput.value = ''
    console.log("Image removed")
}

function useSelectedImage() {
    if (selectedFile) {
        console.log("Sending image to main page:", selectedFile.name)
        
        // Convert file to base64 for transfer
        const reader = new FileReader()
        reader.onload = () => {
            const base64Data = reader.result.split(',')[1] // Remove data URL prefix
            
            // Send message to main page via chrome messaging
            if (chrome.runtime && chrome.runtime.sendMessage) {
                chrome.runtime.sendMessage({
                    action: 'imageSelected',
                    fileName: selectedFile.name,
                    fileSize: selectedFile.size,
                    fileType: selectedFile.type,
                    base64Data: base64Data
                }, (response) => {
                    if (chrome.runtime.lastError) {
                        console.error("Message sending error:", chrome.runtime.lastError)
                    } else {
                        console.log("Image sent successfully")
                        window.close()
                    }
                })
            } else {
                // Fallback for testing outside chrome extension
                console.log("Chrome runtime not available - testing mode")
                window.close()
            }
        }
        reader.onerror = () => {
            alert('Error processing file. Please try again.')
        }
        reader.readAsDataURL(selectedFile)
    }
}

function closeUploadPage() {
    console.log("Closing upload page")
    window.close()
}