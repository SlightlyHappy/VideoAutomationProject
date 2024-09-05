import cv2
import numpy as np
import os
import torch
import tkinter as tk
from tkinter import filedialog
from moviepy.editor import VideoFileClip, vfx
from collections import deque

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select folder containing videos")
    return folder_path

def load_yolov5():
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    model.eval()
    return model

def detect_objects(frame, model):
    results = model(frame)
    return results.xyxy[0].cpu().numpy()

class SmoothCrop:
    def __init__(self, window_size=30):
        self.crop_queue = deque(maxlen=window_size)
    
    def update(self, new_crop):
        self.crop_queue.append(new_crop)
        return np.mean(self.crop_queue, axis=0).astype(int)

def determine_crop_region(frame, detections, smooth_crop):
    height, width = frame.shape[:2]
    if len(detections) == 0:
        return smooth_crop.update((0, 0, width, height))
    
    x_min = min(detection[0] for detection in detections)
    y_min = min(detection[1] for detection in detections)
    x_max = max(detection[2] for detection in detections)
    y_max = max(detection[3] for detection in detections)
    
    center_x = (x_min + x_max) // 2
    crop_width = int(height * 9 / 16)  # 9:16 aspect ratio
    left = max(0, int(center_x - crop_width // 2))
    right = min(width, left + crop_width)
    
    # Adjust if crop goes out of frame
    if left == 0:
        right = crop_width
    elif right == width:
        left = width - crop_width
    
    return smooth_crop.update((left, 0, crop_width, height))

def process_frame(frame, model, smooth_crop):
    detections = detect_objects(frame, model)
    x, y, w, h = determine_crop_region(frame, detections, smooth_crop)
    cropped_frame = frame[y:y+h, x:x+w]
    resized_frame = cv2.resize(cropped_frame, (1080, 1920))  # 9:16 aspect ratio
    return resized_frame

def convert_video(input_path, model):
    clip = VideoFileClip(input_path)
    smooth_crop = SmoothCrop()
    vertical_clip = clip.fl_image(lambda frame: process_frame(frame, model, smooth_crop))
    output_path = input_path.rsplit('.', 1)[0] + '_vertical.mp4'
    vertical_clip.write_videofile(output_path, codec="libx264")
    clip.close()
    vertical_clip.close()
    os.remove(input_path)
    os.rename(output_path, input_path)

def main():
    folder_path = select_folder()
    if not folder_path:
        print("No folder selected. Exiting.")
        return

    print("Loading YOLOv5 model...")
    model = load_yolov5()

    for filename in os.listdir(folder_path):
        if filename.endswith(('.mp4', '.avi', '.mov')):
            input_path = os.path.join(folder_path, filename)
            print(f"Processing {filename}...")
            try:
                convert_video(input_path, model)
                print(f"Successfully processed {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

    print("All videos processed.")

if __name__ == "__main__":
    main()