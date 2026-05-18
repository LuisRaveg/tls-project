
import subprocess
import csv

def limpiar_red():
    subprocess.run(
        "tc qdisc del dev eth0 root",
        shell=True,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL
    )

def aplicar_latencia(latencia):
    cmd = f"tc qdisc add dev eth0 root netem delay {latencia}ms"
    subprocess.run(cmd, shell=True, check=True)

def aplicar_perdida(porcentaje):
    cmd = f"tc qdisc add dev eth0 root netem loss {porcentaje}%"
    subprocess.run(cmd, shell=True, check=True)

def aplicar_jitter(latencia, jitter):
    subprocess.run(
        f"tc qdisc add dev eth0 root netem delay {latencia}ms {jitter}ms",
        shell=True,
        check=True
    )
def aplicar_escenario(delay, jitter, loss):
    cmd = f"tc qdisc add dev eth0 root netem delay {delay}ms {jitter}ms loss {loss}%"
    subprocess.run(cmd, shell=True, check=True)

def medir_tls():
    cmd = (
        'curl --connect-timeout 5 '
        '--tlsv1.3 --tls-max 1.3 '
        '-w "%{time_connect} %{time_appconnect} %{time_total} %{http_code}" '
        '-o /dev/null -s https://www.google.com'
    )

    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if r.returncode == 0:
        t_connect, t_tls, t_total, code = r.stdout.split()

        handshake = (float(t_tls) - float(t_connect)) * 1000

        return [
            float(t_connect),
            float(t_tls),
            round(handshake, 3),
            float(t_total),
            code,
            "OK"
        ]
    else:
        return [None, None, None, None, "000", "ERROR"]
def main(): 
    muestras = 50

    escenarios = [
        ("Servidor_Internacional", 200, 10, 0),
        ("WiFi_Publico", 80, 30, 3),
        ("Datos_Moviles", 100, 40, 1),
        ("Red_Degradada", 300, 50, 10)
    ]

    archivo = "dataset_tls.csv"

    with open(archivo, mode='w', newline='') as f:
        writer = csv.writer(f)

        # encabezados
        writer.writerow([
            "Variable", "Valor", "Iteracion",
            "time_connect", "time_appconnect",
            "handshake_ms", "time_total",
            "http_code", "status"
        ])
        # ========================
        #   EXPERIMENTO LATENCIA
        # ========================
        print("\n===== EXPERIMENTO: LATENCIA =====")

        niveles_latencia = [0, 50, 100, 200, 300]

        for lat in niveles_latencia:
                print(f"\nLatencia = {lat} ms")

                limpiar_red()
                aplicar_latencia(lat)

                for i in range(muestras):
                    datos = medir_tls()

                    fila = ["Latencia", lat, i+1] + datos
                    writer.writerow(fila)

        # ========================
        #   EXPERIMENTO PÉRDIDA
        # ========================
        print("\n===== EXPERIMENTO: PERDIDA =====")

        niveles_perdida = [0, 1, 3, 5, 10]

        for p in niveles_perdida:
                print(f"\nPerdida = {p}%")

                limpiar_red()
                aplicar_perdida(p)

                for i in range(muestras):
                    datos = medir_tls()

                    fila = ["Perdida", p, i+1] + datos
                    writer.writerow(fila)

        # ========================
        #   EXPERIMENTO JITTER
        # ========================
        print("\n===== EXPERIMENTO: JITTER =====")

        niveles_jitter = [0, 10, 20, 50]

        for jitter in niveles_jitter:
                print(f"\nJitter = {jitter} ms")

                limpiar_red()
                aplicar_jitter(100, jitter)

                for i in range(muestras):
                    datos = medir_tls()

                    fila = ["Jitter", jitter, i+1] + datos
                    writer.writerow(fila)

        print("\n===== EXPERIMENTO: ESCENARIOS REALES =====")

        for nombre, delay, jitter, loss in escenarios:
            print(f"\n--- Escenario: {nombre} ---")

            limpiar_red()
            aplicar_escenario(delay, jitter, loss)

            for i in range(muestras):
                datos = medir_tls()

                fila = [nombre, f"{delay}-{jitter}-{loss}", i+1] + datos
                writer.writerow(fila)

    limpiar_red()
    print("\n Datos guardados en dataset_tls.csv")

if __name__ == "__main__":
    main()