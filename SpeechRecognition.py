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

def Speech2Text(lang):
    r = sr.Recognizer()   #Speech recognition
    with sr.Microphone() as source:
        speak("Now you can say something!")
        audio = r.listen(source)
    try:
        my_word = r.recognize_google(audio,language=lang)
        speak(f"You just said: {my_word}."+'Is it correct?')
        print(my_word)
        #check_correctness(sentence)
        return my_word
    except sr.UnknownValueError:
        speak("Google Speech Recognition could not understand your words. Let's try again.")
        Speech2Text()
    except sr.RequestError as e:
        speak("Could not request results from Google Speech Recognition service; {0}".format(e))

def speak(words):
    lang = 'en'
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts = gTTS(words, lang=lang)
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
def check_correctness(sentence):
    speak(f"You just said: {my_word}."+'Is it correct?')
    my_answer = r.recognize_google(audio,language=lang)
    if my_answer == 'yes it is':
        pass
def play_music_on_Youtube(my_word):
    my_song = '+'.join(my_word.split(' ')[1:-2])
    print(my_song)
    Youtube_url = 'https://www.youtube.com'
    res = requests.get(f'{Youtube_url}/results?search_query={my_song}')
    soup = BeautifulSoup(res.text, 'html.parser')
    song_link = Youtube_url+soup.select('h3 a')[0]['href']
    print(song_link)
    webbrowser.open(song_link, new=2)
    return

if __name__ == "__main__":
    lang  = 'en'
    my_word = Speech2Text(lang)
    play_music_on_Youtube(my_word)
    # webbrowser.open(f'https://www.youtube.com/results?search_query={my_song}', new=2)
    # browser = webdriver.Safari()

