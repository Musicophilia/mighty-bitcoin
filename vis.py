''' 
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve --show vis.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/vis
in your browser.
'''
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure

from models import *

def get_util_vs_time_data(times, mining_power=0.2, discount_rate=1.0, btc_f_stolen=0.05, btc_f_owned_0=0.10):
    vals = []
    for t in times:
        model = utility_model(attack_time=t, mining_power=mining_power, discount_rate=discount_rate, btc_f_stolen=btc_f_stolen, btc_f_owned_0=btc_f_owned_0)
        val = model.compute_attack_utility()
        vals.append(val)
    return vals

# Set up data
x = np.arange(0, 30, 1) # times
y = get_util_vs_time_data(x)
source = ColumnDataSource(data=dict(x=x, y=y))


# Set up plot
plot = figure(plot_height=400, plot_width=400, title="mighty bitcoin",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, 30])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)


# Set up widgets
text = TextInput(title="Title", value='mighty bitcoin')
offset = Slider(title="Offset", start=-5e+8, end=5e+8, value=0, step=1e+8)
mining_power = Slider(title="Mining Power", start=0.0, end=1.0, value=0.2, step=0.05)
discount_rate = Slider(title="Discount Rate", start=0.0, end=1.0, value=1.0, step=0.05)
btc_f_stolen = Slider(title="BTF Fraction Stolen", start=0.0, end=1.0, value=0.00, step=0.01)
btc_f_owned_0 = Slider(title="BTF Fraction Owned At Time 0", start=0.0, end=1.0, value=0.00, step=0.01)

# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)

def update_data():

    # Get the current slider values
    alpha = mining_power.value
    gamma = discount_rate.value
    owned = btc_f_owned_0.value
    stolen = btc_f_stolen.value

    # Generate the new curve
    y = get_util_vs_time_data(x, mining_power=alpha, discount_rate=gamma, btc_f_stolen=stolen, btc_f_owned_0=owned)

    source.data = dict(x=x, y=y)

def update_default(attrname, old, new):
    update_data()
    
def update_slider_stolen(attrname, old, new):
    owned = btc_f_owned_0.value
    btc_f_stolen.end = 1.0 - owned
    update_data()
    
def update_slider_owned(attrname, old, new):
    stolen = btc_f_stolen.value
    btc_f_owned_0.end = 1.0 - stolen
    update_data()


for w in [offset, mining_power, discount_rate]:
    w.on_change('value', update_default)

btc_f_owned_0.on_change('value', update_slider_stolen)
btc_f_stolen.on_change('value', update_slider_owned)


# Set up layouts and add to document
inputs = widgetbox(text, mining_power, discount_rate, btc_f_owned_0, btc_f_stolen)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"