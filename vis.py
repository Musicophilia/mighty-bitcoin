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

total_btc = 16000000
max_btc_f_stolen = 0.001
max_btc_stolen = total_btc * max_btc_f_stolen
max_btc_f_owned_0 = 0.5
max_btc_owned_0 = total_btc * max_btc_f_owned_0
max_mining_power = 0.5
max_days = 20


def get_util_vs_time_data(days=[0], mining_power=0.2, discount_rate=1.0, btc_f_stolen=0.0, btc_f_owned_0=0.0, default_exchange_rate=730):
    _, _, attack_utilities = optimal_attack_utility(btc_f_stolen = btc_f_stolen,
                                                    btc_f_owned_0 = btc_f_owned_0,
                                                    mining_power = mining_power,
                                                    discount_rate = discount_rate,
                                                    num_days = max(days) + 1,
                                                    default_exchange_rate = default_exchange_rate)
    return [attack_utilities[d]/1000000 for d in days]

# Set up data
x = np.arange(0, max_days, 1) # times
y = get_util_vs_time_data(days=x)
source = ColumnDataSource(data=dict(x=x, y=y))


# Set up plot
plot = figure(plot_height=400, plot_width=500, title="mighty bitcoin",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, max_days],
              x_axis_label="Days Since Attack",
              y_axis_label="Relative Profit of Attacking (Millions of USD)")

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

# Set up widgets
text = TextInput(title="Title", value='mighty bitcoin')
mining_power = Slider(title="Mining Power", start=0.0, end=max_mining_power, value=0.2, step=max_mining_power/200)
discount_rate = Slider(title="Discount Rate", start=0.99, end=1.0, value=0.995, step=0.0001)
btc_stolen = Slider(title="BTC Stolen", start=0.0, end=max_btc_stolen, value=0, step=max_btc_stolen/200)
btc_owned_0 = Slider(title="BTC Owned At Time 0", start=0.0, end=max_btc_owned_0, value=0, step=max_btc_owned_0/200)
exchange_rate = Slider(title="BTC-USD Exchange Rate", start=0, end=1000, value=730, step=10)

# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)
def update_data():
    # Get the current slider values
    alpha = mining_power.value
    gamma = discount_rate.value
    f_owned = float(btc_owned_0.value) / total_btc
    f_stolen = float(btc_stolen.value) / total_btc
    exchg_rate = float(exchange_rate.value)

    # Generate the new curve
    y = get_util_vs_time_data(days=x, mining_power=alpha, discount_rate=gamma,
            btc_f_stolen=f_stolen, btc_f_owned_0=f_owned, default_exchange_rate
            = exchg_rate)

    source.data = dict(x=x, y=y)

def update_default(attrname, old, new):
    update_data()

for w in [mining_power, discount_rate, exchange_rate, btc_owned_0, btc_stolen]:
    w.on_change('value', update_default)

# Set up layouts and add to document
inputs = widgetbox(text, mining_power, discount_rate, btc_owned_0, btc_stolen, exchange_rate)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"
