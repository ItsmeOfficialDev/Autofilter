import os

class Config:
    # Get from Render Environment Variables
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    TMDB_API_KEY = "0d0a41a7f2bba305b37b0cb05a2956bd"
    CHANNEL_ID = os.environ.get('CHANNEL_ID')
    
    LANGUAGES = [
        ('ml', 'Malayalam', '#Malayalam'),
        ('ta', 'Tamil', '#Tamil'), 
        ('te', 'Telugu', '#Telugu'),
        ('kn', 'Kannada', '#Kannada'),
        ('hi', 'Hindi', '#Hindi'),
        ('en', 'English', '#English')
    ]
    
    REQUESTS_PER_SECOND = 3
    DELAY_BETWEEN_REQUESTS = 0.34
