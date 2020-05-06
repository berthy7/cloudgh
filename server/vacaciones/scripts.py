from server.database.connection import transaction
from ..usuarios.rol.models import *


def insertions():
    with transaction() as session:

        ###Modulo de Operaciones

        vacaciones_m = session.query(Modulo).filter(Modulo.name == 'vacaciones').first()
        if vacaciones_m is None:
            vacaciones_m = Modulo(title='Vacaciones', name='vacaciones', icon='vacaciones.ico')

        v_antiguedad_m = session.query(Modulo).filter(Modulo.name == 'v_antiguedad').first()
        if v_antiguedad_m is None:
            v_antiguedad_m = Modulo(title='Vacacion por Antiguedad', route='/v_antiguedad', name='v_antiguedad', icon='v_antiguedad.ico')

        v_personal_m = session.query(Modulo).filter(Modulo.name == 'v_personal').first()
        if v_personal_m is None:
            v_personal_m = Modulo(title='Vacacion Personal', route='/v_personal', name='v_personal',
                                    icon='v_personal.ico')


        vacaciones_m.children.append(v_antiguedad_m)
        vacaciones_m.children.append(v_personal_m)


        query_v_antiguedad = session.query(Modulo).filter(Modulo.name == 'v_antiguedad_query').first()
        if query_v_antiguedad is None:
            query_v_antiguedad = Modulo(title='Consultar', route='',
                                   name='v_antiguedad_query',
                                   menu=False)

        insert_v_antiguedad = session.query(Modulo).filter(Modulo.name == 'v_antiguedad_insert').first()
        if insert_v_antiguedad is None:
            insert_v_antiguedad = Modulo(title='Adicionar', route='/v_antiguedad_insert',
                                    name='v_antiguedad_insert',
                                    menu=False)
        update_v_antiguedad = session.query(Modulo).filter(Modulo.name == 'v_antiguedad_update').first()
        if update_v_antiguedad is None:
            update_v_antiguedad = Modulo(title='Actualizar', route='/v_antiguedad_update',
                                    name='v_antiguedad_update',
                                    menu=False)
        delete_v_antiguedad = session.query(Modulo).filter(Modulo.name == 'v_antiguedad_delete').first()
        if delete_v_antiguedad is None:
            delete_v_antiguedad = Modulo(title='Dar de Baja', route='/v_antiguedad_delete',
                                    name='v_antiguedad_delete',
                                    menu=False)

        imprimir_v_antiguedad = session.query(Modulo).filter(Modulo.name == 'v_antiguedad_imprimir').first()
        if imprimir_v_antiguedad is None:
            imprimir_v_antiguedad = Modulo(title='Imprimir', route='/v_antiguedad_imprimir',
                                      name='v_antiguedad_imprimir',
                                      menu=False)

        v_antiguedad_m.children.append(query_v_antiguedad)
        v_antiguedad_m.children.append(insert_v_antiguedad)
        v_antiguedad_m.children.append(update_v_antiguedad)
        v_antiguedad_m.children.append(delete_v_antiguedad)
        v_antiguedad_m.children.append(imprimir_v_antiguedad)

        query_v_personal = session.query(Modulo).filter(Modulo.name == 'v_personal_query').first()
        if query_v_personal is None:
            query_v_personal = Modulo(title='Consultar', route='',
                                      name='v_personal_query',
                                      menu=False)

        insert_v_personal = session.query(Modulo).filter(Modulo.name == 'v_personal_insert').first()
        if insert_v_personal is None:
            insert_v_personal = Modulo(title='Adicionar', route='/v_personal_insert',
                                       name='v_personal_insert',
                                       menu=False)
        update_v_personal = session.query(Modulo).filter(Modulo.name == 'v_personal_update').first()
        if update_v_personal is None:
            update_v_personal = Modulo(title='Actualizar', route='/v_personal_update',
                                       name='v_personal_update',
                                       menu=False)

        delete_v_personal = session.query(Modulo).filter(Modulo.name == 'v_personal_delete').first()
        if delete_v_personal is None:
            delete_v_personal = Modulo(title='Dar de Baja', route='/v_personal_delete',
                                       name='v_personal_delete',
                                       menu=False)

        imprimir_v_personal = session.query(Modulo).filter(Modulo.name == 'v_personal_imprimir').first()
        if imprimir_v_personal is None:
            imprimir_v_personal = Modulo(title='Imprimir', route='/v_personal_imprimir',
                                         name='v_personal_imprimir',
                                         menu=False)

        importar_v_personal = session.query(Modulo).filter(Modulo.name == 'v_personal_importar').first()
        if importar_v_personal is None:
            importar_v_personal = Modulo(title='Importar', route='/v_personal_importar',
                                         name='v_personal_importar',
                                         menu=False)

        historico_v_personal = session.query(Modulo).filter(Modulo.name == 'v_personal_historico').first()
        if historico_v_personal is None:
            historico_v_personal = Modulo(title='Importar', route='/v_personal_historico',
                                         name='v_personal_historico',
                                         menu=False)

        v_personal_m.children.append(query_v_personal)
        v_personal_m.children.append(insert_v_personal)
        v_personal_m.children.append(update_v_personal)
        v_personal_m.children.append(delete_v_personal)
        v_personal_m.children.append(imprimir_v_personal)
        v_personal_m.children.append(importar_v_personal)
        v_personal_m.children.append(historico_v_personal)


        admin_role = session.query(Rol).filter(Rol.nombre == 'ADMINISTRADOR').first()

        ###Modulos de Operaciones

        admin_role.modulos.append(vacaciones_m)
        admin_role.modulos.append(v_antiguedad_m)
        admin_role.modulos.append(v_personal_m)

        admin_role.modulos.append(query_v_antiguedad)
        admin_role.modulos.append(insert_v_antiguedad)
        admin_role.modulos.append(update_v_antiguedad)
        admin_role.modulos.append(delete_v_antiguedad)
        admin_role.modulos.append(imprimir_v_antiguedad)

        admin_role.modulos.append(query_v_personal)
        admin_role.modulos.append(insert_v_personal)
        admin_role.modulos.append(update_v_personal)
        admin_role.modulos.append(delete_v_personal)
        admin_role.modulos.append(imprimir_v_personal)
        admin_role.modulos.append(importar_v_personal)
        admin_role.modulos.append(historico_v_personal)

        session.commit()
