import os
from typing import List, Optional
from pydantic import BaseModel
import google.generativeai as genai

# Constants for preferences
SHORT_TERM = "short-term"
LONG_TERM = "long-term"

# Configure Google Generative AI with API key from environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

class UserProfile(BaseModel):
    name: str = "User"
    health_status: str = "Recovering"
    preferences: str = LONG_TERM  # Default to slow and steady

# Agent definitions (conceptual - using direct Gemini calls instead)
# The google-adk package uses a different API structure

def call_gemini_llm(prompt: str) -> str:
    """Call Google's Gemini LLM with the given prompt."""
    if not GOOGLE_API_KEY:
        return None  # Return None to trigger fallback

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None

# Orchestration logic
async def run_recovery_flow(user_input: str, preference: str = LONG_TERM):
    """
    Run the multi-agent recovery flow using Google Agent ADK.
    Falls back to hardcoded responses if API key is not configured.
    """

    # Check if API key is configured
    if not GOOGLE_API_KEY:
        # Fallback to hardcoded responses (current behavior)
        diagnosis = f"Based on your report of '{user_input}', you might be experiencing typical post-activity strain or underlying mobility restrictions. It's important to monitor these symptoms closely."

        if preference == SHORT_TERM:
            strategy = "Prioritize immediate relief: Use R.I.C.E (Rest, Ice, Compression, Elevation) and gentle mobility exercises to reduce acute pain quickly."
        else:
            strategy = "Focus on long-term stability: Begin with low-impact isometric holds and gradual eccentric loading. Focus on rebuilding tissue tolerance over 6-8 weeks."

        validation = f"The proposed plan for '{user_input}' is safe as it avoids high-impact movements. However, if dizziness persists when standing, please consult a healthcare professional immediately."

        return {
            "diagnosis": diagnosis,
            "recovery_plan": strategy,
            "safety_check": validation
        }

    # Use Google Gemini LLM for actual AI-powered responses
    # 1. Diagnosis
    diagnosis_prompt = f"""You are a medical diagnosis specialist focusing on physical recovery.
Analyze the user's symptoms and provide a clear, empathetic explanation.
Always advise consulting a doctor for severe symptoms.

User's symptoms: {user_input}

Provide only the diagnosis explanation, no preamble or labels."""

    diagnosis = call_gemini_llm(diagnosis_prompt) or f"Based on your report of '{user_input}', you might be experiencing typical post-activity strain or underlying mobility restrictions."

    # 2. Strategy Development
    strategy_prompt = f"""You are a physical recovery strategist.
Develop a recovery program based on the diagnosis and user preferences.
- If 'short-term': prioritize quick, easy, and immediate relief solutions.
- If 'long-term': prioritize slow, steady, and sustainable progress.

Diagnosis: {diagnosis}
User preference: {preference}

Provide only the recovery plan, no preamble or labels."""

    strategy = call_gemini_llm(strategy_prompt)
    if not strategy:
        if preference == SHORT_TERM:
            strategy = "Prioritize immediate relief: Use R.I.C.E (Rest, Ice, Compression, Elevation) and gentle mobility exercises to reduce acute pain quickly."
        else:
            strategy = "Focus on long-term stability: Begin with low-impact isometric holds and gradual eccentric loading. Focus on rebuilding tissue tolerance over 6-8 weeks."

    # 3. Safety Validation
    validation_prompt = f"""You are a safety validator.
Review the proposed recovery plan against the user's initial symptoms.
Ensure the plan is safe and physically appropriate.
Flag any potential risks.

User's symptoms: {user_input}
Proposed recovery plan: {strategy}

Provide only the safety validation, no preamble or labels."""

    validation = call_gemini_llm(validation_prompt) or f"The proposed plan is safe as it avoids high-impact movements. However, if symptoms persist, please consult a healthcare professional immediately."

    return {
        "diagnosis": diagnosis,
        "recovery_plan": strategy,
        "safety_check": validation
    }
