from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import sys
import os
import subprocess
from tempfile import gettempdir

class Polly:
    def __init__(self, profile_name: str = "default"):
        self.session = Session(profile_name=profile_name)
        self.client = self.session.client("polly")

    def synthesize_speech(self, text: str) -> bytes:
        try:
            response = self.client.synthesize_speech(
                Text=text, OutputFormat="mp3", VoiceId="Emma"
            )
        except (BotoCoreError, ClientError) as error:
            print(error)
            sys.exit(-1)

        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                return stream.read()
        else:
            print("Could not stream audio")
            sys.exit(-1)


    def save_audio(self, audio_data, save_name: str):
        with open(f'{save_name}.mp3', 'wb') as file:
            file.write(audio_data)


    def stream_audio(self, audio_data):
        output = os.path.join(gettempdir(), "speech.mp3")

        try:
            with open(output, "wb") as file:
                file.write(audio_data)
        except IOError as error:
            print(error)
            sys.exit(-1)

        if sys.platform == "win32":
            os.startfile(output)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, output])
