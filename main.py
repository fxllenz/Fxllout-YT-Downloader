import os
import yt_dlp
import asyncio
from mutagen.easyid3 import EasyID3
from colorama import init, Fore, Style
init(autoreset=True)
def print_banner():
    banner = """
___________        .__   .__                    __    
\_   _____/___  ___|  |  |  |    ____   __ __ _/  |_  
 |    __)  \  \/  /|  |  |  |   /  _ \ |  |  \\   __\ 
 |     \    >    < |  |__|  |__(  <_> )|  |  / |  |   
 \___  /   /__/\_ \|____/|____/ \____/ |____/  |__|   
     \/          \/                                   
                                                      
"""
    print(Fore.BLUE + Style.BRIGHT + '[x] ============================================== [x]')
    print(Fore.RED + Style.BRIGHT + banner)
    print(Fore.BLUE + Style.BRIGHT + '[x] ============================================== [x]\n')
    print(Fore.BLUE + Style.BRIGHT + '[x] ============================================== [x]')
    print(Fore.BLUE + Style.BRIGHT + '[x] Version: 1.0.0')
    print(Fore.BLUE + Style.BRIGHT + '[x] Author: fxllout.dev')
    print(Fore.BLUE + Style.BRIGHT + '[x] Status: ' + Fore.GREEN + 'Ready')
    print(Fore.BLUE + Style.BRIGHT + '[x] ============================================== [x]\n')
    print(Style.RESET_ALL)

def download_song(url, output_template):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info_dict), info_dict

def get_author(song_path):
    audio = EasyID3(song_path)
    return audio['artist'][0] if 'artist' in audio else 'Unknown Artist'

def organize_song(song_path, author):
    author_folder = os.path.join(os.getcwd(), author)
    
    if not os.path.exists(author_folder):
        os.makedirs(author_folder)
    
    target_path = os.path.join(author_folder, os.path.basename(song_path))
    if not os.path.exists(target_path):
        os.rename(song_path, target_path)
        print(Fore.YELLOW + f"[x] Moved {song_path} to {target_path}")
    else:
        print(Fore.RED + f"[x] File {target_path} already exists, skipping.")

def main(url):
    output_template = '%(title)s.%(ext)s'
    
    song_path, info_dict = download_song(url, output_template)
    song_path = song_path.replace('.webm', '.mp3')

    author = info_dict['uploader'] if 'uploader' in info_dict else 'Unknown Artist'
    organize_song(song_path, author)
    print(Fore.GREEN + f"[x] Downloaded and organized {song_path} into {author} folder")

if __name__ == '__main__':
    while True:
     print_banner()
     url = input(Fore.BLUE + "[+] URL: " + Style.RESET_ALL)
     main(url)
     print(Fore.GREEN + '[x] Restarting Automatically In 2 Seconds.. [x]')
     asyncio.sleep(2)
     os.system('clear')
     os.system('cls')
