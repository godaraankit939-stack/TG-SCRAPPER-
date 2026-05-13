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
    # Compact Bordered Banner
    print(RED + "╔" + "═"*45 + "╗")
    print("║" + " "*13 + "S C R A P P E R" + " "*17 + "║")
    print("║" + " "*10 + "BY: DARK METHODS" + " "*19 + "║")
    print("║" + " "*7 + "JOIN: @dark_uploads" + " "*19 + "║")
    print("╚" + "═"*45 + "╝" + RESET)

async def main():
    show_banner()

    # Create Client instance
    app = Client("dark_user_session", api_id=API_ID, api_hash=API_HASH)

    try:
        # Check for existing session
        await app.start()
    except Exception:
        # Direct Login if session not found
        print(f"\n{YELLOW}Login required. Connecting to Telegram...{RESET}")
        phone = input(f"{BLUE}Enter Phone Number (with +country code): {RESET}")
        try:
            sent_code = await app.send_code(phone)
            print(f"{GREEN}OTP has been sent to your Telegram app.{RESET}")
            otp = input(f"{YELLOW}Enter OTP (with spaces like 1 2 3): {RESET}").replace(" ", "")
            await app.sign_in(phone, sent_code.phone_code_hash, otp)
        except SessionPasswordNeeded:
            password = input(f"{BLUE}2FA Detected. Enter Password: {RESET}")
            await app.check_password(password)

    show_banner()
    print(f"{GREEN}[✔] System Online & Connected!{RESET}")

    while True:
        print(f"\n{CYAN}--- OPTIONS MENU ---{RESET}")
        print(f"1. {GREEN}Send Media to Bot{RESET}")
        print(f"2. {GREEN}Save to 'Saved Messages'{RESET}")
        print(f"3. {RED}Exit Tool{RESET}")
        
        choice = input(f"\n{YELLOW}Select Option (1/2/3): {RESET}")

        if choice == "3":
            print(f"{RED}Exiting Dark Methods Tool...{RESET}")
            break

        link = input(f"{BLUE}Paste Restricted Link: {RESET}")

        try:
            # Parsing link to get chat_id and msg_id
            parts = link.split('/')
            msg_id = int(parts[-1])
            if "t.me/c/" in link:
                chat_id = int("-100" + parts[-2])
            else:
                chat_id = parts[-2]

            # Scraping animation
            print(f"{YELLOW}Status: Scraping Content...{RESET}", end="\r")
            msg = await app.get_messages(chat_id, msg_id)
            await asyncio.sleep(1)

            if choice == "1":
                # Bot Token input only when needed
                bot_token = input(f"{BLUE}Enter Destination Bot Token: {RESET}")
                print(f"{YELLOW}Status: Transferring to Bot...{RESET}")
                
                async with Client("temp_bot", api_id=API_ID, api_hash=API_HASH, bot_token=bot_token) as bot_app:
                    if msg.media:
                        await bot_app.send_cached_media(chat_id=msg.chat.id, file_id=msg.media.file_id)
                    else:
                        await bot_app.send_message(chat_id=msg.chat.id, text=msg.text)
                
                print(f"{GREEN}[✔] Successfully sent to Bot!{RESET}")

            elif choice == "2":
                await msg.copy("me")
                print(f"{GREEN}[✔] Successfully saved in 'Saved Messages'!{RESET}")

        except Exception as e:
            print(f"{RED}[✘] Error: {e}{RESET}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{RED}Stopped by user.{RESET}")
