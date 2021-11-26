from server.database.connection import transaction
from .persona.managers import ContratoManager
from ..usuarios.rol.models import *
from ..personal.organigrama.models import *

import schedule

def insertions():
    with transaction() as session:
        ###Modulo de Operaciones

        personal_m = session.query(Modulo).filter(Modulo.name == 'personal').first()
        if personal_m is None:
            personal_m = Modulo(title='Personal', name='personal', icon='personal.png')

        persona_m = session.query(Modulo).filter(Modulo.name == 'persona').first()
        if persona_m is None:
            persona_m = Modulo(title='Personas', route='/persona', name='persona', icon='usuarios.png')

        organigrama_m = session.query(Modulo).filter(Modulo.name == 'organigrama').first()
        if organigrama_m is None:
            organigrama_m = Modulo(title='Organigrama', route='/organigrama', name='organigrama', icon='organigrama.png')

        personal_m.children.append(persona_m)
        personal_m.children.append(organigrama_m)

        query_persona = session.query(Modulo).filter(Modulo.name == 'persona_query').first()
        if query_persona is None:
            query_persona = Modulo(title='Consultar', route='',
                                   name='persona_query',
                                   menu=False)

        insert_persona = session.query(Modulo).filter(Modulo.name == 'persona_insert').first()
        if insert_persona is None:
            insert_persona = Modulo(title='Adicionar', route='/persona_insert',
                                    name='persona_insert',
                                    menu=False)
        update_persona = session.query(Modulo).filter(Modulo.name == 'persona_update').first()
        if update_persona is None:
            update_persona = Modulo(title='Actualizar', route='/persona_update',
                                    name='persona_update',
                                    menu=False)
        delete_persona = session.query(Modulo).filter(Modulo.name == 'persona_delete').first()
        if delete_persona is None:
            delete_persona = Modulo(title='Dar de Baja', route='/persona_delete',
                                    name='persona_delete',
                                    menu=False)

        imprimir_persona = session.query(Modulo).filter(Modulo.name == 'persona_imprimir').first()
        if imprimir_persona is None:
            imprimir_persona = Modulo(title='Imprimir', route='/persona_imprimir',
                                      name='persona_imprimir',
                                      menu=False)

        persona_m.children.append(query_persona)
        persona_m.children.append(insert_persona)
        persona_m.children.append(update_persona)
        persona_m.children.append(delete_persona)
        persona_m.children.append(imprimir_persona)

        query_organigrama = session.query(Modulo).filter(Modulo.name == 'organigrama_query').first()
        if query_organigrama is None:
            query_organigrama = Modulo(title='Consultar', route='',
                                   name='organigrama_query',
                                   menu=False)

        insert_organigrama = session.query(Modulo).filter(Modulo.name == 'organigrama_insert').first()
        if insert_organigrama is None:
            insert_organigrama = Modulo(title='Adicionar', route='/organigrama_insert',
                                    name='organigrama_insert',
                                    menu=False)
        update_organigrama = session.query(Modulo).filter(Modulo.name == 'organigrama_update').first()
        if update_organigrama is None:
            update_organigrama = Modulo(title='Actualizar', route='/organigrama_update',
                                    name='organigrama_update',
                                    menu=False)
        delete_organigrama = session.query(Modulo).filter(Modulo.name == 'organigrama_delete').first()
        if delete_organigrama is None:
            delete_organigrama = Modulo(title='Dar de Baja', route='/organigrama_delete',
                                    name='organigrama_delete',
                                    menu=False)

        organigrama_m.children.append(query_organigrama)
        organigrama_m.children.append(insert_organigrama)
        organigrama_m.children.append(update_organigrama)
        organigrama_m.children.append(delete_organigrama)

        admin_role = session.query(Rol).filter(Rol.nombre == 'SUPER ADMINISTRADOR').first()

        ###Modulos de Operaciones

        admin_role.modulos.append(personal_m)
        admin_role.modulos.append(persona_m)
        admin_role.modulos.append(organigrama_m)

        admin_role.modulos.append(query_persona)
        admin_role.modulos.append(insert_persona)
        admin_role.modulos.append(update_persona)
        admin_role.modulos.append(delete_persona)
        admin_role.modulos.append(imprimir_persona)

        admin_role.modulos.append(query_organigrama)
        admin_role.modulos.append(insert_organigrama)
        admin_role.modulos.append(update_organigrama)
        admin_role.modulos.append(delete_organigrama)

        Cloudbit_new = Organigrama(titulo='Por definir', campos="")

        session.merge(Cloudbit_new)

        session.commit()



def personal_schedule():

    def verificar_contratos():
        with transaction() as db:
            ContratoManager(db).validar_estado()

    schedule.every().day.at("12:09").do(verificar_contratos)