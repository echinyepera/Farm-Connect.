import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def get_crop_advice(problem_description):
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return "AI service is currently unavailable. Please contact your local Agritex officer."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        prompt = f"""
        You are a Zimbabwean agricultural expert helping a smallholder farmer.
        The farmer has described a crop problem: "{problem_description}"

        Please provide a diagnosis and treatment recommendation in the following format:
        
        🌿 CROP DIAGNOSIS
        
        Likely issue: [Name of disease/pest] (confidence: X%)
        
        Symptoms: [Brief description of symptoms]
        
        Recommendation:
        ✓ [Actionable step 1]
        ✓ [Actionable step 2]
        
        Prevention:
        ✓ [How to avoid this in the future]
        
        Still concerned? Contact your local Agritex officer: 0775 123 456
        
        IMPORTANT: 
        - If the description is in Shona or Ndebele, understand it and reply in the same language if appropriate, or English if preferred for technical terms.
        - Be concise and practical for a farmer on WhatsApp.
        - If you are very unsure, emphasize contacting an officer.
        """

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error in Gemini API: {e}")
        return "Sorry, I couldn't process your request right now. Please try again later or contact Agritex."
