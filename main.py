import os
import asyncio
from pyrogram import Client, errors
from pyrogram.errors import SessionPasswordNeeded, FloodWait

# --- COLORS ---
RED, GREEN, YELLOW, BLUE, CYAN, RESET = "\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[96m", "\033[0m"

API_ID, API_HASH = 24168862, "916a9424dd1e58ab7955001ccc0172b3"

def show_banner():
    os.system('clear')
    print(RED + "╔" + "═"*45 + "╗")
    print("║" + " "*13 + "S C R A P P E R" + " "*17 + "║")
    print("║" + " "*10 + "BY: DARK METHODS" + " "*19 + "║")
    print("║" + " "*7 + "JOIN: @dark_uploads" + " "*19 + "║")
    print("╚" + "═"*45 + "╝" + RESET)

def progress(current, total, status_text):
    percentage = current * 100 / total
    completed = int(percentage / 2)
    bar = "█" * completed + "░" * (50 - completed)
    print(f"\r{CYAN}{status_text}: [{bar}] {percentage:.1f}%{RESET}", end="")

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

    # --- ONE TIME SETUP ---
    bot_token = input(f"{CYAN}Enter Bot Token: {RESET}")
    try:
        target_user = int(input(f"{CYAN}Enter Your User ID: {RESET}"))
    except ValueError:
        print(f"{RED}Invalid User ID!{RESET}")
        return

    # Bot client ko start karna
    bot_app = Client("temp_bot", api_id=API_ID, api_hash=API_HASH, bot_token=bot_token)
    await bot_app.start()

    print(f"\n{GREEN}Setup Complete! Bot will send media to ID: {target_user}{RESET}")

    while True:
        print(f"\n{YELLOW}═" * 35 + f"{RESET}")
        link = input(f"{BLUE}Paste Link: {RESET}")
        if not link: continue

        try:
            # Parsing
            parts = link.split('/')
            msg_id = int(parts[-1])
            chat_id = int("-100" + parts[-2]) if "t.me/c/" in link else parts[-2]

            print(f"{YELLOW}Fetching message...{RESET}", end="\r")
            msg = await app.get_messages(chat_id, msg_id)

            if msg.media:
                # Restricted bypass: User account se download
                file_path = await app.download_media(
                    msg, 
                    progress=lambda c, t: progress(c, t, "Downloading")
                )
                print("\n")
                
                # Bot ke zariye delivery
                await bot_app.send_document(
                    chat_id=target_user,
                    document=file_path,
                    caption=msg.caption,
                    progress=lambda c, t: progress(c, t, "Uploading")
                )
                print("\n")
                
                if os.path.exists(file_path):
                    os.remove(file_path)
            else:
                await bot_app.send_message(target_user, msg.text)
            
            print(f"{GREEN}[✔] Success! Media sent by Bot to your ID.{RESET}")

        except FloodWait as e:
            print(f"{RED}FloodWait: Waiting {e.value}s{RESET}")
            await asyncio.sleep(e.value)
        except Exception as e:
            print(f"{RED}[✘] Error: {e}{RESET}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{RED}Tool Stopped.{RESET}")
