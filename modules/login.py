import flet as ft
from database.db_config import connect_db

def login_view(page: ft.Page, on_success):
    def check_login(e):
        username = username_input.value.strip()
        password = password_input.value.strip()

        # Validar campos vacíos
        if not username or not password:
            snack_bar = ft.SnackBar(ft.Text("Please fill in all fields!"))
            page.overlay.append(snack_bar)
            snack_bar.open = True
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
            page.go("/menu")  # Redirigir al menú principal
        else:
            snack_bar = ft.SnackBar(ft.Text("Invalid username or password!"))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

    # Inputs de usuario y contraseña
    username_input = ft.TextField(
        label="Username",
        autofocus=True,
        border_radius=10,
        border_color=ft.Colors.BLUE_800,
        focused_border_color=ft.Colors.BLUE_500,
        width=300,
        height=50,
    )

    password_input = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        border_radius=10,
        border_color=ft.Colors.BLUE_800,
        focused_border_color=ft.Colors.BLUE_500,
        width=300,
        height=50,
    )

    login_button = ft.ElevatedButton(
        "Login",
        on_click=check_login,
        bgcolor=ft.Colors.BLUE_800,
        color=ft.Colors.WHITE,
        width=300,
        height=50,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
        ),
    )

    # Diseño de la pantalla de login
    login_container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Login", size=30, weight="bold", color=ft.Colors.BLUE_800),
                username_input,
                password_input,
                login_button,
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=20,
        ),
        padding=ft.padding.all(20),
        margin=ft.margin.all(20),
        border_radius=15,
        bgcolor=ft.Colors.WHITE,
        width=400,
        height=500,
        alignment=ft.alignment.center,
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.2, ft.Colors.BLUE_900),
            offset=ft.Offset(0, 5),
        ),
    )

    # Centrar el contenedor de login en la página
    return ft.Container(
        content=login_container,
        alignment=ft.alignment.center,
        expand=True,
    )