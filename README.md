


edia Merger Script
Purpose
This Python script merges audio and video files into a single output file. It supports various audio formats (MP3, WAV, FLAC) and video formats (MP4, MOV, AVI) and preserves metadata for audio files.

Requirements
Python 3.6 or higher
Libraries:
pydub
mutagen
moviepy
tqdm
Install the required libraries using:

sh
Copy code
pip install pydub mutagen moviepy tqdm
Usage
Configure the Script:

Set the directory containing your media files.
Optionally, modify the predefined list of files.
Run the Script:

sh
Copy code
python merge_media.py
Follow Prompts:

Enter the desired name for the merged file or wait 5 seconds for a default name.
Choose whether to use all files in the directory or a predefined list.
If both audio and video files are present, choose to merge only audio, only video, or both.
Features
Supports Multiple Formats: Merges MP3, WAV, FLAC, MP4, MOV, and AVI files.
Preserves Metadata: Retains metadata for MP3 files.
User Interaction: Prompts for input to customize file merging.
Progress Indicators: Displays progress bars for merging files and messages for export status.
Timestamped Results: Saves merged files in a timestamped directory.
Limitations
Export Time: Exporting large files may take additional time after the progress bar completes.
Format-Specific Handling: Only MP3 metadata is preserved. Other formats may not retain metadata.
