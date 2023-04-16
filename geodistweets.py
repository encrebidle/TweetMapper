

def geotweets():
    import matplotlib.pyplot as plt
    %matplotlib inline
    import seaborn as sns
    import folium
    from folium.plugins import HeatMapWithTime, TimestampedGeoJson

    import numpy as np # linear algebra
    import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory
    import os
    tweets = pd.read_csv('C:/Users/katulya/Desktop/Atulya_Work_Git_Dev/2023Projects/RealTimeTweetGeoDistribution/modi_tweets.csv')
