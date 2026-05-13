import os
import asyncio
from pyrogram import Client, filters, errors
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PasswordHashInvalid, FloodWait

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
    # Session file name unique rakha hai taaki crash na ho
    app = Client("dark_user_session", api_id=API_ID, api_hash=API_HASH)

    # --- SECURE LOGIN LOGIC ---
    try:
        await app.start()
    except Exception:
        print(f"\n{YELLOW}Login required!{RESET}")
        phone = input(f"{BLUE}Phone (+code): {RESET}")
        try:
            sent_code = await app.send_code(phone)
            print(f"{GREEN}OTP Sent to Telegram!{RESET}")
            otp = input(f"{YELLOW}OTP (ex: 1 2 3): {RESET}").replace(" ", "")
            await app.sign_in(phone, sent_code.phone_code_hash, otp)
        except SessionPasswordNeeded:
            pwd = input(f"{BLUE}2FA Password: {RESET}")
            await app.check_password(pwd)
        except Exception as e:
            print(f"{RED}Login Error: {e}{RESET}")
            return

    show_banner()
    print(f"{GREEN}[✔] Account Connected!{RESET}\n")

    # --- ONE TIME SETUP ---
    bot_token = input(f"{CYAN}Enter Bot Token: {RESET}")
    # target_user ko int me convert karna zaruri hai
    try:
        target_user = int(input(f"{CYAN}Enter Your User ID: {RESET}"))
    except ValueError:
        print(f"{RED}Invalid User ID! Exit and try again.{RESET}")
        return

    # Bot client ko loop se bahar start karenge efficiency ke liye
    bot_app = Client("temp_bot", api_id=API_ID, api_hash=API_HASH, bot_token=bot_token)
    try:
        await bot_app.start()
    except Exception as e:
        print(f"{RED}Bot Token Error: {e}{RESET}")
        return

    print(f"\n{GREEN}Setup Complete! Now just paste links.{RESET}")

    while True:
        print(f"\n{YELLOW}═" * 35 + f"{RESET}")
        link = input(f"{BLUE}Paste Restricted Link: {RESET}")

        if not link or "t.me/" not in link:
            print(f"{RED}Invalid Telegram Link!{RESET}")
            continue

        try:
            # Parsing Link IDs
            parts = link.split('/')
            msg_id = int(parts[-1])
            if "t.me/c/" in link:
                chat_id = int("-100" + parts[-2])
            else:
                chat_id = parts[-2]

            print(f"{YELLOW}Scraping...{RESET}", end="\r")
            
            # Fetch message using user account
            msg = await app.get_messages(chat_id, msg_id)

            # --- ADVANCED SENDING LOGIC ---
            # Restricted content ke liye 'copy' sabse best hai
            # Ye file_id wala error (MEDIA_EMPTY) kabhi nahi dega
            await msg.copy(
                chat_id=target_user,
                caption=msg.caption,
                protect_content=False # User aage forward kar payega
            )
            
            print(f"{GREEN}[✔] Media sent to ID: {target_user}{RESET}")

        except FloodWait as e:
            print(f"{RED}Wait {e.value} seconds (Telegram Limit).{RESET}")
            await asyncio.sleep(e.value)
        except Exception as e:
            print(f"{RED}[✘] Error: {e}{RESET}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{RED}Tool Stopped by user.{RESET}")
            
