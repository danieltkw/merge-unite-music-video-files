


Media Merger Script
Purpose
Merges audio and video files into a single output, supporting MP3, WAV, FLAC, MP4, MOV, and AVI formats.

Requirements
Python 3.6+
Libraries: pydub, mutagen, moviepy, tqdm
Install with:

sh
Copy code
pip install pydub mutagen moviepy tqdm
Usage
Configure: Set the directory for media files and optionally modify the predefined file list.
Run:
sh
Copy code
python merge_media.py
Follow Prompts: Name the merged file, choose file sources, and select content types to merge.
Features
Supports multiple formats
Preserves MP3 metadata
Interactive user prompts
Progress bars and export status messages
Saves results in a timestamped folder
Limitations
Exporting large files may take extra time
Metadata preservation is primarily for MP3 files
