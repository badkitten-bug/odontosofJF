import flet as ft
from database.db_config import connect_db

def login_view(page: ft.Page, on_success):
    def check_login(e):
        username = username_input.value.strip()
        password = password_input.value.strip()

        # Validar campos vacíos
        if not username or not password:
            page.snack_bar = ft.SnackBar(ft.Text("Please fill in all fields!"))
            page.snack_bar.open = True
            page.update()
            return

        # Consultar base de datos
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, role FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()

        # Validar credenciales
        if user:
            user_id, role = user
            on_success({"id": user_id, "role": role})  # Devuelve los detalles del usuario
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Invalid username or password!"))
            page.snack_bar.open = True
            page.update()

    # Inputs de usuario y contraseña
    username_input = ft.TextField(label="Username", autofocus=True)
    password_input = ft.TextField(label="Password", password=True, can_reveal_password=True)
    login_button = ft.ElevatedButton("Login", on_click=check_login)

    # Diseño de la pantalla de login
    return ft.Column(
        [
            ft.Text("Login", size=24, weight="bold"),
            username_input,
            password_input,
            login_button,
        ],
        alignment="center",
        horizontal_alignment="center",
    )
