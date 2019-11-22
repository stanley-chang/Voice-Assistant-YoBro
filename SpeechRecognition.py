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

class VoiceAssistant():
    #Class Variables
    MONTH_LIST = ["january", "february", "march", "april", "may", "june","july", "august", "september","october", "november", "december"]
    DAY_LIST = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    DATE_EXTENTIONS = ["rd", "th", "st", "nd"]
    
    def __init__(self, language='en'):
        self.language = language
        self.my_word = ""
        self.speak("Hallo! My name is YoBro.")

    def Speech2Text(self):
        r = sr.Recognizer()   #Speech recognition
        with sr.Microphone() as source:
            self.speak("Now you can say something!")
            audio = r.listen(source)
        try:
            self.my_word = r.recognize_google(audio,language=self.language)
            self.speak(f"You just said: {self.my_word}."+'Is it correct?')
            print(self.my_word)
            #check_correctness(sentence)
            return self.my_word
        except sr.UnknownValueError:
            self.speak("Google Speech Recognition could not understand your words. Let's try again.")
            self.Speech2Text()
        except sr.RequestError as e:
            self.speak(f"Could not request results from Google Speech Recognition service; {e}.")

    def speak(self, words):
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            tts = gTTS(words, lang=self.language)
            tts.save(f'{fp.name}.mp3')
            mixer.init()
            pygame.display.set_mode((200,100))
            mixer.music.load(f'{fp.name}.mp3')
            mixer.music.play(loops=0, start=0.0)
            clock = pygame.time.Clock()
            clock.tick(10)
            while pygame.mixer.music.get_busy():
                pygame.event.poll()
                clock.tick(10)
        return

    # def check_correctness(self, sentence):
    #     self.speak(f"You just said: {my_word}."+'Is it correct?')
    #     my_answer = r.recognize_google(audio,language=lang)
    #     if my_answer == 'yes it is':
    #         pass

    def play_music_on_Youtube(self):
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
        
        
                


if __name__ == "__main__":
    YoBro = VoiceAssistant()
    my_word = YoBro.Speech2Text()
    date_in_sentence = YoBro.extract_date_from_sentence(my_word)
    print(date_in_sentence)
    # play_music_on_Youtube(my_word)
    # webbrowser.open(f'https://www.youtube.com/results?search_query={my_song}', new=2)
    # browser = webdriver.Safari()

