from celery import Celery
import time

# Configuramos Celery usando Redis como buzón (broker)
celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0" # Para guardar el resultado
)

@celery_app.task
def slow_task(name):
    """Esta es la tarea que ejecutará el worker en segundo plano."""
    print(f"Iniciando tarea pesada para: {name}")
    time.sleep(10)  # Simula un proceso de 10 segundos
    return f"¡Tarea completada para {name}!"