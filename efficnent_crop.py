import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def extract_video_clip_and_save_text(text_file, video_file, output_folder):
    # Read the text file line by line
    with open(text_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Extract video file name without extension
    video_filename = os.path.splitext(os.path.basename(video_file))[0]
    
    # Create output folders if they do not exist
    labels_folder = os.path.join(output_folder, 'labels', video_filename)
    clips_folder = os.path.join(output_folder, 'clips', video_filename)
    os.makedirs(labels_folder, exist_ok=True)
    os.makedirs(clips_folder, exist_ok=True)
    
    # Initialize variables to track clip information
    current_start = None
    current_duration = 0
    current_text = ""
    clip_index = 0

    # Process each line in the text file
    for i, line in enumerate(lines):
        # Example line: Start: 0.12, Duration: 3.84, Text: اهلا قبل فتره اطلقنا اشتراك 8 في العديد
        parts = line.split(", ")
        start = float(parts[0].split(": ")[1])
        duration = float(parts[1].split(": ")[1])
        text = parts[2].split(": ")[1].strip()

        # Check if this is the start of a new clip or part of the current one
        if current_start is None:
            current_start = start
        
        # If the current clip duration is less than 10 seconds, accumulate
        if current_duration + duration < 10:
            current_duration += duration
            current_text += " " + text  # Merge text for this combined clip
        else:
            # If the current clip reaches 10 seconds, create the clip and text file
            clip_filename = f"{video_filename}_clip_{clip_index + 1:03d}.mp4"
            text_filename = f"{video_filename}_clip_{clip_index + 1:03d}.txt"
            
            clip_output_path = os.path.join(clips_folder, clip_filename)
            text_output_path = os.path.join(labels_folder, text_filename)
            
            # Extract the video clip using ffmpeg_extract_subclip (from moviepy)
            ffmpeg_extract_subclip(video_file, current_start, current_start + current_duration, targetname=clip_output_path)
            
            # Save the corresponding text
            with open(text_output_path, 'w', encoding='utf-8') as text_file:
                text_file.write(current_text)
            
            # Reset for next clip
            current_start = start
            current_duration = duration
            current_text = text
            clip_index += 1

    # If the accumulated duration of the final clip is less than 10 seconds, ignore it
    if current_duration >= 10:
        clip_filename = f"{video_filename}_clip_{clip_index + 1:03d}.mp4"
        text_filename = f"{video_filename}_clip_{clip_index + 1:03d}.txt"
        
        clip_output_path = os.path.join(clips_folder, clip_filename)
        text_output_path = os.path.join(labels_folder, text_filename)
        
        ffmpeg_extract_subclip(video_file, current_start, current_start + current_duration, targetname=clip_output_path)
        
        with open(text_output_path, 'w', encoding='utf-8') as text_file:
            text_file.write(current_text)

def process_all_files(transcriptions_folder, videos_folder, output_folder):
    # Get all transcription files
    transcription_files = [f for f in os.listdir(transcriptions_folder) if f.endswith('.txt')]
    
    # Loop through each transcription file
    for transcription_file in transcription_files:
        # Get the corresponding video file (same name but different extension)
        print(transcription_file)
        video_file = os.path.join(videos_folder, os.path.splitext(transcription_file)[0] + '.mp4')
        
        # Check if the corresponding video file exists
        if os.path.exists(video_file):
            # Define full path for the transcription file
            text_file = os.path.join(transcriptions_folder, transcription_file)
            
            # Process the transcription and extract clips
            extract_video_clip_and_save_text(text_file, video_file, output_folder)
        else:
            print(f"Video file {video_file} not found for transcription {transcription_file}")

# Define the input and output paths
transcriptions_folder = "/content/transcriptions"
videos_folder = "/content/videos"
output_folder = "/content/output"

# Call the function to process all transcriptions and videos
process_all_files(transcriptions_folder, videos_folder, output_folder)
