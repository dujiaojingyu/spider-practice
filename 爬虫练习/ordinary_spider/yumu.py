import os 
import random
import time

arr = [0,1,' ']
alpha = 'abcdefghijklmnopqrstuvwxyz        '

def init():
    os.system('PS1=')
    for i in range(24):
        print("\n")

def play(arr):
    init()
    while True:
        for i in range(20):
            print(random.choice(arr),end='  ')
        time.sleep(0.1)
        print()
if __name__ == '__main__':
    play(alpha)