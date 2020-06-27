import requests
from bs4 import BeautifulSoup
import time
from youtube_transcript_api import YouTubeTranscriptApi

videoIDs = ['I_4iRxgX21c','xOSQjURy5h8','CPvho_jUWhU','psjq2msrKIU','0znX34Q7Vaw','gtaQ2MlflKo']

transcripts = []

for video in videoIDs:
    time.sleep(60)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video)
        transcripts.append(transcript)
        print("found " + video)
    except:
        print('Could not retreive transcript for video: ' + video)

finalSpeech = ""

for speech in transcripts:
    for text in speech:
        finalSpeech += text['text'].replace('[','').replace(']','') + " "

f = open("proPalestineFile.txt", "w")
f.write(finalSpeech)
f.close()


