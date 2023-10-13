import sys
import re
import requests
import os
from deepmultilingualpunctuation import PunctuationModel
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def get_safe_filename(filename, replacement='_', max_length=255):
    safe_filename = re.sub(r'[\\/:*?"<>|]', replacement, filename)
    if len(safe_filename) > max_length:
        return safe_filename[:max_length]
    return safe_filename

def get_youtube_video_title(video_id):
    response = requests.get("https://www.youtube.com/watch?v=" + video_id)
    html_content = response.text
    if response.status_code != 200:
        return "unknown"
    title_start = html_content.find("<title>")
    title_end = html_content.find("</title>", title_start)
    return html_content[title_start + 7 : title_end]

def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    #formatter = TextFormatter()
    output = []
    for segment in transcript:
        output.append(segment['text'])
    return " ".join(output)

def add_punctuation(input):
    model = PunctuationModel()
    return model.restore_punctuation(input)

def format_sentences(input):
    capitalized_input = input[0].upper() + input[1:]
    pattern = r'([.?]) (\S)'
    replace = lambda match: f"{match.group(1)}\n\n{match.group(2).upper()}"
    return re.sub(pattern, replace, capitalized_input)

def get_unique_file_path(file_path):
    dir = os.path.dirname(file_path)
    basename_raw = os.path.basename(file_path)
    basename = os.path.splitext(basename_raw)[0]
    extension = os.path.splitext(basename_raw)[1]
    duplicate_counter = 1
    get_file_path = lambda suffix: os.path.join(dir, basename + suffix + extension)
    new_file_path = get_file_path("")
    while (os.path.exists(new_file_path)):
        suffix = f" ({duplicate_counter})" if duplicate_counter > 1 else ""
        new_file_path = get_file_path(suffix)
        duplicate_counter += 1
    return new_file_path

def main():
    # Process CLI arguments
    if len(sys.argv) <= 1:
        print("No YouTube video id provided. Please provide one.")
        return
    video_id = sys.argv[1]
    has_raw_output = len(sys.argv) > 2 and sys.argv[2] == "--raw"

    # Get transcript
    raw_transcript = get_transcript(video_id)
    punctuated_transcript = add_punctuation(raw_transcript)
    formatted_transcript = format_sentences(punctuated_transcript)

    # Print to console if raw
    if (has_raw_output):
        print(formatted_transcript)
        return

    # Write file to output
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    video_title = get_youtube_video_title(video_id)
    raw_title = re.search(r'(.*) - YouTube$', video_title).group(1)
    escaped_title = get_safe_filename(raw_title)
    file_name = f"({video_id}) {escaped_title}"
    output_path = os.path.join(output_dir, file_name + ".txt")
    unique_output_path = get_unique_file_path(output_path)
    with open(unique_output_path, 'w') as file:
        file.write(formatted_transcript)
    print(f"Written transcript to '{unique_output_path}'. ")

if __name__ == "__main__":
    main()
