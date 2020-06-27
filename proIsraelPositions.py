import requests
from bs4 import BeautifulSoup
import time
from youtube_transcript_api import YouTubeTranscriptApi

videoIDs = ['HTugN3Wtb28','V3dg27ilKVQ','kjw0qzY6H44','MSjBiEcCmQA','EwZAmsmXy6w','QcBEDPNbyjA','-pOs99OZN1g','4u2WKAI4luw']

transcripts = []

for video in videoIDs:
    time.sleep(60)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video)
        transcripts.append(transcript)
        print('found ' + video)
    except:
        print('Could not retreive transcript for video: ' + video)

finalSpeech = ""

for speech in transcripts:
    for text in speech:
        finalSpeech += text['text'].replace('[','').replace(']','') + " "

f = open("proIsraelFile.txt", "w")
f.write(finalSpeech)
f.close()
