import os
from datetime import date

from starlette.templating import Jinja2Templates

from fastapi_monitor import VERSION
from fastapi_monitor.constants import BASE_DIR

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
templates.env.globals["VERSION"] = VERSION
templates.env.globals["NOW_YEAR"] = date.today().year
templates.env.add_extension("jinja2.ext.i18n")
templates.env.add_extension("jinja2.ext.autoescape")
