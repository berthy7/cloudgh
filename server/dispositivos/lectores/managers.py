from ...configuraciones.sucursal.models import *
from ...operaciones.bitacora.managers import *
from ...dispositivos.marcaciones.models import *
from ...asistencia.asistenciapersonal.managers import AsistenciaManager
from .models import *


class LectoresManager(SuperManager):

    def __init__(self, db):
        super().__init__(Lectores, db)

    def obtener_x_nombre(self, nombre):
        return self.db.query(self.entity).filter(self.entity.nombre == nombre).first()

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.nombre.asc()).all()

    def obtener_dispositivo(self,id):
        return self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.id == id).first()

    def list_all(self):
        return dict(
            objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True)

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip_maquina, accion="Registro Lector.",
                     fecha=fecha, tabla="cb_dispositivos_lectores", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip_maquina, accion="Modifico Lector.",
                     fecha=fecha, tabla="cb_dispositivos_lectores", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = estado
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Lector.", fecha=fecha,
                     tabla="cb_dispositivos_lectores", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x

    def crear_dispositivos(self):
        sucursal = self.db.query(Sucursal).filter(Sucursal.enabled == True).first()
        self.db.add(Lectores(id=1, ip='192.168.11.218', puerto=4370, tipo="A", descripcion='Modelo Desconocido', modelo='MA300', fksucursal=sucursal.id))
        self.db.add(Lectores(id=2, ip='192.168.25.101', puerto=4370, tipo="A", descripcion='Central RRHH', modelo='G3', fksucursal=sucursal.id))
        self.db.add(Lectores(id=3, ip='192.168.25.103', puerto=4370, tipo="K", descripcion='Central Lecturas', modelo='T6C', fksucursal=sucursal.id))
        self.db.add(Lectores(id=4, ip='192.168.25.104', puerto=4370, tipo="K", descripcion='Central Heroinas', modelo='T6C', fksucursal=sucursal.id))
        self.db.add(Lectores(id=5, ip='192.168.25.105', puerto=4370, tipo="K", descripcion='Central Costaneras', modelo='T6C', fksucursal=sucursal.id))
        self.db.add(Lectores(id=6, ip='192.168.112.8', puerto=4370, tipo="K", descripcion='Quillacollo', modelo='T4-C', fksucursal=sucursal.id))
        self.db.add(Lectores(id=7, ip='192.168.113.8', puerto=4370, tipo="K", descripcion='Vinto', modelo='T6-C', fksucursal=sucursal.id))
        self.db.add(Lectores(id=8, ip='192.168.114.8', puerto=4370, tipo="K", descripcion='Eterazama', modelo='K40', fksucursal=sucursal.id))
        self.db.add(Lectores(id=9, ip='192.168.115.8', puerto=4370, tipo="M", descripcion='Totora', modelo='MA300', fksucursal=sucursal.id))
        self.db.add(Lectores(id=10, ip='192.168.116.8', puerto=4370, tipo="K", descripcion='K40', modelo='K40',fksucursal=sucursal.id))
        self.db.add(Lectores(id=11, ip='192.168.118.8', puerto=4370, tipo="K", descripcion='Tiquipaya', modelo='K40', fksucursal=sucursal.id))
        self.db.add(Lectores(id=12, ip='192.168.119.8', puerto=4370, tipo="K", descripcion='Villa Tunari', modelo='K40',fksucursal=sucursal.id))
        self.db.add(Lectores(id=13, ip='192.168.120.8', puerto=4370, tipo="K", descripcion='Mizque', modelo='K40', fksucursal=sucursal.id))
        self.db.add(Lectores(id=14, ip='192.168.121.8', puerto=4370, tipo="K", descripcion='Punata', modelo='T4-C', fksucursal=sucursal.id))
        self.db.add(Lectores(id=15, ip='192.168.122.8', puerto=4370, tipo="K", descripcion='Tarata', modelo='K40', fksucursal=sucursal.id))
        self.db.add(Lectores(id=16, ip='192.168.123.8', puerto=4370, tipo="M", descripcion='Tiraque', modelo='K40', fksucursal=sucursal.id))
        self.db.add(Lectores(id=17, ip='192.168.124.8', puerto=4370, tipo="K", descripcion='Cliza', modelo='X628-C', fksucursal=sucursal.id))
        self.db.add(Lectores(id=18, ip='192.168.125.8', puerto=4370, tipo="K", descripcion='Sacaba', modelo='K40', fksucursal=sucursal.id))
        self.db.add(Lectores(id=19, ip='192.168.126.8', puerto=4370, tipo="M", descripcion='Colomi', modelo='K40', fksucursal=sucursal.id))
        self.db.add(Lectores(id=20, ip='192.168.127.8', puerto=4370, tipo="K", descripcion='Arani', modelo='K40', fksucursal=sucursal.id))
        self.db.add(Lectores(id=21, ip='192.168.128.8', puerto=4370, tipo="K", descripcion='Capinota', modelo='K40', fksucursal=sucursal.id))
        self.db.add(Lectores(id=22, ip='192.168.129.8', puerto=4370, tipo="A", descripcion='Morochata', modelo='MA300', fksucursal=sucursal.id))
        self.db.add(Lectores(id=23, ip='192.168.130.8', puerto=4370, tipo="A", descripcion='Independecia', modelo='MA300',fksucursal=sucursal.id))
        self.db.add(Lectores(id=24, ip='192.168.131.8', puerto=4370, tipo="K", descripcion='Sipe Sipe', modelo='K40', fksucursal=sucursal.id))
        self.db.add(Lectores(id=25, ip='192.168.132.8', puerto=4370, tipo="K", descripcion='Entrerios', modelo='K40', fksucursal=sucursal.id))
        self.db.add(Lectores(id=26, ip='192.168.133.8', puerto=4370, tipo="K", descripcion='Ivirgarzama', modelo='MA300', fksucursal=sucursal.id))
        self.db.add(Lectores(id=27, ip='192.168.134.8', puerto=4370, tipo="K", descripcion='Seminario', modelo='T4C', fksucursal=sucursal.id))
        self.db.add(Lectores(id=28, ip='192.168.135.8', puerto=4370, tipo="K", descripcion='Seguro Delegado', modelo='Silkbio T100', fksucursal=sucursal.id))
        self.db.add(Lectores(id=29, ip='192.168.136.8', puerto=4370, tipo="M", descripcion='Bolivar', modelo='MA300', fksucursal=sucursal.id))
        self.db.add(Lectores(id=30, ip='192.168.137.8', puerto=4370, tipo="M", descripcion='Cocapata', modelo='MA300', fksucursal=sucursal.id))
        self.db.add(Lectores(id=31, ip='192.168.138.8', puerto=4370, tipo="M", descripcion='Tapacari', modelo='MA300', fksucursal=sucursal.id))
        self.db.add(Lectores(id=32, ip='192.168.139.8', puerto=4370, tipo="M", descripcion='Pocona', modelo='MA300', fksucursal=sucursal.id))
        self.db.add(Lectores(id=33, ip='192.168.140.8', puerto=4370, tipo="M", descripcion='Pojo', modelo='MA300', fksucursal=sucursal.id))
        self.db.add(Lectores(id=34, ip='192.168.141.8', puerto=4370, tipo="M", descripcion='Omereque', modelo='MA300', fksucursal=sucursal.id))
        self.db.add(Lectores(id=35, ip='192.168.142.8', puerto=4370, tipo="M", descripcion='Pasorapa', modelo='MA300', fksucursal=sucursal.id))
        self.db.add(Lectores(id=36, ip='192.168.143.8', puerto=4370, tipo="K", descripcion='Anzaldo', modelo='MA300', fksucursal=sucursal.id))

        self.db.commit()

    def preparar_dispositivos(self):
        dispositivos = self.db.query(Lectores).filter(Lectores.tipo == "A").filter(Lectores.enabled == True).all()

        for dispositivo in dispositivos:
            LectoresManager(self.db).extraer_marcaciones(dispositivo)
        self.db.close()

    def extraer_marcaciones(self, dispositivo):
        from zklib import zklib
        try:

            zk = zklib.ZKLib(dispositivo.ip, dispositivo.puerto)
            print('Extrayendo marcaciones: ', dispositivo.ip)
            ret = zk.connect()
            if ret:
                marcaciones = zk.getAttendance()
                if marcaciones:
                    for marcacion in marcaciones:
                        aux = marcacion[2]
                        query = self.db.query(Marcaciones).filter(Marcaciones.codigo == marcacion[0]).filter(Marcaciones.time == aux).all()
                        if not query:
                            self.db.add(Marcaciones(time=aux, fkdispositivo=dispositivo.id, codigo=marcacion[0]))
                            AsistenciaManager(self.db).insertar_marcaciones(aux,marcacion[0])
                    self.db.commit()

                zk.getTime()
                zk.enableDevice()
                zk.disconnect()
                print('Terminaron las marcaciones ', dispositivo.ip)
                m = 'Marcaciones Extraidas Correctamente '+ str(dispositivo.ip)
                return dict(estado=True, mensaje=m)
            else:
                print('No se puedo conectar con el dispositivo: ', dispositivo.ip)
                m = 'No se puedo conectar con el dispositivo ' + str(dispositivo.ip)
                return dict(estado=False, mensaje=m)
        except Exception as e:
            print(e)
            return dict(estado=False, mensaje=str(e))



