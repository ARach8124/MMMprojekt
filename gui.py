import tkinter as tk
from tkinter import ttk
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SymulatorUkladuRLC:
    def __init__(self,root):
        self.root = root
        self.root.title("Symulator układu RLC")

        self.panel_sterowania()
        self.wykresy()

    def panel_sterowania(self):
        frame=ttk.Frame(self.root)
        frame.grid(row=0, column=0, sticky='n')

        ttk.Label(frame, text="R [Ohm]:").grid(row=0, column=0)
        self.R=tk.DoubleVar(value=100)
        ttk.Entry(frame, textvariable=self.R).grid(row=0, column=1)

        ttk.Label(frame, text="R2 [Ohm]:").grid(row=1, column=0)
        self.R2=tk.DoubleVar(value=100)
        ttk.Entry(frame, textvariable=self.R2).grid(row=1, column=1)
        
        ttk.Label(frame, text="L [H]:").grid(row=2, column=0)
        self.L=tk.DoubleVar(value=0.01)
        ttk.Entry(frame, textvariable=self.L).grid(row=2, column=1)

        ttk.Label(frame, text="C [F]:").grid(row=3, column=0)
        self.C=tk.DoubleVar(value=0.0001)
        ttk.Entry(frame, textvariable=self.C).grid(row=3, column=1)

        ttk.Label(frame,text="Rodzaj sygnału:").grid(row=4, column=0)
        self.rodzaj_sygnalu=tk.StringVar(value="sinusoidalny")
        ttk.Combobox(
            frame,
            textvariable=self.rodzaj_sygnalu,
            values=["prostokątny", "trójkątny", "sinusoidalny"]
        ).grid(row=4, column=1)

        ttk.Label(frame, text="Częstotliwość [Hz]:").grid(row=5, column=0)
        self.czestotliwosc=tk.DoubleVar(value=4)
        ttk.Entry(frame, textvariable=self.czestotliwosc).grid(row=5, column=1)

        ttk.Label(frame, text="Czas symulacji [s]:").grid(row=6, column=0)
        self.czas_symulacji=tk.DoubleVar(value=3)
        ttk.Entry(frame, textvariable=self.czas_symulacji).grid(row=6, column=1)

        ttk.Button(frame, text="Uruchom symulację", command=self.uruchom_symulacje)\
        .grid(row=7, column=0)

    def wykresy(self):
        self.figura, self.osie = plt.subplots(2,1,figsize=(6,5))
        self.canvas=FigureCanvasTkAgg(self.figura, master=self.root)
        self.canvas.get_tk_widget().grid(row=0, column=1)

    def sygnal_wejsciowy(self, t, f):
        omega=2*np.pi*f
        typ=self.rodzaj_sygnalu.get()

        if typ == "prostokątny":
            return signal.square(omega*t)
        elif typ == "trójkątny":
            return signal.sawtooth(omega*t, width=0.5)
        else:
            return np.sin(omega*t)
        
    def uruchom_symulacje(self):
        R=self.R.get()
        R2=self.R2.get()
        L=self.L.get()
        C=self.C.get()
        f=self.czestotliwosc.get()
        czas=self.czas_symulacji.get()

        krok=0.001
        t=np.arange(0, czas, krok)

        a=L*C
        b=L*(R+R2)/(R*R2)

        y=np.zeros(len(t))
        dy=np.zeros(len(t))

        def pochodne(ti, x1, x2):
            u=self.sygnal_wejsciowy(ti, f)
            dx1=x2
            dx2=(u-b*x2-x1)/a
            return dx1, dx2
        
        for i in range(1, len(t)):
            k1_y, k1_dy = pochodne(t[i-1], y[i-1], dy[i-1])
            k2_y, k2_dy = pochodne(t[i-1] + krok/2, y[i-1] + krok*k1_y/2, dy[i-1] + krok*k1_dy/2)
            k3_y, k3_dy = pochodne(t[i-1] + krok/2, y[i-1] + krok*k2_y/2, dy[i-1] + krok*k2_dy/2)
            k4_y, k4_dy = pochodne(t[i-1] + krok, y[i-1] + krok*k3_y, dy[i-1] + krok*k3_dy)

            y[i]=y[i-1]+krok/6*(k1_y+2*k2_y+2*k3_y+k4_y)
            dy[i]=dy[i-1]+krok/6*(k1_dy+2*k2_dy+2*k3_dy+k4_dy)

        u=self.sygnal_wejsciowy(t,f)

        self.osie[0].clear()
        self.osie[1].clear()

        self.osie[0].plot(t,u)
        self.osie[0].set_title("Sygnał wejściowy")

        self.osie[1].plot(t,y)
        self.osie[1].set_title("Odpowiedź układu")

        self.canvas.draw()

if __name__ == "__main__":
    root=tk.Tk()
    app=SymulatorUkladuRLC(root)
    root.mainloop()
