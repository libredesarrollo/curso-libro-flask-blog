
import sys
import types

# --- PARCHE DE COMPATIBILIDAD PARA PYTHON 3.13 (Remoción de pkg_resources) --- Flask seeder
# try:
#     import pkg_resources
# except ModuleNotFoundError:
#     # Creamos un módulo vacío en memoria para que el import de flask_seeder no rompa
#     mock_pkg = types.ModuleType("pkg_resources")
#     sys.modules["pkg_resources"] = mock_pkg

# --- PARCHE GLOBAL PARA PYTHON 3.13 ---
if "pkg_resources" not in sys.modules:
    mock_pkg = types.ModuleType("pkg_resources")
    sys.modules["pkg_resources"] = mock_pkg
# --------------------------------------

from my_app import app


if __name__ == '__main__':
    app.run(debug=True)

#python run.py


#celery -A my_app.tasks.celery_app worker --loglevel=info
