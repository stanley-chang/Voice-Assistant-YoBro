#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 21:01:37 2018

@author: Stanley
"""
import speech_recognition as sr
from gtts import gTTS
import time
import tempfile
from pygame import mixer
import pygame
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import os
import datetime
from GoogleCalendar import get_cred, get_events, add_event
import pyttsx3
import subprocess

class VoiceAssistant():
    '''
    Func1 : Play music on Youtube.
    Func2 : Speak events on specific date.
    Func3 : Add event on specific date.
    '''
    #Class Variables
    MONTH_LIST = ["january", "february", "march", "april", "may", "june","july", "august", "september","october", "november", "december"]
    DAY_LIST = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    DATE_EXTENTIONS = ["st", "nd", "rd", "th"]
    
    def __init__(self, language='en'):
        self.language = language
        self.my_word = ""
        self.speak("Hallo! My name is YoBro.")

    def Speech2Text(self):
        r = sr.Recognizer()   #Speech recognition
        with sr.Microphone() as source:
            self.speak("What can I do for you?")
            try:
                audio = r.listen(source,timeout=5)
            except sr.WaitTimeoutError:
                pass
        try:
            self.my_word = r.recognize_google(audio,language=self.language)
            self.speak(f"You just said: {self.my_word}.")
            print(self.my_word)
            #check_correctness(sentence)
            return self.my_word
        except:
            self.my_word = ""
            return self.my_word
        # except sr.UnknownValueError:
        #     self.speak("Google Speech Recognition could not understand your words. Let's try again.")
        #     self.Speech2Text()
        # except sr.RequestError as e:
        #     self.speak(f"Could not request results from Google Speech Recognition service; {e}.")

    # Woman Sound
    # def speak(self, words):
    #     with tempfile.NamedTemporaryFile(delete=True) as fp:
    #         tts = gTTS(words, lang=self.language)
    #         tts.save(f'{fp.name}.mp3')
    #         mixer.init()
    #         pygame.display.set_mode((200,100))
    #         mixer.music.load(f'{fp.name}.mp3')
    #         mixer.music.play(loops=0, start=0.0)
    #         clock = pygame.time.Clock()
    #         clock.tick(10)
    #         while pygame.mixer.music.get_busy():
    #             pygame.event.poll()
    #             clock.tick(10)
    #     return
    
    # Men Sound
    def speak(self, words):
        engine = pyttsx3.init()
        engine.say(words)
        engine.runAndWait()
        return

    # def check_correctness(self, sentence):
    #     self.speak(f"You just said: {my_word}."+'Is it correct?')
    #     my_answer = r.recognize_google(audio,language=lang)
    #     if my_answer == 'yes it is':
    #         pass

    def play_music_on_Youtube(self, my_word):
        '''
        Please say "Play {Name of the Song} on Youtube."
        '''
        my_song = '+'.join(my_word.split(' ')[1:-2])
        print(my_song)
        Youtube_url = 'https://www.youtube.com'
        res = requests.get(f'{Youtube_url}/results?search_query={my_song}')
        soup = BeautifulSoup(res.text, 'html.parser')
        song_link = Youtube_url+soup.select('h3 a')[0]['href']
        print(song_link)
        webbrowser.open(song_link, new=2)
        return

    def extract_date_from_sentence(self,sentence):
        '''
        Sentence: A string.
        Example:
        "What do I have on December 3rd?"
        "What is my schedule like on Saturday?"
        "Do I have anything next Tuesday?"
        '''
        sentence = sentence.lower()
        today = datetime.date.today()
        next = False

        if "today" in sentence:
            return today
        if "tomorrow" in sentence:
            return today + datetime.timedelta(days=1)
        if "next" in sentence:
            next = True
        
        #Extract info from sentence
        year,month, day_in_week, date = today.year,-1,-1,-1
        for word in sentence.split():

            if word in self.MONTH_LIST:
                month = self.MONTH_LIST.index(word) + 1
            elif word in self.DAY_LIST:
                day_in_week = self.DAY_LIST.index(word)
                break

            if word.isdigit():
                date = int(word)
            else:
                for ext in self.DATE_EXTENTIONS:
                    if ext in word:
                        try:
                            date = int(word[:-len(ext)])
                        except:
                            pass
        
        #Return date by day_in_week
        if day_in_week != -1:
            current_day_in_week = today.weekday()
            diff = day_in_week - current_day_in_week
            if diff >= 1:
                if next:
                    return today + datetime.timedelta(days=diff+7)
                return today + datetime.timedelta(days=diff)
            elif diff <= 0:
                return today + datetime.timedelta(days=diff+7)
        
        if (month != -1 and date != -1):
            if month < today.month:
                year +=1
            return datetime.date(month=month, day=date, year=year)

        # Default : return the event tomorrow
        return today + datetime.timedelta(days=1)
    
    def SpeakEvents(self, events, date):
        month, day = date.month, str(date.day)
        month = self.MONTH_LIST[month-1]

        ext = int(day[-1])
        if ext == 1:
            ext = self.DATE_EXTENTIONS[0]
        elif ext == 2:
            ext = self.DATE_EXTENTIONS[1]
        elif ext == 3:
            ext = self.DATE_EXTENTIONS[2]
        else:
            ext = self.DATE_EXTENTIONS[3]

        if not events:
            self.speak(f'No upcoming events are found on {month} {day}{ext}.')
        else:
            self.speak(f"You have {len(events)} events on {month} {day}{ext}.")

            for event in events:
                # Transform from iso time format to sth like this -> '16:00:00+01:00' #
                event_time = event['start']['dateTime'].split('T')[1]
                event_name = event['summary']
                if int(event_time.split(':')[0]) < 12 :
                    if event_time.split(':')[1] == '00':
                        event_time = event_time.split(':')[0] + 'am'
                    else:
                        event_time = ':'.join(event_time.split(':')[:2]) + 'am'
                else:
                    # Transfrom from 24hr format to 12 hr format
                    if int(event_time.split(':')[0]) > 12 :
                        old_hr = event_time.split(':')[0]
                        event_time = event_time.replace(old_hr,str(int(old_hr)-12),1)
                    if event_time.split(':')[1] == '00':
                        event_time = event_time.split(':')[0] + 'pm'
                    else:
                        event_time = ':'.join(event_time.split(':')[:2]) + 'pm'
                print(event_name +' at ' + event_time+'.')
                self.speak(event_name +' at ' + event_time+'.')
        return
    
    def extract_EventName_from_sentence(self,sentence):
        '''
        sentence: "Please add (event_name) on my calendar on (date)"
        '''
        start = 11
        temp = sentence.find('calendar')
        end = sentence[:temp].find('on')-1
        return sentence[start:end]

if __name__ == "__main__":
    YoBro = VoiceAssistant()
    Wake_up = "yo"
    Music_Keywords = ['i want to listen to music', 'play some music', 'time for music']
    Speak_events_Keywords = ['what do i have', 'show my calendar']
    Add_event_Keywords = ['add event', 'add event on my calendar']
    Done = 'YoBro has done what you asked YoBro to do.'
    service = get_cred()

    while True:
        my_word = YoBro.Speech2Text().lower()
        if my_word.count(Wake_up) >= 1:
            YoBro.speak('What do you want?')
            my_word = YoBro.Speech2Text().lower()
            for keyword in Music_Keywords:
                if keyword in my_word:
                    my_word = YoBro.Speech2Text()
                    # Say "play (music name) on Youtube"
                    YoBro.play_music_on_Youtube(my_word)
                    YoBro.speak(Done)

            for keyword in Speak_events_Keywords:
                if keyword in my_word:
                    my_word = YoBro.Speech2Text()
                    # Say "what doi have on/next (date)"
                    date_in_sentence = YoBro.extract_date_from_sentence(my_word)
                    events = get_events(service, date_in_sentence)
                    YoBro.SpeakEvents(events, date_in_sentence)
                    YoBro.speak(Done)
            
            for keyword in Add_event_Keywords:
                if keyword in my_word:
                    my_word = YoBro.Speech2Text()
                    # Say "Please add (event_name) on my calendar on (date)"
                    date_in_sentence = YoBro.extract_date_from_sentence(my_word)
                    event_name = YoBro.extract_EventName_from_sentence(my_word)
                    add_event(service, date_in_sentence, event_name)
                    YoBro.speak(Done)
            YoBro.speak('End of loop')
        if my_word.count('stop') >= 1:
            break
