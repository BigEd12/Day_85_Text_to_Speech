"""Getting Started Example for Python 2.7+/3.3+"""
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
from PyPDF2 import PdfReader

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
session = Session(profile_name="default")

polly = session.client("polly")

pdf_or_text = input("I can turn your plain text into speech (1) using Polly from AWS.\nI can also turn your PDF into an audio book (2).Which would you prefer: '1' or '2': ")

if pdf_or_text == "1":
    reader = PdfReader("story.pdf")
    page = reader.pages[0]
    text_to_use = page.extract_text()
elif pdf_or_text == "2":
    text_to_use = input("Please type the text you would like converted to speech: ")


try:
    # Request speech synthesis
    response = polly.synthesize_speech(Text=text_to_use, OutputFormat="mp3", VoiceId="Emma")

except (BotoCoreError, ClientError) as error:
    # The service returned an error, exit gracefully
    print(error)
    sys.exit(-1)
# Access the audio stream from the response
if "AudioStream" in response:
    # Note: Closing the stream is important because the service throttles on the
    # number of parallel connections. Here we are using contextlib.closing to
    # ensure the close method of the stream object will be called automatically
    # at the end of the with statement's scope.

        with closing(response["AudioStream"]) as stream:
            stream_or_write = input("Do you want to stream the audio (1), or save it to file (2): ")
            if stream_or_write == "1":
                output = os.path.join(gettempdir(), "speech.mp3")

                try:
                 # Open a file for writing the output as a binary stream
                    with open(output, "wb") as file:
                        file.write(stream.read())
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    sys.exit(-1)
            elif stream_or_write == "2":
                save_name = input("Enter the name you want to give the saved file: ")
                with open(f'{save_name}.mp3', 'wb') as file:
                    file.write(stream.read())
else:
    # The response didn't contain audio data, exit gracefully
    print("Could not stream audio")
    sys.exit(-1)

if stream_or_write == "1":
    # Play the audio using the platform's default player
    if sys.platform == "win32":
        os.startfile(output)
    else:
        # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, output])
