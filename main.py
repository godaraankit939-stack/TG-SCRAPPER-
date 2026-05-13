import os
import asyncio
from pyrogram import Client, filters, errors
from pyrogram.errors import SessionPasswordNeeded, FloodWait

# --- COLORS ---
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

API_ID = 24168862
API_HASH = "916a9424dd1e58ab7955001ccc0172b3"

def show_banner():
    os.system('clear')
    print(RED + "╔" + "═"*45 + "╗")
    print("║" + " "*13 + "S C R A P P E R" + " "*17 + "║")
    print("║" + " "*10 + "BY: DARK METHODS" + " "*19 + "║")
    print("║" + " "*7 + "JOIN: @dark_uploads" + " "*19 + "║")
    print("╚" + "═"*45 + "╝" + RESET)

async def main():
    show_banner()
    app = Client("dark_user_session", api_id=API_ID, api_hash=API_HASH)

    try:
        await app.start()
    except Exception:
        print(f"\n{YELLOW}Login required!{RESET}")
        phone = input(f"{BLUE}Phone (+code): {RESET}")
        sent_code = await app.send_code(phone)
        otp = input(f"{YELLOW}OTP: {RESET}").replace(" ", "")
        try:
            await app.sign_in(phone, sent_code.phone_code_hash, otp)
        except SessionPasswordNeeded:
            await app.check_password(input(f"{BLUE}2FA: {RESET}"))

    show_banner()
    print(f"{GREEN}[✔] Account Connected!{RESET}\n")

    target_user = int(input(f"{CYAN}Enter Your User ID: {RESET}"))

    while True:
        print(f"\n{YELLOW}═" * 35 + f"{RESET}")
        link = input(f"{BLUE}Paste Link: {RESET}")

        try:
            # Better Link Parsing
            if "t.me/c/" in link:
                parts = link.split('/')
                chat_id = int("-100" + parts[-2])
                msg_id = int(parts[-1])
            else:
                parts = link.split('/')
                chat_id = parts[-2]
                msg_id = int(parts[-1])

            print(f"{YELLOW}Bypassing Restriction...{RESET}", end="\r")
            
            # Fetch the message
            msg = await app.get_messages(chat_id, msg_id)

            if msg.media:
                # Jab forwarding restrict ho, toh download/upload hi rasta hai
                # Hum 'app.send_cached_media' try karenge, agar fail hua toh direct send karenge
                print(f"{YELLOW}Downloading & Sending...{RESET}")
                file_path = await app.download_media(msg)
                
                await app.send_document(
                    chat_id=target_user,
                    document=file_path,
                    caption=msg.caption
                )
                
                if os.path.exists(file_path):
                    os.remove(file_path) # Storage clean karne ke liye
            else:
                await app.send_message(chat_id=target_user, text=msg.text)
            
            print(f"{GREEN}[✔] Success! Sent to ID: {target_user}{RESET}")

        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception as e:
            print(f"{RED}[✘] Error: {e}{RESET}")

if __name__ == "__main__":
    asyncio.run(main())
    
