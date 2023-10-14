import re
import requests
import os
import argparse
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

def get_transcript(video_id, languages=['en',], preserve_formatting=True):
    print(preserve_formatting)
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages, preserve_formatting)
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--video")
    parser.add_argument("-l", "--languages")
    parser.add_argument("-r", "--raw", action='store_true')
    parser.add_argument("-m", "--preserve-markup", action='store_true')
    args = parser.parse_args()
    if not args.video or args.video == True:
        print("No YouTube video id provided. Please provide one.")
        return
    video_id = args.video[1:] if args.video.startswith("$") else args.video
    if (len(video_id) != 11):
        print(f"Illegal YouTube video id '{video_id}'. Has to be exactly 11 characters. ")
        return
    default_languages = ['en', 'de', 'fr', 'it']
    languages = args.languages.split(",") if args.languages else default_languages
    for language in languages:
        if (language in default_languages): continue
        print(f"Language {language} is not supported by the language model (supported languages are '{default_languages}'). ")
    preserve_markup = False if args.preserve_markup == None else args.preserve_markup

    # Get transcript
    raw_transcript = get_transcript(video_id, languages, preserve_markup)
    punctuated_transcript = add_punctuation(raw_transcript)
    formatted_transcript = format_sentences(punctuated_transcript)

    # Print to console if raw
    has_raw_output = args.raw
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
    with open(unique_output_path, 'w', encoding='utf-8') as file:
        file.write(formatted_transcript)
    print(f"Written transcript to '{unique_output_path}'. ")

if __name__ == "__main__":
    main()
