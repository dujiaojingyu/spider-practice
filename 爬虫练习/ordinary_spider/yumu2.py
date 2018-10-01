import os 
import random
import time
import threading

arr = [0,1,' ']
alpha = 'abcdefghijklmnopqrstuvwxyz        '
column = 80
lines = 24
picture = []

def init():
    os.system('PS1=')
    

def play(arr):
    init()
    while True:
        draw(arr)
        time.sleep(0.5)

def draw(arr):
    produceline(arr)
    for i in picture:
        print(i)

def produceline(arr):
    newline = ''
    global picture

    for i in range(column//4):
        newline += str(random.choice(arr)) + '   '
    picture.insert(0,newline)
    picture = picture[:lines]


if __name__ == '__main__':
    t = threading.Thread(target=play,args=(arr,))
    t.start()
    t.join()
