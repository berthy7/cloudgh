from ...operaciones.bitacora.managers import *
from server.common.managers import SuperManager
from .models import *
from xhtml2pdf import pisa
from ...configuraciones.empresa.managers import *
from ...personal.persona.managers import *
from ...usuarios.ajustes.models import *
from ..correo.managers import *


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from xhtml2pdf import pisa

import os.path


class Report:
    def html_to_pdf(self, sourceHtml, nombre):
        outputFilename = 'server/common/resources/downloads/correo/' + nombre

        resultFile = open(outputFilename, "w+b")
        pisaStatus = pisa.CreatePDF(
            sourceHtml,
            dest=resultFile)
        resultFile.close()

        return pisaStatus.err

global report
report = Report()
global image_report

image_report = "/server/common/resources/images/logos/elfec.png"

class CorreorrhhManager(SuperManager):

    def __init__(self, db):
        super().__init__(Correorrhh, db)

    def list_all(self):
        return dict(objects=self.db.query(self.entity))

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Correo rrhh.",
                     fecha=fecha, tabla="cb_notificaciones_correos", identificador=a.id)
        super().insert(b)
        return a


    def delete(self, key, state):

        obj = self.db.query(Correorrhh).filter(Correorrhh.fkpersona == key).all()

        for ob in obj:
            ob.enabled = state
            self.db.commit()

        return ob




