from .managers import *
from ...configuraciones.oficina.managers import *
from server.common.controllers import CrudController

import os.path
import uuid
import json
import random

class PersonaController(CrudController):

    manager = PersonaManager
    html_index = "personal/persona/views/index.html"
    html_table = "personal/persona/views/table.html"
    routes = {
        '/persona': {'GET': 'index', 'POST': 'table'},
        '/persona_insert': {'POST': 'insert'},
        '/persona_update': {'PUT': 'edit', 'POST': 'update'},
        '/persona_delete': {'POST': 'delete'},
        '/persona_importar': {'POST': 'importar'},
        '/persona_reporte_xls': {'POST': 'imprimirxls'},
        '/persona_getcontrato': {'POST': 'get_contrato'},
        '/persona_obtener_id': {'POST': 'obtener_id'},
        '/persona_obtener_x_cargo': {'POST': 'obtener_x_cargo'},
        '/persona_contratos': {'POST': 'obtener_contrato'},
        '/persona_listvig': {'POST': 'list_vigente'},
        '/persona_listcon': {'POST': 'list_concluido'},
        '/persona_validcont': {'POST': 'validar_contrato'},
        '/persona_retiro': {'POST': 'retiro'}
    }

    def importar(self):
        self.set_session()
        fileinfo = self.request.files['archivo'][0]
        fname = fileinfo['filename']
        extn = os.path.splitext(fname)[1]
        cname = str(uuid.uuid4()) + extn
        fh = open("server/common/resources/uploads/" + cname, 'wb')
        fh.write(fileinfo['body'])
        fh.close()
        if extn in ['.xlsx', '.xls']:
            mee = self.manager(self.db).importar_excel(cname)
            self.respond(message=mee['message'], success=mee['success'])
        else:
            if extn == '.txt':
                mee = self.manager(self.db).importar_txt(cname)
                self.respond(message=mee['message'], success=mee['success'])
            else:
                self.respond(message='Formato de Archivo no aceptado¡¡', success=False)
        self.db.close()

    def retiro(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))

        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip

        result = PersonaManager(self.db).retiro(diccionary)

        if result:
            self.respond(success=True, message='Baja Realizada Correctamente.')
        else:
            self.respond(success=False, message='ERROR 403')

    def get_extra_data(self):
        aux = super().get_extra_data()
        objeto = []
        aux['pais'] = PaisManager(self.db).listar_todo()
        aux['gerencias'] = GerenciaManager(self.db).listar_todo()
        aux['cargos'] = CargoManager(self.db).listar_todo()
        aux['centros'] = Centro_costoManager(self.db).listar_todo()

        aux['departamentos'] = DepartamentoManager(self.db).listar_todo()
        aux['ciudades'] = CiudadManager(self.db).listar_todo()
        aux['sucursales'] = SucursalManager(self.db).listar_todo()
        aux['oficinas'] = OficinaManager(self.db).listar_todo()
        aux['contratos'] = ContratoManager(self.db).get_all()
        aux['personas'] = PersonaManager(self.db).get_all_per()

        aux['objeto'] = objeto

        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        dtfile = self.request.files

        user = self.get_user_id()
        ip = self.request.remote_ip
        diccionary['user'] = user
        diccionary['ip'] = ip

        if "foto" in dtfile:
            fileinfo = self.request.files["foto"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("server/common/resources/images/personal/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()

            if diccionary['empleado'][0]:
                diccionary['empleado'][0]['foto'] = "/resources/images/personal/" + cname

        if 'id' not in diccionary:
            if diccionary['empleado'][0]['fkpais'] == '':
                diccionary['empleado'][0]['fkpais'] = None

            if diccionary['empleado'][0]['fkdepartamento'] == '':
                diccionary['empleado'][0]['fkdepartamento'] = None

            if diccionary['empleado'][0]['fkciudad'] == '':
                diccionary['empleado'][0]['fkciudad'] = None

            if diccionary['empleado'][0]['fksucursal'] == '':
                diccionary['empleado'][0]['fksucursal'] = None

            if diccionary['empleado'][0]['fkoficina'] == '':
                diccionary['empleado'][0]['fkoficina'] = None

            if diccionary['empleado'][0]['fkgerencia'] == '':
                diccionary['empleado'][0]['fkgerencia'] = None

            if diccionary['empleado'][0]['fkcargo'] == '':
                diccionary['empleado'][0]['fkcargo'] = None

            if diccionary['empleado'][0]['fkcentro'] == '':
                diccionary['empleado'][0]['fkcentro'] = None

            objeto = self.manager(self.db).entity(**diccionary)
            result = PersonaManager(self.db).insert(objeto)

            if result:
                if 'administrativo' in diccionary and len(diccionary['administrativo']) > 0:
                    diccionary['administrativo'][0]['fkpersona'] = result.id
                    diccionary['administrativo'][0]['user'] = user
                    diccionary['administrativo'][0]['ip'] = ip
                    objeto_adm = AdministrativoManager(self.db).entity(**diccionary['administrativo'][0])
                    AdministrativoManager(self.db).insert(objeto_adm)

                if 'estudios' in diccionary and len(diccionary['estudios']) > 0:
                    for itemst in diccionary['estudios']:
                        itemst['fkpersona'] = result.id
                        itemst['user'] = user
                        itemst['ip'] = ip
                        objeto_est = EstudiosManager(self.db).entity(**itemst)
                        EstudiosManager(self.db).insert(objeto_est)

                if 'capacitacion' in diccionary and len(diccionary['capacitacion']) > 0:
                    for itemc in diccionary['capacitacion']:
                        itemc['fkpersona'] = result.id
                        itemc['user'] = user
                        itemc['ip'] = ip
                        objeto_cap = CapacitacionManager(self.db).entity(**itemc)
                        CapacitacionManager(self.db).insert(objeto_cap)

                if 'educacion' in diccionary and len(diccionary['educacion']) > 0:
                    diccionary['educacion'][0]['fkpersona'] = result.id
                    diccionary['educacion'][0]['user'] = user
                    diccionary['educacion'][0]['ip'] = ip
                    objeto_edc = EducacionManager(self.db).entity(**diccionary['educacion'][0])
                    EducacionManager(self.db).insert(objeto_edc)

                if 'memo' in diccionary and len(diccionary['memo']) > 0:
                    for itemb in diccionary['memo']:
                        itemb['fkpersona'] = result.id
                        itemb['user'] = user
                        itemb['ip'] = ip
                        objeto_memo = MemoManager(self.db).entity(**itemb)
                        MemoManager(self.db).insert(objeto_memo)

                if 'idioma' in diccionary and len(diccionary['idioma']) > 0:
                    for itemd in diccionary['idioma']:
                        itemd['fkpersona'] = result.id
                        itemd['user'] = user
                        itemd['ip'] = ip
                        objeto_idm = IdiomaManager(self.db).entity(**itemd)
                        IdiomaManager(self.db).insert(objeto_idm)

                if 'experiencia' in diccionary and len(diccionary['experiencia']) > 0:
                    for itemexp in diccionary['experiencia']:
                        itemexp['fkpersona'] = result.id
                        itemexp['user'] = user
                        itemexp['ip'] = ip
                        objeto_exp = ExperienciaManager(self.db).entity(**itemexp)
                        ExperienciaManager(self.db).insert(objeto_exp)

                if 'padres' in diccionary and len(diccionary['padres']) > 0:
                    for itemp in diccionary['padres']:
                        itemp['fkpersona'] = result.id
                        itemp['user'] = user
                        itemp['ip'] = ip
                        objeto_pad = PadresManager(self.db).entity(**itemp)
                        PadresManager(self.db).insert(objeto_pad)

                if 'conyuge' in diccionary and len(diccionary['conyuge']) > 0:
                    diccionary['conyuge'][0]['fkpersona'] = result.id
                    diccionary['conyuge'][0]['user'] = user
                    diccionary['conyuge'][0]['ip'] = ip
                    objeto_con = ConyugeManager(self.db).entity(**diccionary['conyuge'][0])
                    ConyugeManager(self.db).insert(objeto_con)

                if 'hijos' in diccionary and len(diccionary['hijos']) > 0:
                    for itemh in diccionary['hijos']:
                        itemh['fkpersona'] = result.id
                        itemh['user'] = user
                        itemh['ip'] = ip
                        objeto_hj = HijosManager(self.db).entity(**itemh)
                        HijosManager(self.db).insert(objeto_hj)

                self.respond(success=True, message='Insertado Correctamente.')
            else:
                self.respond(success=False, message='ERROR 403')
        else:
            new_contrato = None
            upd_contrato = None
            if diccionary['contrato']:

                if 'id' not in diccionary['contrato'][0]:
                    new_contrato = diccionary['contrato'][0]
                    del diccionary["contrato"]
                else:
                    upd_contrato = diccionary['contrato'][0]
                    del diccionary["contrato"]

            if diccionary['empleado'][0]['fkpais'] == '':
                diccionary['empleado'][0]['fkpais'] = None

            if diccionary['empleado'][0]['fkdepartamento'] == '':
                diccionary['empleado'][0]['fkdepartamento'] = None

            if diccionary['empleado'][0]['fkciudad'] == '':
                diccionary['empleado'][0]['fkciudad'] = None

            if diccionary['empleado'][0]['fksucursal'] == '':
                diccionary['empleado'][0]['fksucursal'] = None

            if diccionary['empleado'][0]['fkoficina'] == '':
                diccionary['empleado'][0]['fkoficina'] = None

            if diccionary['empleado'][0]['fkgerencia'] == '':
                diccionary['empleado'][0]['fkgerencia'] = None

            if diccionary['empleado'][0]['fkcargo'] == '':
                diccionary['empleado'][0]['fkcargo'] = None

            if diccionary['empleado'][0]['fkcentro'] == '':
                diccionary['empleado'][0]['fkcentro'] = None

            objeto = self.manager(self.db).entity(**diccionary)
            result = PersonaManager(self.db).update(objeto)
            if result:
                if new_contrato:

                    dic_cont = dict(fkpersona=result.id,user=user,ip=ip,nroContrato=new_contrato['nroContrato'],tipo=new_contrato['tipo'],
                                    sueldo=new_contrato['sueldo'] if new_contrato['sueldo'] != "" else None
                                    ,fechaIngreso=new_contrato['fechaIngreso'] if new_contrato['fechaIngreso'] != "" else None,
                                    fechaFin=new_contrato['fechaFin'] if new_contrato['fechaFin'] != "" else None,
                                    fechaForzado=new_contrato['fechaForzado'] if new_contrato[
                                                                                     'fechaForzado'] != "" else None)

                    if dic_cont['fechaIngreso']:
                        dic_cont['fechaIngreso']= datetime.strptime(dic_cont['fechaIngreso'], '%d/%m/%Y')
                    else:
                        dic_cont['fechaIngreso'] = None

                    if dic_cont['fechaFin']:
                        dic_cont['fechaFin'] = datetime.strptime(dic_cont['fechaFin'], '%d/%m/%Y')
                    else:
                        dic_cont['fechaFin'] = None

                    if dic_cont['fechaForzado']:
                        dic_cont['fechaForzado'] = datetime.strptime(dic_cont['fechaForzado'], '%d/%m/%Y')
                    else:
                        dic_cont['fechaForzado'] = None
                    objeto_cont = ContratoManager(self.db).entity(**dic_cont)
                    ContratoManager(self.db).insert(objeto_cont)
                else:

                    dic_cont = dict(id=upd_contrato['id'],fkpersona=result.id, user=user, ip=ip, nroContrato=upd_contrato['nroContrato'],
                                    tipo=upd_contrato['tipo'], sueldo=upd_contrato['sueldo'] if upd_contrato['sueldo'] != "" else None
                                    , fechaIngreso=upd_contrato['fechaIngreso'] if upd_contrato['fechaIngreso'] != "" else None,
                                    fechaFin=upd_contrato['fechaFin'] if upd_contrato['fechaFin'] != "" else None,
                                    fechaForzado=upd_contrato['fechaForzado'] if upd_contrato['fechaForzado'] != "" else None,
                                    descripcion=upd_contrato['descripcion'])





                    if dic_cont.fechaIngreso:
                        dic_cont.fechaIngreso = datetime.strptime(dic_cont.fechaIngreso, '%d/%m/%Y')
                    else:
                        dic_cont.fechaIngreso = None

                    if dic_cont.fechaFin:
                        dic_cont.fechaFin = datetime.strptime(dic_cont.fechaFin, '%d/%m/%Y')
                    else:
                        dic_cont.fechaFin = None

                    if dic_cont.fechaForzado:
                        dic_cont.fechaForzado = datetime.strptime(dic_cont.fechaForzado, '%d/%m/%Y')
                    else:
                        dic_cont.fechaForzado = None

                    objeto_cont = ContratoManager(self.db).entity(**dic_cont)

                    ContratoManager(self.db).update(objeto_cont)

                self.respond(success=True, message='Modificado Correctamente.')
            else:
                self.respond(success=False, message='ERROR 403')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        PersonaManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')

    def imprimirxls(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))

        cname = self.manager(self.db).persona_excel(diccionary['datos'])
        self.respond({'nombre': cname, 'url': 'resources/downloads/persona/' + cname}, True)
        self.db.close()


    def get_contrato(self, persona_contratos):
        self.set_session()

        arraT = ContratoManager(self.db).get_page(1, 10, None, None, True)
        arraT['contratos'] = ContratoManager(self.db).get_all()
        self.respond([item.get_dict() for item in arraT['contratos']])
        self.db.close()

    def obtener_id(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        indicted_object = PersonaManager(self.db).obtener_persona(diccionary['id'])

        password = random.randrange(99999)

        self.respond(indicted_object.get_dict(), message=password)
        self.db.close()

    def delete(self):
        self.set_session()
        id = json.loads(self.get_argument("id"))
        user = self.get_user_id()
        ip = self.request.remote_ip

        result = PersonaManager(self.db).delete(id, user, ip)

        if result:
            self.respond(success=True, message='Baja Realizada Correctamente.')
        else:
            self.respond(success=False, message='ERROR 403')

    def obtener_x_cargo(self):
        self.set_session()
        data = json.loads(self.get_argument("object"))
        arraT = self.manager(self.db).get_page(1, 10, None, None, True)
        arraT['datos'] = PersonaManager(self.db).obtener_x_cargo(data['idcargo'])
        self.respond([item.get_dict() for item in arraT['datos']])
        self.db.close()

    def obtener_contrato(self):
        self.set_session()
        ins_manager = self.manager(self.db)
        diccionary = json.loads(self.get_argument("object"))
        indicted_object = ins_manager.obtener_all_contratos(diccionary['id'])
        if len(ins_manager.errors) == 0:
            self.respond(indicted_object, message='Operacion exitosa!')
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
        self.db.close()

    def list_vigente(self):
        self.set_session()
        arraT = ContratoManager(self.db).get_page(1, 10, None, None, True)
        arraT['contratos'] = ContratoManager(self.db).get_all()
        self.respond([item.get_dict() for item in arraT['contratos']])
        self.db.close()

    def list_concluido(self):
        self.set_session()
        arraT = ContratoManager(self.db).get_page(1, 10, None, None, True)
        arraT['contratos'] = ContratoManager(self.db).obtener_concluido()
        self.respond([item.get_dict() for item in arraT['contratos']])
        self.db.close()

    def validar_contrato(self):
        self.set_session()
        resp = ContratoManager(self.db).validar_estado()
        self.respond(resp)
        self.db.close()
