#include <iostream>
#include <cmath>
#include <string>
#include <iomanip>
#include <stdexcept>
#include <fstream>
#include <cstdlib>

// Estructura para agrupar los datos de entrada
struct DatosEntrada {
    std::string unidad;
    double t1;
    double N0;
    double N1;
    double K;
    double t_futuro;
};

// 1) MODELO MATEMÁTICO
double calcular_r(double N0, double N1, double t1, double K) {
    double numerador = N1 * (K - N0);
    double denominador = N0 * (K - N1);
    
    if (denominador <= 0 || numerador <= 0) {
        throw std::invalid_argument(
            "Los datos no son consistentes con un crecimiento logistico "
            "hacia K (revisa que N0 < N1 < K)."
        );
    }
    return (1.0 / t1) * std::log(numerador / denominador);
}

double solucion_analitica(double t, double N0, double r, double K) {
    double A = (K - N0) / N0;
    return K / (1.0 + A * std::exp(-r * t));
}

// 2) ENTRADA DE DATOS
DatosEntrada pedir_datos() {
    DatosEntrada d;
    std::cout << "============================================================\n";
    std::cout << " PREDICCION DE USUARIOS - MODELO LOGISTICO (SOLUCION C++)\n";
    std::cout << "============================================================\n";

    std::cout << "Unidad de tiempo a usar (dias / semanas / meses / anios): ";
    std::cin >> d.unidad;

    std::cout << "¿Hace cuantos " << d.unidad << " se registro el primer dato de usuarios? ";
    std::cin >> d.t1;
    
    std::cout << "¿Cuantos usuarios tenia la app en ese momento (N0)? ";
    std::cin >> d.N0;

    std::cout << "¿Cuantos usuarios tiene la app en el periodo mas reciente (N1)? ";
    std::cin >> d.N1;

    std::cout << "Estima la capacidad maxima de usuarios (K): ";
    std::cin >> d.K;

    std::cout << "¿Para cuantos " << d.unidad << " en el futuro quieres la prediccion? ";
    std::cin >> d.t_futuro;

    return d;
}

// 3) GENERADOR DE LA INTERFAZ GRÁFICA
void graficar(const std::string& unidad, double t1, double N0, double N1, double K, double r, double t_futuro) {
    // Creamos un script de python temporal con los datos calculados en C++
    std::ofstream script("temp_grafica.py");
    
    script << "import numpy as np\n"
           << "import matplotlib.pyplot as plt\n"
           << "from matplotlib.widgets import Slider\n\n"
           << "def solucion_analitica(t, N0, r, K):\n"
           << "    A = (K - N0) / N0\n"
           << "    return K / (1 + A * np.exp(-r * t))\n\n"
           << "unidad = '" << unidad << "'\n"
           << "t1 = " << t1 << "\n"
           << "N0 = " << N0 << "\n"
           << "N1 = " << N1 << "\n"
           << "K = " << K << "\n"
           << "r = " << r << "\n"
           << "t_futuro = " << t_futuro << "\n"
           << "t_prediccion = t1 + t_futuro\n\n"
           << "t_curva = np.linspace(0, t_prediccion, 400)\n"
           << "N_curva = solucion_analitica(t_curva, N0, r, K)\n\n"
           << "fig, ax = plt.subplots(figsize=(9, 6))\n"
           << "plt.subplots_adjust(bottom=0.28)\n\n"
           << "linea_analitica, = ax.plot(t_curva, N_curva, label='Solucion analitica (Exacta)', color='#2563eb', linewidth=2.5)\n"
           << "linea_K = ax.axhline(K, color='gray', linestyle='--', linewidth=1, label='Capacidad de carga K')\n\n"
           << "ax.scatter([0, t1], [N0, N1], color='black', zorder=5, label='Datos reales')\n"
           << "ax.scatter([t_prediccion], [N_curva[-1]], color='red', zorder=5, label='Prediccion')\n\n"
           << "ax.set_xlabel(f'Tiempo ({unidad})')\n"
           << "ax.set_ylabel('Numero de usuarios')\n"
           << "ax.set_title('Crecimiento de usuarios: modelo logistico (Solucion Analitica)')\n"
           << "ax.legend(loc='lower right')\n"
           << "ax.grid(alpha=0.3)\n\n"
           << "ax_r = plt.axes([0.15, 0.12, 0.7, 0.03])\n"
           << "ax_k = plt.axes([0.15, 0.06, 0.7, 0.03])\n\n"
           << "slider_r = Slider(ax_r, 'r', r * 0.2, r * 3, valinit=r)\n"
           << "slider_k = Slider(ax_k, 'K', K * 0.5, K * 1.5, valinit=K)\n\n"
           << "def actualizar(val):\n"
           << "    r_nuevo = slider_r.val\n"
           << "    K_nuevo = slider_k.val\n"
           << "    N_nueva = solucion_analitica(t_curva, N0, r_nuevo, K_nuevo)\n"
           << "    linea_analitica.set_ydata(N_nueva)\n"
           << "    linea_K.set_ydata([K_nuevo, K_nuevo])\n"
           << "    ax.relim()\n"
           << "    ax.autoscale_view()\n"
           << "    fig.canvas.draw_idle()\n\n"
           << "slider_r.on_changed(actualizar)\n"
           << "slider_k.on_changed(actualizar)\n\n"
           << "plt.show()\n";
           
    script.close();

    std::cout << "\n[INFO] Abriendo la ventana grafica interactiva...\n";
    
    // Ejecuta el script usando el Python del sistema
    int sistema_status = std::system("python temp_grafica.py");
    
    // Si falla 'python', intentamos con el comando 'py' por si acaso
    if (sistema_status != 0) {
        std::system("py temp_grafica.py");
    }
}

// 4) PROGRAMA PRINCIPAL
int main() {
    try {
        DatosEntrada datos = pedir_datos();

        // Calcular r inicial
        double r = calcular_r(datos.N0, datos.N1, datos.t1, datos.K);
        double t_prediccion = datos.t1 + datos.t_futuro;

        std::cout << "\n--- PARAMETROS DEL MODELO ---\n";
        std::cout << "Tasa de crecimiento r      = " << std::fixed << std::setprecision(6) << r << " (1/" << datos.unidad << ")\n";
        std::cout << "Capacidad de carga K       = " << std::fixed << std::setprecision(0) << datos.K << " usuarios\n";

        // Solución analítica en el instante pedido
        double N_analitica_pred = solucion_analitica(t_prediccion, datos.N0, r, datos.K);

        std::cout << "\n--- RESULTADOS DE LA PREDICCION ---\n";
        std::cout << "Dentro de " << datos.t_futuro << " " << datos.unidad << ", la app tendra aproximadamente:\n";
        std::cout << "  Solucion analitica (Exacta): " << N_analitica_pred << " usuarios\n";

        // Lanzar la gráfica
        graficar(datos.unidad, datos.t1, datos.N0, datos.N1, datos.K, r, datos.t_futuro);

    } catch (const std::exception& e) {
        std::cerr << "\nError: " << e.what() << "\n";
        return 1;
    }

    return 0;
}