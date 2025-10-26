import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    TMDB_API_KEY = "0d0a41a7f2bba305b37b0cb05a2956bd"
    CHANNEL_ID = os.getenv('CHANNEL_ID')
    
    LANGUAGES = [
        ('ml', 'Malayalam', '#Malayalam'),
        ('ta', 'Tamil', '#Tamil'), 
        ('te', 'Telugu', '#Telugu'),
        ('kn', 'Kannada', '#Kannada'),
        ('hi', 'Hindi', '#Hindi'),
        ('en', 'English', '#English')
    ]
    
    REQU
