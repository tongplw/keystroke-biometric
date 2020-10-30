import time
import pandas as pd
from pynput.keyboard import Key, Listener
 
def on_press(key):
    global df
    key = str(key)
    print(key)
    df = df.append({'time': time.time(), 'key': key, 'event': 'p'}, ignore_index=True)
    
def on_release(key):
    global df
    df = df.append({'time': time.time(), 'key': key, 'event': 'r'}, ignore_index=True)
    if key == Key.esc:
        return False

df = pd.DataFrame(columns=['time', 'key', 'event'])

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

name = input('enter your name: ')
df.to_csv(f'data/{name}.csv', index=False)