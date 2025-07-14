import sqlite3
import logging
from colorama import Fore, Style 


logging.basicConfig(
    filename='activity.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

DB_FILE = 'contacts.db'

def log_action(message):
    """
    Registra un mensaje de acción en el archivo de log.

    """
    logger.info(message)

def connect_db():
    """
    Establece una conexión con la base de datos SQLite.
    Crea la base de datos si no existe.

    """
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row # Permite acceder a las columnas por nombre
        cursor = conn.cursor()
        log_action(f"Conectado a la base de datos '{DB_FILE}'.")
        return conn, cursor
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al conectar con la base de datos: {e}" + Style.RESET_ALL)
        log_action(f"Error al conectar con la base de datos: {e}")
        return None, None

def init_db():
    """
    Inicializa la base de datos creando la tabla 'contacts' si no existe.

    """
    conn, cursor = connect_db()
    if conn and cursor:
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT,
                    phone TEXT NOT NULL UNIQUE,
                    email TEXT,
                    category TEXT
                )
            ''')
            conn.commit()
            print(Fore.CYAN + "Base de datos inicializada: Tabla 'contacts' asegurada." + Style.RESET_ALL)
            log_action("Base de datos inicializada: Tabla 'contacts' creada o ya existente.")
        except sqlite3.Error as e:
            print(Fore.RED + f"Error al inicializar la base de datos: {e}" + Style.RESET_ALL)
            log_action(f"Error al inicializar la base de datos: {e}")
        finally:
            conn.close()