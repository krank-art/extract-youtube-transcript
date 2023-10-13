from deepmultilingualpunctuation import PunctuationModel
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import sys
import re
import requests

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
    replace = lambda match: f"{match.group(1)}\n{match.group(2).upper()}"
    return re.sub(pattern, replace, capitalized_input)

def main():
    if len(sys.argv) <= 1:
        print("No YouTube video id provided. Please provide one.")
        return
    video_id = sys.argv[1]
    print(get_youtube_video_title(video_id))
    # raw_transcript = get_transcript(video_id)
    # punctuated_transcript = add_punctuation(raw_transcript)
    # formatted_transcript = format_sentences(punctuated_transcript)
    # print(formatted_transcript)

if __name__ == "__main__":
    main()
