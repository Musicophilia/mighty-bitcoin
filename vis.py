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
from bokeh.models import ColumnDataSource, CustomJS, Span, Label
from bokeh.models.widgets import Slider, TextInput, Button
from bokeh.plotting import figure

from models import *
from optimizer import *

# Plot
plot_height = 400
plot_width = 600
doc_width = 1000
plot_title="Relative Profit Over Time of a Bitcoin Attack"

# Misc.
max_days_to_compute = 200
max_days_to_display = 20
total_btc = 16000000
# Mining Power
min_mining_power = 0.0
max_mining_power = 0.5
default_mining_power = 0.2
mining_power_step = max_mining_power/200
# Discount Rate
min_discount = 0.99
max_discount = 1.0
default_discount = 0.995
discount_step = 0.0001
# BTC Fraction Stolen
min_btc_f_stolen = 0.0
max_btc_f_stolen = 0.001
default_btc_f_stolen = 0.0
btc_f_stolen_step = max_btc_f_stolen/200
# BTC Stolen
min_btc_stolen = total_btc * min_btc_f_stolen
max_btc_stolen = total_btc * max_btc_f_stolen
default_btc_stolen = total_btc * default_btc_f_stolen
btc_stolen_step = max_btc_stolen/200
# BTC Fraction Owned at Time 0
min_btc_f_owned_0 = 0.0
max_btc_f_owned_0 = 0.5
default_btc_f_owned_0 = 0.0
btc_f_owned_0_step = max_btc_f_owned_0/200
# BTC Owned at Time 0
min_btc_owned_0 = total_btc * min_btc_f_owned_0
max_btc_owned_0 = total_btc * max_btc_f_owned_0
default_btc_owned_0 = total_btc * default_btc_f_owned_0
btc_owned_0_step = max_btc_owned_0/200
# Exchange Rate
min_rate = 0
max_rate = 1000
default_rate = 772
rate_step = 10


def get_util_vs_time_data(days=[0], mining_power=default_mining_power, discount_rate=default_discount, btc_f_stolen=default_btc_f_stolen, btc_f_owned_0=default_btc_f_owned_0, default_exchange_rate=default_rate):
    _, _, attack_utilities = optimal_attack_utility(btc_f_stolen = btc_f_stolen,
                                                    btc_f_owned_0 = btc_f_owned_0,
                                                    mining_power = mining_power,
                                                    discount_rate = discount_rate,
                                                    num_days = max(days) + 1,
                                                    default_exchange_rate = default_exchange_rate)
    return [attack_utilities[d]/1000000 for d in days]

# Set up data
x = np.arange(0, max_days_to_compute, 1) # times
y = get_util_vs_time_data(days=x)
source = ColumnDataSource(data=dict(x=x, y=y))


# Set up plot
plot = figure(plot_height=plot_height, plot_width=plot_width, title=plot_title,
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, max_days_to_display],
              x_axis_label="Days Since Attack",
              y_axis_label="Relative Profit of Attacking (Millions of USD)")

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

# Set up widgets
text = TextInput(title="Title", value='mighty bitcoin')
mining_power = Slider(title="Mining Power", start=min_mining_power, end=max_mining_power, value=default_mining_power, step=mining_power_step)
discount_rate = Slider(title="Discount Rate", start=min_discount, end=max_discount, value=default_discount, step=discount_step)
btc_stolen = Slider(title="Amount of BTC Stolen", start=min_btc_stolen, end=max_btc_stolen, value=default_btc_stolen, step=btc_stolen_step)
btc_owned_0 = Slider(title="BTC Owned At Time 0", start=min_btc_owned_0, end=max_btc_owned_0, value=default_btc_owned_0, step=btc_owned_0_step)
exchange_rate = Slider(title="BTC-USD Exchange Rate", start=min_rate, end=max_rate, value=default_rate, step=rate_step)

btc_f_stolen = Slider(title="Fraction Amount of BTC Stolen", start=min_btc_f_stolen, end=max_btc_f_stolen, value=default_btc_f_stolen, step=btc_f_stolen_step)
btc_f_owned_0 = Slider(title="Fraction BTC Owned At Time 0", start=min_btc_f_owned_0, end=max_btc_f_owned_0, value=default_btc_f_owned_0, step=btc_f_owned_0_step)

hline = Span(location=0, dimension='width', line_color='green', line_width=1.5)
plot.renderers.extend([hline])


# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)

def update_data():
    # Get the current slider values
    alpha = mining_power.value
    gamma = discount_rate.value
    f_owned = btc_f_owned_0.value
    f_stolen = btc_f_stolen.value
    exchg_rate = float(exchange_rate.value)

    # Generate the new curve
    y = get_util_vs_time_data(days=x, mining_power=alpha, discount_rate=gamma,
            btc_f_stolen=f_stolen, btc_f_owned_0=f_owned, default_exchange_rate
            = exchg_rate)

    source.data = dict(x=x, y=y)

def update_default(attrname, old, new):
    update_data()

def update_f_stolen(attrname, old, new):
    btc_f_stolen.value = float(btc_stolen.value) / total_btc

def update_stolen(attrname, old, new):
    btc_stolen.value = float(btc_f_stolen.value) * total_btc

def update_f_owned_0(attrname, old, new):
    btc_f_owned_0.value = float(btc_owned_0.value) / total_btc

def update_owned_0(attrname, old, new):
    btc_owned_0.value = float(btc_f_owned_0.value) * total_btc

def set_default_settings():
    set_miner_settings(default_mining_power, default_discount, default_rate)

def set_miner_settings(alpha, gamma, x_rate):
    mining_power.value = alpha
    discount_rate.value = gamma
    exchange_rate.value = x_rate

for w in [mining_power, discount_rate, exchange_rate, btc_f_owned_0, btc_f_stolen]:
    w.on_change('value', update_default)

btc_f_stolen.on_change('value', update_stolen)
btc_stolen.on_change('value', update_f_stolen)

btc_f_owned_0.on_change('value', update_owned_0)
btc_owned_0.on_change('value', update_f_owned_0)

default_button = Button(label='Default Miner')
default_button.on_click(set_default_settings)

# Set up layouts and add to document
inputs = widgetbox(mining_power, discount_rate, btc_owned_0, btc_f_owned_0, btc_stolen, btc_f_stolen, exchange_rate)

curdoc().add_root(row(inputs, plot, width=doc_width))
curdoc().add_root(row(default_button, width=doc_width))
curdoc().title = "Sliders"
