import sys
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
        pdf_name = input("Please ensure the PDF is already saved in the script directory.\n"
              "What is the name of the pdf, without the extension (eg. 'story'): ")
        text_to_use = reader.reader(pdf_name=pdf_name)

    else:
        print("Invalid choice")
        sys.exit(-1)

    audio_data = polly.synthesize_speech(text_to_use)

    stream_or_write = input("Do you want to stream the audio (1), or save it to file (2): ")
    if stream_or_write == "1":
        polly.stream_audio(audio_data=audio_data)

    elif stream_or_write == "2":
        save_name = input("Enter the name you want to give the saved file: ")
        polly.save_audio(audio_data=audio_data, save_name=save_name)
    else:
        print("Invalid choice")
        sys.exit(-1)
