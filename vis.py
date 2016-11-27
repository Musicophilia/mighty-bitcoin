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
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure

from models import *

def get_util_vs_time_data(times, alpha=0.2):
    vals = []
    for t in times:
        model = utility_model(attack_time=t, mining_power=alpha)
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


# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)

def update_data(attrname, old, new):

    # Get the current slider values
    b = offset.value
    alpha = mining_power.value

    # Generate the new curve
    y = get_util_vs_time_data(x, alpha)

    source.data = dict(x=x, y=y)

for w in [offset, mining_power]:
    w.on_change('value', update_data)


# Set up layouts and add to document
inputs = widgetbox(text, mining_power)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"