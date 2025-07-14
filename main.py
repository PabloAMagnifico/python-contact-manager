import contact_manager
import database
from colorama import init, Fore, Style


init(autoreset=True) 

def display_menu():
    """
    Muestra el menú de opciones al usuario en la consola.

    """
    print(Fore.CYAN + Style.BRIGHT + "\n--- GESTOR DE CONTACTOS ---" + Style.RESET_ALL)
    print(Fore.YELLOW + "1. Añadir contacto")
    print(Fore.YELLOW + "2. Ver contactos")
    print(Fore.YELLOW + "3. Editar contacto")
    print(Fore.YELLOW + "4. Eliminar contacto")
    print(Fore.RED + "5. Salir")
    print(Fore.CYAN + Style.BRIGHT + "---------------------------" + Style.RESET_ALL)

def main():
    """
    Función principal del gestor de contactos.
    Gestiona el bucle del menú y la interacción con el usuario.

    """
    database.init_db() 

    while True:
        display_menu()
        choice = input(Fore.GREEN + "Elige una opción: " + Style.RESET_ALL).strip()

        if choice == '1':
            print(Fore.BLUE + "\n--- AÑADIR NUEVO CONTACTO ---" + Style.RESET_ALL)
            first_name = input("Primer Nombre (obligatorio): ").strip()
            last_name = input("Apellido (opcional): ").strip()
            phone = input("Teléfono (obligatorio, único): ").strip()
            email = input("Email (opcional): ").strip()
            category = input("Categoría (ej. Familia, Trabajo, Amigos, opcional): ").strip()
            
            contact_manager.add_contact(first_name, last_name, phone, email, category)
            input(Fore.LIGHTBLACK_EX + "\nPresiona Enter para continuar..." + Style.RESET_ALL)

        elif choice == '2':
            print(Fore.BLUE + "\n--- VER CONTACTOS ---" + Style.RESET_ALL)
            filter_option = input("¿Quieres filtrar? (s/n): ").strip().lower()
            filter_by = None
            filter_value = None
            if filter_option == 's':
                filter_by = input("Filtrar por (first_name, last_name, phone, email, category): ").strip().lower()
                filter_value = input(f"Introduce el valor para '{filter_by}': ").strip()
            
            sort_by_option = input("¿Quieres ordenar? (s/n): ").strip().lower()
            sort_by = 'first_name'
            order = 'ASC'
            if sort_by_option == 's':
                sort_by = input("Ordenar por (id, first_name, last_name, phone, email, category): ").strip().lower()
                order_input = input("Orden (ASC/DESC): ").strip().upper()
                if order_input in ['ASC', 'DESC']:
                    order = order_input
            
            contact_manager.view_contacts(filter_by, filter_value, sort_by, order)
            input(Fore.LIGHTBLACK_EX + "\nPresiona Enter para continuar..." + Style.RESET_ALL)

        elif choice == '3':
            print(Fore.BLUE + "\n--- EDITAR CONTACTO ---" + Style.RESET_ALL)
            try:
                contact_id = int(input("Introduce el ID del contacto a editar: ").strip())
                contact = contact_manager.get_contact_by_id(contact_id)
                if contact:
                    print(Fore.CYAN + f"Contacto actual: ID {contact['id']}, Nombre: {contact['first_name']} {contact['last_name']}, Teléfono: {contact['phone']}, Email: {contact['email']}, Categoría: {contact['category']}" + Style.RESET_ALL)
                    field_to_update = input("Campo a editar (first_name, last_name, phone, email, category): ").strip().lower()
                    new_value = input(f"Nuevo valor para '{field_to_update}': ").strip()
                    
                    contact_manager.update_contact(contact_id, field_to_update, new_value)
                else:
                    print(Fore.RED + f"No se encontró ningún contacto con el ID {contact_id}." + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "ID inválido. Por favor, introduce un número entero." + Style.RESET_ALL)
            input(Fore.LIGHTBLACK_EX + "\nPresiona Enter para continuar..." + Style.RESET_ALL)

        elif choice == '4':
            print(Fore.BLUE + "\n--- ELIMINAR CONTACTO ---" + Style.RESET_ALL)
            try:
                contact_id = int(input("Introduce el ID del contacto a eliminar: ").strip())
                contact_manager.delete_contact(contact_id)
            except ValueError:
                print(Fore.RED + "ID inválido. Por favor, introduce un número entero." + Style.RESET_ALL)
            input(Fore.LIGHTBLACK_EX + "\nPresiona Enter para continuar..." + Style.RESET_ALL)

        elif choice == '5':
            print(Fore.MAGENTA + "¡Gracias por usar el Gestor de Contactos! ¡Hasta pronto!" + Style.RESET_ALL)
            database.log_action("Aplicación terminada.")
            break 
        else:
            print(Fore.RED + "Opción no válida. Por favor, elige una opción del 1 al 5." + Style.RESET_ALL)
            input(Fore.LIGHTBLACK_EX + "\nPresiona Enter para continuar..." + Style.RESET_ALL)


if __name__ == "__main__":
    main()