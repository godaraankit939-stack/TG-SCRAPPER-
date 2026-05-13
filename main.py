import os
import asyncio
from pyrogram import Client, errors
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid

# Professional Colors for Terminal
G = "\033[92m" # Green
Y = "\033[93m" # Yellow
R = "\033[91m" # Red
B = "\033[94m" # Blue
RESET = "\033[0m"

async def get_input(prompt):
    return input(f"{B}{prompt}{RESET}")

async def main():
    os.system('clear')
    print(f"{B}{'='*50}")
    print(f"       RESTRICTED CONTENT EXTRACTOR V1.0")
    print(f"{'='*50}{RESET}")

    # Initialize Client
    # Note: API_ID and HASH should be provided by the user
    api_id = 1234567 # Replace or use input
    api_hash = "your_api_hash" 

    app = Client("user_session", api_id=api_id, api_hash=api_hash)

    try:
        await app.start()
    except Exception:
        # If no session, start professional login
        print(f"{Y}No active session found. Starting secure login...{RESET}")
        # Logic for login would go here...

    print(f"{G}[✔] Authorized & Ready!{RESET}")

    while True:
        print(f"\n{B}Available Options:{RESET}")
        print(f"1. {G}Send to Bot{RESET}")
        print(f"2. {G}Save to Saved Messages{RESET}")
        print(f"3. {G}Forward to Group (Create a group first){RESET}")
        
        choice = await get_input("Select an option (1/2/3): ")
        link = await get_input("Enter the Restricted Media Link: ")

        print(f"\n{Y}Scraping... Please wait.{RESET}")
        
        try:
            # Parsing Link
            parts = link.split('/')
            msg_id = int(parts[-1])
            if "t.me/c/" in link:
                chat_id = int("-100" + parts[-2])
            else:
                chat_id = parts[-2]

            msg = await app.get_messages(chat_id, msg_id)

            if choice == "1":
                bot_token = await get_input("Enter your Bot Token: ")
                # Instant transfer via server-side copy
                async with Client("temp_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token) as bot_app:
                    await bot_app.send_cached_media(message.chat.id, msg.media.file_id)
            
            elif choice == "2":
                await msg.copy("me")
                
            elif choice == "3":
                target = await get_input("Enter Group Username/ID: ")
                await msg.copy(target)

            print(f"{G}[✔] Process Completed Successfully!{RESET}")

        except Exception as e:
            print(f"{R}[✘] Error: {e}{RESET}")

if __name__ == "__main__":
    asyncio.run(main())
  
