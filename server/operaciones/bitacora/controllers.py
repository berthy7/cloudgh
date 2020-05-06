from ..bitacora.managers import *
from server.common.controllers import CrudController


class BitacoraController(CrudController):

    manager = BitacoraManager
    html_index = "operaciones/bitacora/views/index.html"
    html_table = "operaciones/bitacora/views/table.html"
    routes = {
        '/bitacora': {'GET': 'index', 'POST': 'table'}
    }
