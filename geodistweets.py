

def geotweets(hashtag):
    import matplotlib.pyplot as plt
    #%matplotlib inline
    import seaborn as sns
    import folium
    from folium.plugins import HeatMapWithTime, TimestampedGeoJson

    import numpy as np # linear algebra
    import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory
    import os
    path ='C:/Users/encre/OneDrive/Desktop/2023LearnigVault/datasets'
    tdata= os.path.join(path,(hashtag[1:] +"_tweets.csv"))
    cdata= os.path.join(path,('worldcities' +".csv"))
    locdata= os.path.join(path,('countries_codes_and_coordinates' +".csv"))
    
    tweets = pd.read_csv(tdata)
    cities = pd.read_csv(cdata)
    avg_countries_loc = pd.read_csv(locdata)
    
    tweets["lat"] = np.NaN
    tweets["lng"] = np.NaN
    tweets["location"] = tweets["user_location"]
    user_location = tweets['location'].fillna(value='').str.split(',')
    # Make a list of all countries in Avg Location Dataset
    codes = avg_countries_loc['Alpha-2 code'].str.replace('"','').str.strip().to_list()
    world_city_iso2 = []
    print(cities)
    print(type(cities["iso2"]))
    for c in cities['iso2'].str.lower().str.strip().values.tolist():
        if c not in world_city_iso2:
            world_city_iso2.append(c)
            
    # Try to identify if both external share same countries codes for tracking between them
    l_codes = [c.lower() for c in codes]
    for a in world_city_iso2:
        if a not in l_codes:
            print(a)
    codes = avg_countries_loc['Alpha-2 code'].str.replace('"','').str.strip().to_list() + ['XW','SX', 'CW','XK']
    code_lat = avg_countries_loc['Latitude (average)'].str.replace('"','').to_list() + ['31.953112', '18.0255', '12.2004', '42.609778']
    code_lng = avg_countries_loc['Longitude (average)'].str.replace('"','').to_list() + ['35.301170', '-63.0450', '-69.0200', '20.918062']
    
    
    ##Feature Engineering
    lat = cities['lat'].fillna(value = '').values.tolist()
    lng = cities['lng'].fillna(value = '').values.tolist()


    # Getting all alpha 3 codes into  a list
    world_city_iso3 = []
    for c in cities['iso3'].str.lower().str.strip().values.tolist():
        if c not in world_city_iso3:
            world_city_iso3.append(c)
            
    # Getting all alpha 2 codes into  a list    
    world_city_iso2 = []
    for c in cities['iso2'].str.lower().str.strip().values.tolist():
        if c not in world_city_iso2:
            world_city_iso2.append(c)
            
    # Getting all countries into  a list        
    world_city_country = []
    for c in cities['country'].str.lower().str.strip().values.tolist():
        if c not in world_city_country:
            world_city_country.append(c)

    # Getting all amdin names into  a list
    world_states = []
    for c in cities['admin_name'].str.lower().str.strip().tolist():
        world_states.append(c)


    # Getting all cities into  a list
    world_city = cities['city'].fillna(value = '').str.lower().str.strip().values.tolist()
    
    for each_loc in range(len(user_location)):
        ind = each_loc
        order = [False,False,False,False,False]
        each_loc = user_location[each_loc]
        for each in each_loc:
            each = each.lower().strip()
            if each in world_city:
                order[0] = world_city.index(each)
            if each in world_states:
                order[1] = world_states.index(each)
            if each in world_city_country:
                order[2] = world_city_country.index(each)
            if each in world_city_iso2:
                order[3] = world_city_iso2.index(each)
            if each in world_city_iso3:
                order[4] = world_city_iso3.index(each)

        if order[0]:
            tweets['lat'][ind] = lat[order[0]]
            tweets['lng'][ind] = lng[order[0]]
            continue
        if order[1]:
            tweets['lat'][ind] = lat[order[1]]
            tweets['lng'][ind] = lng[order[1]]
            continue
        if order[2]:
            try:
                tweets['lat'][ind] = code_lat[codes.index(world_city_iso2[order[2]].upper())]
                tweets['lng'][ind] = code_lng[codes.index(world_city_iso2[order[2]].upper())]
            except:
                pass
            continue
        if order[3]:
            tweets['lat'][ind] = code_lat[codes.index(world_city_iso2[order[3]].upper())]
            tweets['lng'][ind] = code_lng[codes.index(world_city_iso2[order[3]].upper())]
            continue
        if order[4]:
            tweets['lat'][ind] = code_lat[codes.index(world_city_iso2[order[4]].upper())]
            tweets['lng'][ind] = code_lng[codes.index(world_city_iso2[order[4]].upper())]
            continue
        
    
    #NullValues of Locations
    all_tweets = len(tweets)
    bad_tweets_without_location = tweets['user_location'].isnull().sum()
    tweets_unrecovered_location = tweets['lat'].isnull().sum()

    print(all_tweets, bad_tweets_without_location, tweets_unrecovered_location)
    print('\nPercentage of recovering Tweet Locations using extrenal datasets...')
    print((all_tweets-(tweets_unrecovered_location))/(all_tweets-bad_tweets_without_location))
    
    
    map_df = tweets[['lat','lng','user_location','date']].dropna()
    ##map_df.head()
    dates = map_df['date'].str.split(' ').str.get(0).unique().tolist()
    print('Number of Days in dataset:', len(dates))
    
    ####################################################################encrebidle
    
    
    daily_tweets = folium.Map(name = "Tweets Heatmap",tiles='cartodbpositron', min_zoom=2) 
    #adding  political coordinates--optional
    
    #political = ("http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson")
    #folium.GeoJson(political).add_to(daily_tweets)

    # Ensure you're handing it floats
    map_df['lat'] = map_df['lat'].astype(float)
    map_df['lng'] = map_df['lng'].astype(float)
    map_df['date'] = map_df['date'].str.split(' ').str.get(0)

    

    
    # List comprehension to make out list of lists
    heat_data = [[[row['lat'],row['lng']] for index, row in map_df[map_df['date'] == i].iterrows()] for i in dates]

    # Plot it on the map
    hm = HeatMapWithTime(data=heat_data, name=None, radius=7, min_opacity=0, max_opacity=0.8, 
                        scale_radius=False, gradient=None, use_local_extrema=False, auto_play=False, 
                        display_index=True, index_steps=1, min_speed=0.1, max_speed=10, speed_step=0.1, 
                        position='bottomleft', overlay=True, control=True, show=True)
    lat= list(map_df['lat'])
    lon = list(map_df['lng'])
    d = list(map_df['date'])
    
    fg = folium.FeatureGroup(name="Tweets Map")
    for lt, ln, el in zip(lat, lon, d):
        fg.add_child(folium.Marker(location=[lt,ln], popup = [str(el)], icon = folium.Icon(color= 'blue')))

    hm.add_to(daily_tweets)
    daily_tweets.add_child(fg)
    folium.LayerControl().add_to(daily_tweets)
    # Display the map
    
    path ='C:/Users/encre/OneDrive/Desktop/2023LearnigVault/output_pages'
    html_path= os.path.join(path,(hashtag[1:] +"_tweets.html"))
    daily_tweets.save(html_path)
    #daily tweets
    
    map_df = tweets[['lat','lng','user_location','date']].dropna()
    timely_tweets = folium.Map(tiles='cartodbpositron', min_zoom=2) 

    # Ensure you're handing it floats
    map_df['lat'] = map_df['lat'].astype(float)
    map_df['lng'] = map_df['lng'].astype(float)
    map_df['date'] = map_df['date']

    
    # List comprehension to make out list of lists
    heat_data = [[[row['lat'],row['lng']] for index, row in map_df[map_df['date'] == i].iterrows()] for i in dates]

    # Plot it on the map
    hm = TimestampedGeoJson(geojson_features(map_df), transition_time=200, loop=True, auto_play=False, add_last_point=True, 
                    period='P1D', min_speed=0.1, max_speed=10, loop_button=False, date_options='YYYY-MM-DD HH:mm:ss', 
                    time_slider_drag_update=False, duration=None)
    hm.add_to(timely_tweets)
    
    # Display the map
    #timely_tweets
    return daily_tweets    




def geojson_features(map_df):
        features = []
        for _, row in map_df.iterrows():
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type':'Point', 
                    'coordinates':[row['lng'],row['lat']]
                },
                'properties': {
                    'time': row['date'],
                    'style': {'color' : 'red'},
                    'icon': 'circle',
                    'iconstyle':{
                        'fillColor': 'red',
                        'fillOpacity': 0.5,
                        'stroke': 'true',
                        'radius': 3
                    }
                }
            }
            features.append(feature)
        return features    
            
def popup_html(row):
    i = row
    institution_name=df['INSTNM'].iloc[i] 
    institution_url=df['URL'].iloc[i]
    institution_type = df['CONTROL'].iloc[i] 
    highest_degree=df['HIGHDEG'].iloc[i] 
    city_state = df['CITY'].iloc[i] +", "+ df['STABBR'].iloc[i]                     
    admission_rate = df['ADM_RATE'].iloc[i]
    cost = df['COSTT4_A'].iloc[i]
    instate_tuit = df['TUITIONFEE_IN'].iloc[i]
    outstate_tuit = df['TUITIONFEE_OUT'].iloc[i]

    left_col_color = "#19a7bd"
    right_col_color = "#f2f0d3"
    
    html = """<!DOCTYPE html>
<html>
<head>
<h4 style="margin-bottom:10"; width="200px">{}</h4>""".format(institution_name) + """
</head>
    <table style="height: 126px; width: 350px;">
<tbody>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Institution Type</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(institution_type) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Institution URL</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(institution_url) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">City and State</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(city_state) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Highest Degree Awarded</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(highest_degree) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Admission Rate</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(admission_rate) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Annual Cost of Attendance $</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(cost) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">In-state Tuition $</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(instate_tuit) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Out-of-state Tuition $</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(outstate_tuit) + """
</tr>
</tbody>
</table>
</html>
"""
    return html        
geotweets("#NFT")    
        
        
        
        
        
        
    
    
    
    
    
    
    
    