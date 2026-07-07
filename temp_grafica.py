import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def solucion_analitica(t, N0, r, K):
    A = (K - N0) / N0
    return K / (1 + A * np.exp(-r * t))

unidad = 'anios'
t1 = 3
N0 = 10
N1 = 20
K = 100
r = 0.27031
t_futuro = 2
t_prediccion = t1 + t_futuro

t_curva = np.linspace(0, t_prediccion, 400)
N_curva = solucion_analitica(t_curva, N0, r, K)

fig, ax = plt.subplots(figsize=(9, 6))
plt.subplots_adjust(bottom=0.28)

linea_analitica, = ax.plot(t_curva, N_curva, label='Solucion analitica (Exacta)', color='#2563eb', linewidth=2.5)
linea_K = ax.axhline(K, color='gray', linestyle='--', linewidth=1, label='Capacidad de carga K')

ax.scatter([0, t1], [N0, N1], color='black', zorder=5, label='Datos reales')
ax.scatter([t_prediccion], [N_curva[-1]], color='red', zorder=5, label='Prediccion')

ax.set_xlabel(f'Tiempo ({unidad})')
ax.set_ylabel('Numero de usuarios')
ax.set_title('Crecimiento de usuarios: modelo logistico (Solucion Analitica)')
ax.legend(loc='lower right')
ax.grid(alpha=0.3)

ax_r = plt.axes([0.15, 0.12, 0.7, 0.03])
ax_k = plt.axes([0.15, 0.06, 0.7, 0.03])

slider_r = Slider(ax_r, 'r', r * 0.2, r * 3, valinit=r)
slider_k = Slider(ax_k, 'K', K * 0.5, K * 1.5, valinit=K)

def actualizar(val):
    r_nuevo = slider_r.val
    K_nuevo = slider_k.val
    N_nueva = solucion_analitica(t_curva, N0, r_nuevo, K_nuevo)
    linea_analitica.set_ydata(N_nueva)
    linea_K.set_ydata([K_nuevo, K_nuevo])
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw_idle()

slider_r.on_changed(actualizar)
slider_k.on_changed(actualizar)

plt.show()
