# Pipeline Experimental TLS

## Descripción General

Este proyecto evalúa y compara el rendimiento de TLS 1.2 y TLS 1.3 bajo distintas condiciones de red simuladas utilizando `tc netem` en Linux y solicitudes HTTPS realizadas con `curl`.

El experimento mide:

- Tiempo de conexión TCP
- Tiempo de handshake TLS
- Tiempo total de la solicitud HTTPS
- Código de respuesta HTTP

El objetivo es analizar cómo la latencia, la pérdida de paquetes y el jitter afectan el desempeño de conexiones seguras TLS.

Los resultados generados se almacenan en archivos CSV para su posterior análisis estadístico y comparación entre TLS 1.2 y TLS 1.3.

---

## Condiciones de Red Simuladas

El pipeline evalúa el comportamiento de TLS bajo:

- Latencia variable
- Pérdida de paquetes
- Jitter
- Escenarios de red realistas:
  - WiFi público
  - Datos móviles
  - Servidor internacional
  - Red degradada

---

## Requisitos

El proyecto fue desarrollado y ejecutado en Ubuntu/WSL utilizando Python 3.

Herramientas necesarias:

- Python 3
- curl
- `tc` (traffic control de Linux)
- permisos sudo

Instalación de dependencias:

```bash
sudo apt update
sudo apt install -y python3 curl iproute2
```

---

## Estructura del Repositorio

```text
tls-project/
├── experimento.py
├── experimentoTLS_1_2.py
├── dataset_tls.csv
├── dataset_tls_1_2.csv
```

---

## Clonar el Repositorio

```bash
git clone https://github.com/LuisRaveg/tls-project.git
cd tls-project
```

---

## Ejecutar Experimento TLS 1.2

```bash
sudo python3 experimentoTLS_1_2.py
```

Genera:

```text
dataset_tls_1_2.csv
```

---

## Ejecutar Experimento TLS 1.3

```bash
sudo python3 experimento.py
```

Genera:

```text
dataset_tls.csv
```

---

## Resultados Generados

Los scripts generan archivos CSV con las métricas experimentales obtenidas.

Ejemplo de columnas:

- `time_connect`
- `time_appconnect`
- `handshake_ms`
- `time_total`
- `http_code`

---

## Ver los Archivos CSV

Desde Ubuntu:

```bash
ls *.csv
```

Abrir la carpeta del proyecto en el explorador de Windows desde WSL:

```bash
explorer.exe .
```

---

## Metodología

El experimento utiliza:

- `tc netem` para simular condiciones de red
- `curl` forzado a utilizar TLS 1.2 o TLS 1.3
- múltiples ejecuciones por escenario para obtener resultados consistentes

Cada escenario se ejecuta varias veces con el fin de reducir ruido experimental y obtener mediciones representativas.

---

## Notas

Los scripts requieren permisos `sudo` porque `tc netem` modifica configuraciones de red a nivel de kernel.

El proyecto fue probado en Ubuntu utilizando WSL.
