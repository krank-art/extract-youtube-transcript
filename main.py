from deepmultilingualpunctuation import PunctuationModel
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import sys
import re

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
    raw_transcript = get_transcript(video_id)
    punctuated_transcript = add_punctuation(raw_transcript)
    formatted_transcript = format_sentences(punctuated_transcript)
    print(formatted_transcript)

if __name__ == "__main__":
    main()
