# WhatsApp Fitness Coach

A WhatsApp-based AI fitness coach that provides personalized workout and nutrition plans to help users achieve their fitness goals.

## Prerequisites

1. WhatsApp Business API access
   - Meta Developer Account
   - WhatsApp Business Account
   - Phone number verified with WhatsApp Business

2. OpenAI API Key

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a .env file with the following variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   WHATSAPP_TOKEN=your_whatsapp_token
   WHATSAPP_VERIFY_TOKEN=your_webhook_verify_token
   PHONE_NUMBER_ID=your_whatsapp_phone_number_id
   ```

## Running the Application

```bash
uvicorn app.main:app --reload
```

## Features

- Personalized workout plans
- Nutrition guidance
- Progress tracking
- WhatsApp integration
- 24/7 fitness support
- Context-aware responses
- Conversation history tracking