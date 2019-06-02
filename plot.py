# Third-party libraries 
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, show
from matplotlib.widgets import TextBox, RadioButtons, Button
# Standard library
import math

# User input values as global variables
m_1 = 1
m_2 = 1
k_1 = 1
k_2 = 1
b_1 = 1
b_2 = 1
x_1_zero = 0
x_2_zero = 0
A = 1
signal = 'unit step'

def u(t):
    """
    Returns an appropriate signal based on user selection. Sine and square
    waves have a fixed frequency of 0.25Hz
    """
    global A
    if signal == 'sine':
        return A + A*math.sin(0.5 * math.pi * t)
    elif signal == 'square':
        # Equivalent to sgn(sin(t / 2*pi))
        return A + A*math.copysign(1, math.sin(0.5 * math.pi * t))
    else:
        return A


def frange(start, stop = None, step = None):
    if stop == None:
        stop = start + 0.0
        start = 0.0
    if step == None:
        step = 1.0
    while math.fabs(start) < math.fabs(stop):
        yield start
        start = start + step


def v_1_poch(x_1, x_2, v_1, v_2):
    return x_1 * -(k_1 + k_2) / m_1 + x_2 * k_2 / m_2 + v_1 * -(b_1 + b_2) / m_1 + v_2 * b_2 / m_1


def v_2_poch(x_1, x_2, v_1, v_2, u_val):
    return x_1 * k_2 / m_2 + x_2 * -k_2 / m_2 + v_1 * b_2 / m_2 + v_2 * -b_2 / m_2 + u_val / m_2


def integrate(t_i = 0.01, T_s = 20):
    """
    Solves state-space system model for a time interval (0, Ts) with integration
    time Ti using trapezoidal rule. Returns a tuple of lists containing samples
    of mass positions and input every Ti, as well as corresponding time values.
    """
    global x_1_zero
    global x_2_zero
    x_1 = x_1_zero
    x_2 = x_2_zero
    x_1_pre_prev = x_1_prev = 0
    x_2_pre_prev = x_2_prev = 0
    v_1 = v_1_prev = v_1_pre_prev = 0
    v_2 = v_2_prev = v_2_pre_prev = 0
    
    x_1_samples, x_2_samples, u_samples, time_samples = [], [], [], []
    for t in frange(t_i, T_s, t_i):
        x_1 += 0.5 * (v_1_prev + v_1_pre_prev) * t_i
        x_2 += 0.5 * (v_2_prev + v_2_pre_prev) * t_i
        v_1 += 0.5 * (v_1_poch(x_1_prev, x_2_prev, v_1_prev, v_2_prev) + 
            v_1_poch(x_1_pre_prev, x_2_pre_prev, v_1_pre_prev, v_2_pre_prev)) * t_i
        v_2 += 0.5 * (v_2_poch(x_1_prev, x_2_prev, v_1_prev, v_2_prev, u(t)) + 
            v_2_poch(x_1_pre_prev, x_2_pre_prev, v_1_pre_prev, v_2_pre_prev, u(t-t_i))) * t_i

        x_1_pre_prev = x_1_prev
        x_2_pre_prev = x_2_prev
        v_1_pre_prev = v_1_prev
        v_2_pre_prev = v_2_prev
        x_1_prev = x_1
        x_2_prev = x_2
        v_1_prev = v_1
        v_2_prev = v_2

        x_1_samples.append(x_1)
        x_2_samples.append(x_2)
        u_samples.append(u(t))
        time_samples.append(t)

    return x_1_samples, x_2_samples, u_samples, time_samples


# matplotlib initial setup - graph area
x_1, x_2, signal, time = integrate()
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
plt.subplots_adjust(bottom=0.34, left=0.15)
ax1.plot(time, signal, label="input signal")
ax2.plot(time, x_1, label="x1")
ax2.plot(time, x_2, label="x2")
ax1.legend()
ax1.set_ylabel('force [N]')
ax1.set_xlabel('time [s]')
ax2.legend()
ax2.set_ylabel('position [m]')
ax2.set_xlabel('time [s]')


def update(text):
    """
    Updates position signals and rescales the graph. Must be called whenever
    user-specified parameters change
    """
    ax1.clear()
    ax2.clear()
    x_1, x_2, signal, time = integrate()
    plt.subplots_adjust(bottom=0.34, left=0.15)
    ax1.plot(time, signal, label="input signal")
    ax2.plot(time, x_1, label="x1")
    ax2.plot(time, x_2, label="x2")
    ax1.legend()
    ax1.set_ylabel('force [N]')
    ax1.set_xlabel('time [s]')
    ax2.legend()
    ax2.set_ylabel('position [m]')
    ax2.set_xlabel('time [s]')
    ax1.relim()
    ax1.autoscale_view()
    ax2.relim()
    ax2.autoscale_view()
    plt.draw()
    plt.show()


# Matplotlib - handling user controls
def submit_1(text):
    global m_1
    m_1 = eval(text)
def submit_2(text):
    global m_2
    m_2 = eval(text)
def submit_3(text):
    global k_1
    k_1 = eval(text)
def submit_4(text):
    global k_2
    k_2 = eval(text)
def submit_5(text):
    global b_1
    b_1 = eval(text)
def submit_6(text):
    global b_2
    b_2 = eval(text)
def submit_7(text):
    global x_1_zero
    x_1_zero = eval(text)
def submit_8(text):
    global x_2_zero
    x_2_zero = eval(text)
def submit_9(text):
    global A
    A = eval(text)
def change_signal(label):
    global signal
    signal = label
    update("")

# Matplotlib setup - user controls
signal = RadioButtons(plt.axes([0.1, 0.1, 0.14, 0.13]),
                      ['unit step', 'sine', 'square'], activecolor='red')
signal.on_clicked(change_signal)
text_box = TextBox(plt.axes([0.345, 0.1, 0.1, 0.05]), 'm1 [kg] ', initial="2000")
text_box.on_submit(submit_1)
text_box1 = TextBox(plt.axes([0.345, 0.18, 0.1, 0.05]), 'm2 [kg] ', initial="500")
text_box1.on_submit(submit_2)
text_box2 = TextBox(plt.axes([0.56, 0.1, 0.1, 0.05]), 'k1 [N/m] ', initial="500000")
text_box2.on_submit(submit_3)
text_box3 = TextBox(plt.axes([0.56, 0.18, 0.1, 0.05]), 'k2 [N/m] ', initial="100000")
text_box3.on_submit(submit_4)
text_box4 = TextBox(plt.axes([0.8, 0.1, 0.1, 0.05]), 'b1 [N*s/m] ', initial="500")
text_box4.on_submit(submit_5)
text_box5 = TextBox(plt.axes([0.8, 0.18, 0.1, 0.05]), 'b2 [N*s/m] ', initial="15000")
text_box5.on_submit(submit_6)
text_box6 = TextBox(plt.axes([0.345, 0.02, 0.1, 0.05]), 'x1(0) [m]', initial="0")
text_box6.on_submit(submit_7)
text_box7 = TextBox(plt.axes([0.56, 0.02, 0.1, 0.05]), 'x2(0) [m]', initial="0")
text_box7.on_submit(submit_8)
text_box8 = TextBox(plt.axes([0.8, 0.02, 0.1, 0.05]), 'A [N]', initial="800")
text_box8.on_submit(submit_9)
update_button = Button(plt.axes([0.1, 0.02, 0.1, 0.05]), "Update")
update_button.on_clicked(update)
show()
