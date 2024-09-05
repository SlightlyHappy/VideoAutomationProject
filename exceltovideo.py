import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import moviepy.editor as mp
import re

def split_video():
    """
    Step 1:
    This script splits a video into multiple clips based on timestamps and quotes provided in an Excel file.
    It prompts the user to select the video and Excel files using windowed dialogs.
    The timestamps in the Excel file should be in the format "00:00:13 - 00:00:21".
    The output clips are saved in a new folder named "video_clips" in the same directory as the input video.
    """

    # Create a Tkinter window for file selection (hidden)
    root = tk.Tk()
    root.withdraw()

    # Ask user to select the video file
    video_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
    if not video_path:  # Check if user canceled
        return

    # Ask user to select the Excel file
    excel_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel Files", "*.xls;*.xlsx")])
    if not excel_path:  # Check if user canceled
        return

    # Read the Excel file (adjust sheet_name if needed)
    df = pd.read_excel(excel_path, sheet_name='Sheet1')

    # Extract and convert timestamps
    timestamps = []
    for timestamp_range in df['Timestamp']:
        start_time, end_time = timestamp_range.split(' - ')
        start_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(start_time.split(':'))))
        end_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(end_time.split(':'))))
        timestamps.append(start_seconds)
    timestamps.append(end_seconds)  # Add the last end time

    # Extract quotes
    quotes = df['Quote'].tolist()

    # Create output folder
    output_folder = os.path.join(os.path.dirname(video_path), "video_clips")
    os.makedirs(output_folder, exist_ok=True)

    # Load the video
    video = mp.VideoFileClip(video_path)

    # Split the video into clips
    for i in range(len(timestamps) - 1):
        start_time = timestamps[i]
        end_time = timestamps[i + 1]
        clip = video.subclip(start_time, end_time)

        # Create filename with quote (sanitize the filename)
        filename = re.sub(r'[<>:"/\\|?*]', '', quotes[i]) + ".mp4" 
        output_path = os.path.join(output_folder, filename)

        # Save the clip
        clip.write_videofile(output_path)

    # Close the Tkinter window
    root.destroy()

# Run the script
split_video()