# 🧠 Prompt Processor with Vertex AI Gemini-Pro

## Overview

The **Prompt Processor** is a semantic analysis service that uses **Vertex AI's Gemini-Pro LLM** via **LangChain** to extract deep semantic meaning from user chat messages.

## Features

### 🎯 What It Does

1. **Semantic Intent Detection**
   - Classifies user intent (service_search, business_query, etc.)
   - Confidence scoring for intent accuracy

2. **Advanced Entity Extraction**
   - Locations (Sri Lankan cities)
   - Service types (plumber, electrician, etc.)
   - Price ranges and budget mentions
   - Time urgency (today, urgent, asap)
   - Quality requirements (experienced, certified)

3. **Sentiment Analysis**
   - Detects user sentiment (positive, neutral, negative, urgent)
   - Urgency level assessment (low, medium, high, critical)

4. **Semantic Understanding**
   - Extracts underlying user needs
   - Contextual comprehension
   - Conversational memory integration

5. **Action Suggestions**
   - Recommends next steps for the system
   - Actionable insights for agent routing

## Architecture

```
User Message
     │
     ▼
PreProcessor
     │
     ▼
PromptProcessor (Gemini-Pro)
     │
     ├─► System Prompt (Semantic Analysis Instructions)
     │
     ├─► User Context (Role, Location, History)
     │
     ├─► Conversation History (Last 3 messages)
     │
     ▼
Vertex AI Gemini-Pro LLM
     │
     ▼
Structured JSON Response
     │
     ├─► Intent & Confidence
     ├─► Entities
     ├─► Sentiment
     ├─► Urgency Level
     ├─► Semantic Meaning
     ├─► Key Phrases
     ├─► Suggested Actions
     └─► Reasoning
```

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install:
- `langchain==0.1.0`
- `langchain-google-vertexai==0.1.0`
- `langchain-core==0.1.0`
- `google-cloud-aiplatform==1.38.0`
- `google-auth==2.23.4`

### 2. Configure Google Cloud

#### Option A: Using Service Account (Production)

1. Create a service account in GCP Console
2. Download the JSON key file
3. Set environment variable:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

#### Option B: Using gcloud CLI (Development)

```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Login
gcloud auth application-default login

# Set project
gcloud config set project YOUR_PROJECT_ID
```

### 3. Enable Required APIs

```bash
# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com

# Verify
gcloud services list --enabled | grep aiplatform
```

### 4. Configure Environment Variables

Create `backend/.env` file:

```bash
# Copy example file
cp .env.example .env

# Edit with your values
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
VERTEX_AI_LOCATION=us-central1
GEMINI_MODEL=gemini-pro
GEMINI_TEMPERATURE=0.2
GEMINI_MAX_TOKENS=1024
```

## Usage

### In Code

The Prompt Processor is automatically integrated into the PreProcessor:

```python
from app.orchestration.preprocessor import PreProcessor

preprocessor = PreProcessor()

# Process a message
result = await preprocessor.process(
    user_id="user_123",
    message="I need an electrician in Colombo urgently",
    session_id="session_456"
)

# Access semantic analysis
semantic = result["semantic_analysis"]
print(f"Intent: {semantic['intent']}")
print(f"Confidence: {semantic['confidence']}")
print(f"Entities: {semantic['entities']}")
print(f"Urgency: {semantic['urgency_level']}")
```

### Response Format

```json
{
  "intent": "service_search",
  "intent_confidence": 0.95,
  "semantic_meaning": "User needs an electrician in Colombo urgently",
  "entities": {
    "locations": ["Colombo"],
    "service_types": ["Electrician"],
    "time_urgency": ["urgent"],
    "quality_requirements": []
  },
  "sentiment": "urgent",
  "urgency_level": "high",
  "key_phrases": ["need electrician", "Colombo", "urgent"],
  "suggested_actions": [
    "search_providers",
    "filter_by_location",
    "prioritize_available"
  ],
  "confidence": 0.90,
  "reasoning": "Clear service request with location and urgency",
  "user_id": "user_123",
  "timestamp": "2025-11-21T10:30:00.000Z",
  "processor": "gemini-pro"
}
```

## Fallback Mode

If Vertex AI is not configured, the system automatically falls back to rule-based processing:

```python
# Fallback activated when:
# - GOOGLE_CLOUD_PROJECT not set
# - Authentication fails
# - LangChain not installed
# - Network issues

# Fallback uses:
# - Keyword matching
# - Regular expressions
# - Rule-based entity extraction
# - Basic sentiment detection
```

## Testing

### Test the Prompt Processor

```python
# backend/test_prompt_processor.py
import asyncio
from app.services.prompt_processor import PromptProcessor

async def test():
    processor = PromptProcessor()
    
    # Test message
    result = await processor.process_chat(
        message="Find me a plumber in Kandy",
        user_id="test_user",
        user_context={"role": "consumer", "location": "Kandy"}
    )
    
    print(f"Intent: {result['intent']}")
    print(f"Entities: {result['entities']}")
    print(f"Confidence: {result['confidence']}")

asyncio.run(test())
```

Run test:

```bash
python test_prompt_processor.py
```

### Health Check

```python
health = await processor.health_check()
print(health)
# Output: {'status': 'healthy', 'llm_available': True, 'model': 'gemini-pro'}
```

## Configuration Options

### Gemini-Pro Parameters

Adjust in `backend/app/core/config.py`:

```python
# Temperature (0.0 = deterministic, 1.0 = creative)
GEMINI_TEMPERATURE: float = 0.2

# Max tokens in response
GEMINI_MAX_TOKENS: int = 1024

# Top-p (nucleus sampling)
GEMINI_TOP_P: float = 0.8

# Top-k (token selection)
GEMINI_TOP_K: int = 40
```

### System Prompt Customization

Edit the prompt in `prompt_processor.py`:

```python
def _create_semantic_analysis_prompt(self) -> str:
    return """Your custom system prompt here..."""
```

## Integration Points

### 1. PreProcessor Integration

The Prompt Processor is called in the PreProcessor during Step 3:

```python
# app/orchestration/preprocessor.py
semantic_analysis = await self.prompt_processor.process_chat(
    message=cleaned_message,
    user_id=user_id,
    conversation_history=session_context.get("history", []),
    user_context={...}
)
```

### 2. Router Integration

The Router can use semantic analysis for better routing:

```python
# app/orchestration/router.py
semantic = preprocessed_data.get("semantic_analysis")
if semantic:
    intent = semantic["intent"]
    confidence = semantic["confidence"]
    # Use for routing decision
```

### 3. Agent Integration

Agents receive enriched data with semantic insights:

```python
# app/agents/consumer_agent.py
def execute(self, task_plan, user_id, session_id):
    semantic = task_plan.get("preprocessed_data", {}).get("semantic_analysis")
    if semantic:
        urgency = semantic["urgency_level"]
        # Prioritize based on urgency
```

## Cost Optimization

### Vertex AI Pricing

Gemini-Pro pricing (as of Nov 2024):
- **Input**: $0.00025 per 1K characters
- **Output**: $0.0005 per 1K characters

### Optimization Tips

1. **Caching**: Cache results for similar queries
2. **Batch Processing**: Process multiple messages together
3. **Fallback First**: Use rule-based for simple queries
4. **Token Limits**: Keep prompts concise
5. **Region Selection**: Use nearest region for lower latency

Example cost for 1000 messages:
- Average message: 100 characters
- Average response: 500 characters
- Cost: ~$0.30 per 1000 messages

## Monitoring

### Logging

```python
# Enable detailed logging
LOG_LEVEL=DEBUG

# View logs
tail -f logs/backend.log | grep "PromptProcessor"
```

### Metrics to Track

- Response time
- Confidence scores
- Fallback rate
- Error rate
- Token usage

## Troubleshooting

### Common Issues

1. **"LangChain not available"**
   ```bash
   pip install langchain langchain-google-vertexai
   ```

2. **Authentication Error**
   ```bash
   gcloud auth application-default login
   ```

3. **"Permission Denied"**
   - Enable Vertex AI API
   - Check service account permissions
   - Verify IAM roles

4. **"Model not found"**
   - Check VERTEX_AI_LOCATION
   - Verify model availability in region

5. **Timeout Issues**
   - Increase timeout in LangChain config
   - Check network connectivity
   - Try different region

## Best Practices

1. **Always have fallback**: System should work without Gemini
2. **Validate responses**: Check JSON structure
3. **Log everything**: Track performance and errors
4. **Monitor costs**: Set budget alerts in GCP
5. **Version control prompts**: Track prompt changes
6. **Test thoroughly**: Unit tests + integration tests

## Next Steps

1. **Caching Layer**: Add Redis for response caching
2. **Prompt Versioning**: A/B test different prompts
3. **Fine-tuning**: Train custom model for Sri Lankan context
4. **Multi-language**: Add Sinhala/Tamil support
5. **Advanced Analytics**: Track semantic patterns

## Resources

- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [LangChain Documentation](https://python.langchain.com/)
- [Gemini-Pro Guide](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)
- [GCP Pricing Calculator](https://cloud.google.com/products/calculator)

---

**Status**: ✅ Ready for production use with proper GCP setup!
