import os
import google.generativeai as genai

def test_gemini():
    print("Testing Gemini API connection...")
    
    # Load API key from environment
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment variables")
        return False
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    try:
        # Test a simple prompt
        prompt = "Hello Gemini! What's the weather like today?"
        response = model.generate_content(prompt)
        
        # Print response
        print("\nTest Response:")
        print(str(response.text))
        
        print("\nGemini API is working correctly!")
        return True
    except Exception as e:
        print(f"Error testing Gemini API: {str(e)}")
        return False

if __name__ == "__main__":
    test_gemini()
