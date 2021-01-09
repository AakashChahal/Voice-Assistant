# import csv
import sqlite3
import urllib
import Weather
import pyttsx3
import datetime
import re
import smtplib
import webbrowser
import speech_recognition as sr
import wikipedia
import os
import SpeedTest

# noinspection SpellCheckingInspection
users = {
    'aakash': '****************',
    'shivam': '*****************',
    'abhishek': '****************',
}

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


# function to take voice commands from user
def input_command():
    """
    It takes input from user using microphone
    :return: string output
    """

    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)
    with m as source:
        print('listening...')
        audio = r.listen(source)

        try:
            print('recognizing...')
            query = r.recognize_google(audio)
            print(f"\"{query}\"")
        except Exception as e:
            print(e)
            speak("Sorry!! Didn't catch that")
            query = input_command()
    return query


# computers reply to user command
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# greeting at the beginning
def greet():
    """"
    used to greet the user according to the current time
    :return:
    """
    hour = int(datetime.datetime.now().hour)
    if 12 > hour >= 0:
        speak('Good Morning, I am your voice assistant')
    elif 12 <= hour < 17:
        speak('Good Afternoon, I am your voice assistant')
    else:
        speak('Good Evening, I am your voice assistant')

    speak('How may I help you today?')


# function to send email
def send_email(to, msg):
    """
    this function is used to send email
    :param to: name of the person whom you have to send the email
    :param msg: the message you want to send through email
    :return:
    """
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    # login details needed to be stored in separate file.
    server.login('*************', '********')
    server.sendmail('***********', to, msg)
    server.close()


def main():
    greet()
    while True:
        userQuery = input_command().lower()
        # if "What can you do?" in userQuery:
        #     speak("I can send email for you, check weather of any city you want, play any song or check your internet "
        #           "speed")

        if 'thank you' in userQuery:
            speak("You're Welcome. I am happy to assist you")

        elif 'internet speed' in userQuery:
            speed = SpeedTest.check_speed()
            speak(speed)

        elif 'how are you' in userQuery:
            speak('I am very well.')
            speak('What can i do for you?')
            print('try speaking \'send email\', \'tell me a joke\', \'latest news\', ')

        # noinspection SpellCheckingInspection
        elif 'wikipedia' in userQuery:
            userQuery = userQuery.replace("wikipedia", "")
            if userQuery == "":
                speak("what exactly do you want to search")
            else:
                result = wikipedia.summary(userQuery, sentences=3)
                speak("According to wikipedia")
                print(result)
                speak(result)

        elif 'launch' in userQuery:
            regex = re.search('launch (.*)', userQuery)
            if regex:
                app = regex.group(1)
                if 'vs code' in userQuery:
                    speak("Opening VS Code")
                    os.startfile('C:\\Users\\path to\\Code.exe')

                elif 'pycharm' in userQuery:
                    speak("Opening Pycharm")
                    os.startfile(
                        '"C:\\Program Files\\path to\\pycharm64.exe"')
                else:
                    os.startfile(f'C:\\{app}.exe')

        elif 'time' in userQuery:
            time = datetime.datetime.now().strftime('%H:%M')
            speak('current time in 24 hour format is:' + time)

        elif 'open reddit' in userQuery:
            regex = re.search('open reddit (.*)', userQuery)
            url = 'https://www.reddit.com/'
            if regex:
                subreddit = regex.group(1)
                url = url + 'r/' + subreddit
            webbrowser.open(url)
            speak('The Reddit content has been opened for you.')

        # opening any website
        elif 'open' in userQuery:
            regex = re.search('open (.+)', userQuery)
            if regex:
                domain = regex.group(1)
                if '.com' in domain:
                    url = 'https://www.' + domain
                    webbrowser.open(url)
                    speak(f'Opening {domain}...')
                else:
                    url = 'https://www.' + domain + '.com'
                    webbrowser.open(url)
                    speak(f'Opening {domain}.com...')

        elif 'send email' in userQuery:
            conn = sqlite3.connect('Database.db')
            c = conn.cursor()
            c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='contacts' ''')
            if c.fetchone()[0] != 1:
                c.execute('''CREATE TABLE contacts (name text primary key, email text)''')
                conn.commit()

            speak('Who do you want to send an email to?')
            user = input_command().lower()
                
            try:
                c.execute('SELECT * FROM contacts WHERE name =?', (user,))
                name = c.fetchone()
                if name:
                    speak(f"What do you want to say to {user}")
                    message = input_command()
                    send_email(users[user], message)
                    speak(f'email sent to {user}')
                else:
                    raise Exception

            except:
                speak("email account of this user is not available, please type the email below")
                email = input("Email: ")
                speak(f"What do you want to say to {user}")
                message = input_command()
                send_email(email, message)
                speak(f'email sent to {user}')
                speak("do you want me to save this email for future usage?")
                ch = input_command()
                if "yes" in ch.lower():
                    c.execute('INSERT INTO contacts values(?, ?)', (user, email))
                    conn.commit()

                else:
                    speak('email is not saved')

        elif "weather" in userQuery:
            speak("Which city?")
            city = input_command()
            speak("Current weather in " + city + Weather.weather(city))

        elif 'play a song' in userQuery or 'play song':
            speak('What song do you want to play?')
            mySong = input_command()
            speak(f"Searching {mySong} on youtube...")
            # noinspection SpellCheckingInspection
            if mySong:
                flag = 0
                url = "https://www.youtube.com/results?search_query=" + mySong.replace(' ', '+')
                html = urllib.request.URLopener.urlopen(url)
                soup1 = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                url_list = []
                # for vid in soup1:
                vid = soup1[0]
                print(vid)
                if ('https://www.youtube.com/watch?v=' + vid).startswith("https://www.youtube.com/watch?v="):
                    flag = 1
                    final_url = 'https://www.youtube.com/watch?v=' + vid
                    url_list.append(final_url)
                    url = final_url
                # ydl_opts = {}
                # os.chdir(r'C:\Users\aakas\desktop')
                # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                #     ydl.download([url])
                # # vlc.play(os.path)
                if flag == 0:
                    speak('I have not found anything on Youtube ')
                else:
                    speak(f"playing {mySong} on youtube")
                    webbrowser.open(url)
                    exit()

        else:
            speak("Sorry didn't get that")
            input_command()


if __name__ == '__main__':
    main()
