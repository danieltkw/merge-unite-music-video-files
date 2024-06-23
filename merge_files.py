

# ------------------------------------------------------------
# // Daniel T. K. W. - github.com/danieltkw - danielkopolo95@gmail.com
# ------------------------------------------------------------

# Function to merge audio or video files and preserve metadata

# ------------------------------------------------------------
# Imports
import os
import sys
import time
import multiprocessing
import logging
from datetime import datetime, timedelta
from tqdm import tqdm
from pydub import AudioSegment
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageClip, AudioFileClip
from PIL import Image
import io
from fuzzywuzzy import process

if os.name == 'nt':
    import msvcrt  # Windows-specific library for keyboard input
else:
    import signal

# ------------------------------------------------------------

# ------------------------------------------------------------
# Function to clear the terminal
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Clear the terminal
clear_terminal()
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

# Function to get user input with fuzzy matching
def get_user_input(prompt):
    response = input(prompt).strip().lower()
    choices = ["yes", "no"]
    best_match = process.extractOne(response, choices, score_cutoff=80)
    return best_match[0] if best_match else response

# Function to add a timeout to a function
def run_with_timeout(func, args=(), kwargs={}, timeout_duration=300, default=None):
    def wrapper(queue, *args, **kwargs):
        try:
            result = func(*args, **kwargs)
            queue.put(result)
        except Exception as e:
            queue.put(e)
    
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=wrapper, args=(queue, *args), kwargs=kwargs)
    process.start()
    process.join(timeout_duration)
    
    if process.is_alive():
        print(f"Process taking too long (>{timeout_duration} seconds), terminating...")
        process.terminate()
        process.join()
        return default
    else:
        result = queue.get()
        if isinstance(result, Exception):
            raise result
        return result

# Function to print with timestamp
def log(message, start_time):
    current_time = datetime.now()
    duration = current_time - start_time
    print(f"{current_time.strftime('%Y-%m-%d %H:%M:%S')} ({duration}): {message}")

# ------------------------------------------------------------
# Main Script

def main():
    # Setup logging
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    start_time = datetime.now()
    log("Starting script...", start_time)

    # Ask for the input file name with a 5-second timeout
    if os.name == 'nt':
        file_name = get_input_with_timeout("Enter the name for the merged file (or wait 5 seconds for default): ", 5)
    else:
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
    log(f"File name set to: {file_name}", start_time)

    # Directory containing the media files
    directory = "C:\\Users\\Administrator\\Desktop\\a"
    log(f"Media files directory: {directory}", start_time)

    # Create a results folder with a timestamped name
    results_folder = os.path.join(directory, file_name)
    os.makedirs(results_folder, exist_ok=True)
    log(f"Results folder created: {results_folder}", start_time)

    # Get all files from the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    log(f"Files found: {files}", start_time)

    # Separate files into audio and video
    audio_files = [file for file in files if file.lower().endswith(('.mp3', '.wav', '.flac'))]
    video_files = [file for file in files if not file.lower().endswith(('.mp3', '.wav', '.flac'))]
    log(f"Audio files: {audio_files}", start_time)
    log(f"Video files: {video_files}", start_time)

    # Ask the user if they want to merge only videos, only music, or both if both types are present
    if audio_files and video_files:
        merge_choice = get_user_input("Both audio and video files are present. Do you want to merge (audio/video/both): ")
        log(f"Merge choice: {merge_choice}", start_time)
        if merge_choice == 'audio':
            video_files = []
        elif merge_choice == 'video':
            audio_files = []

    # Ask if the user wants to create a video with a static image from the audio files
    create_video = get_user_input("Do you want to create a video with a static image from the merged audio file? (yes/no): ")
    log(f"Create video: {create_video}", start_time)

    # Determine the appropriate output file name based on the content
    if audio_files and video_files:
        output_name = "united_video"
    elif audio_files:
        output_name = "album"
    else:
        output_name = "video"
    log(f"Output name: {output_name}", start_time)

    # Function to extract album cover from the first MP3 file
    def extract_album_cover(audio_files, start_time):
        for file in audio_files:
            file_path = os.path.join(directory, file)
            audio = MP3(file_path, ID3=ID3)
            for tag in audio.tags.values():
                if isinstance(tag, APIC):
                    image_data = tag.data
                    image = Image.open(io.BytesIO(image_data))
                    image_path = os.path.join(results_folder, "cover.jpg")
                    image.save(image_path)
                    log(f"Album cover extracted and saved to {image_path}", start_time)
                    return image_path
        return None

    # Function to merge audio files and preserve metadata
    def merge_audio_files(audio_files, output_name, is_video, start_time):
        combined = AudioSegment.empty()
        for file in tqdm(audio_files, desc="Merging audio files", unit="file"):
            file_path = os.path.join(directory, file)
            audio = AudioSegment.from_file(file_path)
            combined += audio

        output_extension = "mp4" if is_video else "mp3"
        output_path = os.path.join(results_folder, f"{output_name}.{output_extension}")
        log(f"Exporting merged audio file to {output_path}, please wait...", start_time)
        combined.export(output_path, format="mp3" if not is_video else "mp4")
        log("Audio export completed.", start_time)

        # Preserve metadata from the first file
        if audio_files and audio_files[0].lower().endswith('.mp3'):
            first_file_path = os.path.join(directory, audio_files[0])
            first_file = MP3(first_file_path, ID3=ID3)
            merged_file = MP3(output_path, ID3=ID3)
            merged_file.tags = first_file.tags
            merged_file.save()
        return output_path

    # Function to merge video files
    def merge_video_files(video_files, output_name, start_time):
        clips = [VideoFileClip(os.path.join(directory, file)) for file in video_files]
        final_clip = concatenate_videoclips(clips)
        output_path = os.path.join(results_folder, f"{output_name}.mp4")
        log("Exporting merged video file, please wait...", start_time)
        final_clip.write_videofile(output_path)
        log("Video export completed.", start_time)

    # Function to convert audio to video with a static image
    def audio_to_video_with_metadata(audio_file, image_file, output_name, start_time):
        log(f"Starting conversion of audio to video with image {image_file}...", start_time)
        audio = AudioFileClip(audio_file)
        image = ImageClip(image_file)
        
        image = image.set_duration(audio.duration)
        video = image.set_audio(audio)
        
        output_path = os.path.join(results_folder, f"{output_name}.mp4")
        log(f"Exporting video file to {output_path}, please wait...", start_time)
        video.write_videofile(output_path, codec='libx265', fps=30)
        log("Video export completed.", start_time)

    # Merge audio files if there are any
    if audio_files:
        is_video = create_video == 'yes'
        merged_audio_path = merge_audio_files(audio_files, output_name, is_video, start_time)

        # If user wants to create a video, extract album cover and create video
        if create_video == 'yes':
            album_cover_path = extract_album_cover(audio_files, start_time)
            if album_cover_path:
                result = run_with_timeout(audio_to_video_with_metadata, args=(merged_audio_path, album_cover_path, output_name, start_time), timeout_duration=300)
                if result is None:
                    log("Video creation process timed out.", start_time)
                elif isinstance(result, Exception):
                    log(f"Error during video creation: {result}", start_time)
                else:
                    log("Video creation completed successfully.", start_time)
            else:
                log("No album cover found in the audio files.", start_time)

    # Merge video files if there are any
    if video_files:
        merge_video_files(video_files, output_name, start_time)

    log("Script finished successfully.", start_time)

# Execute main function
if __name__ == "__main__":
    main()

# ------------------------------------------------------------

# ------------------------------------------------------------





