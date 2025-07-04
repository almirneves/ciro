import os
import requests
from typing import Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_whatsapp_api():
    print("Testing WhatsApp API connection...")
    
    # Load environment variables
    whatsapp_token = os.getenv("WHATSAPP_TOKEN")
    verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN")
    phone_number_id = os.getenv("PHONE_NUMBER_ID")
    
    if not all([whatsapp_token, verify_token, phone_number_id]):
        print("Error: WhatsApp credentials not found in environment variables")
        return False
    
    print("\nTesting with credentials:")
    print(f"Token length: {len(whatsapp_token)} characters")
    print(f"Phone Number ID: {phone_number_id}")
    
    # Test webhook verification
    webhook_url = f"https://graph.facebook.com/v17.0/{phone_number_id}"
    
    try:
        # Make a GET request to verify the token
        headers = {
            "Authorization": f"Bearer {whatsapp_token}",
            "Content-Type": "application/json"
        }
        
        print(f"\nMaking request to: {webhook_url}")
        response = requests.get(webhook_url, headers=headers)
        
        print(f"\nResponse status: {response.status_code}")
        print("Response headers:", response.headers)
        print("Response text:", response.text)
        
        if response.status_code == 200:
            print("\nWhatsApp API test successful!")
            print("Response body:", response.json())
            return True
        else:
            print(f"\nWhatsApp API test failed with status code {response.status_code}")
            print("Response body:", response.text)
            return False
            
    except Exception as e:
        print(f"Error testing WhatsApp API: {str(e)}")
        return False

if __name__ == "__main__":
    test_whatsapp_api()
