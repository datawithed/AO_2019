# -*- coding: utf-8 -*-
"""
Created on Thu May 19 14:04:02 2022

@author: Ed.Morris
"""

# AO 2019 final dashboard analysis

# ==========================================================
# Set wd
# ==========================================================
# Set wd
import os
path = "C:/Users/ed.morris/Documents/Python Scripts/Streamlit"
os.chdir(path)
cwd = os.getcwd()
print(f"Current working directory is: {cwd}")

# ==========================================================
# Import modules
# ==========================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from PIL import Image
from plotly.offline import iplot

st.set_page_config(page_title = 'AO2019 Final Analysis', layout = 'wide', page_icon = Image.open('AO_logo.jpg'))


@st.cache
# ==========================================================
# Load data
# ==========================================================
def load_data():
    serve_data = pd.read_csv('Aus Open Final 2019 - serve data.csv')
    event_data = pd.read_csv('Aus Open Final 2019 - event data.csv')
    points_data = pd.read_csv('Aus Open Final 2019 - points data.csv')
    rally_data = pd.read_csv('Aus Open Final 2019 - rally data.csv')
    ND_pic = Image.open('ND_pic.jpg')
    RN_pic = Image.open('RN_pic.jpg')
    # Filter serves that are out
    serve_data = serve_data[(serve_data.x >= 1.4) & (serve_data.y > 5.5)].reset_index(drop = True)
    
    return serve_data, event_data, points_data, rally_data, ND_pic, RN_pic

serve_data, event_data, points_data, rally_data, ND_pic, RN_pic = load_data()

# ==========================================================
# Functions for drawing court visualisations
# ==========================================================

ND_serves = serve_data.loc[serve_data.server == 'Djokovic'].reset_index(drop = True)
RN_serves = serve_data.loc[serve_data.server == 'Nadal'].reset_index(drop = True)

height_court = 10.97
width_court = 11.89*2
service_box = 6.4
double_field = 1.37
baseline_serviceline = 5.5
breite_einzel = 8.23
serviceline_net = 6.4

# Map both serves from bottom half of court to top half
for i in range(len(ND_serves)):
    if ND_serves.y[i] < width_court/2 and ND_serves.x[i] < baseline_serviceline:
        ND_serves.x[i] = (2*baseline_serviceline - double_field) - (ND_serves.x[i] - double_field)
        ND_serves.y[i] = (width_court - baseline_serviceline) - (ND_serves.y[i] - baseline_serviceline)
    elif ND_serves.y[i] < width_court/2 and ND_serves.x[i] > baseline_serviceline:
        ND_serves.x[i] = double_field + ((2*baseline_serviceline - double_field) - ND_serves.x[i])
        ND_serves.y[i] = (width_court - baseline_serviceline) - (ND_serves.y[i] - baseline_serviceline)
for i in range(len(RN_serves)):
    if RN_serves.y[i] < width_court/2 and RN_serves.x[i] < baseline_serviceline:
        RN_serves.x[i] = (2*baseline_serviceline - double_field) - (RN_serves.x[i] - double_field)
        RN_serves.y[i] = (width_court - baseline_serviceline) - (RN_serves.y[i] - baseline_serviceline)
    elif RN_serves.y[i] < width_court/2 and RN_serves.x[i] > baseline_serviceline:
        RN_serves.x[i] = double_field + ((2*baseline_serviceline - double_field) - RN_serves.x[i])
        RN_serves.y[i] = (width_court - baseline_serviceline) - (RN_serves.y[i] - baseline_serviceline)

# Add column for serve target
zone_width = (baseline_serviceline - double_field) / 3 # width of service box

# Reset index
ND_serves = ND_serves.reset_index(drop = True)
RN_serves = RN_serves.reset_index(drop = True)

# Split forehand, backhand and body serve data for separate coloured plots
backhand_left_ND = ND_serves.loc[(double_field <= ND_serves.x) & (ND_serves.x < double_field + zone_width)]
backhand_right_ND = ND_serves.loc[(baseline_serviceline <= ND_serves.x) & (ND_serves.x < baseline_serviceline + zone_width)]
body_left_ND = ND_serves.loc[(ND_serves.x >= double_field + zone_width) & (ND_serves.x <= double_field + zone_width*2)]
body_right_ND = ND_serves.loc[(ND_serves.x >= baseline_serviceline + zone_width) & (ND_serves.x <= baseline_serviceline + zone_width*2)]
forehand_left_ND = ND_serves.loc[(ND_serves.x > double_field + zone_width*2) & (ND_serves.x <= baseline_serviceline)]
forehand_right_ND = ND_serves.loc[(ND_serves.x > baseline_serviceline + zone_width*2) & (ND_serves.x <= height_court - double_field)]

backhand_left_RN = RN_serves.loc[(double_field <= RN_serves.x) & (RN_serves.x < double_field + zone_width)]
backhand_right_RN = RN_serves.loc[(baseline_serviceline <= RN_serves.x) & (RN_serves.x < baseline_serviceline + zone_width)]
body_left_RN = RN_serves.loc[(RN_serves.x >= double_field + zone_width) & (RN_serves.x <= double_field + zone_width*2)]
body_right_RN = RN_serves.loc[(RN_serves.x >= baseline_serviceline + zone_width) & (RN_serves.x <= baseline_serviceline + zone_width*2)]
forehand_left_RN = RN_serves.loc[(RN_serves.x > double_field + zone_width*2) & (RN_serves.x <= baseline_serviceline)]
forehand_right_RN = RN_serves.loc[(RN_serves.x > baseline_serviceline + zone_width*2) & (RN_serves.x <= height_court - double_field)]

# Combine dfs
backhands_ND = [backhand_left_ND,backhand_right_ND]
body_ND = [body_left_ND,body_right_ND]
forehands_ND = [forehand_left_ND,forehand_right_ND]
backhands_ND_df = pd.concat(backhands_ND)
body_ND_df = pd.concat(body_ND)
forehands_ND_df = pd.concat(forehands_ND)

backhands_RN = [backhand_left_RN,backhand_right_RN]
body_RN = [body_left_RN,body_right_RN]
forehands_RN = [forehand_left_RN,forehand_right_RN]
backhands_RN_df = pd.concat(backhands_RN)
body_RN_df = pd.concat(body_RN)
forehands_RN_df = pd.concat(forehands_RN)

# Filter out potential lets (short serves)
backhands_ND_df = backhands_ND_df.loc[backhands_ND_df.y > 15]
body_ND_df = body_ND_df.loc[body_ND_df.y > 15]
forehands_ND_df = forehands_ND_df.loc[forehands_ND_df.y > 15]
backhands_RN_df = backhands_RN_df.loc[backhands_RN_df.y > 15]
body_RN_df = body_RN_df.loc[body_RN_df.y > 15]
forehands_RN_df = forehands_RN_df.loc[forehands_RN_df.y > 15]

# Reset index
backhands_ND_df = backhands_ND_df.reset_index(drop = True)
body_ND_df = body_ND_df.reset_index(drop = True)
forehands_ND_df = forehands_ND_df.reset_index(drop = True)
backhands_RN_df = backhands_RN_df.reset_index(drop = True)
body_RN_df = body_RN_df.reset_index(drop = True)
forehands_RN_df = forehands_RN_df.reset_index(drop = True)

# Function to draw top half of court only
def draw_halfcourt(player,hide_axes=False):
    """Sets up field
    Returns matplotlib fig and axes objects.
    """
        
    fig = plt.figure(figsize = (height_court / 2, width_court / 4))
    #fig = plt.figure(figsize=(9, 9))
    fig.patch.set_facecolor('#5080B0')

    axes = fig.add_subplot(1, 1, 1, facecolor = '#5080B0')

    if hide_axes:
        axes.xaxis.set_visible(False)
        axes.yaxis.set_visible(False)
        axes.axis('off')
    
    # Plot points of ND serve, and plot line from avg serve position to points
    if player == 'Djokovic':
        for i in range(len(backhands_ND_df)):
            plt.plot(backhands_ND_df.x, backhands_ND_df.y, 'x', color = 'red')
        for i in range(len(body_ND_df)):
            plt.plot(body_ND_df.x, body_ND_df.y, 'x', color = 'blue')
        for i in range(len(forehands_ND_df)):
            plt.plot(forehands_ND_df.x, forehands_ND_df.y, 'x', color = 'green')
        plt.title("Australian Open Final 2019: \n Djokovic 1st Serve Placement vs Nadal", 
                          fontname = 'Microsoft Sans Serif', 
                          color = 'white', 
                          fontsize = 16)
        
        # Plot first point of each df for legend
        plt.plot(backhands_ND_df.x[0], backhands_ND_df.y[0],'x', color = 'red', label = 'Backhand')
        plt.plot(body_ND_df.x[0], body_ND_df.y[0],'x', color = 'blue', label = 'Body')
        plt.plot(forehands_ND_df.x[0], forehands_ND_df.y[0],'x', color = 'green', label = 'Forehand')
       # Set legend location and fontsize
        legend = plt.legend(loc = 'upper center', fontsize = 8)
        # Set background and frame colour of legend
        frame = legend.get_frame()
        frame.set_facecolor('white')
        frame.set_edgecolor('white')
        
    if player == 'Nadal':
        for i in range(len(backhands_RN_df)):
            plt.plot(backhands_RN_df.x, backhands_RN_df.y, 'x', color = 'red')
        for i in range(len(body_RN_df)):
            plt.plot(body_RN_df.x, body_RN_df.y, 'x', color = 'blue')
        for i in range(len(forehands_RN_df)):
            plt.plot(forehands_RN_df.x, forehands_RN_df.y, 'x', color = 'green')
        plt.title("Australian Open Final 2019: \n Nadal 1st Serve Placement vs Djokovic", 
                          fontname = 'Microsoft Sans Serif', 
                          color = 'white', 
                          fontsize = 16)
    
        # Plot first point of each df for legend
        plt.plot(backhands_RN_df.x[0], backhands_RN_df.y[0],'x', color = 'red', label = 'Forehand')
        plt.plot(body_RN_df.x[0], body_RN_df.y[0],'x', color = 'blue', label = 'Body')
        plt.plot(forehands_RN_df.x[0], forehands_RN_df.y[0],'x', color = 'green', label = 'Backhand')
       # Set legend location and fontsize
        legend = plt.legend(loc = 'upper center', fontsize = 8)
        # Set background and frame colour of legend
        frame = legend.get_frame()
        frame.set_facecolor('white')
        frame.set_edgecolor('white')
    
    axes = draw_patches(axes)
    
    return fig, axes

def draw_patches(axes):
    plt.xlim([-1, 12])
    plt.ylim([width_court/2, width_court + 2])
    
    #net
    axes.add_line(plt.Line2D([height_court, 0],[width_court / 2, width_court / 2], c = 'w'))
    
    # court outline
    y = 0
    dy = width_court
    x = 0 # height_court - double_field
    dx = height_court
    axes.add_patch(plt.Rectangle((x, y), dx, dy, edgecolor = "white", facecolor = "#5581A6", alpha = 1))
    # serving rect
    y = baseline_serviceline
    dy = serviceline_net * 2
    x = 0 + double_field 
    dx = breite_einzel
    axes.add_patch(plt.Rectangle((x, y), dx, dy, edgecolor = "white", facecolor = "none", alpha = 1))
    
    #net
    axes.add_line(plt.Line2D([height_court / 2, height_court / 2], 
                             [width_court/2 - service_box, width_court / 2 + service_box], 
                             c = 'w'))
    
    axes.add_line(plt.Line2D([height_court / 2, height_court / 2], [0, 0 + 0.45], c = 'w'))

    axes.add_line(plt.Line2D([height_court / 2, height_court / 2], [width_court, width_court - 0.45], c = 'w'))
    
    axes.add_line(plt.Line2D([1.37, 1.37], [0, width_court], c = 'w'))
    
    axes.add_line(plt.Line2D( [height_court - 1.37, height_court - 1.37], [0, width_court], c = 'w'))
    
    axes.text(11.5,15.5, '@datawithed', rotation = 270, color = 'white', alpha = 0.5)

    return axes

draw_halfcourt('Djokovic',hide_axes=(True))
plt.savefig("ND serve plot.jpg",dpi = 750)
draw_halfcourt('Nadal',hide_axes=True)
plt.savefig('RN serve plot.jpg',dpi = 750)

ND_serve_plot = Image.open('ND serve plot.jpg')
RN_serve_plot = Image.open('RN serve plot.jpg')

# ==========================================================
# Dashboard configuration
# ==========================================================

# Set-up tab appearance

add_sidebar = st.sidebar.selectbox('Select Page', ('Home','Match Summary','Serve Analysis','Return Analysis'))

if add_sidebar == 'Home':
    t1, t2 = st.columns([2,10])
    t1.image('AO_logo.jpg')
    t2.header('Australian Open 2019 Final Analysis \n By Ed Morris')
    t2.markdown(" **Twitter:** @datawithed **| Instagram:** @data_with_ed")
    st.markdown("Set up to be another classic Grand Slam final in Melbourne, Novak Djokovic was coming off the back of a fantastic 2018 season. The current holder of the previous two Slams, the current world number 1 and 6x Australian Open champion, the numbers seemed to be stacked in Novak's favour. However what no one anticipated was the manner in which he would go about claiming his 7th title in the Rod Laver arena.")
    st.markdown("Nadal, hitting a scintillating run of form in the tournament in his route to the final, hadn't dropped a single set and looked far and away the most likely candidate to cause an upset Down Under. He had spent significantly less time on court than Djokovic in his previous rounds, not letting his ankle surgery before the tournament hinder his play.")
    st.markdown('This dashboard will attempt to delve into some of the key stats, visualising where this tie was won and lost by both players.')
    
        
    
    


if add_sidebar == 'Match Summary':
    st.title('Match Summary Statistics')
    points_won = points_data[['rallyid','winner']].groupby('winner').count()
    points_won['winner'] = points_won.index
    fig = px.bar(points_won, x = 'winner', y = 'rallyid', title = 'Total points won by each player')
    fig.update_layout(xaxis_title = 'Winner', yaxis_title = 'Points')
    st.plotly_chart(fig)
    
    
    
    
    
if add_sidebar == 'Serve Analysis':
    st.title('Serve Analysis')
    players = tuple(serve_data['server'].unique())
    players_select = st.selectbox('Select a player',(players))
    
    if players_select == 'Djokovic':
        st.markdown("Data from: https://www.ultimatetennisstatistics.com/playerProfile?playerId=4920&tab=matches#matchStats-173429Serve")
        col1, col2, col3, col4, col5 = st.columns((1,1,1,1,1))
        col1.metric(label = '1st serve %', value = f"{0.725:.0%}", delta = f"{0.725-0.649:.0%} compared to career", delta_color = 'normal')
        col2.metric(label = '1st serve % won', value = f"{0.8:.0%}", delta = f"{0.8-0.737:.0%} compared to career", delta_color = 'normal')
        col3.metric(label = '2nd serve % won', value = f"{0.842:.0%}", delta = f"{0.842-0.554:.0%} compared to career", delta_color = 'normal')
        col4.metric(label = 'Break Points saved %', value = f"{1:.0%}", delta = f"{1-0.655:.0%} compared to career", delta_color = 'normal')
        col5.metric(label = 'Service games won %', value = f"{1:.0%}", delta = f"{1-0.858:.0%} compared to career", delta_color = 'normal')
        st.image(ND_serve_plot, width=500)
        
    elif players_select == 'Nadal':
        st.markdown("Data from: https://www.ultimatetennisstatistics.com/playerProfile?playerId=4920&tab=matches#matchStats-173429Serve")
        rn_col1, rn_col2, rn_col3, rn_col4, rn_col5 = st.columns((1,1,1,1,1))
        rn_col1.metric(label = '1st serve %', value = f"{0.644:.0%}", delta = f"{0.644-0.681:.0%} compared to career", delta_color = 'normal')
        rn_col2.metric(label = '1st serve % won', value = f"{0.511:.0%}", delta = f"{0.511-0.722:.0%} compared to career", delta_color = 'normal')
        rn_col3.metric(label = '2nd serve % won', value = f"{0.615:.0%}", delta = f"{0.615-0.573:.0%} compared to career", delta_color = 'normal')
        rn_col4.metric(label = 'Break Points saved %', value = f"{0.375:.0%}", delta = f"{0.375-0.663:.0%} compared to career", delta_color = 'normal')
        rn_col5.metric(label = 'Service games won %', value = f"{0.615:.0%}", delta = f"{0.615-0.858:.0%} compared to career", delta_color = 'normal')
        st.image(RN_serve_plot,width=500)

        
    
    
    
if add_sidebar == 'Return Analysis':
    st.title('Return Analysis')
    players = tuple(serve_data['server'].unique())
    players_select = st.selectbox('Select a player',(players))
    #if players_select == 'Djokovic':
        
    #elif players_select == 'Nadal':
        















