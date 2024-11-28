import re

def extract_video_ids(file_path):
    # YouTube video ID pattern (handles both short and full URLs)
    youtube_pattern = r'(?:https?://)?(?:www\.)?(?:youtube|youtu|youtube-nocookie)\.(?:com|be)/(?:[^/\n]+/)*(?:watch\?v=|embed\/)([a-zA-Z0-9_-]{11})'

    video_ids = []

    # Open the file and read its contents
    with open(file_path, 'r') as file:
        for line in file:
            # Search for YouTube video ID in each line
            match = re.search(youtube_pattern, line)
            if match:
                video_ids.append(match.group(1))  # Append the found video ID

    return video_ids

# Example usage
file_path = 'data.txt'  # Path to the text file containing YouTube links
video_ids = extract_video_ids(file_path)
print(video_ids)
