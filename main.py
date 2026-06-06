import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
from scipy import signal

#Parametry początkowe
R_poczatkowe = 100.0     # Ohm
R2_poczatkowe = 100.0    # Ohm
L_poczatkowe_mH = 10.0   # mH
C_poczatkowe_uF = 100.0  # uF
f_poczatkowe = 1.0       # Hz
sygnal_poczatkowe = 'Prostokąt'

#Parametry czasu oraz kroku symulacji
zadany_czas = 3.0
krok = 0.001
t = np.arange(0, zadany_czas, krok)
w = np.logspace(0, 5, 1000)  # Pulsacja [rad/s]

#Konfiguracja okna wykresów
wykres, osie = plt.subplots(4, 1, figsize=(11, 10))
plt.subplots_adjust(bottom=0.35, hspace=0.65)
os_u, os_y, os_ampl, os_faza = osie[0], osie[1], osie[2], osie[3]

#Sygnał wejściowy
def generuj_sygnal_wejsciowy(wektor_t, val_f, typ_sygnalu):
    omega = val_f * 2 * np.pi
    if typ_sygnalu == 'Prostokąt':
        return signal.square(omega * wektor_t)
    elif typ_sygnalu == 'Trójkąt':
        return signal.sawtooth(omega * wektor_t, width=0.5)
    elif typ_sygnalu == 'Sinus':
        return np.sin(omega * wektor_t)
    return np.zeros_like(wektor_t)

#Algorytm całkowania Rungego-Kutty czwartego rzędu
def symulacja_rk4(R, R2, L, C, val_f, typ_sygnalu):
    val_R = max(R, 1e-6)
    val_R2 = max(R2, 1e-6)
    val_L = max(L, 1e-8)
    val_C = max(C, 1e-8)
    
    a = val_L * val_C
    b = val_L * (val_R + val_R2) / (val_R * val_R2)
    
    wynik_y = np.zeros(len(t))
    wynik_dy = np.zeros(len(t))
    tablica_u = generuj_sygnal_wejsciowy(t, val_f, typ_sygnalu)
    
    def oblicz_pochodne(x1, x2, val_u):
        return x2, (val_u - b * x2 - x1) / a

    for i in range(1, len(t)):
        y_n, dy_n = wynik_y[i-1], wynik_dy[i-1]
        u_n, u_nastepne = tablica_u[i-1], tablica_u[i]
        u_polowa = (u_n + u_nastepne) / 2.0
        
        k1_y, k1_dy = oblicz_pochodne(y_n, dy_n, u_n)
        k2_y, k2_dy = oblicz_pochodne(y_n + krok*k1_y/2, dy_n + krok*k1_dy/2, u_polowa)
        k3_y, k3_dy = oblicz_pochodne(y_n + krok*k2_y/2, dy_n + krok*k2_dy/2, u_polowa)
        k4_y, k4_dy = oblicz_pochodne(y_n + krok*k3_y, dy_n + krok*k3_dy, u_nastepne)
        
        wynik_y[i] = y_n + (krok / 6.0) * (k1_y + 2*k2_y + 2*k3_y + k4_y)
        wynik_dy[i] = dy_n + (krok / 6.0) * (k1_dy + 2*k2_dy + 2*k3_dy + k4_dy)
        
    return wynik_y

#Rysowanie wykresów
L_si_poczatkowe = L_poczatkowe_mH * 1e-3
C_si_poczatkowe = C_poczatkowe_uF * 1e-6

u_poczatkowe = generuj_sygnal_wejsciowy(t, f_poczatkowe, sygnal_poczatkowe)
y_poczatkowe = symulacja_rk4(R_poczatkowe, R2_poczatkowe, L_si_poczatkowe, C_si_poczatkowe, f_poczatkowe, sygnal_poczatkowe)

a_poczatkowe = L_si_poczatkowe * C_si_poczatkowe
b_poczatkowe = L_si_poczatkowe * (R_poczatkowe + R2_poczatkowe) / (R_poczatkowe * R2_poczatkowe)
uklad_poczatkowe = signal.TransferFunction([1], [a_poczatkowe, b_poczatkowe, 1])
_, ampl_poczatkowe, faza_poczatkowe = signal.bode(uklad_poczatkowe, w)

wykres_u, = os_u.plot(t, u_poczatkowe, color='blue',linewidth=1)
os_u.set_title('Sygnał wejściowy u(t)')
os_u.grid(True)

wykres_y, = os_y.plot(t, y_poczatkowe, color='red', linewidth=1)
os_y.set_title('Sygnał wyjściowy y(t) = U_R')
os_y.grid(True)

wykres_ampl, = os_ampl.semilogx(w, ampl_poczatkowe, color='purple', linewidth=1)
os_ampl.set_title('Charakterystyka amplitudowa')
os_ampl.grid(True, which='both')

wykres_faza, = os_faza.semilogx(w, faza_poczatkowe, color='green', linewidth=1)
os_faza.set_title('Charakterystyka fazowa')
os_faza.grid(True, which='both')

#Pozycja oraz parametry sliderów
pos_R  = plt.axes([0.15, 0.25, 0.30, 0.020])
pos_R2 = plt.axes([0.15, 0.2, 0.30, 0.020])
pos_L  = plt.axes([0.15, 0.15, 0.30, 0.020])
pos_C  = plt.axes([0.15, 0.1, 0.30, 0.020])
pos_f  = plt.axes([0.60, 0.25, 0.30, 0.020])
pos_radio = plt.axes([0.60, 0.14, 0.18, 0.10])

slider_R  = Slider(pos_R, 'R', 1.0, 1000.0, valinit=R_poczatkowe, valfmt='%1.0f Ω')
slider_R2 = Slider(pos_R2, 'R2', 1.0, 1000.0, valinit=R2_poczatkowe, valfmt='%1.0f Ω')
slider_L  = Slider(pos_L, 'L', 1.0, 100.0, valinit=L_poczatkowe_mH, valfmt='%1.1f mH')
slider_C  = Slider(pos_C, 'C', 1.0, 500.0, valinit=C_poczatkowe_uF, valfmt='%1.1f µF')
slider_f  = Slider(pos_f, 'Częst.', 0.5, 20.0, valinit=f_poczatkowe, valfmt='%1.1f Hz')

radio_signal = RadioButtons(pos_radio, ('Prostokąt', 'Trójkąt', 'Sinus'))

#Funkcja aktualizacji programu
def update(val):
    R_si = slider_R.val
    R2_si = slider_R2.val
    L_si = slider_L.val * 1e-3
    C_si = slider_C.val * 1e-6
    val_f = slider_f.val
    typ_sygnalu = radio_signal.value_selected
    
    u_nowe = generuj_sygnal_wejsciowy(t, val_f, typ_sygnalu)
    y_nowe = symulacja_rk4(R_si, R2_si, L_si, C_si, val_f, typ_sygnalu)
    
    a = L_si * C_si
    b = L_si * (R_si + R2_si) / (R_si * R2_si)
    uklad_nowy = signal.TransferFunction([1], [a, b, 1])
    _, ampl_nowa, faza_nowa = signal.bode(uklad_nowy, w)
    
    wykres_u.set_ydata(u_nowe)
    wykres_y.set_ydata(y_nowe)
    wykres_ampl.set_ydata(ampl_nowa)
    wykres_faza.set_ydata(faza_nowa)
    
    os_u.relim(); os_u.autoscale_view(True, True, True)
    os_y.relim(); os_y.autoscale_view(True, True, True)
    os_ampl.relim(); os_ampl.autoscale_view(True, True, True)
    os_faza.relim(); os_faza.autoscale_view(True, True, True)
    
    wykres.canvas.draw_idle()

#Gdy, któryś z parametrów jest aktualizowany wywołana zostaje funkcja update
slider_R.on_changed(update)
slider_R2.on_changed(update)
slider_L.on_changed(update)
slider_C.on_changed(update)
slider_f.on_changed(update)
radio_signal.on_clicked(update)

plt.show()