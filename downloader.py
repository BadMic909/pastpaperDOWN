import requests
import os
import sys
import time

# --- LIVE SEARCH UTILITY (Now with Reverse Search) ---
def get_char():
    """Captures a single keystroke for live updates."""
    if os.name == 'nt':
        import msvcrt
        try: return msvcrt.getch().decode('utf-8')
        except: return ""
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def get_live_sub(prompt, subs_list):
    """Handles live searching of both Name and Code."""
    current_text = ""
    while True:
        suggestion_name = ""
        suggestion_code = ""
        
        if current_text:
            # Check for matches in Names (subs[0]) OR Codes (subs[1])
            for i in range(len(subs_list[0])):
                name = subs_list[0][i]
                code = subs_list[1][i]
                
                # If typing matches name OR typing matches the code
                if name.lower().startswith(current_text.lower()) or code.startswith(current_text):
                    suggestion_name = name
                    suggestion_code = code
                    break
        
        # Display: Clear line and show match
        display = f"\r\033[K{prompt}{current_text} | Match: {suggestion_name} ({suggestion_code})"
        print(display, end="", flush=True)

        char = get_char()
        if char in ('\r', '\n'): # Enter key
            print() 
            # If a match was found, return the code. Otherwise return what they typed.
            return suggestion_code if suggestion_code else current_text
        elif char in ('\x08', '\x7f'): # Backspace
            current_text = current_text[:-1]
        else:
            current_text += char
            if current_text == "-1":
                print()
                return "-1"

# --- YOUR ORIGINAL FUNCTIONS (UNTOUCHED) ---
def download_file(url, save_path):
    try:
        with requests.get(url, stream=True, timeout=15) as response:
            if response.status_code != 200: return -1
            total_size = int(response.headers.get('content-length', 0))
            if total_size == 0: return -1

            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            downloaded = 0
            with open(save_path, 'wb') as file:
                for data in response.iter_content(1024):
                    file.write(data)
                    downloaded += len(data)
                    percent = downloaded / total_size * 100
                    print(f"\rDownloading: {percent:.2f}%", end="")
            print(f"\nDownloaded → {save_path}")
            return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

def download(url, save, comp, sub, years, types, exc3):
    print("Years being downloaded: " + str(years))
    season = ["m", "s", "w"]
    parts = ["1", "2", "3", "4", "5"]
    if(exc3=="Y"):
        parts = ["1", "2", "4", "5"]
    
    for i in range(len(season)):
        urll = url + season[i]
        for j in range(len(years)):
            if(types=="qp"):
                urlll = urll + years[j] + "_qp_"
                if season[i] == "m":
                    urllll = urlll + comp + "2.pdf"
                    download_file(urllll, save + "/" + sub + "/QP_"+str(years)+"/" + urllll.split('/')[-1])
                else:
                    for k in range(len(parts)):
                        urllll = urlll + comp + parts[k] + ".pdf"
                        download_file(urllll, save + "/" + sub + "/QP_"+str(years)+"/" + urllll.split('/')[-1])
            elif(types=="ms"):
                urlll = urll + years[j] + "_ms_"
                if season[i] == "m":
                    urllll = urlll + comp + "2.pdf"
                    download_file(urllll, save + "/" + sub + "/MS_"+str(years)+"/" + urllll.split('/')[-1])
                else:
                    for k in range(len(parts)):
                        urllll = urlll + comp + parts[k] + ".pdf"
                        download_file(urllll, save + "/" + sub +"/MS_"+str(years)+"/" + urllll.split('/')[-1])
            else:
                urlll = urll + years[j] + "_qp_"
                if season[i] == "m":
                    urllll = urlll + comp + "2.pdf"
                    download_file(urllll, save + "/" + sub + "/QP_"+str(years)+"/" + urllll.split('/')[-1])
                else:
                    for k in range(len(parts)):
                        urllll = urlll + comp + parts[k] + ".pdf"
                        download_file(urllll, save + "/" + sub + "/QP_"+str(years)+"/" + urllll.split('/')[-1])
                urlll = urll + years[j] + "_ms_"
                if season[i] == "m":
                    urllll = urlll + comp + "2.pdf"
                    download_file(urllll, save + "/" + sub + "/MS_"+str(years)+"/" + urllll.split('/')[-1])
                else:
                    for k in range(len(parts)):
                        urllll = urlll + comp + parts[k] + ".pdf"
                        download_file(urllll, save + "/" + sub +"/MS_"+str(years)+"/" + urllll.split('/')[-1])
# --- DATA ---
subs = [["Accounting","Afrikaans - Language","Arabic","Arabic - Language (AS only)","Art & Design","Biblical Studies","Biology","Business","Chemistry","Chinese - Language & Literature (A level)","Chinese Language (AS only)","Classical Studies","Divinity","Drama","Economics","English Language","Language and Literature in English (AS)","English Literature","Environmental Management (AS only)","Further Mathematics","Food Studies (AS only)","French Language (AS/A Level)","French Literature (AS only)","Geography","German Language (AS/A Level)","Global Perspectives & Research","Hindi Language (AS/A Level)","Hindi Literature (AS only)","History","Information Technology","Islamic Studies","Japanese Language (AS only)","Latin (AS only)","Law","Marine Science","Mathematics","Media Studies","Music","Physical Education","Physics","Psychology","Sociology","Spanish Language (AS/A Level)","Spanish Literature (AS only)","Portuguese Language (AS/A Level)","Tamil","Urdu","Applied ICT / ICT (older codes)"],["9706","8679","9680","8680","9479","9484","9700","9609","9701","9868","8238","9274","9011","9482","9708","9093","8695","9695","8291","9231","9336","8682","8670","9696","8683","9239","8687","8675","9389","9626","9013","8281","8282","9084","9693","9709","9607","9703","9396","9702","9990","9699","8685","8673","8684","9689","9676","9713/9691"]]

# --- MAIN LOOP ---
print("--------------------------------------------------------------------------------")
print("Original code by Paramesh S (BADMIC909).")
print("Type -1 at any time to restart the inputs.")
print("--------------------------------------------------------------------------------")

while True:
    # 1. Subject (Live Reverse Search enabled)
    sub = get_live_sub("Enter subject code or name [NUMBER OR TEXT]: ", subs)
    if sub == "-1": continue

    # 2. Directory
    save = input("Enter directory to save files [Path(use full path if relative doesn't work)]: ")
    if save == "-1": continue

    # 3. Component
    comp = input("Enter component number [NUMBER ONLY]: ")
    if comp == "-1": continue

    # 4. Years
    yearS = input("Enter start year [NUMBER ONLY]: ")
    if yearS == "-1": continue
    yearF = input("Enter final year [NUMBER ONLY]: ")
    if yearF == "-1": continue

    # 5. exclude p3
    exc3 = input("Exclude 3rd paper?(Y/N) [Some subs have repeated 3rd session papers(11,13 same)] ")
    if exc3 == "-1": continue

    types= input("MS,QP or both? ['MS','QP','BOTH']").lower()
    # All inputs collected, exit the while loop to start downloading
    break

# --- FINAL EXECUTION ---
year = []
yS, yF = int(yearS), int(yearF)
if yF < yS: yS, yF = yF, yS

for i in range(yS, yF + 1):
    year.append(str(i)[-2:])

url = "https://pastpapers.papacambridge.com/directories/CAIE/CAIE-pastpapers/upload/" + sub + "_"
download(url, save, comp, sub, year, types, exc3)
