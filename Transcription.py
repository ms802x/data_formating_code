import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter, TextFormatter
from yt_dlp import YoutubeDL

def download_youtube_video(video_id):
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    transcription_path = f"transcriptions/{video_id}.txt"
    video_folder = "videos"
    transcription_folder = "transcriptions"
    
    # Ensure the required folders exist
    os.makedirs(video_folder, exist_ok=True)
    os.makedirs(transcription_folder, exist_ok=True)

    transcript = None
    try:
        # Try to fetch manually uploaded Arabic transcription
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ar'])
        print("Arabic transcription found.")
    except NoTranscriptFound:
        try:
            # Attempt to fetch auto-generated Arabic transcription
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ar-auto'])
            print("Auto-generated Arabic transcription found.")
        except (NoTranscriptFound, CouldNotRetrieveTranscript):
            print(f"No Arabic transcription (manual or auto-generated) available for video ID: {video_id}")
            return  # Skip video download if no transcription is found

    # Save transcription to file, ignoring the last entry
    with open(transcription_path, "w", encoding="utf-8") as f:
        for i in range(len(transcript) - 1):  # Exclude the last entry
            entry = transcript[i]
            start_time = entry['start']
            # Recalculate duration based on the next subtitle's start time
            duration = transcript[i + 1]['start'] - start_time
            
            # Write transcription details to the file
            text = entry['text']
            f.write(f"Start: {start_time:.2f}, Duration: {duration:.2f}, Text: {text}\n")
    print(f"Transcription saved to {transcription_path}")

    # Download video in medium quality
    ydl_opts = {
        'format': 'best[height<=480]',  # Downloads best quality video and audio in 480p or lower
        'outtmpl': f'{video_folder}/{video_id}.%(ext)s',  # Save video in 'videos' folder
        'quiet': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    print(f"Video downloaded to '{video_folder}/{video_id}.mp4'")

if __name__ == "__main__":
    # Assuming extract_video_ids is defined somewhere
    video_ids = extract_video_ids(file_path)
    for vid in video_ids:
        download_youtube_video(vid)
