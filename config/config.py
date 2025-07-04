from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    WHATSAPP_TOKEN: str
    VERIFY_TOKEN: str
    PHONE_NUMBER_ID: str
    
    # Fitness-specific settings
    DEFAULT_WORKOUT_DAYS: int = 5
    DEFAULT_WORKOUT_DURATION: int = 60  # in minutes
    DEFAULT_CALORIE_GOAL: int = 2000
    
    # Body metrics
    DEFAULT_WEIGHT_GOAL: float = 75.0  # in kg
    DEFAULT_BODY_FAT_GOAL: float = 15.0  # in %
    DEFAULT_MUSCLE_MASS_GOAL: float = 45.0  # in %
    
    # Hydration
    DEFAULT_DAILY_WATER_GOAL: int = 3000  # in ml
    
    # Nutrition
    DEFAULT_PROTEIN_GOAL: int = 1.5  # grams per kg of body weight
    DEFAULT_CARBS_GOAL: int = 4.0  # grams per kg of body weight
    DEFAULT_FATS_GOAL: int = 0.8  # grams per kg of body weight
    
    # Supplements
    DEFAULT_WHEY_PROTEIN_GOAL: int = 20  # grams per serving
    DEFAULT_BCAA_GOAL: int = 5  # grams per serving
    DEFAULT_CREATINE_GOAL: int = 5  # grams per day
    
    # Mood tracking
    MOOD_SCALE: str = "1-5"  # 1 being very bad, 5 being excellent
    
    # Habits
    DEFAULT_HABITS: list = [
        "Drink water every 2 hours",
        "Get 7-9 hours of sleep",
        "Practice mindfulness or meditation",
        "Take a 5-minute walk after meals",
        "Prepare meals in advance"
    ]
    
    class Config:
        env_file = ".env"

settings = Settings()
