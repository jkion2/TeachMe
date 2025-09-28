# 🎓 TeachMe - Shell Hacks 2025

*Transform any question into an immersive learning experience with AI-powered tutoring and stunning mathematical animations*

[![Shell Hacks 2025](https://img.shields.io/badge/Shell%20Hacks-2025-blue?style=for-the-badge)](https://shellhacks.net/)
[![Made with AI](https://img.shields.io/badge/Made%20with-AI-brightgreen?style=for-the-badge)](https://github.com)
[![Manim Powered](https://img.shields.io/badge/Manim-Powered-orange?style=for-the-badge)](https://manim.community/)
[![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-4285F4?style=for-the-badge)](https://developer.chrome.com/docs/extensions/)

## 🌟 Overview

**TeachMe** revolutionizes education by combining the power of conversational AI with breathtaking mathematical animations. Available as a Chrome extension, students can ask questions through text or images and receive not just answers, but a complete learning experience featuring:

- 🤖 **Google ADK-Powered AI Tutor** - Advanced conversational AI with Google's Gemini models
- 🎬 **Auto-Generated Manim Animations** - Beautiful visual explanations created in real-time
- � **Intelligent Link Discovery** - Curated educational resources and references
- 📸 **Multi-Modal Input** - Support for both text questions and image-based problems
- 🌐 **Browser Integration** - Seamless Chrome extension for instant access

## ✨ Key Features

### 🧠 **Intelligent Problem Analysis**
- Accepts questions in text format or image uploads through Chrome extension popup
- Powered by Google ADK and Gemini models for advanced AI parsing
- Multi-modal understanding of mathematical concepts, physics problems, and more
- Context-aware agent system that builds on previous interactions

### 🎨 **Automated Visual Explanations**
- Real-time Manim animation generation using AI-driven script creation
- Aesthetic, publication-quality mathematical visualizations
- Intuitive graphics that minimize explanation and maximize understanding
- Animations tailored to specific problem domains with minimal visual clutter

### 💭 **Personal Tutoring Experience**
- Google ADK agent-based conversational AI with memory persistence
- Step-by-step breakdowns of complex problems with educational context
- Curated educational links and resources for deeper learning
- Adaptive responses based on problem complexity and student needs

### 🚀 **Seamless Browser Integration**
- Chrome extension with clean, modern popup interface
- One-click access from any webpage
- Real-time processing with FastAPI backend
- Embedded video player for instant animation viewing

## 🏗️ Architecture

```
┌──────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Chrome Extension │◄──►│  FastAPI Backend │◄──►│  Manim Engine   │
│                  │    │                  │    │                 │
│ • Popup UI       │    │ • Google ADK     │    │ • AI Script Gen │
│ • Image Upload   │    │ • Agent System   │    │ • Video Export  │
│ • Chat Interface │    │ • Link Discovery │    │ • Asset Storage │
└──────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │   Google AI         │
                    │                     │
                    │ • Gemini Models     │
                    │ • Multi-Agent Chat  │
                    │ • Vision API        │
                    └─────────────────────┘
```

## 🎯 How It Works

1. **📝 Input Question**: Students click the Chrome extension and submit a question via text or upload an image
2. **🔍 AI Analysis**: Google ADK agents with Gemini models parse and understand the educational context
3. **💬 Interactive Response**: Multi-agent system provides conversational explanations with curated links
4. **🎬 Animation Generation**: AI generates Manim scripts and renders visual explanations automatically
5. **🎥 Visual Learning**: Students view the generated animation directly in the extension popup
6. **🔄 Continuous Learning**: Session-persistent conversations with follow-up questions and clarifications

## 🛠️ Tech Stack

### Frontend (Chrome Extension)
- **Framework**: Vanilla HTML/CSS/JavaScript
- **UI Components**: Modern popup interface with file upload
- **Extension API**: Chrome Extension Manifest v3
- **Real-time**: Direct API communication with FastAPI backend

### Backend (Python)
- **API Framework**: FastAPI with CORS middleware
- **Dependency Management**: UV package manager with pyproject.toml
- **AI Integration**: Google ADK (Agent Development Kit)
- **Language Models**: Google Gemini Pro and Gemini Vision
- **Session Management**: InMemorySessionService for conversation persistence

### AI & Animation
- **Conversational AI**: Google ADK multi-agent system with specialized roles
- **Vision Processing**: Google Gemini Vision for image-based problem analysis
- **Animation Engine**: Manim Community Edition with AI-generated scripts
- **Educational Content**: Automated link curation and resource discovery

### Infrastructure
- **Development**: Python 3.12+ with modern tooling (Ruff linting)
- **Image Processing**: Pillow (PIL) for image handling
- **File Upload**: Python-multipart for handling form data
- **Environment**: Python-dotenv for configuration management

## 🚀 Quick Start

### Prerequisites
```bash
# Install Python 3.12+
python --version  # Should be 3.12 or higher

# Install UV package manager
pip install uv

# Install Chrome browser for extension testing
```

### Installation
```bash
# Clone the repository
git clone https://github.com/jkion2/TeachMe.git
cd TeachMe

# Set up backend environment
cd backend
uv sync  # Install all dependencies from pyproject.toml

# Set up environment variables
cp .env.example .env
# Add your Google API key to .env file
```

### Configuration
Create a `.env` file in the backend directory:
```env
GOOGLE_API_KEY=your_google_api_key_here

# Optional: Manim settings
MANIM_QUALITY=low_quality  # Options: low_quality, medium_quality, high_quality
```

### Running the Application
```bash
# Start the FastAPI backend
cd backend
uv run uvicorn main:app --reload --port 8000

# Load Chrome Extension
1. Open Chrome and go to chrome://extensions/
2. Enable "Developer mode" (top right toggle)
3. Click "Load unpacked" and select the /frontend directory
4. The TeachMe extension icon should appear in your toolbar
```

## 🎬 Demo Examples

### Example 1: Calculus Problem
**Input**: "Explain the derivative of sin(x)" *(typed in extension popup)*

**AI Response**: "The derivative of sin(x) is cos(x). Let me walk you through why this is true using the limit definition..."

**Generated Animation**: A smooth Manim visualization showing:
- The sine function graphed on a coordinate plane
- A tangent line moving along the curve  
- The slope values being plotted as the cosine function
- Visual representation of the limit process

### Example 2: Physics Problem  
**Input**: *[Uploaded image of projectile motion problem via extension]*

**AI Response**: "I can see this is a projectile motion problem. Let me break down the components and provide some helpful resources..."

**Generated Animation**: 
- Animated projectile trajectory with vector decomposition
- Time-step analysis with position markers
- Solution derivation with key equations highlighted
- Clean, educational visual style with minimal text overlay

## 🎨 Animation Capabilities

Our Manim integration can generate visualizations for:

- **📐 Mathematics**: Calculus, linear algebra, geometry, statistics
- **🔬 Physics**: Mechanics, waves, electromagnetism, thermodynamics  
- **💻 Computer Science**: Algorithms, data structures, complexity analysis
- **📊 Data Science**: Statistical concepts, machine learning visualizations
- **🧮 Engineering**: Signal processing, control systems, circuit analysis

## 🏆 Shell Hacks 2025 Innovation

This project represents several cutting-edge innovations for Shell Hacks 2025:

- **🎯 AI-Driven Animation Generation**: First-of-its-kind automatic Manim script creation and rendering
- **� Google ADK Integration**: Advanced multi-agent conversational AI with persistent memory
- **🌐 Browser-Native Education**: Seamless Chrome extension bringing AI tutoring to any webpage
- **⚡ Real-time Processing**: Sub-minute turnaround from question to complete visual explanation
- **🎨 Aesthetic Excellence**: Publication-quality animations that rival professional educational content
- **📚 Intelligent Resource Curation**: AI-powered discovery of relevant educational links and materials

## 🔮 Future Enhancements

- **📱 Progressive Web App**: PWA version for mobile device access
- **👥 Collaborative Learning**: Multi-student sessions with shared animations
- **🎙️ Voice Integration**: Audio question submission and text-to-speech responses  
- **🌐 Multi-language Support**: Internationalization for global student access
- **� Learning Analytics**: Progress tracking and personalized study recommendations
- **🏫 LMS Integration**: Canvas, Blackboard, and Google Classroom compatibility

## 👥 Team

Built with ❤️ by the TeachMe team for Shell Hacks 2025

- **Samarth Upadhya** - Full Stack Developer & AI Integration Specialist
- **Kush Havinal** - Frontend Developer & Chrome Extension Lead  
- **Marion Forrest** - Backend Developer & Manim Animation Expert
- **Alvin Abraham** - Full Stack Developer & System Architecture

## 🙏 Acknowledgments

- Shell Hacks 2025 organizers for this incredible hackathon opportunity
- Google ADK team for providing cutting-edge conversational AI tools
- Manim Community for the outstanding mathematical animation framework  
- The open-source Python ecosystem for robust development tools
- Chrome Extensions API for seamless browser integration capabilities

---

<div align="center">

**Ready to revolutionize education? Star ⭐ this repo and join the visual learning revolution!**

[🚀 Try the Extension](https://github.com/jkion2/TeachMe) • [📖 Documentation](https://github.com/jkion2/TeachMe/wiki) • [🎬 Demo Video](https://github.com/jkion2/TeachMe)

*Made with 💻 and ☕ at Shell Hacks 2025*

</div>
