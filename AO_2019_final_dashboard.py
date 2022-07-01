# -*- coding: utf-8 -*-
"""
Created on Thu May 19 14:04:02 2022

@author: Ed.Morris
"""

# AO 2019 final dashboard analysis

# ==========================================================
# Set wd
# ==========================================================
# import os
# path = "C:/Users/ed.morris/Documents/Python Scripts/Streamlit_apps"
# os.chdir(path)
# cwd = os.getcwd()
# print(f"Current working directory is: {cwd}")

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
import seaborn as sns

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
    # Filter serves that are out
    serve_data = serve_data[(serve_data.x >= 1.4) & (serve_data.y > 5.5)].reset_index(drop = True)
    
    return serve_data, event_data, points_data, rally_data

serve_data, event_data, points_data, rally_data = load_data()

# ==========================================================
# Data manipulation for SERVING data vis
# ==========================================================

# Filter for server, reset indexes
ND_serves = serve_data.loc[serve_data.server == 'Djokovic'].reset_index(drop = True)
RN_serves = serve_data.loc[serve_data.server == 'Nadal'].reset_index(drop = True)

# Court measurements for plot and mapping calcs
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

# Add column for serve target zones
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

# Combine dfs (ND)
backhands_ND = [backhand_left_ND, backhand_right_ND]
body_ND = [body_left_ND, body_right_ND]
forehands_ND = [forehand_left_ND, forehand_right_ND]
backhands_ND_df = pd.concat(backhands_ND)
body_ND_df = pd.concat(body_ND)
forehands_ND_df = pd.concat(forehands_ND)

# Combine dfs (RN)
backhands_RN = [backhand_left_RN, backhand_right_RN]
body_RN = [body_left_RN, body_right_RN]
forehands_RN = [forehand_left_RN, forehand_right_RN]
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

# ==========================================================
# Data manipulation for GROUNDSTROKE data vis
# ==========================================================

# Filter for players
ND_shots = event_data.loc[(event_data.hitter == 'Djokovic') & (event_data.stroke != '__undefined__')].reset_index(drop = True)
RN_shots = event_data.loc[event_data.hitter == 'Nadal'].reset_index(drop = True)

# Map groundstrokes from bottom half of court to top half
for i in range(len(ND_shots)):
    if ND_shots.hitter_y[i] < width_court/2 and ND_shots.hitter_x[i] < baseline_serviceline:
        ND_shots.hitter_x[i] = (2*baseline_serviceline - double_field) - (ND_shots.hitter_x[i] - double_field)
        ND_shots.hitter_y[i] = (width_court - baseline_serviceline) - (ND_shots.hitter_y[i] - baseline_serviceline)
    elif ND_shots.hitter_y[i] < width_court/2 and ND_shots.hitter_x[i] > baseline_serviceline:
        ND_shots.hitter_x[i] = double_field + ((2*baseline_serviceline - double_field) - ND_shots.hitter_x[i])
        ND_shots.hitter_y[i] = (width_court - baseline_serviceline) - (ND_shots.hitter_y[i] - baseline_serviceline)
for i in range(len(RN_shots)):
    if RN_shots.hitter_y[i] < width_court/2 and RN_shots.hitter_x[i] <= baseline_serviceline:
        RN_shots.hitter_x[i] = (2*baseline_serviceline - double_field) - (RN_shots.hitter_x[i] - double_field)
        RN_shots.hitter_y[i] = (width_court - baseline_serviceline) - (RN_shots.hitter_y[i] - baseline_serviceline)
    elif RN_shots.hitter_y[i] < width_court/2 and RN_shots.hitter_x[i] > baseline_serviceline:
        RN_shots.hitter_x[i] = double_field + ((2*baseline_serviceline - double_field) - RN_shots.hitter_x[i])
        RN_shots.hitter_y[i] = (width_court - baseline_serviceline) - (RN_shots.hitter_y[i] - baseline_serviceline)

ND_fh = ND_shots.loc[ND_shots.stroke == 'forehand'].reset_index(drop = True)
ND_bh = ND_shots.loc[ND_shots.stroke == 'backhand'].reset_index(drop = True)
RN_fh = RN_shots.loc[RN_shots.stroke == 'forehand'].reset_index(drop = True)
RN_bh = RN_shots.loc[RN_shots.stroke == 'backhand'].reset_index(drop = True)

# Find average coords of groundstrokes

# Average depths
ND_avg_fh_y = sum(ND_fh.hitter_y) / len(ND_fh.hitter_y)
ND_avg_bh_y = sum(ND_bh.hitter_y) / len(ND_bh.hitter_y)
RN_avg_fh_y = sum(RN_fh.hitter_y) / len(RN_fh.hitter_y)
RN_avg_bh_y = sum(RN_bh.hitter_y) / len(RN_bh.hitter_y)
plot_x = np.linspace(0, height_court)
plot_ND_fh_y = [ND_avg_fh_y]*len(plot_x)
plot_ND_bh_y = [ND_avg_bh_y]*len(plot_x)
plot_RN_fh_y = [RN_avg_fh_y]*len(plot_x)
plot_RN_bh_y = [RN_avg_bh_y]*len(plot_x)

# Average widths
ND_avg_fh_x = sum(ND_fh.hitter_x) / len(ND_fh.hitter_x)
ND_avg_bh_x = sum(ND_bh.hitter_x) / len(ND_bh.hitter_x)
RN_avg_fh_x = sum(RN_fh.hitter_x) / len(RN_fh.hitter_x)
RN_avg_bh_x = sum(RN_bh.hitter_x) / len(RN_bh.hitter_x)

# ==========================================================
# Functions for drawing court visualisations
# ==========================================================

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
    
    axes.text(10,15.5, '@datawithed', rotation = 270, color = 'white', alpha = 0.5)

    return axes

def draw_groundstrokecourt(player,width=False,depth=True,hide_axes=False):
    """Sets up field
    Returns matplotlib fig and axes objects.
    """
        
    fig = plt.figure(figsize = (height_court/2, width_court/4))
    #fig = plt.figure(figsize=(9, 9))
    fig.patch.set_facecolor('#5080B0')

    axes = fig.add_subplot(1, 1, 1, facecolor='#5080B0')

    if hide_axes:
        axes.xaxis.set_visible(False)
        axes.yaxis.set_visible(False)
        axes.axis('off')
        
    if player == 'Djokovic':
        for i in range(len(ND_fh)):
            plt.plot(ND_fh.hitter_x, ND_fh.hitter_y, 'x', color = 'red')
        for i in range(len(ND_bh)):
            plt.plot(ND_bh.hitter_x, ND_bh.hitter_y, 'x', color = 'blue')
        plt.title('Australian Open Final 2019: \n Djokovic Baseline Shot Locations',
                  fontname = 'Microsoft Sans Serif',
                  color = 'white',
                  fontsize = 16)
        if depth == True:
            plt.plot(ND_fh.hitter_x[0], ND_fh.hitter_y[0], 'x', color = 'red', label = 'Forehand')
            plt.plot(ND_bh.hitter_x[0], ND_bh.hitter_y[0], 'x', color = 'blue', label = 'Backhand')
            plt.plot(plot_x, plot_ND_fh_y, color = 'green', label = 'Average forehand contact depth')
            plt.plot(plot_x, plot_ND_bh_y, color = 'orange', label = 'Average backhand contact depth')
        if width == True:
            plt.plot(ND_fh.hitter_x[0], ND_fh.hitter_y[0], 'x', color = 'red', label = 'Forehand')
            plt.plot(ND_bh.hitter_x[0], ND_bh.hitter_y[0], 'x', color = 'blue', label = 'Backhand')
            plt.plot(ND_avg_fh_x, ND_avg_fh_y, '.', markersize = 20, color = 'green', label = 'Average forehand location')
            plt.plot(ND_avg_bh_x, ND_avg_bh_y, '.', markersize = 20, color = 'orange', label = 'Average backhand location')
        
        plt.plot()
        # set legend location and fontsize
        legend = plt.legend(loc = 'upper center', fontsize = 8)
        # Set background and frame colour of legend
        frame = legend.get_frame()
        frame.set_facecolor('white')
        frame.set_edgecolor('white')
        
    if player == 'Nadal':
        for i in range(len(RN_fh)):
            plt.plot(RN_fh.hitter_x, RN_fh.hitter_y, 'x', color = 'red')
        for i in range(len(RN_bh)):
            plt.plot(RN_bh.hitter_x, RN_bh.hitter_y, 'x', color = 'blue')
        plt.title('Australian Open Final 2019: \n Nadal Baseline Shot Locations',
                  fontname = 'Microsoft Sans Serif',
                  color = 'white',
                  fontsize = 16)
        if depth == True:
            plt.plot(RN_fh.hitter_x[0], RN_fh.hitter_y[0], 'x', color = 'red', label = 'Forehand')
            plt.plot(RN_bh.hitter_x[0], RN_bh.hitter_y[0], 'x', color = 'blue', label = 'Backhand')
            plt.plot(plot_x, plot_RN_fh_y, color = 'green', label = 'Average forehand contact depth', alpha = 0.5)
            plt.plot(plot_x, plot_RN_bh_y, color = 'orange', label = 'Average backhand contact depth', alpha = 0.5)
        if width == True:
            plt.plot(RN_fh.hitter_x[0], RN_fh.hitter_y[0], 'x', color = 'red', label = 'Forehand')
            plt.plot(RN_bh.hitter_x[0], RN_bh.hitter_y[0], 'x', color = 'blue', label = 'Backhand')
            plt.plot(RN_avg_fh_x, RN_avg_fh_y, '.', markersize = 20, color = 'green', label = 'Average forehand location')
            plt.plot(RN_avg_bh_x, RN_avg_bh_y, '.', markersize = 20, color = 'orange', label = 'Average backhand location')
        
        # set legend location and fontsize
        legend = plt.legend(loc = 'upper center', fontsize = 8)
        # Set background and frame colour of legend
        frame = legend.get_frame()
        frame.set_facecolor('white')
        frame.set_edgecolor('white')

    axes = draw_groundpatches(axes)
    
    return fig, axes

def draw_groundpatches(axes):
    plt.xlim([-3, 14])
    plt.ylim([width_court/2, width_court + 9])
    
    #net
    axes.add_line(plt.Line2D([height_court, 0],[width_court/2, width_court/2], c = 'w'))
    
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
    axes.add_line(plt.Line2D([height_court / 2, height_court / 2], [width_court/2 - service_box, width_court / 2 + service_box], c = 'w'))
    
    axes.add_line(plt.Line2D([height_court / 2, height_court / 2], [0, 0 + 0.45], c = 'w'))

    axes.add_line(plt.Line2D([height_court / 2, height_court / 2], [width_court, width_court - 0.45], c = 'w'))
    
    axes.add_line(plt.Line2D([1.37, 1.37], [0, width_court], c = 'w'))
    
    axes.add_line(plt.Line2D( [height_court - 1.37, height_court - 1.37], [0, width_court], c = 'w'))
    
    axes.text(10,15.5, '@datawithed', rotation = 270, color = 'white', alpha = 0.5)

    return axes


# Filter data for returns only
returns = event_data.loc[(event_data.strokeid == 2) & (event_data.isserve == False)].reset_index(drop=True)

# Map all shots to top half of court
for i in range(len(returns)):
    if returns.hitter_y[i] < width_court/2 and returns.hitter_x[i] < baseline_serviceline:
        returns.hitter_x[i] = (2*baseline_serviceline - double_field) - (returns.hitter_x[i] - double_field)
        returns.hitter_y[i] = (width_court - baseline_serviceline) - (returns.hitter_y[i] - baseline_serviceline)
    elif returns.hitter_y[i] < width_court/2 and returns.hitter_x[i] > baseline_serviceline:
        returns.hitter_x[i] = double_field + ((2*baseline_serviceline - double_field) - returns.hitter_x[i])
        returns.hitter_y[i] = (width_court - baseline_serviceline) - (returns.hitter_y[i] - baseline_serviceline)

# Filter by player
ND_returns = returns.loc[returns.hitter == 'Djokovic'].reset_index(drop = True)
RN_returns = returns.loc[(returns.hitter == 'Nadal') & (returns.hitter_y > 18.5)].reset_index(drop = True)

# Create function for heatmap return plot
def draw_returncourt(player, hide_axes = False):
    """Sets up field
    Returns matplotlib fig and axes objects.
    """
    fig = plt.figure(figsize = (height_court/2, width_court/4))
    #fig = plt.figure(figsize=(9, 9))
    fig.patch.set_facecolor('#5080B0')

    axes = fig.add_subplot(1, 1, 1, facecolor = '#5080B0')

    if hide_axes:
        axes.xaxis.set_visible(False)
        axes.yaxis.set_visible(False)
        axes.axis('off')
        
    if player == 'Djokovic':
        sns.kdeplot(ND_returns.hitter_x, ND_returns.hitter_y, shade = 'True', color = 'black', n_levels = 25, alpha = 0.75, zorder = 1)
        plt.ylim(width_court/2, width_court + 5)
        plt.axis('off')
        plt.title('Australian Open Final 2019: \nDjokovic serve return heatmap',
                  fontname = 'Microsoft Sans Serif',
                  color = 'white',
                  fontsize = 16)
        plt.plot()
        
    if player == 'Nadal':
        sns.kdeplot(RN_returns.hitter_x, RN_returns.hitter_y, color = '#E3783B', shade = 'True', n_levels = 25, alpha = 0.75, zorder = 1)
        plt.ylim(width_court/2,width_court + 5)
        plt.axis('off')
        plt.title('Australian Open Final 2019: \nNadal serve return heatmap',
                  fontname = 'Microsoft Sans Serif',
                  color = 'white',
                  fontsize = 16)

    axes = draw_returnpatches(axes)
    
    return fig, axes

def draw_returnpatches(axes):
    plt.xlim([-5.5, 16.5])
    plt.ylim([width_court/2, width_court + 5.5])
    
    #net
    axes.add_line(plt.Line2D([height_court, 0],[width_court/2, width_court/2], c = 'w')).set_zorder(-1)
    
    # court outline
    y = 0
    dy = width_court
    x = 0 # height_court - double_field
    dx = height_court
    axes.add_patch(plt.Rectangle((x, y), dx, dy, edgecolor = "white", facecolor = "#5581A6", alpha = 1)).set_zorder(-1)
    # serving rect
    y = baseline_serviceline
    dy = serviceline_net * 2
    x = 0 + double_field 
    dx = breite_einzel
    axes.add_patch(plt.Rectangle((x, y), dx, dy, edgecolor = "white", facecolor = "none", alpha = 1)).set_zorder(-1)
    
    #net
    axes.add_line(plt.Line2D([height_court / 2, height_court / 2], [width_court/2 - service_box, width_court / 2 + service_box], c = 'w')).set_zorder(-1)
    
    axes.add_line(plt.Line2D([height_court / 2, height_court / 2], [0, 0 + 0.45], c = 'w')).set_zorder(-1)

    axes.add_line(plt.Line2D([height_court / 2, height_court / 2], [width_court, width_court - 0.45], c = 'w')).set_zorder(-1)
    
    axes.add_line(plt.Line2D([1.37, 1.37], [0, width_court], c = 'w')).set_zorder(-1)
    
    axes.add_line(plt.Line2D([height_court - 1.37, height_court - 1.37], [0, width_court], c = 'w')).set_zorder(-1)
    
    axes.text(9.9, 15.5, '@datawithed', rotation = 270, color = 'white', alpha = 0.5)

    return axes


# ==========================================================
# Save plots as images for use
# ==========================================================
#draw_halfcourt('Djokovic', hide_axes = True)
#plt.savefig("ND serve plot.jpg", dpi = 750)
#draw_halfcourt('Nadal', hide_axes = True)
#plt.savefig('RN serve plot.jpg', dpi = 750)

#draw_returncourt('Djokovic')
#plt.savefig("ND return heatmap plot.jpg", dpi = 750)
#draw_returncourt('Nadal')
#plt.savefig("RN return heatmap plot.jpg", dpi = 750)

#draw_groundstrokecourt('Djokovic', width = True, depth = False, hide_axes = True)
#plt.savefig("ND baseline width plot.jpg", dpi = 750)
#draw_groundstrokecourt('Djokovic', width = False, depth = True, hide_axes = True)
#plt.savefig("ND baseline depth plot.jpg", dpi = 750)
#draw_groundstrokecourt('Nadal', width = True, depth = False, hide_axes = True)
#plt.savefig("RN baseline width plot.jpg", dpi = 750)
#draw_groundstrokecourt('Nadal', width = False, depth = True, hide_axes = True)
#plt.savefig("RN baseline depth plot.jpg", dpi = 750)

ND_serve_plot = Image.open('ND serve plot.jpg')
RN_serve_plot = Image.open('RN serve plot.jpg')

ND_baseline_width_plot = Image.open('ND baseline width plot.jpg')
ND_baseline_depth_plot = Image.open('ND baseline depth plot.jpg')
RN_baseline_depth_plot = Image.open('RN baseline depth plot.jpg')
RN_baseline_width_plot = Image.open('RN baseline width plot.jpg')

ND_return_plot = Image.open('ND return heatmap plot.jpg')
RN_return_plot = Image.open('RN return heatmap plot.jpg')


# ==========================================================
# Dashboard configuration
# ==========================================================

# Create multiple page dashboard with sidebar + selectbox
add_sidebar = st.sidebar.selectbox('Select Page', ('Home','Match Summary','Baseline Analysis','Serve Analysis','Return Analysis'))

# Home page content
if add_sidebar == 'Home':
    t1, t2 = st.columns([2,10])
    t1.image('AO_logo.jpg')
    t2.header("""
              Australian Open 2019 Final Analysis 
              \n By Ed Morris
              \n 08/06/2022
              """)
    t2.markdown(""" **Twitter:** @datawithed 
                \n **Instagram:** @data_with_ed
                """)
    st.markdown("""
                **Navgating the dashboard:** 
                \n- Use the arrow in the top left to open the sidebar
                \n- Select a page from the drop-down bar to move between analyses    
                """)
    st.markdown("""
                **Context:**
                """)
    st.markdown("Set up to be another classic Grand Slam final in Melbourne, Novak Djokovic was coming off the back of a fantastic 2018 season. The current holder of the previous two Slams, the current world number 1 and 6x Australian Open champion, the numbers seemed to be stacked in Novak's favour. However what no one anticipated was the manner in which he would go about claiming his 7th title in the Rod Laver arena.")
    st.markdown("Nadal, hitting a scintillating run of form in the tournament in his route to the final, hadn't dropped a single set and looked far and away the most likely candidate to cause an upset Down Under. He had spent significantly less time on court than Djokovic in his previous rounds, not letting his ankle surgery before the tournament hinder his play.")
    st.markdown('This dashboard will attempt to delve into some of the key stats, visualising where this tie was won and lost by both players.')
    st.header('Historic Head-to-Head: Djokovic vs Nadal')
    h1, h2, h3, h4, h5 = st.columns(5)
    h1.metric(label = 'H2H record (at 25/01/2019)', value = "27-25")
    h2.metric(label = 'Record in finals (at 25/01/2019)', value = "14-10")
    h3.metric(label = 'Grand Slam record (at 25/01/2019)', value = "5-9")
    h4.metric(label = 'Grand Slam Final record (at 25/01/2019)', value = "3-4")
    h5.metric(label = 'H2H record @ Aus Open (at 25/01/2019)', value = "1-0")

# Match Summary tab content
if add_sidebar == 'Match Summary':
    st.title('Match Summary Statistics')
    a1, a2 = st.columns(2)
    points_won = points_data[['rallyid','winner']].groupby('winner').count()
    points_won['winner'] = points_won.index
    fig = px.bar(points_won, x = 'winner', y = 'rallyid', title = 'Figure 1: Total points won by each player',height = 450)
    fig.update_layout(xaxis_title = 'Winner', yaxis_title = 'Points')
    a1.plotly_chart(fig)
    
    point_end = points_data.groupby('reason')['winner'].value_counts()
    point_end = point_end.rename('total')
    point_end = point_end.reset_index()
    fig = px.bar(point_end, x = 'reason', y = 'total', color = 'winner', barmode = 'group')
    fig.update_layout(xaxis_title = 'Point won via', yaxis_title = 'Points won', title = 'Figure 2: Points won breakdown')
    a2.plotly_chart(fig)
    st.markdown('A high-level view of the match from Figure 1 and 2 above shows that Djokovic dominated in all key areas of the match.')
    i1, i2 = st.columns(2)
    i1.header("Djokovic stats")
    i1.metric(label = '1st serve %', value = f"{0.725:.0%}", delta = f"{0.725-0.649:.0%} compared to career", delta_color = 'normal')
    i1.metric(label = 'Break Points saved %', value = f"{1:.0%}", delta = f"{1-0.655:.0%} compared to career", delta_color = 'normal')
    i1.metric(label = 'Forehand winners', value = f"{13}")
    i1.metric(label = 'Backhand winners', value = f"{12}")
    i1.metric(label = 'Aces', value = f"{8}")
    i2.header('Nadal stats')
    i2.metric(label = '1st serve %', value = f"{0.644:.0%}", delta = f"{0.644-0.681:.0%} compared to career", delta_color = 'normal')
    i2.metric(label = 'Break Points saved %', value = f"{0.375:.0%}", delta = f"{0.375-0.663:.0%} compared to career", delta_color = 'normal')
    i2.metric(label = 'Forehand winners', value = f"{4}")
    i2.metric(label = 'Backhand winners', value = f"{5}")
    i2.metric(label = 'Aces', value = f"{3}")
    

if add_sidebar == 'Baseline Analysis':
    st.title('Baseline/Groundstroke Analysis')
    players1 = tuple(event_data['hitter'].unique())
    players1_select = st.selectbox('Select a player',(players1))
    
    if players1_select == 'Djokovic':
        st.header('Depth analysis')
        e1, e2 = st.columns(2)
        e1.image(ND_baseline_depth_plot)
        e2.markdown("""
                    - Firstly, the difference in average depth of forehands versus backhands is apparent. Since the backhand is typically targeted in tennis, Novak's counter to this has been to take the backhand on the rise and early in the court. 
    \n- He has employed this well against Nadal previously, driving the backhand cross-court flat and deep into the Spaniard's forehand
                    \n There are a number of advantages for taking the backhand early: 
1. It takes time away from the opponent to recover positionally from the previous shot, leaving more space open to attack 
2. It allows you to dictate the rally on both forehand and backhand side - stepping into the court gives you more angles of the court to use and allows you to play more aggressively
    
However, this strategy is high risk. Taking the ball so early in the court means the ball will likely always be on the rise, which is always harder to time than stepping back and hitting the ball as it falls.
    \n Secondly, the average depth of the forehands is deeper than the backhands. Intuitively, one would expect the forehand depth to be higher up the court, as this is typically the player's stronger shot and one which tends to be used more aggressively. This can be explained by:
- On Nadal's width analysis, we can see the average backhand was played from much wider than his forehand
- This is because Djokovic's topspin forehand is hit with more RPM than his backhand, allowing him to create greater angles cross-court
- To utilise a topspin-heavy forehand, this is best attempted when the ball is falling rather than rising, hence the forehand is hit from deeper in the court on average than the backhand
                    """)
        st.header('Width analysis')
        g1, g2 = st.columns(2)
        g1.image(ND_baseline_width_plot)
        g2.markdown("""
                    It's clear to see that Djokovic's backhand is not only hit higher up into the court, but further wide than his forehand on the opposite side of the court. This can be attributed to Nadal's angle creation on his cross-court forehand - he can generate very high RPM (see below) allowing him to get the ball up over the net and back down into the court at tighter angles.
                    \n From this diagram it is clear to see that Nadal aimed to utilise this weapon in order to both: 
- Draw Djokovic wide on the cross-court to open up spaces elsewhere in the court
- Force Djokovic to either concede ground and hit the ball on the defensive, or take a difficult rising backhand
                    \n It's also noticeable how central the average location of Djokovic's forehands are, only just into the deuce side of the court. 
        \n- However, before reading too much into this it is important to add some context to the forehand data - since players often run around their backhands to hit a forehand, there will inevitably be a more centralised bias when calculating the average forehand location, so it is important not to base any conclusions from this data without first considering the context.
                    \n Given Nadal's strongest shots are his cross-court forehand and strategic use of his inside-out forehand, these were going to be crucial to his match strategy. Djokovic was able to nullify the cross-court forehands by stepping into the court and taking his backhands early, and Nadal couldn't create any consistent width with his backhands/inside-out forehands to stretch the Djokovic forehand.
                    """)

        st.markdown("Event level data from: https://www.kaggle.com/code/robseidl/australian-open-mens-final-2019-data-exploration/data")
    
    if players1_select == 'Nadal':
        st.header('Depth analysis')
        f1, f2 = st.columns(2)
        f1.image(RN_baseline_depth_plot)
        f2.markdown("""
                    - Interestingly, Nadal's forehand and backhand contact points have almost identical average depths throughout the match. 
                    \n- Nadal has a greater vertical spread, having more short balls inside the court but also more balls deep behind the baseline (often associated with passive/defensive play)
                    \n- Typically, Djokovic tries to dominate rallies by pushing Nadal deep behind the baseline, then mixing up the play by hitting drop shots to disrupt his rhythm. 
        \n- This has the added bonus of bringing Nadal to the net, and whilst he isn't a poor volleyer, it's definitely not his preferred area of the court. 
\n- The drop shot is typically played when Nadal leaves a short ball on Djokovic's backhand - where he hits a short backhand slice down the line (as seen by the short balls in the service box)
                    \n- This exhibit shows that Djokovic hit his backhand higher up the court, using a flat grip to drill the backhand deep to push Nadal back, whilst using the topspin forehand to create angles off-court. This is shown as the spread of forehands (red) is more vertical than the spread of backhands (blue).
                    \n- In addition to this, Djokovic avoided opening the court on Nadal's forehand which would have helped him create more angles with his forehand. We can see, Nadal's forehands are spread more vertically than wide - again worth noting the forehands have a centralised bias due to inside-out/in shots.
                    \n In conclusion, Djokovic worked Nadal vertically up and down the court throughout the match, not allowing the Spaniard to get into a comfortable rhythm at the baseline and using the backhand to drive Nadal deep behind the baseline, creating opportunities for the drop shot.
                    """)
        
        st.header('Width analysis')
        f1, f2 = st.columns(2)
        f1.image(RN_baseline_width_plot)
        f2.markdown("""
                    - This exhibit shows Nadal's average backhands were being hit from a wider position than his forehand. 
                    \n- The width analyses for both players have shown that they have applied the typical left-hander vs right-hander strategy; attacking the backhand with their forehand to open up the court with angles and draw a short ball. 
                    \n- Djokovic executed a well planned trade-off on his bcross-court backhand; to hit deeper and more centrally rather than creating an angle to pull Nadal off-court. This lowered the margin for error that had significantly increased by taking the backhand on the rise, whilst simultaneously reducing the angles that Nadal could create on his forehand. 
                    \n- This can easily be seen in the exhibit as Nadal only hit one forehand wide of the outer tramline. 
                    \n- Djokovic managed to generate great angles on his cross-court forehand, working Nadal wide of the tramlines frequently on his backhand as seen in the exhibit.
                    \n- Once again (particularly when considering Nadal and his fondness of running around his backhand to hit a forehand), we must remember that the average forehand location has a centralised bias. In particular, we can see a high concentration of forehands hit on the left-hand side and behind the centre of the court. The high concentration around the centre of the court agrees with our Djokovic hypothesis, where he has attempted to minimise the angles he concedes to the Nadal forehand by hitting centrally to this wing. This prevents Nadal from opening up the court as effectively as he would like, giving Djokovic more time to stabilise and pick his shots more effectively.
                    """)
        st.markdown("Event level data from: https://www.kaggle.com/code/robseidl/australian-open-mens-final-2019-data-exploration/data")
    
    st.header('Historic forehand analysis')
    b1, b2 = st.columns([2,2])
    b1.image(Image.open('Forehand trajectory comparison.jpg'))
    b2.markdown("""
                Although nearly a decade old it's clear to see Nadal's superior net clearance, topspin RPM and bounce height compared to the rest of the Big 4. The average net clearance statistic here in particular demonstrating that Rafa doesn't often hit the net compared to his peers, an element which almost certainly played a part in his undoing here. 
                \n This stat also shows us his relative ease at creating depth on his forehands, pushing opponents back and making them play more defensively; when combined with an insanely high average RPM and bounce height on these forehands this means that opponents are left with two choices:
                
1. Get bullied deep behind the baseline, playing shots outside their comfortable hitting zone, or             
2. Try to take their shots on the rise or even on the half volley which is difficult even for the pros
                """)
    
# Serve analysis tab content
if add_sidebar == 'Serve Analysis':
    st.title('Serve Analysis')
    players = tuple(serve_data['server'].unique())
    players_select = st.selectbox('Select a player',(players))
    
    if players_select == 'Djokovic':
        col1, col2, col3, col4, col5, col6 = st.columns((1,1,1,1,1,1))
        col1.metric(label = '1st serve %', value = f"{0.725:.0%}", delta = f"{0.725-0.649:.0%} compared to career", delta_color = 'normal')
        col2.metric(label = '1st serve % won', value = f"{0.8:.0%}", delta = f"{0.8-0.737:.0%} compared to career", delta_color = 'normal')
        col6.metric(label = 'Aces', value = f"{8}")
        col3.metric(label = '2nd serve % won', value = f"{0.842:.0%}", delta = f"{0.842-0.554:.0%} compared to career", delta_color = 'normal')
        col4.metric(label = 'Break Points saved %', value = f"{1:.0%}", delta = f"{1-0.655:.0%} compared to career", delta_color = 'normal')
        col5.metric(label = 'Service games won %', value = f"{1:.0%}", delta = f"{1-0.858:.0%} compared to career", delta_color = 'normal')
        col13, col14 = st.columns(2)
        col13.image(ND_serve_plot, use_column_width = True)
        col14.markdown("""
                       This exhibit further shows how Djokovic looked to restrict the Nadal forehand angles, by hitting a higher percentage of serves at the forehand on the deuce court (down the T) and the Nadal backhand on the advantage court (down the T also). 
                       \n Whilst he applied this strategy, he wasn't afraid to open the court up a bit more frequently on the deuce court, still employing a wide slice serve to the Nadal backhand to both keep Nadal guessing and attempt to open up the court just like with Djokovic's forehand.
                       \n The body serve was only employed sporadically by Novak, which isn't surprising as the body serve doesn't generate the same gains as serving to either corner of the service box does in a singles match. If this was a doubles match, we might have seen a higher percentage of first serves targetting the body; this tactic usually offers up a "chipped" return which is easier to follow up with a volley, the trade-off being that the opponent will rarely be aced.
                       \n Finally, we see that Djokovic wasn't pushing his serve to the limit very often since the serves (especially in the advantage court) are comfortably inside the lines. If Djokovic was pushing hard on his serve, we would have seen:
1. A lower first serve percentage
2. Serves much closer to the service line
                        \n In addition to the above, Djokovic was able to maintain a very respectable 1st serve percentage and winning 80% of all points he started with a first serve. He outperformed his career average in both these areas significantly on the day, making it hard for Nadal to get a foothold in the rallies by consistently having to return 1st serves. This dominant serving performance resulted in Novak seeing out all his service games as the victor, a remarkable feat against not only one of his fiercest rivals, but one of the greatest players of all time.
                       """)
        st.markdown("Match data from: https://www.ultimatetennisstatistics.com/playerProfile?playerId=4920&tab=matches#matchStats-173429Serve")
        st.markdown("Event level data from: https://www.kaggle.com/code/robseidl/australian-open-mens-final-2019-data-exploration/data")
     
    elif players_select == 'Nadal':
        rn_col1, rn_col2, rn_col3, rn_col4, rn_col5, rn_col6 = st.columns((1,1,1,1,1,1))
        rn_col1.metric(label = '1st serve %', value = f"{0.644:.0%}", delta = f"{0.644-0.681:.0%} compared to career", delta_color = 'normal')
        rn_col2.metric(label = '1st serve % won', value = f"{0.511:.0%}", delta = f"{0.511-0.722:.0%} compared to career", delta_color = 'normal')
        rn_col3.metric(label = '2nd serve % won', value = f"{0.615:.0%}", delta = f"{0.615-0.573:.0%} compared to career", delta_color = 'normal')
        rn_col4.metric(label = 'Break Points saved %', value = f"{0.375:.0%}", delta = f"{0.375-0.663:.0%} compared to career", delta_color = 'normal')
        rn_col5.metric(label = 'Service games won %', value = f"{0.615:.0%}", delta = f"{0.615-0.858:.0%} compared to career", delta_color = 'normal')
        rn_col6.metric(label = 'Aces', value = f"{3}")
        col11, col12 = st.columns(2)
        col11.image(RN_serve_plot, use_column_width = True)
        col12.markdown("""
                       Interestingly, a few parallels can be drawn between the two players' serving; they employed a similar strategy on serve, by hitting a high percentage of serves down the T on both sides of the court to reduce angle creation (particularly on the deuce court from Nadal), but not being afraid to hit a slice serve out wide on the advantage court into the Djokovic backhand, opening the court up.
                       \n One of the first things we can see after looking at the Djokovic serving exhibit is the absolute number of first serves Nadal has hit compared to Djokovic; the exhibit for Nadal is much more densely populated than Djokovic's, from which we can easily infer that Nadal had to play many more points on his service games, hence the higher number of first serves plotted. Djokovic is widely regarded as one of the best returners on the tour, and he caused Nadal plenty of problems on his service games early on and was relentless throughout the match.
                       \n On the deuce court, Nadal hit few first serves to the Djokovic forehand, trying to reduce the angle of return and hit to the weaker backhand side. He hit a high percentage of serves on this side to the body/backhand. 
                       \n As hypothesised in the Djokovic serve analysis, it isn't an orthodox singles tactic to hit frequent body serves (with the exception of big servers, Karlovic, Isner etc.), since a higher proportion of serves will be returned from this area. There are a few theories that could explain this relatively even distribution of body and backhand serves:
- Nadal was struggling to generate enough slice on his serves to pull them down the T and into the backhand side
- This was purposeful in order to prevent the serves from becoming predictable, whilst preventing Djokovic from getting returns on his favoured forehand angle
                        \n On the advantage court, Nadal hit a much more even distribution of serves. Keeping true to targetting the middle of the court, a solid number of sevres were hit down the T. However, Nadal was much happier targetting the wide serve on this side of the court and accepting the trade-off between angle exposure and open court creation as a result.
                       """)
        st.markdown("Match data from: https://www.ultimatetennisstatistics.com/playerProfile?playerId=4920&tab=matches#matchStats-173429Serve")
        st.markdown("Event level data from: https://www.kaggle.com/code/robseidl/australian-open-mens-final-2019-data-exploration/data")

        
# Return analysis tab content
## Heatmap of return positions
## Average depth of return
if add_sidebar == 'Return Analysis':
    st.title('Return Analysis')
    players = tuple(serve_data['server'].unique())
    players_select = st.selectbox('Select a player',(players))
    if players_select == 'Djokovic':
        col100, col101 = st.columns(2)
        col100.image(ND_return_plot, caption = 'Djokovic heatmap of return positions', use_column_width = True)
        col101.markdown("""
                        This heatmap allows us to see the key positions both players were taking when returning serve. This not only allows us to analyse where they were having to make shots from, but also shows us which side the server was attempting to attack when starting out the point.
- We can see a strong concentration of returns on the deuce court across the middle of the returner and towards the middle of the court, which aligns with the serve analysis for Nadal showing a high percentage of first serves directed at the body/down the T to the backhand on the deuce court.
                        \n This concentration spreads slowly across to the advantage court, but is more even across the T and wide serves. The main difference on the advantage court is the concentration of returns on the Djokovic backhand - the concentration on this side of the court is shifted up into the court. As hypothesised in the prior analyses, Djokovic was clearly taking his backhand returns out wide higher up in the court. This prevents Nadal from creating his intended angle to open up space on the deuce court and also takes time away from Nadal to recover from his service action.
                        \n Since Nadal is left handed, naturally Djokovic didn't have to return forehands from very wide on the deuce court, but had to deal with backhands further wide of the tramlines on the advantage court. We would expect to see a similar but opposite pattern on the Nadal return heatmap.
                        \n In retrospect, Nadal would probably have hoped to create more trouble for Djokovic on the deuce court with his serves; the highest concentration is within easy reach of the returner, while perhaps aiming to force chipped returns for easy follow up shots, it means that Nadal will not have generated many 'free' points from his service on the deuce court ('free' meaning aces, forced errors, or creation of short returns for easy winners on the 2nd shot).
                        \n The spread of the heatmap vertically is much narrower on Djokovic's returns than Nadal's. From this it is clear that Djokovic was attempting to be more aggressive on his returns by taking them further up the court. When compared to Nadal's heatmap, he was opting to return from much deeper behind the baseline at times, as the spread of the heatmap pushes out very far back.
                        \n Finally, the heatmap spills high into the court with a particular concentration into the right tramline. Nadal was attempting to utilise his wide serve on the advantage court, and to counter this we can see Djokovic taking an uber-aggressive returning approach, meeting these serves early and high into the court to mitigate the effect of being pulled off the court whilst giving Nadal less time to set up for his second shot.
                        """)
        
    if players_select == 'Nadal':
        col102, col103 = st.columns(2)
        col102.image(RN_return_plot, caption = 'Nadal heatmap of return positions', use_column_width = True)
        col103.markdown("""
                        This heatmap allows us to see the key positions both players were taking when returning serve. This not only allows us to analyse where they were having to make shots from, but also shows us which side the server was attempting to attack when starting out the point.
                        \n This heatmap raises an important point to note when comparing these plots against the serve analysis plots earlier - whilst we noted that Djokovic did use this wide serve to the Nadal backhand, it was not nearly as frequent as the T serve to the forehand. These plots won't always align, since the serve analysis was only considering the first serves of each player and doesn't show any information about the second serves. Typically players will attempt to hit serves to the opponent's weaker shot, usually the backhand side. This would appear to be true in this case, as there is a very dense concentration of returns hit from the backhand side even though the number of first serves hit to this area wasn't particularly frequent.
                        \n There are three key areas of interest from this heatmap:
1. The high concentration of returns above the right tramline (Nadal backhand side)
2. The medium concentration of returns centrally, but deep behind the baseline
3. The other medium concentration of returns centrally, but just on the baseline
                        \n Firstly, let's look at the first area. It is very clear that the majority of returns were being hit from this location, as a result of Djokovic's wide serve on the deuce court. The high concentration indicates high frequency, which would explain how Nadal managed to consistently return from not far behind the baseline on this side. Djokovic clearly believed the effectiveness of hitting this serve outweighed how easy it became to anticipate this serve.
                        \n The second area complements this, as Nadal was often expecting the wide serve on the deuce court, when Djokovic did decide to hit a T serve into the Nadal forehand Nadal needed more time to adjust to respond, hence taking his forehand returns on the deuce court from a much deeper position on court. To ensure Nadal didn't get too comfortable in antici[ating the backhand return, mixing up the serve down the T was clearly working to good effect.
                        \n Finally, the third area. This one mirrors the first area in some ways, as Nadal was receiving this serve to his backhand which Djokovic was targetting on both sides of the court with his serve. Nadal again was able to predict the serve to the backhand more confidently/frequently hence could take the returns on this wing earlier/more aggressively. As we saw on the Djokovic 1st serve analysis, he rarely served out wide to the Nadal forehand and looking at where the heatmap ends horizontally on the advantage court, it's clear he wasn't putting many second serves out here either.
                        """)
