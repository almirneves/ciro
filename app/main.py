import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
import requests
from typing import Dict
import json
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Add webhook endpoint
@app.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return Response(content=challenge, media_type="text/plain")
    return Response(status_code=403)

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    
    if "object" in data and data["object"] == "whatsapp_business_account":
        for entry in data["entry"]:
            for change in entry["changes"]:
                if change["value"]["messages"]:
                    message = change["value"]["messages"][0]
                    sender_id = message["from"]
                    message_text = message["text"]["body"]
                    
                    # Process the message
                    await process_message(sender_id, message_text)
    return Response(status_code=200)

# Configure Gemini
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

# Initialize Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Store conversation history (in production, use a proper database)
conversations: Dict[str, list] = {}

# System Prompt
system_prompt = """You are a professional fitness coach and nutritionist. Your goal is to help clients achieve their fitness goals through comprehensive health management. Be professional, friendly, and supportive. Ask relevant questions to understand their complete health picture. Provide practical, achievable recommendations based on their current situation and goals.

Key principles:
1. Holistic health approach (exercise, nutrition, recovery, mental health)
2. Personalized recommendations based on individual metrics
3. Progress tracking and adjustment
4. Education and habit formation
5. Safety and gradual progression
6. Evidence-based practices
7. Individualized approach
8. Long-term sustainability

When creating workout plans:
- Start with a 5-10 minute warm-up and end with a 5-10 minute cool-down
- Include exercises for all major muscle groups (push, pull, legs, core)
- Progress from basic to advanced exercises using periodization
- Include modifications for different fitness levels and injuries
- Suggest appropriate rest days (24-48 hours between muscle groups)
- Consider body metrics and goals (muscle building, fat loss, strength)
- Include variety to prevent plateaus
- Progressively increase intensity, volume, or frequency
- Include mobility and flexibility exercises
- Consider time constraints and equipment availability

When giving nutrition advice:
- Calculate caloric needs based on goals and activity level
- Provide balanced macronutrient ratios (typically 40% carbs, 30% protein, 30% fats)
- Suggest healthy meal ideas with portion control
- Consider dietary restrictions (vegetarian, vegan, gluten-free, etc.)
- Focus on sustainable habits rather than restrictive diets
- Include hydration recommendations (at least 2-3L per day)
- Provide supplement guidance based on individual needs
- Consider meal timing and nutrient timing
- Include healthy snacking options
- Address common nutritional deficiencies

When tracking progress:
- Monitor body measurements:
  * Weight (weekly)
  * Body fat percentage (monthly)
  * Muscle mass percentage (monthly)
  * Waist circumference (monthly)
- Track hydration levels (daily goal: 2-3L)
- Monitor mood and energy levels (daily 1-5 scale)
- Track supplement intake (daily)
- Monitor habit completion (daily)
- Track sleep quality and duration
- Monitor workout performance
- Track recovery status
- Record any injuries or pain

Daily Motivation:
- Provide encouraging messages tailored to current progress
- Share relevant success stories
- Offer tips for maintaining motivation
- Celebrate small victories and milestones
- Help overcome setbacks with practical solutions
- Provide positive reinforcement
- Offer accountability and support
- Share inspiring quotes and tips

Supplement Recommendations:
- Base recommendations on scientific evidence
- Consider individual needs and goals
- Focus on quality over quantity
- Suggest timing for optimal absorption
- Provide dosage guidelines
- Address potential interactions
- Consider budget constraints
- Prioritize whole foods first

Habit Formation:
- Break down goals into small, manageable steps
- Focus on consistency over perfection
- Use habit stacking techniques
- Create accountability systems
- Track progress visually
- Set realistic expectations
- Celebrate small wins
- Address obstacles proactively

Mental Health Focus:
- Address stress management
- Provide mindfulness tips
- Encourage proper sleep hygiene
- Address body image concerns
- Provide coping mechanisms
- Encourage self-care practices
- Address perfectionism
- Promote positive self-talk

Communication Style:
- Always be positive and encouraging
- Use clear, simple language
- Provide specific, actionable advice
- Show empathy and understanding
- Be patient and supportive
- Celebrate progress
- Be realistic about timelines
- Provide education
- Address concerns proactively

Always maintain a positive, encouraging tone while being realistic about progress. Emphasize the journey over the destination and focus on sustainable, healthy practices rather than quick fixes.

Commands and Features:
- !weight [number] [kg/lbs] - Track weight measurements
- !bodyfat [percentage] - Track body fat percentage
- !hydration [ml] - Track water intake
- !mood [1-5] - Track mood and energy levels
- !supplements [list] - Track supplement intake
- !habits [completed habits] - Track habit completion
- !meal [description] - Track meals and nutrition
- !progress - Show comprehensive progress summary
- !workout [goal] - Get personalized workout plan
- !nutrition [goal] - Get personalized nutrition plan
- !supplements [goal] - Get supplement recommendations
- !habits - Get habit suggestions
- !motivation - Get motivational message
- !sleep [hours] - Track sleep duration
- !recovery [1-5] - Track recovery status

Remember to always prioritize safety, individual needs, and long-term sustainability in all recommendations.
"""

def get_ai_response(message: str, phone_number: str) -> str:
    """Get AI response using OpenAI's GPT with fitness tracking features"""
    # Get conversation history or create new one
    if phone_number not in conversations:
        conversations[phone_number] = []
    
    # Parse commands
    if message.startswith('!'):
        command = message.split()[0][1:]  # Remove '!' and get command
        args = message.split()[1:] if len(message.split()) > 1 else []
        
        if command == 'weight':
            if len(args) >= 2:
                weight = float(args[0])
                unit = args[1].lower()
                if unit == 'lbs':
                    weight = weight * 0.453592  # Convert to kg
                conversations[phone_number].append({"role": "system", "content": f"Current weight: {weight:.1f} kg"})
                return f"Weight recorded: {weight:.1f} kg"
            
        elif command == 'bodyfat':
            if len(args) >= 1:
                bodyfat = float(args[0])
                conversations[phone_number].append({"role": "system", "content": f"Current body fat: {bodyfat:.1f}%"})
                return f"Body fat recorded: {bodyfat:.1f}%"
            
        elif command == 'hydration':
            if len(args) >= 1:
                water = float(args[0])
                conversations[phone_number].append({"role": "system", "content": f"Water intake: {water} ml"})
                return f"Water intake recorded: {water} ml"
            
        elif command == 'mood':
            if len(args) >= 1:
                mood = int(args[0])
                if 1 <= mood <= 5:
                    conversations[phone_number].append({"role": "system", "content": f"Mood: {mood}/5"})
                    return f"Mood recorded: {mood}/5"
            
        elif command == 'supplements':
            if len(args) >= 1:
                supplements = ' '.join(args)
                conversations[phone_number].append({"role": "system", "content": f"Supplements: {supplements}"})
                return f"Supplements recorded: {supplements}"
            
        elif command == 'habits':
            if len(args) >= 1:
                habits = ' '.join(args)
                conversations[phone_number].append({"role": "system", "content": f"Completed habits: {habits}"})
                return f"Habits recorded: {habits}"
            
        elif command == 'meal':
            if len(args) >= 1:
                meal = ' '.join(args)
                conversations[phone_number].append({"role": "system", "content": f"Meal: {meal}"})
                return f"Meal recorded: {meal}"
            
        elif command == 'progress':
            # Generate progress summary
            return "Progress summary: [TODO: Implement progress tracking]"
            
    # Add user message to history
    conversations[phone_number].append({"role": "user", "content": message})
    
    # Prepare the conversation context with fitness-specific data
    messages = [
        {"role": "system", "content": system_prompt},
        *conversations[phone_number][-10:]  # Keep last 10 messages for context
    ]
    
    # Get response from Gemini
    try:
        response = model.generate_content(messages)
        ai_message = str(response.text)
        
        # Store AI response in conversation history
        conversations[phone_number].append({"role": "assistant", "content": ai_message})
        
        # Store the last workout/nutrition plan if it was provided
        if "workout plan" in ai_message.lower() or "nutrition plan" in ai_message.lower():
            last_plan = ai_message
            conversations[phone_number].append({"role": "system", "content": f"Last plan: {last_plan}"})
        
        return ai_message
    except Exception as e:
        print(f"Error getting AI response: {e}")
        return "I apologize, but I'm having trouble processing your message. Please try again later."

def send_whatsapp_message(phone_number: str, message: str):
    """Send message using WhatsApp Cloud API"""
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": message}
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")

@app.get("/webhook")
async def verify_webhook(request: Request):
    """Verify webhook for WhatsApp API setup"""
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return Response(content=challenge, media_type="text/plain")
        return Response(status_code=403)

@app.post("/webhook")
async def webhook(request: Request):
    """Handle incoming WhatsApp messages"""
    try:
        body = await request.json()
        
        # Extract message data
        entry = body.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        message = value.get("messages", [{}])[0]
        
        if message:
            phone_number = message.get("from")
            message_text = message.get("text", {}).get("body", "")
            
            # Get AI response
            response = get_ai_response(message_text, phone_number)
            
            # Send response back via WhatsApp
            send_whatsapp_message(phone_number, response)
        
        return {"status": "success"}
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
