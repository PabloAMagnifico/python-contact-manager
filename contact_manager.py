import database
import sqlite3 
from tabulate import tabulate
from colorama import Fore, Style

def add_contact(first_name, last_name, phone, email, category):
    """
    Añade un nuevo contacto a la base de datos.
    
    """
    if not first_name or not phone:
        print(Fore.RED + "Error: El nombre y el teléfono son campos obligatorios." + Style.RESET_ALL)
        return False

    conn, cursor = database.connect_db()
    if conn and cursor:
        try:
            cursor.execute('''
                INSERT INTO contacts (first_name, last_name, phone, email, category)
                VALUES (?, ?, ?, ?, ?)
            ''', (first_name, last_name, phone, email, category))
            conn.commit()
            print(Fore.GREEN + f"Contacto '{first_name} {last_name}' añadido con éxito." + Style.RESET_ALL)
            database.log_action(f"Contacto añadido: {first_name} {last_name} ({phone})")
            return True
        except sqlite3.IntegrityError:
            print(Fore.RED + f"Error: Ya existe un contacto con el teléfono '{phone}'. El teléfono debe ser único." + Style.RESET_ALL)
            database.log_action(f"Error al añadir contacto: Teléfono duplicado '{phone}'.")
            return False
        except sqlite3.Error as e:
            print(Fore.RED + f"Error al añadir contacto: {e}" + Style.RESET_ALL)
            database.log_action(f"Error al añadir contacto: {e}")
            return False
        finally:
            conn.close()
    return False

def view_contacts(filter_by=None, value=None, sort_by='first_name', order='ASC'):
    """
    Muestra la lista de contactos, con opciones de filtrado y ordenación.

    """
    conn, cursor = database.connect_db()
    if conn and cursor:
        try:
            query = "SELECT id, first_name, last_name, phone, email, category FROM contacts"
            params = []

            if filter_by and value:
                if filter_by in ['first_name', 'last_name', 'category', 'email']:
                    query += f" WHERE {filter_by} LIKE ?"
                    params.append(f'%{value}%')
                elif filter_by == 'phone':
                    query += " WHERE phone LIKE ?"
                    params.append(f'%{value}%')
                else:
                    print(Fore.YELLOW + f"Filtro '{filter_by}' no válido. Mostrando todos los contactos." + Style.RESET_ALL)
            
            if sort_by in ['id', 'first_name', 'last_name', 'phone', 'email', 'category']:
                query += f" ORDER BY {sort_by} {order}"
            else:
                print(Fore.YELLOW + f"Ordenación por '{sort_by}' no válida. Ordenando por 'first_name'." + Style.RESET_ALL)
                query += " ORDER BY first_name ASC"

            cursor.execute(query, params)
            contacts = cursor.fetchall()

            if not contacts:
                print(Fore.YELLOW + "No hay contactos para mostrar con los criterios actuales." + Style.RESET_ALL)
                database.log_action(f"No se encontraron contactos con filtro: {filter_by}={value}")
                return

            headers = [Fore.CYAN + h for h in ["ID", "Primer Nombre", "Apellido", "Teléfono", "Email", "Categoría"]]
            
            """ 
            Convertir Rows a listas para tabulate y aplicar colores a las celdas 
            
            """ 
            table_data = []
            for contact in contacts:
                
                row = [
                    Fore.MAGENTA + str(contact['id']) + Style.RESET_ALL,
                    Fore.WHITE + contact['first_name'] + Style.RESET_ALL,
                    (Fore.WHITE + contact['last_name'] + Style.RESET_ALL) if contact['last_name'] else '',
                    Fore.YELLOW + contact['phone'] + Style.RESET_ALL,
                    (Fore.GREEN + contact['email'] + Style.RESET_ALL) if contact['email'] else '',
                    (Fore.BLUE + contact['category'].capitalize() + Style.RESET_ALL) if contact['category'] else ''
                ]
                table_data.append(row)

            print(Fore.BLUE + "\n--- LISTA DE CONTACTOS ---" + Style.RESET_ALL)
            print(tabulate(table_data, headers=headers, tablefmt="fancy_grid")) 
            database.log_action(f"Contactos mostrados. Filtro: {filter_by}={value}, Orden: {sort_by} {order}")

        except sqlite3.Error as e:
            print(Fore.RED + f"Error al recuperar contactos: {e}" + Style.RESET_ALL)
            database.log_action(f"Error al recuperar contactos: {e}")
        finally:
            conn.close()

def update_contact(contact_id, field, new_value):
    """
    Actualiza un campo específico de un contacto en la base de datos.

    """
    if not isinstance(contact_id, int) or contact_id <= 0:
        print(Fore.RED + "Error: ID de contacto inválido." + Style.RESET_ALL)
        return False
    
    valid_fields = ['first_name', 'last_name', 'phone', 'email', 'category']
    if field not in valid_fields:
        print(Fore.RED + f"Error: Campo '{field}' no válido para actualizar." + Style.RESET_ALL)
        return False

    conn, cursor = database.connect_db()
    if conn and cursor:
        try:
            """ 
            Verifica si el contacto existe
            
            """
            cursor.execute("SELECT id FROM contacts WHERE id = ?", (contact_id,))
            if cursor.fetchone() is None:
                print(Fore.RED + f"Error: No se encontró ningún contacto con el ID {contact_id}." + Style.RESET_ALL)
                database.log_action(f"Intento de actualizar contacto ID {contact_id}: No encontrado.")
                return False

            query = f"UPDATE contacts SET {field} = ? WHERE id = ?"
            cursor.execute(query, (new_value, contact_id))
            conn.commit()
            print(Fore.GREEN + f"Contacto con ID {contact_id} actualizado: '{field}' a '{new_value}'." + Style.RESET_ALL)
            database.log_action(f"Contacto actualizado: ID {contact_id}, Campo '{field}' a '{new_value}'.")
            return True
        except sqlite3.IntegrityError: 
            print(Fore.RED + f"Error: El valor '{new_value}' para el campo '{field}' ya existe y debe ser único." + Style.RESET_ALL)
            database.log_action(f"Error al actualizar contacto ID {contact_id}: Valor duplicado para '{field}'.")
            return False
        except sqlite3.Error as e:
            print(Fore.RED + f"Error al actualizar contacto: {e}" + Style.RESET_ALL)
            database.log_action(f"Error al actualizar contacto: {e}")
            return False
        finally:
            conn.close()
    return False

def delete_contact(contact_id):
    """
    Elimina un contacto de la base de datos por su ID.

    """
    if not isinstance(contact_id, int) or contact_id <= 0:
        print(Fore.RED + "Error: ID de contacto inválido." + Style.RESET_ALL)
        return False

    conn, cursor = database.connect_db()
    if conn and cursor:
        try:
            cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
            conn.commit()
            if cursor.rowcount > 0: 
                print(Fore.GREEN + f"Contacto con ID {contact_id} eliminado con éxito." + Style.RESET_ALL)
                database.log_action(f"Contacto eliminado: ID {contact_id}.")
                return True
            else:
                print(Fore.YELLOW + f"Error: No se encontró ningún contacto con el ID {contact_id}." + Style.RESET_ALL)
                database.log_action(f"Intento de eliminar contacto ID {contact_id}: No encontrado.")
                return False
        except sqlite3.Error as e:
            print(Fore.RED + f"Error al eliminar contacto: {e}" + Style.RESET_ALL)
            database.log_action(f"Error al eliminar contacto: {e}")
            return False
        finally:
            conn.close()
    return False

def get_contact_by_id(contact_id):
    """
    Obtiene un contacto por su ID. Útil para verificar existencia antes de actualizar/eliminar.

    """
    conn, cursor = database.connect_db()
    if conn and cursor:
        try:
            cursor.execute("SELECT id, first_name, last_name, phone, email, category FROM contacts WHERE id = ?", (contact_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(Fore.RED + f"Error al buscar contacto por ID: {e}" + Style.RESET_ALL)
            database.log_action(f"Error al buscar contacto ID {contact_id}: {e}")
            return None
        finally:
            conn.close()
    return None