import time
import glob
import pickle
import numpy as np
from utils import RunningStats
from pynput.keyboard import Key, Listener
from statistics import NormalDist
 
N_GRAM = 3
d = {}
q = []
t = {}

def load_template():
    templates = {}
    for filename in glob.glob('template/*.pickle'):
        with open(filename, 'rb') as handle:
            templates[filename[9:-7]] = pickle.load(handle)
    return templates

def on_press(key):
    cal(str(key), 'p')
    
def on_release(key):
    if key == Key.esc: 
        return False
    cal(str(key), 'r')

def _cal_c(m1, m2, std1, std2):
    area = NormalDist(mu=m1, sigma=std1).overlap(NormalDist(mu=m2, sigma=std2))
    return area ** (1/4)

def cal(key, event):
    global q, d
    _t = time.time()
    if event == 'p':
        d[key] = _t
    else:
        if key not in d:
            return
        _time = _t - d[key]
        if key not in t:
            t[key] = RunningStats()
        t[key].update(_time)
        
    q += [(_t, key + event)]
    if len(q) > N_GRAM:
        q.pop(0)
    for i in range(2, min(len(q), N_GRAM)):
        k = ''.join([e[1] for e in q[-i:]])
        _time = q[-1][0] - q[-i][0]
        if key not in t:
            t[key] = RunningStats()
        t[key].update(_time)
        
    for person in templates:
        tem = templates[person]
        prop = []
        count = 0
        for k in t:
            if k in tem:
                m1 = t[k].get_mean()
                m2 = tem[k].get_mean()
                std1 = t[k].get_std()
                std2 = tem[k].get_std()
                if std1 and std2:
                    c = t[k].get_count()
                    count += c
                    prop += [_cal_c(m1, m2, std1, std2) * c]
        print(person, np.sum(prop) / count, end='\t')
    print('')
    
    
if __name__ == '__main__':
    
    templates = load_template()
    print('Go!')
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()