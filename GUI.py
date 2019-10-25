from tkinter import *
from SpeechRecognition import *
#test func
def main():
    lang  = 'en'
    my_word = Speech2Text(lang)
    play_music_on_Youtube(my_word)
window = Tk()
window.geometry("200x100")
window.title("Play Youtube video")
button_1 = Button(window, text = 'Start', width=10, bg='blue', fg='black', command=main)
button_1.place(x=50,y=50)
window.mainloop()