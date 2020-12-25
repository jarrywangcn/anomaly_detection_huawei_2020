import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import sys
import os

# import detector
from adtk.visualization import plot
from adtk.data import validate_series
from adtk.detector import LevelShiftAD, PersistAD, SeasonalAD, VolatilityShiftAD
from adtk.aggregator import OrAggregator
from adtk.pipe import Pipenet


# load data for adtk
def read_for_adtk( folder_name, file_name ):#读取csv文件
    df = pd.read_csv('%s'%folder_name + '%s'%file_name, index_col = ['timestamp'],  parse_dates=True, squeeze=True)
    try:
        df = df.drop(['request_count'], axis=1)
    except:
        print('non')
    return df

def load_file(folder_path, file_name):
    df = read_for_adtk(folder_path, file_name)
    s_train = validate_series(df)
    return df, s_train

# detect anomaly by mode
# data 为 adtk validate_series
def detect_anomaly( data, mode = 'LevelShift'):
    
    if mode == 'LevelShift':
        print('mode is', mode)
        dect = LevelShiftAD(20)
    elif mode == 'Persist':
        print('mode is', mode)
        dect = PersistAD(window = 1150)
    elif mode == 'Seasonal':
        print('mode is', mode)
        dect = SeasonalAD()
    elif mode == 'VolatilityShift':
        print('mode is', mode)
        dect = VolatilityShiftAD(window = 25)
    elif mode == 'PersistLevelShiftMixed':
        # detect levelshift and persist(spike) anomaly simultaneously
        # 为什么连接之后, 数据少了dataset4  22695->22683
        steps = {
            'levelshift': {
                'model': LevelShiftAD(80),
                "input": "original"
            },
            'persist':{
                'model': PersistAD(window = 1150),
                "input": "original"
            },
            'mixed':{
                'model': OrAggregator(),
                "input": ["levelshift", "persist"]
            }
        }
        dect = Pipenet(steps)
        
    anomalies = dect.fit_detect(data)
    # plot
    #plot(data, anomaly=anomalies, anomaly_color="red", anomaly_tag="marker")
    return anomalies

def output_result(folder_path, file_name, original_df, anomaly, replace = False ):
    if replace == True:
        final_path = folder_path + file_name
    else:
        final_path = folder_path + 'res_' + file_name
    print(final_path)
    # 修改anomaly的名字(原先为数据名)
    anomaly.name = 'anomaly_label'
    # 填充空值
    anomaly = anomaly.fillna(value = 0)
    print(anomaly[anomaly == '1'])
    # 修改为int
    anomaly = anomaly.astype(int) 
    # 两表连接
    anomaly = anomaly[~anomaly.index.duplicated()]
    original_df = original_df[~original_df.index.duplicated()]
    out = pd.concat([original_df, anomaly], axis = 1)
    # 输出
    out.to_csv(final_path, index=True)

def individual(folder_name, file, mode, replace, factors = []):
    df, s_train = load_file( folder_path, file)
    anomalies = detect_anomaly(s_train, mode )
    output_result(folder_path, file, df, anomalies, replace)
    
    
# four mode: LevelShift, Persist, Seasonal, VolatilityShift, PersistLevelShiftMixed
mode_dict = {'dataset_1.csv': 'LevelShift',
             'dataset_2.csv': 'LevelShift', 
             'dataset_3.csv': 'LevelShift', 
             'dataset_4.csv': 'PersistLevelShiftMixed', 
             'dataset_5.csv': 'LevelShift',
             'dataset_6.csv': 'LevelShift',
             'dataset_7.csv': 'LevelShift',
             'dataset_8.csv': 'LevelShift', 
             'dataset_9.csv': 'VolatilityShift', 
             'dataset_10.csv': 'LevelShift',
             'dataset_11.csv': 'Seasonal', 
             'dataset_12.csv': 'VolatilityShift', 
             'dataset_13.csv': 'Seasonal', 
             'dataset_100.csv': 'LevelShift',
             'dataset_101.csv': 'LevelShift',
             'dataset_102.csv': 'LevelShift',
             'dataset_103.csv': 'LevelShift',
             'dataset_105.csv': 'LevelShift',
             'dataset_106.csv': 'LevelShift',
            }

# running
folder_path = sys.path[0] + '/data_v2/'
all_files = os.listdir(folder_path)

for file_name in all_files:
    if file_name[-4:] == '.csv':
        print(file_name)
        mode = mode_dict[file_name]
        individual(folder_path, file_name, mode, replace = False)
        print('successfully output', file_name)
        '''
        except:
            print('something wrong about', file_name)
            continue
        '''