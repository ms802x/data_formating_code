import os  # For file and folder operations
import yt_dlp

def download_youtube_video(video_id):
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    transcription_path = f"transcription/{video_id}.txt"
    video_folder = 'videos'
    transcription_folder = 'transcription'

    # Create the folders if they do not exist
    os.makedirs(video_folder, exist_ok=True)
    os.makedirs(transcription_folder, exist_ok=True)

    # Credentials for YouTube login (use your own credentials or generate a Google OAuth token)
    ydl_opts = {
        'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        'outtmpl': f'{video_folder}/{video_id}.%(ext)s',
        'quiet': True,
        'writesubtitles': True,  # Enable subtitle download
        'subtitleslangs': ['ar'],  # Specify Arabic subtitles
        'writeautomaticsub': True,  # Try to download auto-generated subtitles if available
        'skip_download': False,  # Download the video as well
        'username': 'your_email@example.com',  # Your YouTube login email
        'password': 'your_password',  # Your YouTube login password
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(video_url, download=True)

            # Check if subtitles are available
            if 'subtitles' in result and 'ar' in result['subtitles']:
                subtitle_file = f"{video_folder}/{video_id}.ar.vtt"
                # Convert the VTT subtitles to a text file
                with open(subtitle_file, 'r', encoding='utf-8') as f:
                    subtitles = f.readlines()

                # Save transcription to a text file, excluding the last entry
                with open(transcription_path, "w", encoding="utf-8") as f:
                    for line in subtitles[:-1]:
                        # Write each subtitle line to the text file
                        f.write(line.strip() + '\n')

                print(f"Transcription saved to {transcription_path}")
            else:
                print(f"No Arabic subtitles available for video ID: {video_id}")
                return  # Skip video download if no subtitles are found

            print(f"Video downloaded to '{video_folder}/{video_id}.mp4'")

        except Exception as e:
            print(f"Error downloading video: {e}")

if __name__ == "__main__":
    # List of video IDs to process
    video_ids = extract_video_ids(file_path)

    for vid in video_ids:
        download_youtube_video(vid)
