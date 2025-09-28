# TeachMe – ShellHacks 2025

*A Chrome extension that turns questions into step-by-step explanations with AI tutoring and Manim animations.*

[![Shell Hacks 2025](https://img.shields.io/badge/Shell%20Hacks-2025-blue?style=for-the-badge)](https://shellhacks.net/) 
[![Manim Powered](https://img.shields.io/badge/Manim-Powered-orange?style=for-the-badge)](https://manim.community/) 
[![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-4285F4?style=for-the-badge)](https://developer.chrome.com/docs/extensions/) 

---

<img width="1919" height="1079" alt="Screenshot 2025-09-28 102559" src="https://github.com/user-attachments/assets/96fc018a-0a7a-48c5-9b21-048ef947749d" />
<img width="1919" height="1079" alt="Screenshot 2025-09-28 102923" src="https://github.com/user-attachments/assets/58990943-0fd0-4c9d-902d-8a43d417d8c0" />
<img width="1919" height="1079" alt="Screenshot 2025-09-28 102712" src="https://github.com/user-attachments/assets/064290d2-c4af-43cf-9b6a-8c7c8330fb2e" />
<img width="1919" height="1079" alt="Screenshot 2025-09-28 102622" src="https://github.com/user-attachments/assets/4c789961-cff0-4932-bb51-3eb1b7270795" />

---

## Overview

TeachMe is a learning tool built at ShellHacks 2025. It allows students to ask questions (typed or uploaded as images) directly through a Chrome extension. The system analyzes the problem using Google’s Gemini models and generates both a conversational explanation and an accompanying **Manim animation** for visual understanding.

### Core Features
- **Problem analysis** with Google Gemini (text + image inputs)  
- **Automatic Manim animations** for math, physics, CS, and more  
- **Conversational tutoring** with step-by-step breakdowns  
- **Chrome extension integration** for easy, in-browser access  

---

## Architecture

```
┌──────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Chrome Extension │◄──►│  FastAPI Backend │◄──►│  Manim Engine   │
│ • Popup UI       │    │ • Gemini Models  │    │ • Animation Gen │
│ • Image Upload   │    │ • Agent System   │    │ • Video Export  │
└──────────────────┘    └──────────────────┘    └─────────────────┘
```

---

## How It Works

1. Open the extension and enter a question or upload an image.  
2. The backend uses Google Gemini to analyze the input.  
3. An explanation is generated and paired with curated resources.  
4. A Manim script is created, rendered, and sent back as an animation.  
5. The animation plays directly in the extension popup.  

---

## Tech Stack

- **Frontend:** Chrome Extension (HTML/CSS/JS, Manifest v3)  
- **Backend:** Python (FastAPI, uvicorn)  
- **AI:** Google Gemini Pro & Vision models, ADK multi-agent system  
- **Animations:** Manim CE, AI-generated scripts  
- **Other tools:** Pillow (image handling), dotenv (config), Ruff (linting)  

---

## Quick Start

### Prerequisites
- Python 3.12+  
- Chrome browser  
- UV package manager (`pip install uv`)  

### Setup
```bash
git clone https://github.com/jkion2/TeachMe.git
cd TeachMe/backend

uv sync
cp .env.example .env   # Add your Google API key
```

### Run Backend
```bash
uv run uvicorn main:app --reload --port 8000
```

### Load Chrome Extension
1. Go to `chrome://extensions/`  
2. Enable **Developer mode**  
3. Click **Load unpacked** → select `/frontend`  
4. The TeachMe icon will appear in your toolbar  

---

## Examples

**Input:** “Explain the derivative of sin(x)”  
**Output:** Conversational explanation with a Manim animation showing the slope of sine evolving into cosine.  

**Input:** Image of a projectile motion problem  
**Output:** Animation of trajectory, vector breakdowns, and formula derivation.  

---

## Future Work

- Progressive Web App version  
- Voice input + text-to-speech output  
- Collaborative study sessions  
- LMS (Canvas/Blackboard) integration  
- Learning analytics and progress tracking  

---

## Team

Built at ShellHacks 2025 by:  
- **Alvin Abraham** – Full Stack 
- **Samarth Upadhya** – Full Stack 
- **Kush Havinal** – Frontend   
- **Marion Forrest** – Backend     

---

## Acknowledgments
- ShellHacks organizers  
- Google ADK / Gemini teams  
- Manim community  
- Chrome Extension API  

---

If you like this project, give us a star on GitHub! :D 
