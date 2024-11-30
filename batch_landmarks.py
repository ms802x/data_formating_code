import os
import glob
from batch_face import RetinaFace

def read_video_frames(video_path):
    """
    Reads frames from a video file and returns them in a list.
    """
    frames = []
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames

def process_clips_in_batches(clips_dir, batch_size=10, threshold=0.95):
    """
    Processes all .mp4 files inside the clips directory and maps the landmarks.

    Args:
        clips_dir (str): The root directory containing the clips.
        batch_size (int): The number of clips to process in one batch.
        threshold (float): Confidence threshold for face detection.

    Returns:
        dict: A mapping of file paths to detection results.
    """
    # Initialize the detector
    detector = RetinaFace(gpu_id=0, fp16=True)

    # Collect all .mp4 files
    all_video_files = glob.glob(os.path.join(clips_dir, "**", "*.mp4"), recursive=True)
    print(f"Found {len(all_video_files)} video files.")

    # Initialize results dictionary
    results_mapping = {}

    # Process in batches
    for i in range(0, len(all_video_files), batch_size):
        batch_files = all_video_files[i:i + batch_size]
        print(f"Processing batch {i // batch_size + 1} with {len(batch_files)} files.")

        # List to hold all frames (flattened) and a mapping to track each frame's corresponding clip
        all_frames = []
        frames_mapping = []

        # Read frames for all files in the batch and create the flattened list
        for video_path in batch_files:
            frames = read_video_frames(video_path)
            all_frames.extend(frames)  # Add the frames to the list
            frames_mapping.extend([video_path] * len(frames))  # Map each frame to the video
            print(video_path,len(frames_mapping))
        # Perform detection on the frames (all_frames is the flattened list)
        batch_results = detector(all_frames, threshold=threshold)

        # Map results back to the original video files using the frames_mapping
        for idx, faces in enumerate(batch_results):
            video_path = frames_mapping[idx]  # Find which clip the frame belongs to
            if video_path not in results_mapping:
                results_mapping[video_path] = []
            results_mapping[video_path].append(faces)

    return results_mapping


# Example usage
clips_dir = "clips"  # Root directory containing clip folders
landmark_mapping = process_clips_in_batches(clips_dir, batch_size=20, threshold=0.95)

# Save or inspect results
print(f"Processed {len(landmark_mapping)} clips.")
