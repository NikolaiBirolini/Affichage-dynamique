import matplotlib.pyplot as plt
import matplotlib.animation as animation
from serial import *

# Create figure for plotting
fig = plt.figure(figsize = (10, 10))
ax = fig.add_subplot(7, 1, 1)
ax2 = fig.add_subplot(7,1,3)
ax3 = fig.add_subplot(7,1,5)
ax4 = fig.add_subplot(7,1,7)

# Initialise list for plotting
xs = [] # Time in second
ys = [] # Temperature in C
Ps= [] # Pressure in KPa
Hs=[] # Humidity in %
As=[] #Altitude in m

# This function is called periodically from FuncAnimation
def animate(i, xs, ys, Hs, Ps, As):

    # Save the data in the serial port
    mesure = port_serie.readline()  # read the data
    instant = time.time() - start  # Determine the time

    #Debug serial byte string
    print(mesure)
    print(mesure.split(b';')) # Data = temperature;humidity;pressure\n

    # Fill Lists for plotting
    mesure.split(b'\r\n')
    ys.append(mesure.split(b';')[0])  # Temperature list
    xs.append(instant)  # Time list
    Hs.append(mesure.split(b';')[1]) # Humidity list
    Ps.append(mesure.split(b';')[2]) # Pressure list
    As.append(mesure.split(b';')[3])

    # Limit all lists to 5 items
    xs = xs[-5:]
    ys = ys[-5:]
    Hs = Hs[-5:]
    Ps = Ps[-5:]
    As = As[-5:]

    # Draw temperature
    plt.subplot(711)
    ax.clear()
    plt.title('Temperature')
    plt.ylabel('Temperature (deg C)')
    plt.xlabel("temps en s")
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)


    # Draw Humidity
    plt.subplot(713)
    ax2.clear()
    ax2.plot(xs, Hs)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)

    plt.title('Humidité')
    plt.ylabel('Taux Humidité (%)')
    plt.xlabel("temps en s")

    # Draw Pressure
    plt.subplot(715)
    ax3.clear()
    ax3.plot(xs, Ps)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)

    plt.title('Pression')
    plt.ylabel('Pression (KPa)')
    plt.xlabel("temps en s")

    # Draw Altitude
    plt.subplot(717)
    ax4.clear()
    ax4.plot(xs, As)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)

    plt.title('Altitude')
    plt.ylabel('Altitude (m)')
    plt.xlabel("temps en s")


# We define witch port we will reading
with Serial(port="COM5", baudrate=9600, timeout=5, writeTimeout=1) as port_serie:
    if port_serie.isOpen():
        start = time.time()  # Save the strat time
        temp = port_serie.readline() # Catch the first transmission : "Start !!!"
    while True:

        # Set up plot to call animate() function periodically
        ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, Hs, Ps, As), interval=1000)
        plt.show()

