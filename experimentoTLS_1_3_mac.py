import subprocess
import csv


PF_CONF = "pf_tls.conf"
URL = "https://www.google.com"

CURL = "/opt/homebrew/opt/curl/bin/curl"

def crear_pf_conf():
    """
    Crea el archivo de reglas de pf que redirige el trafico TCP
    del puerto 443 (HTTPS) hacia el pipe de dummynet.
    """
    reglas = (
        "dummynet in quick proto tcp from any to any port 443 pipe 1\n"
        "dummynet out quick proto tcp from any to any port 443 pipe 1\n"
    )
    with open(PF_CONF, "w") as f:
        f.write(reglas)

def limpiar_red():
    """
    Apaga pf y limpia los pipes de dummynet.
    """
    subprocess.run("sudo pfctl -d", shell=True,
                   stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    subprocess.run("sudo dnctl -q flush", shell=True,
                   stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def aplicar_red(latencia=0, perdida=0):
    """
    Configura un pipe de dummynet con la latencia y perdida indicadas.
    NOTA: dnctl en macOS NO soporta jitter real como netem en Linux.
    Cuando se simula jitter, se aplica solo el delay base.
    """
    plr = perdida / 100.0

    subprocess.run("sudo dnctl -q flush", shell=True,
                   stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    subprocess.run(
        f"sudo dnctl pipe 1 config delay {latencia}ms plr {plr}",
        shell=True, check=True
    )

    subprocess.run(f"sudo pfctl -f {PF_CONF}", shell=True,
                   stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    subprocess.run("sudo pfctl -e", shell=True,
                   stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def medir_tls():
    """
    Mide tiempos de conexion TCP, handshake TLS 1.3 y total con curl.
    """
    cmd = (
        f'{CURL} --connect-timeout 5 '
        f'--tlsv1.3 '
        f'-w "%{{time_connect}} %{{time_appconnect}} %{{time_total}} %{{http_code}}" '
        f'-o /dev/null -s {URL}'
    )

    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if r.returncode == 0 and r.stdout.strip():
        try:
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
        except ValueError:
            return [None, None, None, None, "000", "ERROR"]
    return [None, None, None, None, "000", "ERROR"]

def main():
    muestras = 50
    archivo = "dataset_tls_1_3_mac.csv"

    crear_pf_conf()
    limpiar_red()

    with open(archivo, mode='w', newline='') as f:
        writer = csv.writer(f)

        writer.writerow([
            "SO", "Fase", "Variable_o_Escenario", "Valor_o_Latencia",
            "Jitter_ms", "Perdida_pct", "TLS", "Iteracion",
            "time_connect", "time_appconnect", "handshake_ms",
            "time_total", "http_code", "status"
        ])

        print("\nFASE 1: PARAMETROS INDIVIDUALES")

        print("\nVariable: LATENCIA")
        niveles_latencia = [0, 50, 100, 200, 300]
        for lat in niveles_latencia:
            print(f"\nLatencia = {lat} ms")
            aplicar_red(latencia=lat, perdida=0)
            for i in range(muestras):
                datos = medir_tls()
                fila = ["macOS", "Parametro", "Latencia", lat, 0, 0, "tls13", i + 1] + datos
                writer.writerow(fila)
                print(f"  Muestra {i+1}/{muestras} -> handshake={datos[2]} ms")

        print("\nVariable: PERDIDA")
        niveles_perdida = [0, 1, 3, 5, 10]
        for p in niveles_perdida:
            print(f"\nPerdida = {p}%")
            aplicar_red(latencia=0, perdida=p)
            for i in range(muestras):
                datos = medir_tls()
                fila = ["macOS", "Parametro", "Perdida", p, 0, p, "tls13", i + 1] + datos
                writer.writerow(fila)
                print(f"  Muestra {i+1}/{muestras} -> handshake={datos[2]} ms")

        print("\nVariable: JITTER")
        print("(Nota: dnctl no simula jitter real en Mac, se registra como metadato)")
        niveles_jitter = [0, 10, 20, 50]
        for jitter in niveles_jitter:
            print(f"\nJitter = {jitter} ms (con latencia base 100ms)")
            aplicar_red(latencia=100, perdida=0)
            for i in range(muestras):
                datos = medir_tls()
                fila = ["macOS", "Parametro", "Jitter", jitter, jitter, 0, "tls13", i + 1] + datos
                writer.writerow(fila)
                print(f"  Muestra {i+1}/{muestras} -> handshake={datos[2]} ms")

        print("\nFASE 2: ESCENARIOS COMBINADOS")

        escenarios = [
            ("Servidor_Internacional", 200, 10, 0),
            ("WiFi_Publico", 80, 30, 3),
            ("Datos_Moviles", 100, 40, 1),
            ("Red_Degradada", 300, 50, 10)
        ]

        for nombre, lat, jitter, perdida in escenarios:
            print(f"\nEscenario: {nombre}")
            print(f"Latencia={lat}ms | Jitter={jitter}ms | Perdida={perdida}%")
            aplicar_red(latencia=lat, perdida=perdida)
            for i in range(muestras):
                datos = medir_tls()
                fila = ["macOS", "Escenario", nombre, lat, jitter, perdida, "tls13", i + 1] + datos
                writer.writerow(fila)
                print(f"  Muestra {i+1}/{muestras} -> handshake={datos[2]} ms")

    limpiar_red()
    print(f"\nListo. Datos guardados en {archivo}")

if __name__ == "__main__":
    main()
