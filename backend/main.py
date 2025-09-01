
# 🌟 CLEAN FastAPI Backend - Returns properly formatted responses
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import your AI agent components
from ai_agent import parse_response

app = FastAPI(title="SerenityAI Mental Health API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class ChatQuery(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    tool_used: str = "mental_health_specialist"

def extract_clean_text_only(response_text):
    """Extract ONLY the therapeutic text, clean up any artifacts"""
    try:
        # Clean up any remaining artifacts
        content = response_text.replace('"response":', '').replace('"', '').strip()
        
        # Remove any tool information if present
        if "Tool used:" in content:
            if "Tool result:" in content:
                content = content.split("Tool result:")[-1].strip()
            else:
                lines = [line for line in content.split('\n') 
                        if not line.startswith("Tool used:")]
                content = '\n'.join(lines).strip()
        
        # Return just the therapeutic message
        if content:
            return content
        
        return "Hi there! I'm here to listen and support you. What's on your mind today?"
        
    except Exception as e:
        print(f"Error extracting response: {e}")
        return "I'm here to support you. How can I help you today?"

@app.post("/ask")
async def chat_with_ai(query: ChatQuery):
    """Return clean therapeutic response"""
    try:
        if not query.message or not query.message.strip():
            return ChatResponse(
                response="I'd love to hear what's on your mind. Please share with me.",
                tool_used="validation"
            )
        
        # Process through AI agent
        tool_called_name, final_response = parse_response(query.message.strip())
        
        # Get clean text response
        clean_response = extract_clean_text_only(final_response)
        
        # Map tool names to consistent format
        tool_mapping = {
            "ask_mental_health_specialist": "mental_health_specialist",
            "emergency_call_tool": "emergency_support",
            "find_nearby_therapists_by_location": "therapist_referral",
            "direct_response": "mental_health_specialist",
            "error": "error_fallback",
            "unknown_tool": "error_fallback",
            "parse_error": "error_fallback"
        }
        
        mapped_tool = tool_mapping.get(tool_called_name, "mental_health_specialist")
        
        return ChatResponse(
            response=clean_response,
            tool_used=mapped_tool
        )
        
    except Exception as e:
        print(f"Error: {e}")
        return ChatResponse(
            response="I'm experiencing some technical difficulties, but I'm still here to support you. What would you like to talk about?",
            tool_used="error_fallback"
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "SerenityAI is ready to help"}

if __name__ == "__main__":
    print("🌟 Starting Clean SerenityAI API...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
