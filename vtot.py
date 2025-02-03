import speech_recognition as sr

recognizer = sr.Recognizer()

audio_path = r"path"

# Open the audio file with sr.AudioFile
with sr.AudioFile(audio_path) as source:
    # Adjust for ambient noise
    recognizer.adjust_for_ambient_noise(source)
    # Record the audio
    audio_data = recognizer.record(source)

text = ""

def convert(audio_data):
    try:
        text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    return text

def write_text(text):
    with open('output.txt', 'a') as f:
        f.write(text)
        f.write('\n')
    return

# Convert the audio to text and write it
text = convert(audio_data)
write_text(text)