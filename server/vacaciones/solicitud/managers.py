from ...operaciones.bitacora.managers import *
from ...configuraciones.empresa.managers import EmpresaManager
from ...asistencia.asistenciapersonal.models import *
from ...asistencia.tipoausencia.models import *
from ...usuarios.ajustes.models import *
from ...personal.organigrama.managers import *
from ...notificaciones.correo.managers import *
from ...calendario.feriado.managers import *
from ..historico.managers import *
from ..personal.managers import *

from server.common.managers import SuperManager
from .models import *

from sqlalchemy.sql import func, and_
from datetime import datetime


class V_solicitudManager(SuperManager):
    def __init__(self, db):
        super().__init__(V_solicitud, db)


    def persona_excel(self, personal):
        fecha = datetime.now()
        cname = "Empleados" + fecha.strftime('%Y-%m-%d') + ".xlsx"

        wb = Workbook()
        ws = wb.active
        ws.title = 'Reporte Empleados'


        indice = 0
        # --------------------------------------------------------------------
        indice = indice + 1
        ws['A' + str(indice)] = 'PERSONAL QUE NO CUENTA CON LA TOTALIDAD DE DIAS DE VACACION REQUERIDO.'
        indice = indice + 2

        ws['A' + str(indice)] = 'Nº'
        ws['B' + str(indice)] = 'CODIGO'
        ws['C' + str(indice)] = 'NOMBRE COMPLETO'
        ws['D' + str(indice)] = 'DIAS DISPONIBLES'


        ws['A' + str(indice)].font = Font(bold=True)
        ws['B' + str(indice)].font = Font(bold=True)
        ws['C' + str(indice)].font = Font(bold=True)
        ws['D' + str(indice)].font = Font(bold=True)
        contador = 1
        for i in personal['sin_vacacion']:

            per = PersonaManager(self.db).obtener_x_id(i['id'])

            vacacion_persona = V_personalManager(self.db).obtener_vacacion_disponible(per.id)



            indice = indice + 1
            ws['A' + str(indice)] = str(contador)
            ws['B' + str(indice)] = str(per.empleado[0].codigo)
            ws['C' + str(indice)] = per.fullname
            ws['D' + str(indice)] = str(vacacion_persona['dias'])

            contador = contador + 1

        wb.save("server/common/resources/downloads/" + cname)

        return cname

    def obtener_x_nombre(self, nombre):
        return self.db.query(self.entity).filter(self.entity.nombre == nombre).first()

    def obtener_x_id(self, id):
        return self.db.query(self.entity).filter(self.entity.id == id).first()

    def listar_todo(self):
        return self.db.query(self.entity).order_by(self.entity.id.desc()).all()

    def obtener_x_persona(self, fkpersona):
        return self.db.query(self.entity).filter(self.entity.fkpersona == fkpersona).all()

    def obtener_vacacion(self,fkpersona,fecha):
        respuesta = ""

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled== True).first()
        # print("fecha: "+str(fecha))
        if ajuste.oracle:
            # version oracle
            # print("version oracle")
            solicitud = self.db.query(V_solicitud).filter(V_solicitud.fkpersona == fkpersona)\
                .filter(V_solicitud.estadoaprobacion == "Aceptado")\
                .filter(and_(V_solicitud.fechai <= fecha,V_solicitud.fechaf >= fecha)).first()

            if solicitud is None:
                solicitud = self.db.query(V_solicitud).join(V_colectiva).filter(V_colectiva.fkpersona == fkpersona) \
                    .filter(V_solicitud.estadoaprobacion == "Aceptado")\
                    .filter(and_(V_solicitud.fechai <= fecha, V_solicitud.fechaf >= fecha)).first()

        else:

            # version postgres
            solicitud = self.db.query(V_solicitud).filter(V_solicitud.fkpersona == fkpersona)\
                .filter(V_solicitud.estadoaprobacion == "Aceptado")\
                .filter(and_(func.date(V_solicitud.fechai) <= fecha, func.date(V_solicitud.fechaf) >= fecha)).first()

            if solicitud is None:
                solicitud = self.db.query(V_solicitud).join(V_colectiva).filter(V_colectiva.fkpersona == fkpersona) \
                    .filter(V_solicitud.estadoaprobacion == "Aceptado") \
                    .filter(and_(func.date(V_solicitud.fechai) <= fecha, func.date(V_solicitud.fechaf) >= fecha)).first()


        if solicitud:
             respuesta = solicitud.tipovacacion.nombre

        return respuesta

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.nombre.asc()).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True)

    def insert(self, diccionary):

        if diccionary['horaf'] == "":
            diccionary['horaf'] = "00:00"

        if diccionary['horai'] == "":
            diccionary['horai'] = "00:00"


        fecha = BitacoraManager(self.db).fecha_actual()
        diccionary['fechai'] = datetime.strptime(diccionary['fechai'] + " " +diccionary['horai'], '%d/%m/%Y %H:%M')
        diccionary['fechaf'] = datetime.strptime(diccionary['fechaf'] + " " +diccionary['horaf'], '%d/%m/%Y %H:%M')
        diccionary['fechar'] = fecha

        if int(diccionary['fktipovacacion']) != 3:

            if diccionary['mañana']:
                diccionary['jornada'] = "Mañana"
            elif diccionary['tarde']:
                diccionary['jornada'] = "Tarde"

            superiores = OrganigramaManager(self.db).obtener_autorizacion_aprobacion(diccionary['fkpersona'])

            diccionary['fkautorizacion'] = superiores['fkautorizacion']
            diccionary['fkaprobacion'] = superiores['fkaprobacion']
            diccionary['estadoautorizacion'] = superiores['estadoautorizacion']
            diccionary['estadoaprobacion'] = superiores['estadoaprobacion']


            # # idsuperior es None cuando no tiene Superior
            # if superiores is None:
            #     diccionary['fkautorizacion'] = None
            # else:
            #     diccionary['fkautorizacion'] = superiores

            objeto = V_solicitudManager(self.db).entity(**diccionary)

            objeto.dias = decimal.Decimal(objeto.dias)

            a = super().insert(objeto)
            CorreoManager(self.db).notificar_vacacion(objeto)

            b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro solicitud vacacion.",
                         fecha=fecha, tabla="cb_vacaciones_solicitud", identificador=a.id)
            super().insert(b)

            return a
        else:
            lista_colectiva = list()

            repetidos = set(diccionary['personas_arbol']).intersection(diccionary['personas'])

            for rep in repetidos:
                diccionary['personas'].remove(rep)

            for per in diccionary['personas']:
                diccionary['personas_arbol'].append(per)

            for sv in diccionary['sin_vacacion']:
                if sv['estado'] == False:
                    diccionary['personas_arbol'].remove(int(sv['id']))


            for p in diccionary['personas_arbol']:


              lista_colectiva.append(dict(fkpersona=p))

            diccionary['colectiva'] = lista_colectiva

            if diccionary['fkpersona'] == "":
                diccionary['fkpersona'] = None


            objeto =  V_solicitudManager(self.db).entity(**diccionary)
            a = super().insert(objeto)
            idsuperior = CorreoManager(self.db).notificar_vacacion(objeto)
            b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro solicitud vacacion.",
                         fecha=fecha, tabla="cb_vacaciones_solicitud", identificador=a.id)
            super().insert(b)

            return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        objeto.fechai = datetime.strptime(objeto.fechai, '%d/%m/%Y')
        objeto.fechaf = datetime.strptime(objeto.fechaf, '%d/%m/%Y')

        if objeto.mañana:
            objeto.jornada = "Mañana"
        elif objeto.tarde:
            objeto.jornada = "Tarde"

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico V_solicitud.",
                     fecha=fecha, tabla="cb_vacaciones_solicitud", identificador=a.id)
        super().insert(b)
        return a

    def autorizacion(self, diccionary):
        fecha = BitacoraManager(self.db).fecha_actual()

        ausencia = self.db.query(V_solicitud).filter(V_solicitud.id == diccionary['id']).first()
        ausencia.estadoautorizacion = diccionary['estadoautorizacion']
        ausencia.respuestaautorizacion = diccionary['respuestaautorizacion']

        a = super().update(ausencia)
        b = Bitacora(fkusuario=diccionary['user'], ip=diccionary['ip'], accion="Autorizacion V_solicitud.", fecha=fecha, tabla="cb_vacaciones_solicitud", identificador=a.id)
        super().insert(b)

        if a.fkpersona:
            if not a.persona.empleado[0].aprobacion:
                if ausencia.estadoautorizacion == "Aceptado":
                    if int(ausencia.fktipovacacion) == 3:
                        for persona_colectiva in ausencia.colectiva:
                            V_historicoManager(self.db).actualizar_vacaciones_solicitud(ausencia, persona_colectiva.fkpersona, diccionary['user'], diccionary['ip'])
                            V_solicitudManager(self.db).actualizar_vacacion(ausencia, persona_colectiva.fkpersona)
                    else:
                        V_historicoManager(self.db).actualizar_vacaciones_solicitud(ausencia, ausencia.fkpersona, diccionary['user'], diccionary['ip'])
                        V_solicitudManager(self.db).actualizar_vacacion(ausencia, ausencia.fkpersona)

        idsuperior = CorreoManager(self.db).notificar_vacacion_respuesta_autorizacion(ausencia)

        return ausencia

    def aprobacion(self, diccionary):
        fecha = BitacoraManager(self.db).fecha_actual()

        ausencia = self.db.query(V_solicitud).filter(V_solicitud.id == diccionary['id']).first()
        ausencia.estadoaprobacion = diccionary['estadoaprobacion']
        ausencia.respuestaaprobacion = diccionary['respuestaaprobacion']

        a = super().update(ausencia)
        b = Bitacora(fkusuario=diccionary['user'], ip=diccionary['ip'], accion="Aprobacion V_solicitud.", fecha=fecha, tabla="cb_vacaciones_solicitud", identificador=a.id)
        super().insert(b)
        idsuperior = CorreoManager(self.db).notificar_vacacion_respuesta_aprobacion(ausencia)

        if ausencia.estadoaprobacion == "Aceptado":
            if int(ausencia.fktipovacacion) == 3:
                for persona_colectiva in ausencia.colectiva:
                    lista_Gestion = V_historicoManager(self.db).actualizar_vacaciones_solicitud(ausencia,persona_colectiva.fkpersona,diccionary['user'],diccionary['ip'])
                    V_solicitudGestionManager(self.db).insert(lista_Gestion,diccionary['user'],diccionary['ip'])

                    V_solicitudManager(self.db).actualizar_vacacion(ausencia, persona_colectiva.fkpersona)
            else:
                lista_Gestion = V_historicoManager(self.db).actualizar_vacaciones_solicitud(ausencia, ausencia.fkpersona,diccionary['user'], diccionary['ip'])
                V_solicitudGestionManager(self.db).insert(lista_Gestion,diccionary['user'],diccionary['ip'])

                V_solicitudManager(self.db).actualizar_vacacion(ausencia, ausencia.fkpersona)

        return ausencia

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó V_solicitud.", fecha=fecha,
                     tabla="cb_asistencia_ausencia", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

    def actualizar_vacacion(self, objeto,persona):

        fechas = BitacoraManager(self.db).rango_fechas(objeto.fechai, objeto.fechaf)

        for fech in fechas:
            fecha_hoy = fech.date()

            ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

            if ajuste.oracle:
                # version oracle
                asistencia_personal = self.db.query(Asistencia).filter(Asistencia.fkpersona == persona).filter(
                    func.to_date(Asistencia.fecha).between(fecha_hoy, fecha_hoy)).all()
            else:
                # version postgres
                asistencia_personal = self.db.query(Asistencia).filter(Asistencia.fkpersona == persona).filter(
                    func.date(Asistencia.fecha) == fecha_hoy).all()

            feriado = FeriadoManager(self.db).obtener_x_fecha(fech)
            if feriado is None:
                for asistencia in asistencia_personal:
                    tipoausencia = self.db.query(V_tipovacacion).filter(V_tipovacacion.id == objeto.fktipovacacion).first()
                    asistencia.observacion = tipoausencia.nombre
                    super().update(asistencia)

        return objeto




class V_tipovacacionManager(SuperManager):

    def __init__(self, db):
        super().__init__(V_tipovacacion, db)

    def list_all(self):
        return dict(objects=self.db.query(self.entity))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.id.asc()).all()

    def listar_para_personal(self):
        return self.db.query(self.entity).filter(and_(self.entity.nombre != "VACACION COLECTIVA",self.entity.nombre != "ADELANTO VACACION")).filter(self.entity.enabled == True).order_by(self.entity.id.asc()).all()

    def obtener_x_nombre(self, nombre):
        return self.db.query(self.entity).filter(self.entity.nombre == nombre).filter(
            self.entity.enabled == True).first()


class V_solicitudGestionManager(SuperManager):

    def __init__(self, db):
        super().__init__(V_solicitudGestion, db)

    def list_all(self):
        return dict(objects=self.db.query(self.entity))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.id.asc()).all()

    def obtener_x_solicitud(self, idSolicitud):
        print(str(idSolicitud))

        return self.db.query(self.entity).filter(self.entity.fksolicitud == idSolicitud).filter(
            self.entity.enabled == True).all()

    def insert(self, lista_diccionary,user,ip):

        for i in lista_diccionary:
            objeto = V_solicitudGestionManager(self.db).entity(**i)

            fecha = BitacoraManager(self.db).fecha_actual()

            a = super().insert(objeto)
            b = Bitacora(fkusuario=user, ip=ip, accion="Registro solicitudGestion.", fecha=fecha,tabla="cb_vacaciones_solicitud_gestion", identificador=a.id)
            super().insert(b)
        return a

