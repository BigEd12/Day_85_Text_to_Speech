from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
from typing import Union
from PyPDF2 import PdfFileReader
from audio import Polly
from pdf import Reader


if __name__ == "__main__":
    polly = Polly()
    reader = Reader()

    pdf_or_text = input(
        "I can turn your plain text into speech (1) using Polly from AWS.\n"
        "I can also turn your PDF into an audiobook (2).\n"
        "Which would you prefer: '1' or '2': "
    )

    if pdf_or_text == "1":
        text_to_use = input("Please type the text you would like converted to speech: ")
    elif pdf_or_text == "2":

        text_to_use = reader.reader()
    else:
        print("Invalid choice")
        sys.exit(-1)

    audio_data = polly.synthesize_speech(text_to_use)

    stream_or_write = input("Do you want to stream the audio (1), or save it to file (2): ")
    if stream_or_write == "1":
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

    elif stream_or_write == "2":
        save_name = input("Enter the name you want to give the saved file: ")
        with open(f'{save_name}.mp3', 'wb') as file:
            file.write(audio_data)
    else:
        print("Invalid choice")
        sys.exit(-1)
