import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
import numpy as np

# Just creating a random example image
x = np.arange(20)
y = np.random.rand(20)

fig, ax = plt.subplots()
ax.plot(x, y, 'o')

# Function to be called when the rectangle is released
# The `eclick` and `erelease` are the click and release events
def line_select_callback(eclick, erelease):
    'eclick and erelease are the press and release events'
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    print(f"({x1:3.2f}, {y1:3.2f}) --> ({x2:3.2f}, {y2:3.2f})")
    print(f" The button you used were: {eclick.button}")

# Create the rectangle selector object
rectprops = dict(facecolor='red', edgecolor = 'black', alpha=0.2, fill=True)
rect = RectangleSelector(ax, line_select_callback,
                         drawtype='box', useblit=True,
                         button=[1, 3],  # don't use middle button
                         minspanx=5, minspany=5,
                         spancoords='pixels',
                         interactive=True,
                         rectprops=rectprops)

plt.show()
