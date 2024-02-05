import sys
import os

# Activate your virtual environment
activate_this = '/home/ubuntu/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Add the app's directory to the PYTHONPATH
project_home = '/home/ubuntu'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

from flaskapp import app as application  # noqa

if __name__ == "__main__":
    application.run()
