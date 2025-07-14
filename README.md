Gestor de Contactos 
Este programa gestiona tus contactos, permitiéndote añadirlos, verlos, editarlos y eliminarlos. Utiliza sqlite3 para almacenar los datos y tabulate para una visualización clara en consola.

Uso y Funcionalidad
El programa te presentará un menú interactivo en la consola para gestionar tus contactos. Puedes añadir nuevos contactos con nombre, teléfono y otros detalles; ver la lista completa o filtrada; editar cualquier campo de un contacto existente; y eliminar los que ya no necesites. Todos los datos se guardan automáticamente en contacts.db y las acciones importantes se registran en activity.log

Requisitos y Ejecución
Asegúrate de tener Python 3 instalado. Para configurar y ejecutar:

Clona este repositorio.

Crea y activa un entorno virtual (venv):
Bash
python -m venv venv
.\venv\Scripts\activate

Instala dependencias: pip install -r requirements.txt (el archivo requirements.txt contendrá tabulate y colorama).

Ejecuta: python main.py

