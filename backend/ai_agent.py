
import google.generativeai as genai
import json
from tools import query_medgemma, call_emergency
from config import GEMINI_API_KEY

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash-exp", generation_config={"temperature": 0.2})

def ask_mental_health_specialist(query: str) -> str:
    """Generate a therapeutic response using the MedGemma model."""
    return query_medgemma(query)

def emergency_call_tool() -> str:
    """Place an emergency call to the safety helpline."""
    call_emergency()
    return "Emergency call placed. Help is on the way."

def find_nearby_therapists_by_location(location: str) -> str:
    """Find licensed therapists near the specified location."""
    return (
        f"Here are some therapists near {location}:\n"
        "- Dr. Ayesha Kapoor - +1 (555) 123-4567\n"
        "- Dr. James Patel - +1 (555) 987-6543\n"
        "- MindCare Counseling Center - +1 (555) 222-3333"
    )

SYSTEM_PROMPT = """
You are an AI supporting mental health conversations with warmth and vigilance.
You have 3 tools - respond with JSON to use them:

1. For mental health questions: {"tool": "ask_mental_health_specialist", "query": "user's question"}
2. For therapist locations: {"tool": "find_nearby_therapists_by_location", "location": "city name"}  
3. For emergencies/self-harm: {"tool": "emergency_call_tool"}

Use tools when needed, otherwise respond normally. Always prioritize safety.
"""

def parse_response(user_input: str):
    """Process user input and return (tool_called_name, final_response)"""
    try:
        # Generate response
        prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_input}\nAssistant:"
        response = model.generate_content(prompt).text.strip()
        
        # Check if JSON tool call
        if response.startswith('{') and response.endswith('}'):
            try:
                tool_call = json.loads(response)
                tool_name = tool_call.get("tool")
                
                if tool_name == "ask_mental_health_specialist":
                    result = ask_mental_health_specialist(tool_call.get("query", ""))
                elif tool_name == "find_nearby_therapists_by_location":
                    result = find_nearby_therapists_by_location(tool_call.get("location", ""))
                elif tool_name == "emergency_call_tool":
                    result = emergency_call_tool()
                else:
                    return "unknown_tool", "I'm not sure how to help with that."
                    
                return tool_name, result
            except json.JSONDecodeError:
                pass
        
        # Direct response
        return "direct_response", response
        
    except Exception as e:
        return "error", f"Sorry, I encountered an error: {str(e)}"

# Example usage
if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        tool_called_name, final_response = parse_response(user_input)
        print("TOOL CALLED:", tool_called_name)
        print("ANSWER:", final_response)
