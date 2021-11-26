from server.database.connection import transaction
from ..usuarios.rol.models import *
from ..usuarios.usuario.models import *
from ..comensales.menu.models import *
from datetime import datetime


def insertions():
    with transaction() as session:

        ###Modulo de Operaciones

        calendario_m = session.query(Modulo).filter(Modulo.name == 'calendario').first()
        if calendario_m is None:
            calendario_m = Modulo(title='Calendario', name='calendario', icon='calendar.png')

        feriado_m = session.query(Modulo).filter(Modulo.name == 'feriado').first()
        if feriado_m is None:
            feriado_m = Modulo(title='Feriados', route='/feriado', name='feriado', icon='libre.png')

        calendario_m.children.append(feriado_m)

        query_feriado = session.query(Modulo).filter(Modulo.name == 'feriado_query').first()
        if query_feriado is None:
            query_feriado = Modulo(title='Consultar', route='',
                                   name='feriado_query',
                                   menu=False)

        insert_feriado = session.query(Modulo).filter(Modulo.name == 'feriado_insert').first()
        if insert_feriado is None:
            insert_feriado = Modulo(title='Adicionar', route='/feriado_insert',
                                    name='feriado_insert',
                                    menu=False)
        update_feriado = session.query(Modulo).filter(Modulo.name == 'feriado_update').first()
        if update_feriado is None:
            update_feriado = Modulo(title='Actualizar', route='/feriado_update',
                                    name='feriado_update',
                                    menu=False)
        delete_feriado = session.query(Modulo).filter(Modulo.name == 'feriado_delete').first()
        if delete_feriado is None:
            delete_feriado = Modulo(title='Dar de Baja', route='/feriado_delete',
                                    name='feriado_delete',
                                    menu=False)

        imprimir_feriado = session.query(Modulo).filter(Modulo.name == 'feriado_imprimir').first()
        if imprimir_feriado is None:
            imprimir_feriado = Modulo(title='Imprimir', route='/feriado_imprimir',
                                      name='feriado_imprimir',
                                      menu=False)

        feriado_m.children.append(query_feriado)
        feriado_m.children.append(insert_feriado)
        feriado_m.children.append(update_feriado)
        feriado_m.children.append(delete_feriado)
        feriado_m.children.append(imprimir_feriado)

        admin_role = session.query(Rol).filter(Rol.nombre == 'SUPER ADMINISTRADOR').first()

        ###Modulos de Operaciones

        admin_role.modulos.append(calendario_m)
        admin_role.modulos.append(feriado_m)

        admin_role.modulos.append(query_feriado)
        admin_role.modulos.append(insert_feriado)
        admin_role.modulos.append(update_feriado)
        admin_role.modulos.append(delete_feriado)
        admin_role.modulos.append(imprimir_feriado)

        session.commit()
