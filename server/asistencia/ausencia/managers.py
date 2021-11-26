from ...operaciones.bitacora.managers import *
from ...configuraciones.empresa.managers import EmpresaManager
from ...asistencia.asistenciapersonal.models import *
from ...asistencia.tipoausencia.models import *
from ...usuarios.ajustes.models import *
from ...personal.organigrama.managers import *
from ...notificaciones.correo.managers import *

from server.common.managers import SuperManager
from .models import *

from sqlalchemy.sql import func, and_
from datetime import datetime

