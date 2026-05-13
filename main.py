import os
import asyncio
import time
from pyrogram import Client, errors
from pyrogram.errors import FloodWait

# --- COLORS ---
RED, GREEN, YELLOW, BLUE, CYAN, RESET = "\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[96m", "\033[0m"

API_ID, API_HASH = 24168862, "916a9424dd1e58ab7955001ccc0172b3"

def progress(current, total):
    percentage = current * 100 / total
    completed = int(percentage / 2)
    bar = "█" * completed + "░" * (50 - completed)
    print(f"\r{CYAN}[{bar}] {percentage:.1f}%{RESET}", end="")

async def main():
    os.system('clear')
    print(RED + "╔═════════════════════════════════════════════╗\n║             DARK METHODS SCRAPPER           ║\n╚═════════════════════════════════════════════╝" + RESET)
    
    app = Client("dark_session", api_id=API_ID, api_hash=API_HASH)
    await app.start()
    
    # --- BOT TOKEN SYSTEM ADDED ---
    bot_token = input(f"{CYAN}Enter Bot Token: {RESET}")
    target_user = int(input(f"{BLUE}Enter Your User ID: {RESET}"))
    
    bot_app = Client("temp_bot", api_id=API_ID, api_hash=API_HASH, bot_token=bot_token)
    await bot_app.start()

    while True:
        link = input(f"\n{YELLOW}Paste Link: {RESET}")
        try:
            parts = link.split('/')
            msg_id, chat_id = int(parts[-1]), (int("-100" + parts[-2]) if "t.me/c/" in link else parts[-2])

            msg = await app.get_messages(chat_id, msg_id)
            
            if msg.media:
                print(f"{YELLOW}Downloading media...{RESET}")
                file_path = await app.download_media(msg, progress=progress)
                
                print(f"\n{YELLOW}Uploading to your ID via Bot...{RESET}")
                # Bot ke zariye bhej raha hai
                await bot_app.send_document(chat_id=target_user, document=file_path, caption=msg.caption, progress=progress)
                
                os.remove(file_path)
                print(f"\n{GREEN}[✔] Done! Data saved/sent.{RESET}")
            else:
                # Text bhi bot hi bhejega
                await bot_app.send_message(target_user, msg.text)

        except Exception as e: print(f"{RED}Error: {e}{RESET}")

asyncio.run(main())
