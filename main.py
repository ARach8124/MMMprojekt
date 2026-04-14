import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

rodzaj_sygnalu=1
f=4
zadany_czas=3
krok=0.001

r = 100.0   
r_2 = 100.0  
l = 0.01    
c = 0.0001
a = l * c
b = l * (r + r_2) / (r * r_2)

def sygnal_wejsciowy(f, t):
    omega = f * 2 * np.pi
    if rodzaj_sygnalu == 1:
        u = signal.square(omega * t)
    elif rodzaj_sygnalu == 2:
        u = signal.sawtooth(omega * t, width=0.5)
    elif rodzaj_sygnalu == 3:
        u = np.sin(omega * t)
    else:
        u = 0
    return u

# POPRAWKA 1: Kolejność (czas, zmienna 1, zmienna 2)
def pochodne(t, x1, x2):
    u = sygnal_wejsciowy(f, t)
    dx1 = x2
    dx2 = (u - b*x2 - x1) / a
    return dx1, dx2

t = np.arange(0, zadany_czas, krok)
y = np.zeros(len(t))
dy = np.zeros(len(t))

# POPRAWKA 2: Pętla od 1, korzystamy z i-1, zapisujemy do i
for i in range(1, len(t)):
    t_n = t[i-1]
    y_n = y[i-1]
    dy_n = dy[i-1]
    
    k1_y, k1_dy = pochodne(t_n, y_n, dy_n)
    k2_y, k2_dy = pochodne(t_n + krok/2, y_n + krok*k1_y/2, dy_n + krok*k1_dy/2)
    k3_y, k3_dy = pochodne(t_n + krok/2, y_n + krok*k2_y/2, dy_n + krok*k2_dy/2)
    k4_y, k4_dy = pochodne(t_n + krok, y_n + krok*k3_y, dy_n + krok*k3_dy)
    
    y[i] = y_n + (krok / 6.0) * (k1_y + 2*k2_y + 2*k3_y + k4_y)
    dy[i] = dy_n + (krok / 6.0) * (k1_dy + 2*k2_dy + 2*k3_dy + k4_dy)

u_wykres = sygnal_wejsciowy(f, t)

figure, wykres = plt.subplots(2, 1, figsize=(10, 8))

wykres[0].plot(t, u_wykres, label='Wejście: u(t)', color='blue')
wykres[0].set_title('Sygnał wejściowy (wymuszenie)')
wykres[0].set_ylabel('Napięcie [V]')
wykres[0].grid(True)
wykres[0].legend(loc='upper right')

wykres[1].plot(t, y, label='Wyjście: y(t) = U_R', color='red', linewidth=2)
wykres[1].set_title('Odpowiedź układu RLC')
wykres[1].set_xlabel('Czas [s]') 
wykres[1].set_ylabel('Napięcie [V]')
wykres[1].grid(True)
wykres[1].legend(loc='upper right')

plt.tight_layout()
plt.show()
