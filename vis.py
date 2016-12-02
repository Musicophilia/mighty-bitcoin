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
from optimizer import *

max_btc_f_stolen = 0.001
max_btc_f_owned_0 = 0.5
max_mining_power = 0.5
max_days = 20


def get_util_vs_time_data(days=[0], mining_power=0.2, discount_rate=1.0, btc_f_stolen=0.0, btc_f_owned_0=0.0):
    _, _, attack_utilities = optimal_attack_utility(btc_f_stolen = btc_f_stolen,
                                                    btc_f_owned_0 = btc_f_owned_0,
                                                    mining_power = mining_power,
                                                    discount_rate = discount_rate,
                                                    num_days = max(days) + 1)
    return [attack_utilities[d] for d in days]

# Set up data
x = np.arange(0, max_days, 1) # times
y = get_util_vs_time_data(days=x)
source = ColumnDataSource(data=dict(x=x, y=y))


# Set up plot
plot = figure(plot_height=400, plot_width=400, title="mighty bitcoin",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, max_days])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)


# Set up widgets
text = TextInput(title="Title", value='mighty bitcoin')
mining_power = Slider(title="Mining Power", start=0.0, end=max_mining_power, value=0.2, step=max_mining_power/200)
discount_rate = Slider(title="Discount Rate", start=0.99, end=1.0, value=1.0, step=0.0001)
btc_f_stolen = Slider(title="BTC Fraction Stolen", start=0.0, end=max_btc_f_stolen, value=0.00, step=max_btc_f_stolen/200)
btc_f_owned_0 = Slider(title="BTC Fraction Owned At Time 0", start=0.0, end=max_btc_f_owned_0, value=0.0, step=max_btc_f_owned_0/200)

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
    y = get_util_vs_time_data(days=x, mining_power=alpha, discount_rate=gamma, btc_f_stolen=stolen, btc_f_owned_0=owned)

    source.data = dict(x=x, y=y)

def update_default(attrname, old, new):
    update_data()
    
def update_slider_stolen(attrname, old, new):
    owned = btc_f_owned_0.value
    btc_f_stolen.end = min(1.0 - owned, max_btc_f_stolen)
    update_data()
    
def update_slider_owned(attrname, old, new):
    stolen = btc_f_stolen.value
    btc_f_owned_0.end = min(1.0 - stolen, max_btc_f_owned_0)
    update_data()


for w in [mining_power, discount_rate]:
    w.on_change('value', update_default)

btc_f_owned_0.on_change('value', update_slider_stolen)
btc_f_stolen.on_change('value', update_slider_owned)


# Set up layouts and add to document
inputs = widgetbox(text, mining_power, discount_rate, btc_f_owned_0, btc_f_stolen)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"
