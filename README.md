# README #

This README would normally document whatever steps are necessary to get your application up and running.

## What is this repository for? ##

* This respositoy is for monitor anomaly in time-series Key Performance Indicators (KPIs) for potiential indicents.
* Version: 1.0


## Installation ##

Prerequisites: Python 3.5, adtk

```shell
pip install adtk
```

## Explanation of our solution ##


### step 1: learning from training dataset ###

from training dataset, we know the anomaly in this challenge includes point anomaly and point anomaly and most of their types are as follows:

1. outlier
2. spike
3. level shift
4. pattern change
5. seasonality


### step 2: choose detector for various anomaly

After step 1, we work on to choose detector for above anomaly pattern. Finally, we choose PersistAD detector for spike, LevelShiftAD detector for level shift, VolatilityShiftAD for pattern change, SeasonalAD for seasonality from package ["ADTK"](https://github.com/arundo/adtk), which includes differnt detection algorithms, feature engineering methods and ensemble methods.


### step 3: combine detectors

After knowing the nature of anomaly varies in this challenge, we realized a model may not work for all the datasets. So we combine detectors, feature enginnering methods and ensemble methods to solve different anomaly pattern.


- Example 1: single detector
the anomaly pattern in dataset10 is a typical seasonality, you can choose SeasonalAD to detect to anomaly.
        

- Example 2: multiple detector

the anomaly pattern in dataset4 is mixed with level shift and spike. We could combine LevelShiftAD detector and PersistAD dectector and finally aggregate the two results.
```shell
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
```

### Alternative Solution

We also try facebook's [fbprophet](https://pypi.org/project/fbprophet/) to forecast and detect anomaly for these time series data.

### Who do I talk to? ###

* Zhang Ran <ranzhang46@gmail.com>
* Wang Jialu <jarrywangcn@outlook.com>
* Zhong Yezhao <1125644188@qq.com>