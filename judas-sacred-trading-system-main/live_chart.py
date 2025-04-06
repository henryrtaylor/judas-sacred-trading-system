from ib_insync import *
from config import IBKR_HOST, IBKR_PORT, CLIENT_ID
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Init
ib = IB()
ib.connect(IBKR_HOST, IBKR_PORT, clientId=CLIENT_ID)

contract = Forex('EURUSD')
ticker = ib.reqMktData(contract)

# Data storage
x_data = []
y_data = []

# Chart setup
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_title("Live EUR/USD Price")
ax.set_xlabel("Time (ticks)")
ax.set_ylabel("Price")

# Animation update
def update(frame):
    ib.sleep(0.5)
    price = ticker.bid or ticker.last
    if price:
        x_data.append(len(x_data))
        y_data.append(price)
        line.set_data(x_data, y_data)
        ax.relim()
        ax.autoscale_view()
    return line,

ani = animation.FuncAnimation(fig, update, interval=1000)
plt.show()

ib.cancelMktData(contract)
ib.disconnect()
