from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import sys

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