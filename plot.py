# Third-party libraries 
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, show
from matplotlib.widgets import TextBox, RadioButtons
# Standard library
import math
# External helper functions
from matrix import exp_mat, zeros, scale_mat_square, add_mat_square

# User input values as global variables
m_1 = 1
m_2 = 1
k_1 = 1
k_2 = 1 
b_1 = 1
b_2 = 1
signal = "unit step"

def u(t):
    """
    Returns an appropriate signal based on user selection. Sine and square
    waves have a fixed frequency of 1Hz
    """
    if signal == "sine":
        return math.sin(t / 2*math.pi)
    elif signal == "square":
        # Equivalent to sgn(sin(t / 2*pi))
        return math.copysign(1, math.sin(t / 2*math.pi))
    else:
        return 1

def integrate(Ts, Ti = 0.1):
    """
    Solves state-space system model for a time interval (0, Ts) with integration
    time Ti using trapezoidal rule. Returns a pair of lists containing samples
    of mass positions every Ti.
    """
    # Construct A matrix from current parameter values 
    A = [[-(b_1+b_2)/m_1, b_2/m_1, -(k_1+k_2)/m_1, k_2/m_1],
        [b_2/m_2, -b_2/m_2, k_2/m_2, -k_2/m_2],
        [1, 0, 0, 0],
        [0, 1, 0, 0]]
    # Initialization
    x_1 = []
    x_2 = []
    exp_A_left = zeros(len(A))
    exp_A_right = zeros(len(A))
    # Actual integration - assuming zero intial conditions, model solution
    # is equal to the integral of e^A(t-tau)*B*u(t)dtau from 0 to t
    for i in range(int(Ts / Ti)):
        # In each e^A(t-tau) is equal to a sum of the previous value and e^At
        exp_A_right = add_mat_square(exp_A_right, exp_mat(scale_mat_square(A, i * Ti)))

        # "Sampling" positions 1, 2 and 1, 3 in the resulting matrix for to get
        # mass position values
        x_1.append((exp_A_left[1][2] + exp_A_right[1][2]) * u(t[i]) / 2)
        x_2.append((exp_A_left[1][3] + exp_A_right[1][3]) * u(t[i]) / 2)

        # Saving previous e^A(t-tau)
        exp_A_left = exp_A_right
    
    return x_1, x_2

# Time period and sample count definitions
Ts = 5
samples = 500
# Time values list generation
t = []
for i in range(samples):
    t.append(i * Ts / samples)
x_1, x_2 = integrate(Ts, Ts / samples)

# matplotlib initial setup - graph area
fig, ax1 = plt.subplots()
plt.subplots_adjust(bottom=0.34, left=0.15)
x_1_p, = ax1.plot(t, x_1, label="x1")
x_2_p, = ax1.plot(t, x_2, label="x2")
ax1.legend()
ax1.set_ylabel('position')
ax1.set_xlabel('time')

def update():
    """
    Updates position signals and rescales the graph. Must be called whenever
    user-specified parameters change
    """

    ax1.clear()
    x_1, x_2 = integrate(Ts, Ts / samples)
    x_1_p, = ax1.plot(t, x_1, label="x1")
    x_2_p, = ax1.plot(t, x_2, label="x2")
    ax1.legend()
    ax1.set_ylabel('position')
    ax1.set_xlabel('time')
    ax1.relim()
    ax1.autoscale_view()
    plt.draw()
    plt.show()


# Matplotlib - handling user controls
def submit_1(text):
    global m_1
    m_1 = eval(text)
    update()
def submit_2(text):
    global m_2
    m_2 = eval(text)
    update()
def submit_3(text):
    global k_1
    k_1 = eval(text)
    update()
def submit_4(text):
    global k_2
    k_2 = eval(text)
    update()
def submit_5(text):
    global b_1
    b_1 = eval(text)
    update()
def submit_6(text):
    global b_2
    b_2 = eval(text)
    update()
def change_signal(label):
    global signal
    signal = label
    update()

# Matplotlib setup - user controls
signal = RadioButtons(plt.axes([0.1, 0.1, 0.14, 0.13]), 
    ['sine', 'square', 'unit step'], activecolor='red')
signal.on_clicked(change_signal)
text_box = TextBox(plt.axes([0.345, 0.1, 0.1, 0.05]), 'm1 [kg] ', initial="1")
text_box.on_submit(submit_1)
text_box1 = TextBox(plt.axes([0.345, 0.18, 0.1, 0.05]), 'm2 [kg] ', initial="1")
text_box1.on_submit(submit_2)
text_box2 = TextBox(plt.axes([0.56, 0.1, 0.1, 0.05]), 'k1 [N/m] ', initial="1")
text_box2.on_submit(submit_3)
text_box3 = TextBox(plt.axes([0.56, 0.18, 0.1, 0.05]), 'k2 [N/m] ', initial="1")
text_box3.on_submit(submit_4)
text_box4 = TextBox(plt.axes([0.8, 0.1, 0.1, 0.05]), 'b1 [N*s/m] ', initial="1")
text_box4.on_submit(submit_5)
text_box5 = TextBox(plt.axes([0.8, 0.18, 0.1, 0.05]), 'b2 [N*s/m] ', initial="1")
text_box5.on_submit(submit_6)

show()