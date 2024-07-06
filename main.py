import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey  # Make sure you have your OpenAI API key in a config file
import datetime
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech

chatStr = ""

def list_microphones():
    """Lists available microphones and their indices."""
    print("Available microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"{index}: {name}")

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"User: {query}\nJarvis: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    try:
        response_text = response["choices"][0]["text"].strip()
        say(response_text)
        chatStr += f"{response_text}\n"
        return response_text
    except Exception as e:
        print(f"Error: {e}")
        say("An error occurred")
        return None

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt}\n{'*'*25}\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text += response["choices"][0]["text"].strip()
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    file_name = "_".join(prompt.split()[:5]) + ".txt"
    with open(f"Openai/{file_name}", "w") as f:
        f.write(text)

def say(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand(device_index=None):
    r = sr.Recognizer()
    with sr.Microphone(device_index=device_index) as source:
        r.pause_threshold = 0.6
        print("Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-IN")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Could not understand audio")
            return "Sorry, I did not understand that."
        except sr.RequestError:
            print("Could not request results; check your network connection")
            return "Sorry, there seems to be an issue with the network."
        except Exception as e:
            print(f"Error: {e}")
            return "Some error occurred. Sorry from Jarvis."

def test_microphone(device_index=None):
        """Tests the selected microphone by recording and recognizing speech."""
        recognizer = sr.Recognizer()
        with sr.Microphone(device_index=device_index) as source:
            print(f"Testing microphone {device_index}. Please speak into the microphone.")
            audio = recognizer.listen(source)
            try:
                print("Recognizing...")
                query = recognizer.recognize_whisper(audio, language="en-IN")
                print(f"Microphone test successful. Recognized: {query}")
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError:
                print("Could not request results; check your network connection.")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == '__main__':
    print('Welcome to Jarvis AI')
    say("Hello, I am your AI Powered Desktop Assistant.")

    list_microphones()
    selected_device = input("Enter the microphone index you want to use (or press Enter to use default): ")
    device_index = int(selected_device) if selected_device else None


    while True:
        print("Listening....")
        query = takeCommand(device_index=device_index).lower()

        if "open youtube" in query:
            say("Opening YouTube, sir...")
            webbrowser.open("https://www.youtube.com")

        elif "open wikipedia" in query:
            say("Opening Wikipedia, sir...")
            webbrowser.open("https://www.wikipedia.com")

        elif "open google" in query:
            say("Opening Google, sir...")
            webbrowser.open("https://www.google.com")

        elif "open music" in query:
            musicPath = "C:\\Users\\YourUsername\\Music\\downfall-21371.mp3"  # Adjust the path accordingly
            os.system(f"start {musicPath}")

        elif "the time" in query:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Sir, the time is {current_time}")

        elif "open facetime" in query:
            say("FaceTime is not available on Windows.")

        elif "open pass" in query:
            os.system("start passkey.exe")  # Adjust the path to the executable accordingly

        elif "using artificial intelligence" in query:
            ai(prompt=query)

        elif "jarvis quit" in query:
            say("Goodbye, sir!")
            break

        elif "reset chat" in query:
            chatStr = ""
            say("Chat history has been reset.")

        else:
            print("Chatting...")
            chat(query)

'''hjyfhfkhkyjygbjfjjhjhk0.gysyufggudsvyfydggdyttdvdhybvdjnhdhghdthdgy'''