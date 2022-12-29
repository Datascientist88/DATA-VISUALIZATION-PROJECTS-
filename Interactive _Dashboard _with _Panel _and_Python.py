#!/usr/bin/env python
# coding: utf-8

# # INTERACTIVE DASHBOARD WITH PANEL & PYTHON 

# -Panel is an interactive data visualization library which is part of big array of libraries known as holoviews , it offers python developers the ability to design interactive dashboards through the wigdets which make the visualizations dynamic , and the web applications can be hosted online 

# ## import required libraries for data manipulation and visualization

# In[1]:


import numpy as np
import pandas as pd
from matplotlib.figure import Figure
import panel as pn 
pn.extension()
import hvplot .pandas 


# ### read the data 

# In[2]:


data_url = "https://cdn.jsdelivr.net/gh/holoviz/panel@master/examples/assets/occupancy.csv"
data = pd.read_csv(data_url, parse_dates=["date"]).set_index("date")


# ## choosing the Custom colours 

# In[4]:


primary_color = "#0072B5"
secondary_color = "#94EA84"


# ### Plot with Matplotlib using the artistic layer

# In[5]:


# Define ploting function 
def mpl_plot(avg, highlight):
    fig = Figure(figsize=(10,5))
    ax = fig.add_subplot()
    avg.plot(ax=ax, c=primary_color)
    if len(highlight):
        highlight.plot(style="o", ax=ax, c=secondary_color)
    return fig


# In[6]:


# Identify the outliers 
def find_outliers(variable="Temperature", window=20, sigma=10, view_fn=mpl_plot):
    avg = data[variable].rolling(window=window).mean()
    residual = data[variable] - avg
    std = residual.rolling(window=window).std()
    outliers = np.abs(residual) > std * sigma
    return view_fn(avg, avg[outliers])


# In[7]:


pn.extension(sizing_mode="stretch_width", template="fast")


# ## Define the Markdown and Create the Widgets 

# In[8]:


# Define labels and widgets
pn.pane.Markdown("Variable").servable(area="sidebar")
variable = pn.widgets.RadioBoxGroup(
    name="Variable", value="Temperature", options=list(data.columns), margin=(-10, 5, 10, 10)
).servable(area="sidebar")
window = pn.widgets.IntSlider(name="Window", value=20, start=1, end=60).servable(area="sidebar")


# ## Convert the function to interactive one 

# In[9]:


ifind_outliers = pn.bind(find_outliers, variable, window, 10)

# Layout the interactive functions
pn.panel(ifind_outliers, sizing_mode="scale_both").servable()


# In[11]:


variable


# In[ ]:




