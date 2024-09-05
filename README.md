# Video Processing Scripts

This repository contains Python scripts for video processing tasks. The scripts provided are:

1. **Video Splitter**: Splits a video into multiple clips based on timestamps and quotes provided in an Excel file.
2. **Vertical Video Converter**: Converts videos to a vertical format by cropping and resizing them based on object detection.

## Requirements

- Python 3.x
- `cv2` (OpenCV)
- `numpy`
- `torch` (PyTorch)
- `tkinter` (usually included with Python)
- `moviepy`
- `pandas`
- `ultralytics/yolov5` (for YOLOv5 model)

You can install the required packages using `pip`:

```bash
pip install opencv-python numpy torch moviepy pandas

1. Video Splitter
This script splits a video into multiple clips based on timestamps and quotes provided in an Excel file. Each clip is saved with a filename based on the corresponding quote.

Usage
Prepare Excel File: Create an Excel file with two columns:

Timestamp: Contains start and end times in the format "00:00:13 - 00:00:21".
Quote: Contains a quote or description for each clip.
Run the Script: Execute the script using Python. A file dialog will prompt you to select the video file and the Excel file.

Select Files:

Video File: Select the video you want to split.
Excel File: Select the Excel file with timestamps and quotes.
Output: The script will create a folder named video_clips in the same directory as the input video. Each clip will be saved with a filename based on the corresponding quote.

Script Details
Function split_video(): Main function to handle file selection, reading timestamps and quotes, and splitting the video.
Important Notes
The timestamps in the Excel file must be in the format "00:00:13 - 00:00:21".
Filenames are sanitized to remove any characters that are not allowed in filenames.
2. Vertical Video Converter
This script converts videos to a vertical format by cropping and resizing them. It uses the YOLOv5 object detection model to focus on detected objects.

Usage
Run the Script: Execute the script using Python. A folder dialog will prompt you to select the folder containing the videos to process.

Select Folder: Choose the folder that contains your video files. The script supports .mp4, .avi, and .mov formats.

Processing: The script will load the YOLOv5 model and process each video in the selected folder. It crops the video to a vertical format (9:16 aspect ratio), focusing on detected objects, and resizes the cropped video to 1080x1920 pixels.

Output: The original video file will be replaced with the processed vertical video.

Script Details
Function select_folder(): Opens a file dialog for selecting the folder containing videos.
Function load_yolov5(): Loads the pre-trained YOLOv5 model.
Function detect_objects(frame, model): Detects objects in a frame using YOLOv5.
Class SmoothCrop: Maintains a smoothed cropping region based on recent frames.
Function determine_crop_region(frame, detections, smooth_crop): Determines the cropping region based on detected objects and smooths it using the SmoothCrop class.
Function process_frame(frame, model, smooth_crop): Processes a single frame by cropping and resizing it.
Function convert_video(input_path, model): Converts a video file to a vertical format and replaces the original file.
Function main(): Manages folder selection, model loading, and video processing.
Important Notes
Ensure that the YOLOv5 model and its dependencies are correctly installed.
The script will replace the original video files with the processed ones. Make sure to back up any important videos before running the script.
Troubleshooting
Ensure that all required Python packages are installed.
Verify that the selected files or folder contain the correct video formats and data.
Check for any errors in the console output if a file fails to process.
License
These scripts are provided under the MIT License. See the LICENSE file for more details.

Author
SlightlyHappy
