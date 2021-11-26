from ...operaciones.bitacora.managers import *
from server.common.managers import SuperManager
from .models import *
from ..personal.managers import *


class V_historicoManager(SuperManager):

    def __init__(self, db):
        super().__init__(V_historico, db)

    def obtener_historico(self, fkpersona):
        return self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.fkpersona == fkpersona).all()

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True)

    def listar_x_ciudad(self, idciudad):
        return self.db.query(self.entity).filter(self.entity.fkciudad == idciudad).filter(
            self.entity.enabled == True)

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro V_historico.",
                     fecha=fecha, tabla="cb_vacaciones_historico", identificador=a.id)
        super().insert(b)

        lista_Gestion = V_personalManager(self.db).actualizar_nro_vacacion(a.fkpersona, a.dias, a.operacion, objeto.user, objeto.ip, objeto.idSolicitud)

        return lista_Gestion

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico V_historico.",
                     fecha=fecha, tabla="cb_vacaciones_historico", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = estado
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó V_historico.", fecha=fecha,
                     tabla="cb_vacaciones_historico", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x

    def actualizar_vacaciones_solicitud(self, solicitud, persona, user, ip):

        fecha_historico = datetime.now(pytz.timezone('America/La_Paz'))
        nro_dias = BitacoraManager(self.db).obtener_cant_dias(solicitud.fktipovacacion, solicitud.fechai, solicitud.fechaf)
        v_historico = V_historico(fkpersona=persona, dias=nro_dias, descripcion=solicitud.descripcion, operacion="-", fecha=fecha_historico, user=user, ip=ip,idSolicitud=solicitud.id)
        lista_Gestion = V_historicoManager(self.db).insert(v_historico)

        return lista_Gestion


