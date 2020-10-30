import glob
import pickle
import pandas as pd
from utils import RunningStats

N_GRAM = 6

def gen_template(df):
    template = {'_pr': RunningStats()}
    d = {}
    # press release
    for i, (time, key, event) in df.iterrows():
        if key not in d:
            d[key] = time
        else:
            t = time - d[key]
            del d[key]
            if key not in template:
                template[key] = RunningStats()
            template[key].update(t)
            template['_pr'].update(t)
    # n-gram
    df.key = df.key + df.event
    for i in range(N_GRAM, len(df)):
        for j in range(2, N_GRAM+1):
            _df = df.iloc[i:i+j]
            key = ''.join(map(str, _df.key.to_list()))
            time = _df.iloc[-1].time - _df.iloc[0].time
            if key not in template:
                template[key] = RunningStats()
            if f'_{j}' not in template:
                template[f'_{j}'] = RunningStats()
            template[key].update(time)
            template[f'_{j}'].update(time)
    return template

if __name__ == '__main__':
    
    for filename in glob.glob('data/*.csv'):
        df = pd.read_csv(filename)
        tem = gen_template(df)
        with open(f'template/{filename[5:-4]}.pickle', 'wb') as handle:
            pickle.dump(tem, handle, protocol=pickle.HIGHEST_PROTOCOL)