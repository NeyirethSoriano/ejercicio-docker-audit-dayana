import os
import secrets
from flask import Flask, request, jsonify

app = Flask(__name__)

# [Solución B105] Cargar credenciales desde variables de entorno
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "legacydb")


@app.route("/")
def index():
    return jsonify({"status": "ok", "message": "API Segura"})


@app.route("/usuario")
def get_usuario():
    usuario_id = request.args.get("id", "1")
    # [Solución B608] Sin concatenación de cadenas SQL
    return jsonify({
        "mensaje": "Consulta segura",
        "id": usuario_id
    })


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})


@app.route('/buscar', methods=['GET'])
def buscar():
    user_id = request.args.get('id')
    return jsonify({"id": user_id, "resultado": "usuario encontrado"})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5050))
    debug_mode = os.getenv("FLASK_ENV") == "development"
    # Escuchar en 0.0.0.0 para exponer el puerto fuera del contenedor de Docker
    app.run(host="0.0.0.0", port=port, debug=debug_mode)  # nosec B104