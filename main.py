import os
import asyncio
from pyrogram import Client, filters, errors
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PasswordHashInvalid

# --- COLORS ---
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

# --- BANNER ---
def show_banner():
    os.system('clear')
    print(RED + """
███████╗ ██████╗██████╗  █████╗ ██████╗ ██████╗ ███████╗██████╗ 
██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
███████╗██║     ██████╔╝███████║██████╔╝██████╔╝█████╗  ██████╔╝
╚════██║██║     ██╔══██╗██╔══██║██╔══██╗██╔══██╗██╔══╝  ██╔══██╗
███████║╚██████╗██║  ██║██║  ██║██║  ██║██║  ██║███████╗██║  ██║
╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
    """ + RESET)
    print(RED + "            BY: DARK METHODS")
    print(RED + "            JOIN: @dark_uploads")
    print(RED + "═" * 65 + RESET)

async def main():
    show_banner()

    # API Details (User se input lega pehli baar)
    print(f"{YELLOW}Enter your API details from my.telegram.org{RESET}")
    api_id = input(f"{BLUE}Enter API ID: {RESET}")
    api_hash = input(f"{BLUE}Enter API HASH: {RESET}")

    # Initialize User Client
    app = Client("dark_user_session", api_id=api_id, api_hash=api_hash)

    try:
        await app.start()
    except Exception:
        print(f"\n{YELLOW}Login required. Please enter your phone number.{RESET}")
        phone = input(f"{BLUE}Phone Number (with +country code): {RESET}")
        try:
            sent_code = await app.send_code(phone)
            otp = input(f"{GREEN}Enter the OTP (with spaces like 1 2 3): {RESET}").replace(" ", "")
            await app.sign_in(phone, sent_code.phone_code_hash, otp)
        except SessionPasswordNeeded:
            password = input(f"{BLUE}Two-Step Verification detected. Enter Password: {RESET}")
            await app.check_password(password)

    show_banner()
    print(f"{GREEN}[✔] Account Connected Successfully!{RESET}")

    while True:
        print(f"\n{BLUE}--- MAIN MENU ---{RESET}")
        print(f"1. {GREEN}Send Media to Bot{RESET}")
        print(f"2. {GREEN}Save to 'Saved Messages'{RESET}")
        print(f"3. {GREEN}Exit Tool{RESET}")
        
        choice = input(f"\n{YELLOW}Select an option (1/2/3): {RESET}")

        if choice == "3":
            print(f"{RED}Exiting... Goodbye!{RESET}")
            break

        link = input(f"{BLUE}Enter Restricted Media Link: {RESET}")

        # Parsing Link
        try:
            parts = link.split('/')
            msg_id = int(parts[-1])
            if "t.me/c/" in link:
                chat_id = int("-100" + parts[-2])
            else:
                chat_id = parts[-2]

            # Scraping Animation
            for i in range(3):
                print(f"\r{YELLOW}Scraping Media{'.' * (i+1)}{RESET}", end="")
                await asyncio.sleep(0.5)
            print("\n")

            msg = await app.get_messages(chat_id, msg_id)

            if choice == "1":
                # BOT TOKEN SIRF YAHAN MANGNA CHAHIYE
                bot_token = input(f"{BLUE}Enter your Destination Bot Token: {RESET}")
                print(f"{YELLOW}Transferring to Bot...{RESET}")
                
                async with Client("temp_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token) as bot_app:
                    await bot_app.send_cached_media(chat_id=msg.chat.id, file_id=msg.media.file_id if msg.media else None)
                print(f"{GREEN}[✔] Successfully sent to your Bot!{RESET}")

            elif choice == "2":
                await msg.copy("me")
                print(f"{GREEN}[✔] Media saved to 'Saved Messages'!{RESET}")

        except Exception as e:
            print(f"{RED}[✘] Error: {e}{RESET}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    
