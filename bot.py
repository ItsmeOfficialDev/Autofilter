import logging
import asyncio
import time
import os
import sys
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError

from config import Config
from tmdb_handler import TMDBHandler
from database import is_movie_posted, mark_movie_posted

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class MovieAutoPoster:
    def __init__(self):
        self.bot = Bot(token=Config.BOT_TOKEN)
        self.tmdb = TMDBHandler()
        self.channel_id = Config.CHANNEL_ID
        self.posted_count = 0
        
    async def send_notification(self, message):
        try:
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=message
            )
        except Exception as e:
            logger.error(f"Notification error: {e}")
    
    def format_movie_message(self, movie_details, language_tag):
        title = movie_details.get('title', 'N/A')
        original_title = movie_details.get('original_title', '')
        year = movie_details.get('release_date', '')[:4] if movie_details.get('release_date') else 'N/A'
        
        if original_title and original_title != title:
            display_title = f"{title} | {original_title}"
        else:
            display_title = title
        
        message = f"""🎬 Title : {display_title}
🗓 Year : {year}
🔊 Language : {language_tag}
💿 Quality : HDRip

⭐ Rating: {movie_details.get('vote_average', 'N/A')}/10
📝 Overview: {movie_details.get('overview', 'No description available')}

#Movie #AutoFilter"""
        
        return message
    
    async def post_movie_to_channel(self, movie, language_code, language_name, language_tag):
        try:
            if is_movie_posted(movie['id']):
                logger.info(f"Already posted: {movie['title']}")
                return True
            
            movie_details = self.tmdb.get_movie_details(movie['id'])
            if not movie_details:
                return False
            
            message = self.format_movie_message(movie_details, language_tag)
            poster_path = movie_details.get('poster_path')
            poster_url = self.tmdb.get_movie_poster(poster_path) if poster_path else None
            
            if poster_url:
                await self.bot.send_photo(
                    chat_id=self.channel_id,
                    photo=poster_url,
                    caption=message
                )
            else:
                await self.bot.send_message(
                    chat_id=self.channel_id,
                    text=message
                )
            
            year = movie_details.get('release_date', '')[:4]
            if year and year.isdigit():
                year = int(year)
            else:
                year = 0
                
            mark_movie_posted(movie['id'], movie_details.get('title', 'Unknown'), language_code, year)
            self.posted_count += 1
            logger.info(f"Posted: {movie['title']} ({language_name})")
            return True
            
        except Exception as e:
            logger.error(f"Error posting {movie['title']}: {e}")
            return False
    
    async def fetch_and_post_movies(self):
        if not Config.BOT_TOKEN or not Config.CHANNEL_ID:
            logger.error("❌ BOT_TOKEN or CHANNEL_ID not set")
            return
        
        total_start_time = time.time()
        await self.send_notification("🚀 Movie Auto-Poster Started! Fetching movies...")
        
        for lang_code, lang_name, lang_tag in Config.LANGUAGES:
            try:
                logger.info(f"Processing {lang_name} movies...")
                await self.send_notification(f"📥 Fetching {lang_name} movies...")
                
                movies = self.tmdb.search_movies(lang_code)
                logger.info(f"Found {len(movies)} {lang_name} movies")
                
                if len(movies) == 0:
                    await self.send_notification(f"❌ No {lang_name} movies found! Check TMDB API.")
                    continue
                
                await self.send_notification(f"📊 Found {len(movies)} {lang_name} movies. Posting...")
                
                successful_posts = 0
                for i, movie in enumerate(movies):
                    if await self.post_movie_to_channel(movie, lang_code, lang_name, lang_tag):
                        successful_posts += 1
                    
                    await asyncio.sleep(1)
                    
                    if (i + 1) % 20 == 0:
                        await self.send_notification(f"📈 {lang_name}: {i+1}/{len(movies)} processed")
                
                logger.info(f"Completed {lang_name}: {successful_posts}/{len(movies)} posted")
                await self.send_notification(f"✅ {lang_name}: {successful_posts}/{len(movies)} posted")
                
            except Exception as e:
                logger.error(f"Error processing {lang_name}: {e}")
                await self.send_notification(f"❌ Error in {lang_name}: {str(e)}")
        
        total_time = time.time() - total_start_time
        final_message = f"""
🎉 MOVIE AUTO-POSTER COMPLETED! 🎉

📊 Total Movies Posted: {self.posted_count}
⏰ Total Time: {total_time/60:.2f} minutes
📅 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Bot will now STOP automatically.
"""
        await self.send_notification(final_message)
        logger.info("Movie posting completed!")
        
        # FORCE EXIT - PREVENT AUTO-RESTART
        print("🛑 Bot finished successfully - Exiting now!")
        sys.exit(0)

async def main():
    poster = MovieAutoPoster()
    await poster.fetch_and_post_movies()

if __name__ == '__main__':
    print("🚀 Starting Movie Auto-Poster")
    print("✅ This will run ONCE and then STOP automatically")
    print("📝 No auto-restart issues")
    
    asyncio.run(main())
