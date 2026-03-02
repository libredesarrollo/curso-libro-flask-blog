from flask import Blueprint, jsonify
from my_app.tasks import slow_task

# Definimos un Blueprint para las rutas relacionadas con Celery
celery_bp = Blueprint('celery_views', __name__)

@celery_bp.route("/run-task/<name>", methods=["POST", "GET"])
def run_background_task(name):
    # .delay() le dice a Python: "No ejecutes esto aquí, mándalo al worker"
    # Esto es asíncrono: Flask responde inmediatamente al usuario.
    task = slow_task.delay(name)
    
    return jsonify({
        "message": "Tarea recibida y enviada al sótano",
        "task_id": task.id
    })
