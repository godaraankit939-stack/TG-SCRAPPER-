import os
import asyncio
from pyrogram import Client, filters, errors
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PasswordHashInvalid

# --- COLORS ---
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

# --- PUBLIC API CONFIG ---
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
        # Choti line taaki Termux me break na ho
        phone = input(f"{BLUE}Phone (+code): {RESET}")
        try:
            sent_code = await app.send_code(phone)
            print(f"{GREEN}OTP Sent!{RESET}")
            otp = input(f"{YELLOW}OTP (ex: 1 2 3): {RESET}").replace(" ", "")
            await app.sign_in(phone, sent_code.phone_code_hash, otp)
        except SessionPasswordNeeded:
            pwd = input(f"{BLUE}2FA Password: {RESET}")
            await app.check_password(pwd)

    show_banner()
    print(f"{GREEN}[✔] Account Connected!{RESET}\n")

    # --- ONE TIME SETUP ---
    bot_token = input(f"{CYAN}Enter Bot Token: {RESET}")
    target_user = input(f"{CYAN}Enter Your User ID (to receive media): {RESET}")
    
    # User ID integer honi chahiye
    try:
        target_user = int(target_user)
    except:
        pass

    print(f"\n{GREEN}Setup Complete! Now just paste links.{RESET}")

    async with Client("temp_bot", api_id=API_ID, api_hash=API_HASH, bot_token=bot_token) as bot_app:
        while True:
            print(f"\n{YELLOW}═" * 30 + f"{RESET}")
            link = input(f"{BLUE}Paste Link: {RESET}")

            try:
                # Parsing
                parts = link.split('/')
                msg_id = int(parts[-1])
                chat_id = int("-100" + parts[-2]) if "t.me/c/" in link else parts[-2]

                print(f"{YELLOW}Scraping...{RESET}", end="\r")
                msg = await app.get_messages(chat_id, msg_id)

                if msg.media:
                    # Fix: Har tarah ke media se file_id nikalna
                    media_type = msg.media.value
                    media_obj = getattr(msg, media_type)
                    
                    await bot_app.send_cached_media(
                        chat_id=target_user,
                        file_id=media_obj.file_id,
                        caption=msg.caption
                    )
                else:
                    await bot_app.send_message(chat_id=target_user, text=msg.text)
                
                print(f"{GREEN}[✔] Sent successfully to ID: {target_user}{RESET}")

            except Exception as e:
                print(f"{RED}[✘] Error: {e}{RESET}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{RED}Tool Stopped.{RESET}")
        
