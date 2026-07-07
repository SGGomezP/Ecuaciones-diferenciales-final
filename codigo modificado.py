import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


# ---------------------------------------------------------------
# 1) MODELO MATEMATICO (SOLUCIÓN ANALÍTICA)
# ---------------------------------------------------------------

def calcular_r(N0, N1, t1, K):
    """
    Calcula la tasa de crecimiento 'r' del modelo logistico a partir
    de dos mediciones reales (N0 en t=0 y N1 en t=t1) y una capacidad
    de carga K ya estimada por el usuario.

    Formula (despejada de la solucion analitica):
        r = (1/t1) * ln( [N1 * (K - N0)] / [N0 * (K - N1)] )
    """
    numerador = N1 * (K - N0)
    denominador = N0 * (K - N1)
    if denominador <= 0 or numerador <= 0:
        raise ValueError(
            "Los datos no son consistentes con un crecimiento logistico "
            "hacia K (revisa que N0 < N1 < K)."
        )
    r = (1 / t1) * np.log(numerador / denominador)
    return r


def solucion_analitica(t, N0, r, K):
    """
    Evalua la solucion analitica de la ecuacion logistica en el
    tiempo t (o en un arreglo de tiempos t), tomando N0 como la
    poblacion en t = 0.

        N(t) = K / (1 + A * e^(-r*t)),   A = (K - N0) / N0
    """
    A = (K - N0) / N0
    return K / (1 + A * np.exp(-r * t))


# ---------------------------------------------------------------
# 2) ENTRADA DE DATOS POR CONSOLA
# ---------------------------------------------------------------

def pedir_datos():
    """
    Pide al usuario los datos del problema de forma interactiva.
    """
    print("=" * 60)
    print(" PREDICCION DE USUARIOS - MODELO LOGISTICO (SOLUCION ANALITICA)")
    print("=" * 60)

    unidad = input(
        "Unidad de tiempo a usar (dias / semanas / meses / anios): "
    ).strip().lower()

    t1 = float(input(
        f"¿Hace cuantos {unidad} se registro el primer dato de usuarios? "
    ))
    N0 = float(input("¿Cuantos usuarios tenia la app en ese momento (N0)? "))

    N1 = float(input(
        "¿Cuantos usuarios tiene la app en el periodo mas reciente "
        "(por ejemplo el ultimo mes) (N1)? "
    ))

    K = float(input(
        "Estima la capacidad maxima de usuarios que la app podria "
        "llegar a tener (mercado potencial, K): "
    ))

    t_futuro = float(input(
        f"¿Para cuantos {unidad} en el futuro (desde el dato mas "
        "reciente) quieres la prediccion? "
    ))

    return unidad, t1, N0, N1, K, t_futuro


# ---------------------------------------------------------------
# 3) PROGRAMA PRINCIPAL
# ---------------------------------------------------------------

def main():
    unidad, t1, N0, N1, K, t_futuro = pedir_datos()

    # --- Paso 1: calcular r a partir de los dos datos reales ---
    r = calcular_r(N0, N1, t1, K)

    # tiempo total de simulacion: desde el dato antiguo (t=0)
    # hasta la prediccion futura (t = t1 + t_futuro)
    t_prediccion = t1 + t_futuro

    print("\n--- PARAMETROS DEL MODELO ---")
    print(f"Tasa de crecimiento r      = {r:.6f} (1/{unidad})")
    print(f"Capacidad de carga K       = {K:.0f} usuarios")

    # --- Paso 2: solucion analitica en el instante pedido ---
    N_analitica_pred = solucion_analitica(t_prediccion, N0, r, K)

    print("\n--- RESULTADOS DE LA PREDICCION ---")
    print(f"Dentro de {t_futuro} {unidad}, la app tendra aproximadamente:")
    print(f"  Solucion analitica (Exacta): {N_analitica_pred:,.0f} usuarios")

    graficar(unidad, t1, N0, N1, K, r, t_prediccion, t_futuro)


def graficar(unidad, t1, N0, N1, K, r, t_prediccion, t_futuro):
    """
    Grafica la curva analitica exacta, marca los datos reales y el punto 
    de prediccion, y mantiene los sliders interactivos para r y K.
    """
    t_curva = np.linspace(0, t_prediccion, 400)
    N_curva = solucion_analitica(t_curva, N0, r, K)

    fig, ax = plt.subplots(figsize=(9, 6))
    plt.subplots_adjust(bottom=0.28)

    linea_analitica, = ax.plot(t_curva, N_curva, label="Solucion analitica (Exacta)",
                               color="#2563eb", linewidth=2.5)

    linea_K = ax.axhline(K, color="gray", linestyle="--", linewidth=1,
                         label="Capacidad de carga K")

    ax.scatter([0, t1], [N0, N1], color="black", zorder=5,
               label="Datos reales")
    ax.scatter([t_prediccion], [N_curva[-1]], color="red", zorder=5,
               label="Prediccion")

    ax.set_xlabel(f"Tiempo ({unidad})")
    ax.set_ylabel("Numero de usuarios")
    ax.set_title("Crecimiento de usuarios: modelo logistico (Solucion Analitica)")
    ax.legend(loc="lower right")
    ax.grid(alpha=0.3)

    # --- Sliders interactivos para r y K ---
    ax_r = plt.axes([0.15, 0.12, 0.7, 0.03])
    ax_k = plt.axes([0.15, 0.06, 0.7, 0.03])

    slider_r = Slider(ax_r, "r", r * 0.2, r * 3, valinit=r)
    slider_k = Slider(ax_k, "K", K * 0.5, K * 1.5, valinit=K)

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


if __name__ == "__main__":
    main()