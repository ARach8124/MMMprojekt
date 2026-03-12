# MMMprojekt

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install numpy matplotlib scipy

na potem
rodzaj_sygnalu=int(input("Podaj rodzaj sygnału:\n 1-Prostokątny\n 2-Trójkątny\n 3-Sinusoidalny"))
def pochodne(t, y, i_L):
u=uwejsciowe(t)
t=np.linspace(0,zadanyczas,1000)
