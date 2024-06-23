


# // Daniel T. K. W. - github.com/danieltkw - danielkopolo95@gmail.com
# ------------------------------------------------------------

# Function to merge audio or video files and preserve metadata

# ------------------------------------------------------------
# Imports
import os
import sys
import time
from datetime import datetime
from tqdm import tqdm
from pydub import AudioSegment
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from moviepy.editor import VideoFileClip, concatenate_videoclips
# ------------------------------------------------------------

# ------------------------------------------------------------
# Function to clear the terminal
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Clear the terminal
clear_terminal()
# ------------------------------------------------------------

# ------------------------------------------------------------
# Function to get user input with a timeout
def get_input_with_timeout(prompt, timeout=5):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    start_time = time.time()
    input_string = ''
    while True:
        if os.name == 'nt' and msvcrt.kbhit():
            char = msvcrt.getche()
            if char == b'\r':  # Enter key
                break
            elif char == b'\b':  # Backspace key
                input_string = input_string[:-1]
            else:
                input_string += char.decode('utf-8')
        elif os.name != 'nt':
            try:
                input_string = input(prompt)
            except:
                input_string = ''
            break
        if len(input_string) == 0 and (time.time() - start_time) > timeout:
            break
    print()  # Move to the next line
    return input_string

# Function to get user input
def get_user_input(prompt):
    return input(prompt).strip().lower()

# Ask for the input file name with a 5-second timeout
if os.name == 'nt':
    import msvcrt  # Windows-specific library for keyboard input
    file_name = get_input_with_timeout("Enter the name for the merged file (or wait 5 seconds for default): ", 5)
else:
    import signal

    def timeout_handler(signum, frame):
        raise TimeoutError

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(5)  # Set the timeout to 5 seconds
    try:
        file_name = input("Enter the name for the merged file (or wait 5 seconds for default): ")
    except TimeoutError:
        file_name = ''
    signal.alarm(0)  # Disable the alarm

if not file_name:
    file_name = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
# ------------------------------------------------------------

# ------------------------------------------------------------
# Directory containing the media files
directory = "C:\\Users\\Desktop\\Python\\Python\\merge_mp3\\media_files"

# Create a results folder with a timestamped name
results_folder = os.path.join(directory, file_name)
os.makedirs(results_folder, exist_ok=True)

# List of predefined media files
predefined_files = [
    "music1.mp3",
    "music2.mp3",
    "music3.mp3",
    "video1.mp4",
    "video2.mp4",
    "video3.mp4"
]

# Ask the user if they want to use all files in the folder or predefined files
use_all_files = get_user_input("Do you want to use all files in the folder? (yes/no): ")

if use_all_files == 'yes':
    # Get all files from the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
else:
    files = predefined_files
# ------------------------------------------------------------

# ------------------------------------------------------------
# Separate files into audio and video
audio_files = [file for file in files if file.lower().endswith(('.mp3', '.wav', '.flac'))]
video_files = [file for file in files if not file.lower().endswith(('.mp3', '.wav', '.flac'))]

# Ask the user if they want to merge only videos, only music, or both if both types are present
if audio_files and video_files:
    merge_choice = get_user_input("Both audio and video files are present. Do you want to merge (audio/video/both): ")
    if merge_choice == 'audio':
        video_files = []
    elif merge_choice == 'video':
        audio_files = []

# Function to merge audio files and preserve metadata
def merge_audio_files(audio_files, output_name):
    combined = AudioSegment.empty()
    for file in tqdm(audio_files, desc="Merging audio files", unit="file"):
        file_path = os.path.join(directory, file)
        audio = AudioSegment.from_file(file_path)
        combined += audio

    output_path = os.path.join(results_folder, f"{output_name}.mp3")
    print("Exporting merged audio file, please wait...")
    combined.export(output_path, format="mp3")
    print("Audio export completed.")

    # Preserve metadata from the first file
    if audio_files and audio_files[0].lower().endswith('.mp3'):
        first_file_path = os.path.join(directory, audio_files[0])
        first_file = MP3(first_file_path, ID3=ID3)
        merged_file = MP3(output_path, ID3=ID3)
        merged_file.tags = first_file.tags
        merged_file.save()

# Function to merge video files
def merge_video_files(video_files, output_name):
    clips = [VideoFileClip(os.path.join(directory, file)) for file in video_files]
    final_clip = concatenate_videoclips(clips)
    output_path = os.path.join(results_folder, f"{output_name}.mp4")
    print("Exporting merged video file, please wait...")
    final_clip.write_videofile(output_path)
    print("Video export completed.")

# Determine the appropriate output file name based on the content
if audio_files and video_files:
    output_name = "united_video"
elif audio_files:
    output_name = "album"
else:
    output_name = "video"

# Merge audio files if there are any
if audio_files:
    merge_audio_files(audio_files, output_name)

# Merge video files if there are any
if video_files:
    merge_video_files(video_files, output_name)
# ------------------------------------------------------------



# ------------------------------------------------------------




