from deepmultilingualpunctuation import PunctuationModel
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import sys
import re
import http.client
import socket

def get_ipv4_from_hostname(hostname):
    address_info = socket.getaddrinfo(hostname, 80, proto=socket.IPPROTO_TCP)
    return address_info[1][4][0]

def get_http_content(domain, path):
    connection = http.client.HTTPConnection(domain, 80)
    connection.request("GET", path)
    response = connection.getresponse()
    print(response.status)
    connection.close()
    if response.status == 200:
        return response.read().decode("utf-8")
    return None

def get_youtube_video_title(video_id):
    youtube_ipv4 = get_ipv4_from_hostname("youtube.com")
    html_content = get_http_content(youtube_ipv4, "/watch?v=" + video_id)
    print(html_content)
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
