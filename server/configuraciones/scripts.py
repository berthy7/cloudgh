from server.database.connection import transaction
from ..usuarios.rol.models import *


def insertions():
    with transaction() as session:

        ###Modulo de Operaciones

        configuraciones_m = session.query(Modulo).filter(Modulo.name == 'configuraciones').first()
        if configuraciones_m is None:
            configuraciones_m = Modulo(title='Configuraciones', name='configuraciones', icon='ajuste.ico')

        centro_costo_m = session.query(Modulo).filter(Modulo.name == 'centro_costo').first()
        if centro_costo_m is None:
            centro_costo_m = Modulo(title='Centro de costos', route='/centro_costo', name='centro_costo',
                                    icon='costos.ico')

        empresa_m = session.query(Modulo).filter(Modulo.name == 'empresa').first()
        if empresa_m is None:
            empresa_m = Modulo(title='Empresa', route='/empresa', name='empresa', icon='empresa.ico')

        gerencia_m = session.query(Modulo).filter(Modulo.name == 'gerencia').first()
        if gerencia_m is None:
            gerencia_m = Modulo(title='Gerencias', route='/gerencia', name='gerencia', icon='gerencia.ico')

        cargo_m = session.query(Modulo).filter(Modulo.name == 'cargo').first()
        if cargo_m is None:
            cargo_m = Modulo(title='Cargos', route='/cargo', name='cargo', icon='cargos.ico')

        localizacion_m = session.query(Modulo).filter(Modulo.name == 'localizacion_Modulo').first()
        if localizacion_m is None:
            localizacion_m = Modulo(title='Localización', name='localizacion', icon='localizacion.ico')

        pais_m = session.query(Modulo).filter(Modulo.name == 'pais').first()
        if pais_m is None:
            pais_m = Modulo(title='País', route='/pais', name='pais', icon='pais.ico')

        departamento_m = session.query(Modulo).filter(Modulo.name == 'departamento').first()
        if departamento_m is None:
            departamento_m = Modulo(title='Departamentos', route='/departamento', name='departamento',
                                    icon='departamento.ico')

        ciudad_m = session.query(Modulo).filter(Modulo.name == 'ciudad').first()
        if ciudad_m is None:
            ciudad_m = Modulo(title='Ciudades', route='/ciudad', name='ciudad', icon='ciudad.ico')

        sucursal_m = session.query(Modulo).filter(Modulo.name == 'sucursal').first()
        if sucursal_m is None:
            sucursal_m = Modulo(title='Sucursales', route='/sucursal', name='sucursal', icon='sucursal.ico')

        oficina_m = session.query(Modulo).filter(Modulo.name == 'oficina').first()
        if oficina_m is None:
            oficina_m = Modulo(title='Oficinas', route='/oficina', name='oficina', icon='oficina.ico')

        configuraciones_m.children.append(centro_costo_m)
        configuraciones_m.children.append(empresa_m)
        configuraciones_m.children.append(gerencia_m)
        configuraciones_m.children.append(cargo_m)
        configuraciones_m.children.append(localizacion_m)

        localizacion_m.children.append(pais_m)
        localizacion_m.children.append(departamento_m)
        localizacion_m.children.append(ciudad_m)
        localizacion_m.children.append(sucursal_m)
        localizacion_m.children.append(oficina_m)


        query_centro_costo = session.query(Modulo).filter(Modulo.name == 'centro_costo_query').first()
        if query_centro_costo is None:
            query_centro_costo = Modulo(title='Consultar', route='',
                                   name='centro_costo_query',
                                   menu=False)

        insert_centro_costo = session.query(Modulo).filter(Modulo.name == 'centro_costo_insert').first()
        if insert_centro_costo is None:
            insert_centro_costo = Modulo(title='Adicionar', route='/centro_costo_insert',
                                    name='centro_costo_insert',
                                    menu=False)
        update_centro_costo = session.query(Modulo).filter(Modulo.name == 'centro_costo_update').first()
        if update_centro_costo is None:
            update_centro_costo = Modulo(title='Actualizar', route='/centro_costo_update',
                                    name='centro_costo_update',
                                    menu=False)
        delete_centro_costo = session.query(Modulo).filter(Modulo.name == 'centro_costo_delete').first()
        if delete_centro_costo is None:
            delete_centro_costo = Modulo(title='Dar de Baja', route='/centro_costo_delete',
                                    name='centro_costo_delete',
                                    menu=False)

        imprimir_centro_costo = session.query(Modulo).filter(Modulo.name == 'centro_costo_imprimir').first()
        if imprimir_centro_costo is None:
            imprimir_centro_costo = Modulo(title='Imprimir', route='/centro_costo_imprimir',
                                      name='centro_costo_imprimir',
                                      menu=False)

        centro_costo_m.children.append(query_centro_costo)
        centro_costo_m.children.append(insert_centro_costo)
        centro_costo_m.children.append(update_centro_costo)
        centro_costo_m.children.append(delete_centro_costo)
        centro_costo_m.children.append(imprimir_centro_costo)

        query_empresa = session.query(Modulo).filter(Modulo.name == 'empresa_query').first()
        if query_empresa is None:
            query_empresa = Modulo(title='Consultar', route='',
                                   name='empresa_query',
                                   menu=False)

        insert_empresa = session.query(Modulo).filter(Modulo.name == 'empresa_insert').first()
        if insert_empresa is None:
            insert_empresa = Modulo(title='Adicionar', route='/empresa_insert',
                                    name='empresa_insert',
                                    menu=False)
        update_empresa = session.query(Modulo).filter(Modulo.name == 'empresa_update').first()
        if update_empresa is None:
            update_empresa = Modulo(title='Actualizar', route='/empresa_update',
                                    name='empresa_update',
                                    menu=False)
        delete_empresa = session.query(Modulo).filter(Modulo.name == 'empresa_delete').first()
        if delete_empresa is None:
            delete_empresa = Modulo(title='Dar de Baja', route='/empresa_delete',
                                    name='empresa_delete',
                                    menu=False)

        imprimir_empresa = session.query(Modulo).filter(Modulo.name == 'empresa_imprimir').first()
        if imprimir_empresa is None:
            imprimir_empresa = Modulo(title='Imprimir', route='/empresa_imprimir',
                                      name='empresa_imprimir',
                                      menu=False)

        empresa_m.children.append(query_empresa)
        empresa_m.children.append(insert_empresa)
        empresa_m.children.append(update_empresa)
        empresa_m.children.append(delete_empresa)
        empresa_m.children.append(imprimir_empresa)

        query_gerencia = session.query(Modulo).filter(Modulo.name == 'gerencia_query').first()
        if query_gerencia is None:
            query_gerencia = Modulo(title='Consultar', route='',
                                   name='gerencia_query',
                                   menu=False)

        insert_gerencia = session.query(Modulo).filter(Modulo.name == 'gerencia_insert').first()
        if insert_gerencia is None:
            insert_gerencia = Modulo(title='Adicionar', route='/gerencia_insert',
                                    name='gerencia_insert',
                                    menu=False)
        update_gerencia = session.query(Modulo).filter(Modulo.name == 'gerencia_update').first()
        if update_gerencia is None:
            update_gerencia = Modulo(title='Actualizar', route='/gerencia_update',
                                    name='gerencia_update',
                                    menu=False)
        delete_gerencia = session.query(Modulo).filter(Modulo.name == 'gerencia_delete').first()
        if delete_gerencia is None:
            delete_gerencia = Modulo(title='Dar de Baja', route='/gerencia_delete',
                                    name='gerencia_delete',
                                    menu=False)

        imprimir_gerencia = session.query(Modulo).filter(Modulo.name == 'gerencia_imprimir').first()
        if imprimir_gerencia is None:
            imprimir_gerencia = Modulo(title='Imprimir', route='/gerencia_imprimir',
                                      name='gerencia_imprimir',
                                      menu=False)

        gerencia_m.children.append(query_gerencia)
        gerencia_m.children.append(insert_gerencia)
        gerencia_m.children.append(update_gerencia)
        gerencia_m.children.append(delete_gerencia)
        gerencia_m.children.append(imprimir_gerencia)

        query_cargo = session.query(Modulo).filter(Modulo.name == 'cargo_query').first()
        if query_cargo is None:
            query_cargo = Modulo(title='Consultar', route='',
                                   name='cargo_query',
                                   menu=False)

        insert_cargo = session.query(Modulo).filter(Modulo.name == 'cargo_insert').first()
        if insert_cargo is None:
            insert_cargo = Modulo(title='Adicionar', route='/cargo_insert',
                                    name='cargo_insert',
                                    menu=False)
        update_cargo = session.query(Modulo).filter(Modulo.name == 'cargo_update').first()
        if update_cargo is None:
            update_cargo = Modulo(title='Actualizar', route='/cargo_update',
                                    name='cargo_update',
                                    menu=False)
        delete_cargo = session.query(Modulo).filter(Modulo.name == 'cargo_delete').first()
        if delete_cargo is None:
            delete_cargo = Modulo(title='Dar de Baja', route='/cargo_delete',
                                    name='cargo_delete',
                                    menu=False)

        imprimir_cargo = session.query(Modulo).filter(Modulo.name == 'cargo_imprimir').first()
        if imprimir_cargo is None:
            imprimir_cargo = Modulo(title='Imprimir', route='/cargo_imprimir',
                                      name='cargo_imprimir',
                                      menu=False)

        cargo_m.children.append(query_cargo)
        cargo_m.children.append(insert_cargo)
        cargo_m.children.append(update_cargo)
        cargo_m.children.append(delete_cargo)
        cargo_m.children.append(imprimir_cargo)

        query_pais = session.query(Modulo).filter(Modulo.name == 'pais_query').first()
        if query_pais is None:
            query_pais = Modulo(title='Consultar', route='',
                                   name='pais_query',
                                   menu=False)

        insert_pais = session.query(Modulo).filter(Modulo.name == 'pais_insert').first()
        if insert_pais is None:
            insert_pais = Modulo(title='Adicionar', route='/pais_insert',
                                    name='pais_insert',
                                    menu=False)
        update_pais = session.query(Modulo).filter(Modulo.name == 'pais_update').first()
        if update_pais is None:
            update_pais = Modulo(title='Actualizar', route='/pais_update',
                                    name='pais_update',
                                    menu=False)
        delete_pais = session.query(Modulo).filter(Modulo.name == 'pais_delete').first()
        if delete_pais is None:
            delete_pais = Modulo(title='Dar de Baja', route='/pais_delete',
                                    name='pais_delete',
                                    menu=False)

        imprimir_pais = session.query(Modulo).filter(Modulo.name == 'pais_imprimir').first()
        if imprimir_pais is None:
            imprimir_pais = Modulo(title='Imprimir', route='/pais_imprimir',
                                      name='pais_imprimir',
                                      menu=False)

        pais_m.children.append(query_pais)
        pais_m.children.append(insert_pais)
        pais_m.children.append(update_pais)
        pais_m.children.append(delete_pais)
        pais_m.children.append(imprimir_pais)

        query_departamento = session.query(Modulo).filter(Modulo.name == 'departamento_query').first()
        if query_departamento is None:
            query_departamento = Modulo(title='Consultar', route='',
                                   name='departamento_query',
                                   menu=False)

        insert_departamento = session.query(Modulo).filter(Modulo.name == 'departamento_insert').first()
        if insert_departamento is None:
            insert_departamento = Modulo(title='Adicionar', route='/departamento_insert',
                                    name='departamento_insert',
                                    menu=False)
        update_departamento = session.query(Modulo).filter(Modulo.name == 'departamento_update').first()
        if update_departamento is None:
            update_departamento = Modulo(title='Actualizar', route='/departamento_update',
                                    name='departamento_update',
                                    menu=False)
        delete_departamento = session.query(Modulo).filter(Modulo.name == 'departamento_delete').first()
        if delete_departamento is None:
            delete_departamento = Modulo(title='Dar de Baja', route='/departamento_delete',
                                    name='departamento_delete',
                                    menu=False)

        imprimir_departamento = session.query(Modulo).filter(Modulo.name == 'departamento_imprimir').first()
        if imprimir_departamento is None:
            imprimir_departamento = Modulo(title='Imprimir', route='/departamento_imprimir',
                                      name='departamento_imprimir',
                                      menu=False)

        departamento_m.children.append(query_departamento)
        departamento_m.children.append(insert_departamento)
        departamento_m.children.append(update_departamento)
        departamento_m.children.append(delete_departamento)
        departamento_m.children.append(imprimir_departamento)

        query_ciudad = session.query(Modulo).filter(Modulo.name == 'ciudad_query').first()
        if query_ciudad is None:
            query_ciudad = Modulo(title='Consultar', route='',
                                   name='ciudad_query',
                                   menu=False)

        insert_ciudad = session.query(Modulo).filter(Modulo.name == 'ciudad_insert').first()
        if insert_ciudad is None:
            insert_ciudad = Modulo(title='Adicionar', route='/ciudad_insert',
                                    name='ciudad_insert',
                                    menu=False)
        update_ciudad = session.query(Modulo).filter(Modulo.name == 'ciudad_update').first()
        if update_ciudad is None:
            update_ciudad = Modulo(title='Actualizar', route='/ciudad_update',
                                    name='ciudad_update',
                                    menu=False)
        delete_ciudad = session.query(Modulo).filter(Modulo.name == 'ciudad_delete').first()
        if delete_ciudad is None:
            delete_ciudad = Modulo(title='Dar de Baja', route='/ciudad_delete',
                                    name='ciudad_delete',
                                    menu=False)

        imprimir_ciudad = session.query(Modulo).filter(Modulo.name == 'ciudad_imprimir').first()
        if imprimir_ciudad is None:
            imprimir_ciudad = Modulo(title='Imprimir', route='/ciudad_imprimir',
                                      name='ciudad_imprimir',
                                      menu=False)

        ciudad_m.children.append(query_ciudad)
        ciudad_m.children.append(insert_ciudad)
        ciudad_m.children.append(update_ciudad)
        ciudad_m.children.append(delete_ciudad)
        ciudad_m.children.append(imprimir_ciudad)

        query_sucursal = session.query(Modulo).filter(Modulo.name == 'sucursal_query').first()
        if query_sucursal is None:
            query_sucursal = Modulo(title='Consultar', route='',
                                   name='sucursal_query',
                                   menu=False)

        insert_sucursal = session.query(Modulo).filter(Modulo.name == 'sucursal_insert').first()
        if insert_sucursal is None:
            insert_sucursal = Modulo(title='Adicionar', route='/sucursal_insert',
                                    name='sucursal_insert',
                                    menu=False)
        update_sucursal = session.query(Modulo).filter(Modulo.name == 'sucursal_update').first()
        if update_sucursal is None:
            update_sucursal = Modulo(title='Actualizar', route='/sucursal_update',
                                    name='sucursal_update',
                                    menu=False)
        delete_sucursal = session.query(Modulo).filter(Modulo.name == 'sucursal_delete').first()
        if delete_sucursal is None:
            delete_sucursal = Modulo(title='Dar de Baja', route='/sucursal_delete',
                                    name='sucursal_delete',
                                    menu=False)

        imprimir_sucursal = session.query(Modulo).filter(Modulo.name == 'sucursal_imprimir').first()
        if imprimir_sucursal is None:
            imprimir_sucursal = Modulo(title='Imprimir', route='/sucursal_imprimir',
                                      name='sucursal_imprimir',
                                      menu=False)

        sucursal_m.children.append(query_sucursal)
        sucursal_m.children.append(insert_sucursal)
        sucursal_m.children.append(update_sucursal)
        sucursal_m.children.append(delete_sucursal)
        sucursal_m.children.append(imprimir_sucursal)

        query_oficina = session.query(Modulo).filter(Modulo.name == 'oficina_query').first()
        if query_oficina is None:
            query_oficina = Modulo(title='Consultar', route='',
                                   name='oficina_query',
                                   menu=False)

        insert_oficina = session.query(Modulo).filter(Modulo.name == 'oficina_insert').first()
        if insert_oficina is None:
            insert_oficina = Modulo(title='Adicionar', route='/oficina_insert',
                                    name='oficina_insert',
                                    menu=False)
        update_oficina = session.query(Modulo).filter(Modulo.name == 'oficina_update').first()
        if update_oficina is None:
            update_oficina = Modulo(title='Actualizar', route='/oficina_update',
                                    name='oficina_update',
                                    menu=False)
        delete_oficina = session.query(Modulo).filter(Modulo.name == 'oficina_delete').first()
        if delete_oficina is None:
            delete_oficina = Modulo(title='Dar de Baja', route='/oficina_delete',
                                    name='oficina_delete',
                                    menu=False)

        imprimir_oficina = session.query(Modulo).filter(Modulo.name == 'oficina_imprimir').first()
        if imprimir_oficina is None:
            imprimir_oficina = Modulo(title='Imprimir', route='/oficina_imprimir',
                                      name='oficina_imprimir',
                                      menu=False)

        oficina_m.children.append(query_oficina)
        oficina_m.children.append(insert_oficina)
        oficina_m.children.append(update_oficina)
        oficina_m.children.append(delete_oficina)
        oficina_m.children.append(imprimir_oficina)

        admin_role = session.query(Rol).filter(Rol.nombre == 'ADMINISTRADOR').first()

        ###Modulos de Operaciones

        admin_role.modulos.append(configuraciones_m)
        admin_role.modulos.append(centro_costo_m)
        admin_role.modulos.append(empresa_m)
        admin_role.modulos.append(gerencia_m)
        admin_role.modulos.append(cargo_m)
        admin_role.modulos.append(localizacion_m)
        admin_role.modulos.append(pais_m)
        admin_role.modulos.append(departamento_m)
        admin_role.modulos.append(ciudad_m)
        admin_role.modulos.append(sucursal_m)
        admin_role.modulos.append(oficina_m)

        admin_role.modulos.append(query_centro_costo)
        admin_role.modulos.append(insert_centro_costo)
        admin_role.modulos.append(update_centro_costo)
        admin_role.modulos.append(delete_centro_costo)
        admin_role.modulos.append(imprimir_centro_costo)

        admin_role.modulos.append(query_empresa)
        admin_role.modulos.append(insert_empresa)
        admin_role.modulos.append(update_empresa)
        admin_role.modulos.append(delete_empresa)
        admin_role.modulos.append(imprimir_empresa)

        admin_role.modulos.append(query_gerencia)
        admin_role.modulos.append(insert_gerencia)
        admin_role.modulos.append(update_gerencia)
        admin_role.modulos.append(delete_gerencia)
        admin_role.modulos.append(imprimir_gerencia)

        admin_role.modulos.append(query_cargo)
        admin_role.modulos.append(insert_cargo)
        admin_role.modulos.append(update_cargo)
        admin_role.modulos.append(delete_cargo)
        admin_role.modulos.append(imprimir_cargo)

        admin_role.modulos.append(query_pais)
        admin_role.modulos.append(insert_pais)
        admin_role.modulos.append(update_pais)
        admin_role.modulos.append(delete_pais)
        admin_role.modulos.append(imprimir_pais)

        admin_role.modulos.append(query_departamento)
        admin_role.modulos.append(insert_departamento)
        admin_role.modulos.append(update_departamento)
        admin_role.modulos.append(delete_departamento)
        admin_role.modulos.append(imprimir_departamento)

        admin_role.modulos.append(query_ciudad)
        admin_role.modulos.append(insert_ciudad)
        admin_role.modulos.append(update_ciudad)
        admin_role.modulos.append(delete_ciudad)
        admin_role.modulos.append(imprimir_ciudad)

        admin_role.modulos.append(query_sucursal)
        admin_role.modulos.append(insert_sucursal)
        admin_role.modulos.append(update_sucursal)
        admin_role.modulos.append(delete_sucursal)
        admin_role.modulos.append(imprimir_sucursal)

        admin_role.modulos.append(query_oficina)
        admin_role.modulos.append(insert_oficina)
        admin_role.modulos.append(update_oficina)
        admin_role.modulos.append(delete_oficina)
        admin_role.modulos.append(imprimir_oficina)


        session.commit()
