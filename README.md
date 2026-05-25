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

### Ubuntu / WSL

Los siguientes scripts deben ejecutarse en Ubuntu o WSL:

- `m_protocolo_1_2.py`
- `m_protocolo_1_3.py`

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

### macOS

Los siguientes scripts deben ejecutarse en una Mac:

- `experimentoTLS_1_2_mac.py`
- `experimentoTLS_1_3_mac.py`

Herramientas necesarias:

- Python 3
- curl
```

---

## Estructura del Repositorio

```text
tls-project/
├── Mediciones_Linux_tls_1_2.csv
├── Mediciones_Linux_tls_1_3.csv
├── Proyecto_TLS.ipynb
├── README.md
├── dataset_tls_1_2_mac_open.csv
├── dataset_tls_1_3_mac_open.csv
├── experimentoTLS_1_2_mac.py
├── experimentoTLS_1_3_mac.py
├── m_protocolo_1_2.py
└── m_protocolo_1_3.py
```

---

## Clonar el Repositorio

```bash
git clone https://github.com/LuisRaveg/tls-project.git
cd tls-project
```

---

## Ejecutar Experimentos en Ubuntu / WSL

### Ejecutar Experimento TLS 1.2

```bash
sudo python3 m_protocolo_1_2.py
```

Genera:

```text
Mediciones_Linux_tls_1_2.csv
```

---

### Ejecutar Experimento TLS 1.3

```bash
sudo python3 m_protocolo_1_3.py
```

Genera:

```text
Mediciones_Linux_tls_1_3.csv
```

---

## Ejecutar Experimentos en macOS

### Ejecutar Experimento TLS 1.2

```bash
python3 experimentoTLS_1_2_mac.py
```

Genera:

```text
dataset_tls_1_2_mac_open.csv
```

---

### Ejecutar Experimento TLS 1.3

```bash
python3 experimentoTLS_1_3_mac.py
```

Genera:

```text
dataset_tls_1_3_mac_open.csv
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

Desde Ubuntu / WSL:

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

Los scripts de Ubuntu/WSL requieren permisos `sudo` porque `tc netem` modifica configuraciones de red a nivel de kernel.

Los scripts de macOS realizan mediciones desde una Mac utilizando `curl`.

El análisis y visualización de resultados puede realizarse desde:

```text
Proyecto_TLS.ipynb
```

---

## Referencias

Performance Evaluation of SSL/TLS Handshake Latency in Distributed Web Service Architectures. (2025). International Journal Of Communication And Computer Technologies, 13(2). https://doi.org/10.31838/ijccts.13.02.05

Jonker, A., & Krantz, T. (2025, 26 noviembre). Transport Layer Security. IBM. https://www.ibm.com/mx-es/think/topics/transport-layer-security

What happens in a TLS Handshake? | Cloudflare. (n.d.). https://www.cloudflare.com/es-es/learning/ssl/what-happens-in-a-tls-handshake/

Amaya, J. R. (2025, 23 diciembre). Entendiendo la Fortaleza de Una Suite de Cifrado. ISecAuditors. https://blog.isecauditors.com/entendiendo-la-fortaleza-de-una-suite-de-cifrado
