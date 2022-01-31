from ..dispositivos.marcaciones.models import *
from ..usuarios.usuario.models import Modulo
from ..usuarios.rol.models import Rol
from server.database.connection import transaction
from ..dispositivos.lectores.managers import *

import schedule


def insertions():
    with transaction() as session:

        ###Modulo de Operaciones

        dispositivos_m = session.query(Modulo).filter(Modulo.name == 'dispositivos').first()
        if dispositivos_m is None:
            dispositivos_m = Modulo(title='Dispositivos', name='dispositivos', icon='dispositivo.png')

        lectores_m = session.query(Modulo).filter(Modulo.name == 'lectores').first()
        if lectores_m is None:
            lectores_m = Modulo(title='Lectores', route='/lectores', name='lectores',
                                    icon='biometrico.png')

        marcaciones_m = session.query(Modulo).filter(Modulo.name == 'marcaciones').first()
        if marcaciones_m is None:
            marcaciones_m = Modulo(title='Marcaciones', route='/marcaciones', name='marcaciones',
                                icon='marcacion.png')

        dispositivos_m.children.append(lectores_m)
        dispositivos_m.children.append(marcaciones_m)

        query_lectores = session.query(Modulo).filter(Modulo.name == 'lectores_query').first()
        if query_lectores is None:
            query_lectores = Modulo(title='Consultar', route='',
                                    name='lectores_query',
                                    menu=False)

        insert_lectores = session.query(Modulo).filter(Modulo.name == 'lectores_insert').first()
        if insert_lectores is None:
            insert_lectores = Modulo(title='Adicionar', route='/lectores_insert',
                                     name='lectores_insert',
                                     menu=False)
        update_lectores = session.query(Modulo).filter(Modulo.name == 'lectores_update').first()
        if update_lectores is None:
            update_lectores = Modulo(title='Actualizar', route='/lectores_update',
                                     name='lectores_update',
                                     menu=False)
        delete_lectores = session.query(Modulo).filter(Modulo.name == 'lectores_delete').first()
        if delete_lectores is None:
            delete_lectores = Modulo(title='Dar de Baja', route='/lectores_delete',
                                     name='lectores_delete',
                                     menu=False)

        imprimir_lectores = session.query(Modulo).filter(Modulo.name == 'lectores_imprimir').first()
        if imprimir_lectores is None:
            imprimir_lectores = Modulo(title='Imprimir', route='/lectores_imprimir',
                                       name='lectores_imprimir',
                                       menu=False)

        lectores_m.children.append(query_lectores)
        lectores_m.children.append(insert_lectores)
        lectores_m.children.append(update_lectores)
        lectores_m.children.append(delete_lectores)
        lectores_m.children.append(imprimir_lectores)

        query_marcaciones = session.query(Modulo).filter(Modulo.name == 'marcaciones_query').first()
        if query_marcaciones is None:
            query_marcaciones = Modulo(title='Consultar', route='',
                                    name='marcaciones_query',
                                    menu=False)

        imprimir_marcaciones = session.query(Modulo).filter(Modulo.name == 'marcaciones_imprimir').first()
        if imprimir_marcaciones is None:
            imprimir_marcaciones = Modulo(title='Imprimir', route='/marcaciones_imprimir',
                                       name='marcaciones_imprimir',
                                       menu=False)

        marcaciones_m.children.append(query_marcaciones)
        marcaciones_m.children.append(imprimir_marcaciones)

        admin_role = session.query(Rol).filter(Rol.nombre == 'SUPER ADMINISTRADOR').first()

        ###Modulos de Operaciones

        admin_role.modulos.append(dispositivos_m)
        admin_role.modulos.append(lectores_m)
        admin_role.modulos.append(marcaciones_m)

        admin_role.modulos.append(query_lectores)
        admin_role.modulos.append(insert_lectores)
        admin_role.modulos.append(update_lectores)
        admin_role.modulos.append(delete_lectores)
        admin_role.modulos.append(imprimir_lectores)

        admin_role.modulos.append(query_marcaciones)
        admin_role.modulos.append(imprimir_marcaciones)

        session.commit()


def dispositivos_schedule():

    def extraer_marcaciones():
        with transaction() as db:
            print("inicio")
            LectoresManager(db).preparar_dispositivos()

    schedule.every().day.at("04:00").do(extraer_marcaciones)
    # schedule.every().day.at("09:00").do(extraer_marcaciones)
    # schedule.every().day.at("15:00").do(extraer_marcaciones)
    # schedule.every().day.at("22:00").do(extraer_marcaciones)

