


# Function to merge audio or video files and preserve metadata

## Description

This script merges audio or video files while preserving metadata. It is designed to handle audio and video files, with user input to specify preferences for merging. The script leverages several libraries, including `pydub` for audio processing, `mutagen` for handling metadata, and `moviepy` for video processing.

## Functionality

### 1. Imports and Setup
The script imports necessary libraries for file manipulation, terminal operations, and multimedia processing.

### 2. Clearing the Terminal
A function `clear_terminal()` is defined and called to clear the terminal screen.

### 3. User Input with Timeout
- `get_input_with_timeout(prompt, timeout=5)`: This function prompts the user for input, with a timeout feature to handle scenarios where the user does not respond in time.
- `get_user_input(prompt)`: A simple function to get user input without a timeout.

### 4. File and Directory Setup
The script prompts the user to enter a name for the merged file, defaulting to a timestamped name if no input is given.
The working directory and results folder are set up to store media files and the merged output.

### 5. File Selection
The user is prompted to decide whether to use all files in the directory or predefined files for merging.

### 6. File Classification
The script separates the selected files into audio and video categories.

### 7. Merge Options
If both audio and video files are present, the user is asked whether they want to merge only audio, only video, or both.

### 8. Merging Functions
- `merge_audio_files(audio_files, output_name, is_video, start_time)`: This function merges the selected audio files and preserves metadata from the first audio file. It also handles the export format based on whether the user wants to create a video from the audio.
- `merge_video_files(video_files, output_name, start_time)`: This function merges the selected video files into a single video clip.
- `audio_to_video_with_metadata(audio_file, image_file, output_name, start_time)`: This function converts an audio file into a video with a static image.

### 9. Execution
The script determines the appropriate output file name based on the merged content type.
It then calls the respective merging functions for audio and/or video files as needed.

## Usage

1. Ensure you have the required libraries installed (`pydub`, `mutagen`, `moviepy`, `tqdm`).
2. Place your media files in the specified directory.
3. Run the script. Follow the prompts to specify your preferences for merging files.
4. The merged file(s) will be saved in a timestamped results folder within the directory.

### requirements.txt

```
pip install pydub mutagen moviepy tqdm fuzzywuzzy python-Levenshtein Pillow

