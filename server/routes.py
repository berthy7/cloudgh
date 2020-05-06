import os

from .usuarios.usuario.controllers import *
from .usuarios.rol.controllers import *
from .usuarios.login.controllers import *
from .usuarios.ajustes.controllers import *

from .calendario.feriado.controllers import *


from .asistencia.turno.controllers import *
from .asistencia.horario.controllers import *
from .asistencia.asistenciapersonal.controllers import *
from .asistencia.asignacion.controllers import *
from .asistencia.tipoausencia.controllers import *
from .asistencia.ausencia.controllers import *
from .asistencia.politicas.controllers import *
from .asistencia.autorizacionextra.controllers import *

from .vacaciones.personal.controllers import *
from .vacaciones.antiguedad.controllers import *
from .vacaciones.historico.controllers import *


from server.operaciones.bitacora.controllers import *

from .comensales.menu.controllers import *
from .comensales.pedido.controllers import *

from .dispositivos.lectores.controllers import *
from .dispositivos.marcaciones.controllers import *

from .configuraciones.pais.controllers import *
from .configuraciones.centro_costo.controllers import *
from .configuraciones.empresa.controllers import *
from .configuraciones.gerencia.controllers import *
from .configuraciones.cargo.controllers import *
from .configuraciones.departamento.controllers import *
from .configuraciones.ciudad.controllers import *
from .configuraciones.sucursal.controllers import *
from .configuraciones.oficina.controllers import *

from .notificaciones.correo.controllers import *
from .notificaciones.correo_rrhh.controllers import *

from .control.tarea.controllers import *
from .control.proyecto.controllers import *

from .portal.ausencia.controllers import *
from .portal.marcaciones.controllers import *
from .portal.pedido.controllers import *
from .portal.tarea.controllers import *

from server.personal.persona.controllers import *
from server.personal.organigrama.controllers import *

from .main.controllers import Index
from tornado.web import StaticFileHandler


def get_handlers():
    """Retorna una lista con las rutas, sus manejadores y datos extras."""
    handlers = list()
    # Login
    handlers.append((r'/login', LoginController))
    handlers.append((r'/logout', LogoutController))
    handlers.append((r'/manual', ManualController))

    # Principal
    handlers.append((r'/', Index))

    # Usuario
    handlers.extend(get_routes(UsuarioController))
    handlers.extend(get_routes(RolController))
    handlers.extend(get_routes(AjustesController))

    # Calendario
    handlers.extend(get_routes(FeriadoController))

    # Asistencia
    handlers.extend(get_routes(TurnoController))
    handlers.extend(get_routes(HorarioController))
    handlers.extend(get_routes(AsignacionController))
    handlers.extend(get_routes(AsistenciaController))
    handlers.extend(get_routes(PoliticasController))
    handlers.extend(get_routes(TipoausenciaController))
    handlers.extend(get_routes(AusenciaController))
    handlers.extend(get_routes(AutorizacionextraController))

    # Vacaciones
    handlers.extend(get_routes(V_personalController))
    handlers.extend(get_routes(V_antiguedadController))

    # Operaciones
    handlers.extend(get_routes(BitacoraController))

    # Comensales
    handlers.extend(get_routes(MenuController))
    handlers.extend(get_routes(PedidoController))

    # Dispositivos
    handlers.extend(get_routes(LectoresController))
    handlers.extend(get_routes(MarcacionesController))

    # Personal
    handlers.extend(get_routes(PersonaController))
    handlers.extend(get_routes(OrganigramaController))

    # Control de tareas
    handlers.extend(get_routes(ProyectoController))
    handlers.extend(get_routes(TareaController))

    # Portal del Empleado
    handlers.extend(get_routes(PortalAusenciaController))
    handlers.extend(get_routes(PortalMarcacionesController))
    handlers.extend(get_routes(PortalPedidoController))
    handlers.extend(get_routes(PortalTareaController))

    # Configuraciones
    handlers.extend(get_routes(PaisController))
    handlers.extend(get_routes(Centro_costoController))
    handlers.extend(get_routes(EmpresaController))
    handlers.extend(get_routes(GerenciaController))
    handlers.extend(get_routes(CargoController))
    handlers.extend(get_routes(DepartamentoController))
    handlers.extend(get_routes(CiudadController))
    handlers.extend(get_routes(SucursalController))
    handlers.extend(get_routes(OficinaController))


    # Notificaciones
    handlers.extend(get_routes(CorreoController))
    handlers.extend(get_routes(CorreorrhhController))

    # Recursos por submodulo
    handlers.append((r'/resources/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'common', 'resources')}))

    handlers.append((r'/common/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'common', 'assets')}))
    handlers.append((r'/main/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'main', 'assets')}))
    handlers.append((r'/calendario/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'calendario')}))
    handlers.append((r'/asistencia/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'asistencia')}))
    handlers.append((r'/vacaciones/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'vacaciones')}))
    handlers.append((r'/comensales/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'comensales')}))
    handlers.append((r'/dispositivos/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'dispositivos')}))
    handlers.append((r'/configuraciones/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'configuraciones')}))
    handlers.append((r'/operaciones/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'operaciones')}))
    handlers.append((r'/personal/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'personal')}))
    handlers.append((r'/usuarios/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'usuarios')}))
    handlers.append((r'/control/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'control')}))
    handlers.append((r'/notificaciones/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'notificaciones')}))
    handlers.append((r'/portal/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'portal')}))

    return handlers


def get_routes(handler):
    routes = list()
    for route in handler.routes:
        routes.append((route, handler))
    return routes
