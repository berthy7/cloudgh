from server.database.connection import transaction
from ..usuarios.rol.models import *
from ..usuarios.usuario.models import *
from ..comensales.menu.models import *
from datetime import datetime


def insertions():
    with transaction() as session:

        ###Modulo de Operaciones

        comensal_m = session.query(Modulo).filter(Modulo.name == 'comensal').first()
        if comensal_m is None:
            comensal_m = Modulo(title='Comensales', name='comensal', icon='comensal.png')

        menu_m = session.query(Modulo).filter(Modulo.name == 'menu').first()
        if menu_m is None:
            menu_m = Modulo(title='Menú', route='/menu', name='menu', icon='menu.png')

        pedido_m = session.query(Modulo).filter(Modulo.name == 'pedido').first()
        if pedido_m is None:
            pedido_m = Modulo(title='Pedidos', route='/pedido', name='pedido', icon='pedido.png')

        comensal_m.children.append(menu_m)
        comensal_m.children.append(pedido_m)

        query_menu = session.query(Modulo).filter(Modulo.name == 'menu_query').first()
        if query_menu is None:
            query_menu = Modulo(title='Consultar', route='',
                                name='menu_query',
                                menu=False)

        insert_menu = session.query(Modulo).filter(Modulo.name == 'menu_insert').first()
        if insert_menu is None:
            insert_menu = Modulo(title='Adicionar', route='/menu_insert',
                                 name='menu_insert',
                                 menu=False)
        update_menu = session.query(Modulo).filter(Modulo.name == 'menu_update').first()
        if update_menu is None:
            update_menu = Modulo(title='Actualizar', route='/menu_update',
                                 name='menu_update',
                                 menu=False)
        delete_menu = session.query(Modulo).filter(Modulo.name == 'menu_delete').first()
        if delete_menu is None:
            delete_menu = Modulo(title='Dar de Baja', route='/menu_delete',
                                 name='menu_delete',
                                 menu=False)

        imprimir_menu = session.query(Modulo).filter(Modulo.name == 'menu_imprimir').first()
        if imprimir_menu is None:
            imprimir_menu = Modulo(title='Imprimir', route='/menu_imprimir',
                                   name='menu_imprimir',
                                   menu=False)
            
        query_menu_plato = session.query(Modulo).filter(Modulo.name == 'menu_plato_query').first()
        if query_menu_plato is None:
            query_menu_plato = Modulo(title='Consultar Platos', route='',
                                name='menu_plato_query',
                                menu=False)

        insert_menu_plato = session.query(Modulo).filter(Modulo.name == 'menu_plato_insert').first()
        if insert_menu_plato is None:
            insert_menu_plato = Modulo(title='Adicionar Platos', route='/menu_plato_insert',
                                 name='menu_plato_insert',
                                 menu=False)
        update_menu_plato = session.query(Modulo).filter(Modulo.name == 'menu_plato_update').first()
        if update_menu_plato is None:
            update_menu_plato = Modulo(title='Actualizar Platos', route='/menu_plato_update',
                                 name='menu_plato_update',
                                 menu=False)
        delete_menu_plato = session.query(Modulo).filter(Modulo.name == 'menu_plato_delete').first()
        if delete_menu_plato is None:
            delete_menu_plato = Modulo(title='Dar de Baja Platos', route='/menu_plato_delete',
                                 name='menu_plato_delete',
                                 menu=False)

        imprimir_menu_plato = session.query(Modulo).filter(Modulo.name == 'menu_plato_imprimir').first()
        if imprimir_menu_plato is None:
            imprimir_menu_plato = Modulo(title='Imprimir Platos', route='/menu_plato_imprimir',
                                   name='menu_plato_imprimir',
                                   menu=False)

        menu_m.children.append(query_menu)
        menu_m.children.append(insert_menu)
        menu_m.children.append(update_menu)
        menu_m.children.append(delete_menu)
        menu_m.children.append(imprimir_menu)
    
        menu_m.children.append(query_menu_plato)
        menu_m.children.append(insert_menu_plato)
        menu_m.children.append(update_menu_plato)
        menu_m.children.append(delete_menu_plato)
        menu_m.children.append(imprimir_menu_plato)

        query_pedido = session.query(Modulo).filter(Modulo.name == 'pedido_query').first()
        if query_pedido is None:
            query_pedido = Modulo(title='Consultar', route='',
                                  name='pedido_query', menu=False)

        insert_pedido = session.query(Modulo).filter(Modulo.name == 'pedido_insert').first()
        if insert_pedido is None:
            insert_pedido = Modulo(title='Adicionar', route='/pedido_insert',
                                   name='pedido_insert', menu=False)
        update_pedido = session.query(Modulo).filter(Modulo.name == 'pedido_update').first()
        if update_pedido is None:
            update_pedido = Modulo(title='Actualizar', route='/pedido_update',
                                   name='pedido_update', menu=False)
        delete_pedido = session.query(Modulo).filter(Modulo.name == 'pedido_delete').first()
        if delete_pedido is None:
            delete_pedido = Modulo(title='Dar de Baja', route='/pedido_delete',
                                   name='pedido_delete',
                                   menu=False)

        imprimir_pedido = session.query(Modulo).filter(Modulo.name == 'pedido_imprimir').first()
        if imprimir_pedido is None:
            imprimir_pedido = Modulo(title='Imprimir', route='/pedido_imprimir',
                                     name='pedido_imprimir', menu=False)

        pedido_m.children.append(query_pedido)
        pedido_m.children.append(insert_pedido)
        pedido_m.children.append(update_pedido)
        pedido_m.children.append(delete_pedido)
        pedido_m.children.append(imprimir_pedido)

        admin_role = session.query(Rol).filter(Rol.nombre == 'SUPER ADMINISTRADOR').first()

        ###Modulos de Operaciones

        admin_role.modulos.append(comensal_m)
        admin_role.modulos.append(menu_m)
        admin_role.modulos.append(pedido_m)

        admin_role.modulos.append(query_menu)
        admin_role.modulos.append(insert_menu)
        admin_role.modulos.append(update_menu)
        admin_role.modulos.append(delete_menu)
        admin_role.modulos.append(imprimir_menu)
        admin_role.modulos.append(query_menu_plato)
        admin_role.modulos.append(insert_menu_plato)
        admin_role.modulos.append(update_menu_plato)
        admin_role.modulos.append(delete_menu_plato)
        admin_role.modulos.append(imprimir_menu_plato)

        admin_role.modulos.append(query_pedido)
        admin_role.modulos.append(insert_pedido)
        admin_role.modulos.append(update_pedido)
        admin_role.modulos.append(delete_pedido)
        admin_role.modulos.append(imprimir_pedido)

        horariocomensal = HorarioComensal(id=1, horaLimite=datetime.strptime('01/01/2000 10:00' , '%d/%m/%Y %H:%M'), horaInicio=datetime.strptime('01/01/2000 12:30' , '%d/%m/%Y %H:%M'), horaFin=datetime.strptime('01/01/2000 14:00' , '%d/%m/%Y %H:%M'))

        session.merge(horariocomensal)

        # session.commit()
