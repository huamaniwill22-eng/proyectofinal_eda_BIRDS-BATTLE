Birds Battle 🐦🎯
Videojuego de físicas en Python (Pygame). Lanza aves con habilidades únicas para destruir estructuras y derrotar enemigos en 10 niveles progresivos, con motor físico propio y guardado de progreso local.

🚀 Características
Motor Físico Personalizado: Simulación de gravedad, trayectorias parabólicas, fricción y sistema de colisiones con detección de geometría.

Sistema de Destrucción: Estructuras formadas por bloques de Madera, Cristal y Piedra, cada uno con diferentes resistencias, reacciones físicas y puntajes.

Escuadrón de Aves: 5 personajes jugables con mecánicas únicas:

Red: Ave estándar y equilibrada.

Speed: Impulso de velocidad en el aire.

Bomb: Cae en picada y genera una explosión en área.

Split: Se divide en tres aves más pequeñas durante el vuelo.

Giant: Ave masiva con gran poder de impacto y destrucción.

Progresión: 10 niveles integrados con aumento de dificultad y sistema de clasificación por estrellas (⭐).

Persistencia de Datos: Guardado automático local (save.json) de niveles desbloqueados y puntajes máximos.

Efectos Visuales: Sistema de partículas dinámicas para destrucción de bloques, explosiones e impactos.

💻 Tecnologías Utilizadas
Lenguaje: Python 3.x

Librerías:

pygame (Renderizado gráfico, eventos y sonido)

math, random, json, os, sys (Módulos estándar de Python)

🛠️ Instalación y Ejecución
Clonar el repositorio:

Bash
git clone https://github.com/TU_USUARIO/BirdsBattle.git
cd BirdsBattle
Instalar la dependencia principal (Pygame):

Bash
pip install pygame
Ejecutar el juego:

Bash
python main.py
(Nota: El juego generará automáticamente la carpeta de niveles y configuraciones iniciales al ejecutarse por primera vez).

🎮 Controles
Ratón (Click Izquierdo Mantener y Arrastrar): Tensar la resortera, apuntar y medir la potencia guiándote por la línea de trayectoria.

Ratón (Soltar Click): Lanzar el ave.

Ratón (Click Izquierdo durante el vuelo): Activar la habilidad especial del ave (Speed, Bomb, Split).

Tecla ESC: Abrir el menú de pausa.

📂 Estructura del Proyecto
El código está implementado utilizando Programación Orientada a Objetos (POO) y modularizado para facilitar su escalabilidad:

main.py: Bucle principal y gestor de estados.

game.py: Lógica principal del nivel, colisiones y físicas.

physics.py / particles.py: Motor matemático y efectos visuales.

bird.py / block.py / enemy.py: Entidades del juego.

level.py: Gestor procedural y lector de niveles JSON.

menu.py / ui.py: Interfaces gráficas, botones y guardado.
