'''
The main entrypoint for the XMARTe Runner application:
a service which provides a REST API to execute MARTe2 Configurations on remote machines.
'''
import threading
import os
import yaml
import uvicorn
from starlette.applications import Starlette

from xmarterunner.server import run_ftp, clean_dir, exception_handlers,routes


# Established our Root Directory from our Environment configuration or go to default
root_dir = os.environ.get("MARTEC_ROOTDIR", "/opt/xmarterunner")
try:
    with open(os.path.join(root_dir,'settings.yml'), 'r', encoding='utf-8') as infile:
        settings = yaml.safe_load(infile)
except FileNotFoundError:
    print("Error: settings.yml file not found.")
except IsADirectoryError:
    print("Error: settings.yml is a directory, not a file.")
except PermissionError:
    print("Error: Permission denied when accessing settings.yml.")
except OSError as e:
    print(f"OS error occurred: {e}")
except yaml.YAMLError as e:
    print(f"YAML syntax error: {e}")
except (UnicodeDecodeError, UnicodeError) as e:
    print(f"Invalid UTF-8 sequences detected in settings file: {e}")


app = Starlette(debug=True, routes=routes, exception_handlers=exception_handlers)

x = threading.Thread(target=run_ftp)
x.start()
x = threading.Thread(target=clean_dir)
x.start()

uvicorn.run(app, host='0.0.0.0', port=settings['http_port'],h11_max_incomplete_event_size=16777216)
