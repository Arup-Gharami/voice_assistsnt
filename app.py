import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import requests
from datetime import datetime

# Init pyttsx
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)  # 1 for Female voice, 0 for Male

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)  # Reduce background noise
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except Exception:
        return "None"
    return query.lower()

def greet_user():
    """ Greet User Based on Time """
    hour = int(datetime.now().hour)
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("Meettra Assistant activated. How can I assist you?")

def get_weather(city="New Delhi"):
    """ Fetch Weather Information """
    api_key = 'cd27d5f632d14a04bcd100746252203'  # WeatherAPI Key
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
    response = requests.get(url).json()

    if "error" in response:
        speak("Sorry, I couldn't fetch the weather details.")
        return

    temp = response['current']['temp_c']
    weather_desc = response['current']['condition']['text']
    speak(f"The temperature in {city} is {temp} degrees Celsius with {weather_desc}.")

apps = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe"
}

if __name__ == '__main__':
    greet_user()

    while True:
        query = take_command()

        if 'wikipedia' in query:
            speak("Searching Wikipedia ...")
            query = query.replace("wikipedia", '')
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia:")
            speak(results)

        elif 'who are you' in query:
            speak("I am Meettra, your AI assistant developed by, mister, Arup Gharami.")

        elif 'open' in query:
            if 'youtube' in query:
                webbrowser.open("youtube.com")
            elif 'google' in query:
                webbrowser.open("google.com")
            elif 'github' in query:
                webbrowser.open("github.com")
            elif 'stackoverflow' in query:
                webbrowser.open("stackoverflow.com")
            elif 'spotify' in query:
                webbrowser.open("spotify.com")
            elif 'whatsapp' in query:
                speak("Opening WhatsApp")
                try:
                    os.system("start shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!WhatsApp")
                except Exception:
                    speak("Sorry, I was unable to open WhatsApp.")
            else:
                app_name = query.replace('open ', '').strip()
                if app_name in apps:
                    speak(f"Opening {app_name}")
                    os.startfile(apps[app_name])
                else:
                    speak(f"Sorry, I don't know how to open {app_name}")

        elif 'local disk' in query:
            try:
                disk_letter = query.split()[-1].upper()
                webbrowser.open(f"{disk_letter}://")
            except Exception:
                speak("Sorry, I couldn't open the disk.")

        elif 'weather' in query:
            speak("Please say the city name.")
            city = take_command().lower()
            get_weather(city)

        elif 'time' in query:
            speak(f"The time is {datetime.now().strftime('%H:%M')}")

        elif 'sleep' in query or 'close' in query:
            speak("I am going to sleep now. Say 'Hi Mitra' to wake me up.")
            
            while True:
                wake_command = take_command()
                if 'hi mitra' in wake_command:
                    speak("I am back! How can I help you?")
                    break
        elif 'shutdown'  in query:
            speak("'Shutting down', 'thanks you for using meetra voice assistance',,, 'Goodbye!'")
            exit(0)
