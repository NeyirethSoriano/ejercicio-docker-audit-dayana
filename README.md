# Reporte de Auditoría de Seguridad con Bandit

## Resumen de la Auditoría
- **Líneas de código analizadas:** 34
- **Archivos analizados:** `app.py`, `test_app.py`
- **Total de vulnerabilidades encontradas:** 6
  - **Severidad Alta:** 1
  - **Severidad Media:** 2
  - **Severidad Baja:** 3

---

## Detalle de Vulnerabilidades y Soluciones

### 1. [B201] Modo Debug de Flask Activado
- **Severidad:** Alta | **Confianza:** Media
- **Ubicación:** `app.py` (Línea 35)
- **Descripción:** Ejecutar Flask con `debug=True` en producción expone la consola interactiva Werkzeug, lo que permite a un atacante ejecutar código arbitrario de manera remota (RCE).
- **Solución:**
  Desactivar el modo debug o parametrizarlo mediante variables de entorno para que solo se active en desarrollo.
  ```python
  debug_mode = os.getenv("FLASK_ENV") == "development"
  app.run(host="0.0.0.0", port=port, debug=debug_mode)

### 2 [B608] Inyección SQL por Concatenación de Strings
Severidad: Media | Confianza: Baja

Ubicación: app.py (Línea 25)

Descripción: Concatenar parámetros ingresados por el usuario directamente en una consulta SQL permite que un atacante altere la lógica de la base de datos (Inyección SQL).

Solución:
Evitar la concatenación manual y utilizar consultas parametrizadas o un ORM (como SQLAlchemy).

# Consulta segura usando parámetros
cursor.execute("SELECT * FROM usuarios WHERE id = %s", (usuario_id,))

### 3 [B104] Exposición en Todas las Interfaces de Red
Severidad: Media | Confianza: Media

Ubicación: app.py (Línea 35)

Descripción: Configurar host='0.0.0.0' expone la aplicación directamente a todas las redes públicas y privadas de la máquina sin restricciones.

Solución:
Parametrizar el puerto/host e integrar un proxy inverso (Nginx) enfrente de la aplicación en la fase de arquitectura.


### 4 [B105] Credenciales Expuestas en Código (Hardcoded Password)
Severidad: Baja | Confianza: Media

Ubicación: app.py (Línea 10)

Descripción: Almacenar claves o contraseñas en texto plano dentro del código fuente facilita la filtración de credenciales en repositorios como GitHub.

Solución:
Cargar las credenciales mediante un archivo de configuración .env y variables de entorno.

DB_PASS = os.getenv("DB_PASS")

### 5. [B311] Generador de Números Pseudoaleatorios Inseguro
Severidad: Baja | Confianza: Alta

Ubicación: app.py (Línea 30)

Descripción: El uso del módulo estándar random no es criptográficamente seguro y sus valores pueden ser predichos.

Solución:
Utilizar el módulo secrets estándar de Python para operaciones donde la aleatoriedad sea crítica.

import secrets
if secrets.randbelow(100) < 5:
    ...

### 6. [B101] Uso de Sentencias assert
Severidad: Baja | Confianza: Alta

Ubicación: test_app.py (Línea 7)

Descripción: Las sentencias assert se eliminan automáticamente cuando Python compila a bytecode optimizado (-O), dejando sin efecto las comprobaciones en producción.

Solución:
En archivos de pruebas unitarias (test_app.py), el uso de assert con pytest es aceptable. Para código de producción en app.py, se deben usar validaciones con condicionales if y excepciones explícitas.

Cómo Re-ejecutar el Análisis Localmente
Para generar nuevamente el reporte excluyendo librerías externas o entornos virtuales:

bandit -r . -x ./.venv -f html -o reporte_bandit.html



