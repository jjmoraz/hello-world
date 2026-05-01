# hello-world
Primer prueba de mi experiencia GitHub
Estoy interesado en aprender la nueva era de programación

## Juego de Asteroids

Este repositorio incluye un juego simple inspirado en **Asteroids** de Atari 2600.
El archivo `asteroids.py` utiliza la biblioteca [Pygame](https://www.pygame.org/) para
simular la nave, los asteroides y los disparos.

## ¿Cómo lo ejecuto?

### 1) Verifica tu versión de Python
```bash
python3 --version
```
Necesitas Python **3.11 o superior**.

### 2) (Opcional, recomendado) Crea un entorno virtual
```bash
python3 -m venv .venv
source .venv/bin/activate
```

En Windows (PowerShell):
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3) Instala Pygame
```bash
python3 -m pip install pygame
```

### 4) Ejecuta el juego
Desde la raíz del repositorio:
```bash
python3 asteroids.py
```

## Controles
- Flecha izquierda/derecha: girar nave
- Flecha arriba: acelerar
- Barra espaciadora: disparar

Si tu nave choca con un asteroide, el juego termina.
