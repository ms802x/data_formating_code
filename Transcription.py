def download_youtube_video(video_id):
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    transcription_path = f"transcription/{video_id}.txt"

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

    # Save transcription to file
    with open(transcription_path, "w", encoding="utf-8") as f:
        for i, entry in enumerate(transcript):
            start_time = entry['start']
            
            # Recalculate duration based on the next subtitle's start time
            if i < len(transcript) - 1:
                duration = transcript[i + 1]['start'] - start_time
            else:
                duration = 2.0  # Default duration for the last entry
            
            # Write transcription details to the file
            text = entry['text']
            f.write(f"Start: {start_time:.2f}, Duration: {duration:.2f}, Text: {text}\n")
    print(f"Transcription saved to {transcription_path}")

    # Download video in medium quality
    ydl_opts = {
        'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        'outtmpl': f'videos/{video_id}.%(ext)s',
        'quiet': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    print(f"Video downloaded to 'videos/{video_id}.mp4'")

if __name__ == "__main__":
    # List of video IDs to process
    video_ids = [
        "4kTR_qGqOJc",  # Example video ID (replace with your own)
        
    ]

    for vid in video_ids:
        download_youtube_video(vid)

