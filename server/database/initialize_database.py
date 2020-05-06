import sqlite3
import sys

from sqlalchemy.engine import create_engine
from configparser import ConfigParser

from ..usuarios.scripts import insertions as user_insertions
from ..calendario.scripts import insertions as calendario_insertions
from ..asistencia.scripts import insertions as asistencia_insertions
from ..vacaciones.scripts import insertions as vacaciones_insertions
from ..comensales.scripts import insertions as comensal_insertions
from ..dispositivos.scripts import insertions as dispositivos_insertions
from ..personal.scripts import insertions as personal_insertions
from ..configuraciones.scripts import insertions as configuraciones_insertions
from ..control.scripts import insertions as control_insertions
from ..notificaciones.scripts import insertions as notificaciones_insertions
from ..portal.scripts import insertions as portal_insertions


from server.database import connection
from .models import Base


def main():
    reload_db()
    user_insertions()
    calendario_insertions()
    asistencia_insertions()
    vacaciones_insertions()
    notificaciones_insertions()
    comensal_insertions()
    dispositivos_insertions()
    personal_insertions()
    portal_insertions()
    control_insertions()
    configuraciones_insertions()
    print('Database created/updated correctly!')


def reload_db():
    config = ConfigParser()
    config.read('settings.ini')
    db_url = config['Database']['url']
    connection.db_url = config['Database']['url']
    if 'sqlite' in db_url:
        dbname = db_url.split('///')[1]
        sqlite3.connect(dbname)
    engine = create_engine(config['Database']['url'])
    Base.metadata.drop_all(engine, checkfirst=True)
    Base.metadata.create_all(engine, checkfirst=True)


if __name__ == '__main__':
    sys.exit(int(main() or 0))
