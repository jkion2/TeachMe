# TeachMe Chat Service (Google ADK) - Text & Image Support

A conversational AI service that provides educational assistance for math and science problems using Google's Agent Development Kit (ADK). This service supports **both text and image inputs** and offers:

1. **Relevant Links Discovery** - Uses ADK search agent with Google Search tool
2. **Interactive Chat** - Provides tutoring-style conversation using ADK conversation agent  
3. **Vision Analysis** - Analyzes educational images to extract math problems and content

## Features

### 🔗 Links Endpoints
- **POST `/links`** - Accepts text context and/or base64 encoded images
- **POST `/links/upload`** - Accepts direct file uploads with optional text
- AI-powered educational content filtering using vision analysis
- Intelligent relevance scoring
- Fallback to curated educational sites when needed

### 💬 Chat Endpoints  
- **POST `/chat`** - Traditional text-only conversation
- **POST `/chat/with-image`** - Conversation with image upload support
- Powered by Google ADK with Gemini 2.0 Flash model
- Educational tutor agent with specialized instruction
- Multi-agent architecture with coordinator
- Context-aware conversations with learning focus

### 👁️ Vision Analysis
- Extracts mathematical equations and formulas from images
- Identifies problem types and educational context
- Processes handwritten and printed content
- Supports diagrams, graphs, and geometric figures
- Integrates seamlessly with search and chat functionality

## Architecture

### **Agent Hierarchy:**
```
Coordinator Agent (gemini-2.0-flash-exp)
├── Vision Agent (image analysis)
├── Search Agent (with google_search tool)
└── Conversation Agent (educational tutor)
```

### **Key Components:**

1. **Vision Agent** - Analyzes educational images
   - Extracts mathematical content from images
   - Identifies problem types and context
   - Supports handwritten and printed content
   - Processes diagrams and geometric figures

2. **Search Agent** - Specialized in finding educational resources
   - Uses Google ADK's `google_search` tool
   - Optimized prompts for educational content discovery
   - Intelligent link extraction and relevance scoring

3. **Conversation Agent** - Expert educational tutor
   - Gemini 2.0 Flash model with educational instruction
   - Step-by-step learning approach
   - Socratic method questioning
   - Patient, encouraging personality

4. **Coordinator Agent** - Manages agent delegation
   - Routes requests to appropriate sub-agents
   - Maintains conversation context
   - Ensures cohesive educational experience

## Setup

### 1. Install Dependencies
```bash
cd backend
uv sync
```

### 2. Set Up Environment Variables

Copy `.env.example` to `.env` and fill in your API key:

```bash
cp .env.example .env
```

#### Required API Key:

**Google AI API Key** (Required for ADK agents):
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Set `GOOGLE_API_KEY` in your `.env` file

**Note**: Google ADK handles search functionality internally through the `google_search` tool, so no additional search API configuration is needed.

### 3. Run the Server

```bash
uvicorn main:app --reload
```

The server will start on `http://localhost:8000`

## API Usage

### Get Educational Links (Text Input)

**POST** `/links`

```json
{
  "context": "I need help solving quadratic equations like x^2 + 5x + 6 = 0",
  "image_base64": ""
}
```

### Get Educational Links (Image Input)

**POST** `/links`

```json
{
  "context": "Help me understand this problem",
  "image_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEA..."
}
```

### Get Educational Links (File Upload)

**POST** `/links/upload`

Form data:
- `image`: Image file (PNG, JPEG, etc.)
- `text`: Optional descriptive text

**Response for all link endpoints:**
```json
{
  "links": [
    {
      "title": "Khan Academy - Factoring quadratics",
      "url": "https://www.khanacademy.org/math/algebra/...",
      "snippet": "Learn how to factor quadratic expressions...",
      "relevance": 0.85
    }
  ],
  "status": "success"
}
```

### Chat About Problems (Text Only)

**POST** `/chat`

```json
{
  "chat_history": [
    {
      "role": "user",
      "content": "I'm stuck on factoring x^2 + 5x + 6 = 0. Can you help?"
    }
  ]
}
```

### Chat About Problems (With Image)

**POST** `/chat/with-image`

Form data:
- `chat_history`: JSON string of chat messages
- `image`: Image file containing math problem

**Response for chat endpoints:**
```json
{
  "response": "I'd be happy to help you factor x^2 + 5x + 6 = 0! Let's break this down step by step...",
  "suggestions": [
    "Can you show me a similar example?",
    "What's the next step in solving this?"
  ],
  "follow_up_questions": [
    "Does this step make sense to you?",
    "Would you like me to explain any part in more detail?"
  ],
  "image_analyzed": true,
  "status": "success"
}
```

## Testing

Use the provided test script to verify everything is working:

```bash
python test_chat_service.py
```

This will test both endpoints and show you sample interactions.

## Architecture

### Components

1. **SearchAgent** - Handles finding relevant educational resources
   - Google Custom Search integration
   - Relevance scoring algorithm
   - Educational content filtering
   - Fallback resources for reliability

2. **ConversationAgent** - Manages educational conversations
   - Gemini AI integration
   - Educational tutor system prompt
   - Context management
   - Response enhancement with suggestions

## Key Features

- **Multi-Agent Architecture**: Uses Google ADK's agent system for specialized tasks
- **Educational Focus**: Optimized specifically for math and science tutoring
- **Intelligent Search**: AI-powered educational resource discovery
- **Step-by-step Learning**: Breaks down complex problems systematically
- **Adaptive Responses**: Adjusts based on conversation context and student needs
- **Robust Fallbacks**: Works even when external search fails
- **Comprehensive Logging**: Detailed monitoring and debugging support
- **Modern AI Models**: Powered by Gemini 2.0 Flash for latest capabilities

## Performance Notes

- **Initial Response Time**: ADK agents may take 10-30 seconds for first response
- **Subsequent Responses**: Faster due to agent warm-up and context retention
- **Search Quality**: Google ADK's search tool provides more comprehensive results
- **Agent Coordination**: Multi-agent system provides more nuanced responses

## Integration with Frontend

The service is designed to work with your Chrome extension frontend:

1. When a user submits a problem, call `/links` to get educational resources
2. Display the links to the user as reference material
3. Use `/chat` for the conversational interface
4. Maintain chat history in the frontend and send it with each request

## Error Handling

- All endpoints return structured error responses
- Graceful degradation when external APIs fail
- Comprehensive logging for debugging
- Input validation with helpful error messages

## Customization

### Adding New Problem Types

Extend `analyze_problem_type()` in `service_chat.py`:

```python
def analyze_problem_type(context: str) -> str:
    context_lower = context.lower()
    
    if any(term in context_lower for term in ['your', 'new', 'keywords']):
        return "your_new_type"
    # ... existing logic
```

### Custom Educational Resources

Modify `get_subject_specific_resources()` to add your preferred educational sites.

### Conversation Personality

Adjust the `system_prompt` in `ConversationAgent` to change the AI's teaching style.

## Troubleshooting

1. **"API key not found" errors**: Make sure your `.env` file is in the backend directory and properly formatted

2. **Search not working**: The service will use fallback links if Google Custom Search isn't configured

3. **Chat responses are generic**: Ensure `GOOGLE_API_KEY` is set correctly for Gemini AI

4. **Import errors**: Run `uv sync` to install all dependencies

## Future Enhancements

- [ ] Image OCR integration for problem text extraction
- [ ] Subject-specific specialized agents
- [ ] Learning progress tracking
- [ ] Personalized difficulty adjustment
- [ ] Integration with more educational APIs
