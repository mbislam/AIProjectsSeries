import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import random

engine = pyttsx3.init()

jokes = [
    "Why did the computer go to school? To improve its memory.",
    "Why was the math book sad? Because it had too many problems.",
    "Why do programmers prefer dark mode? Because light attracts bugs."
]

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        command = command.lower()
        print("You said:", command)
        return command
    except:
        return ""

def process_command(command):
    if "time" in command:
        now = datetime.datetime.now()
        return "The current time is " + now.strftime("%I:%M %p")

    elif "youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."

    elif "joke" in command:
        return random.choice(jokes)

    elif "who are you" in command:
        return (
            "I am your voice-based virtual assistant."
        )

    elif "hello" in command:
        return "Hello! How can I help you?"

    elif "stop" in command or "exit" in command:
        return "Goodbye!"

    elif command == "":
        return "I did not understand that."

    else:
        return (
            "I am still learning. Please try another command."
        )

def main():
    speak("Hello! I am your virtual assistant.")

    while True:
        command = listen()
        response = process_command(command)
        speak(response)

        if "Goodbye!" in response:
            break

if __name__ == "__main__":
    main()