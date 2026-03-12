import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import scipy
#wartości testowe potem będzie input
rodzaj_sygnalu=1
f=4
zadanyczas=3
krok=0.002


#
def uwejsciowe(t):
    omega=f*2*np.pi
    if rodzaj_sygnalu==1:
        u=signal.square(omega*t)
        return u
    elif rodzaj_sygnalu==2:
        u=signal.sawtooth(omega*t,width=0.5)
        return u
    elif rodzaj_sygnalu==3:
        u=np.sin(omega*t)
        return u
    else:
        return

def sygnalwejsciowy(f):
    omega=f*2*np.pi
    t=np.arange(0,zadanyczas,krok)
    if rodzaj_sygnalu==1:
        u=signal.square(omega*t)
        return u
    elif rodzaj_sygnalu==2:
        u=signal.sawtooth(omega*t,width=0.5)
        return u
    elif rodzaj_sygnalu==3:
        u=np.sin(omega*t)
        return u
    else:
        return

plt.plot(sygnalwejsciowy(f))
plt.show()    
        
        




    

    

