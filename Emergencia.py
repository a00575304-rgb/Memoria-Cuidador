import flet as ft

def build_view(page: ft.Page) -> ft.View:
    return ft.View(
        route="/emergencia",
        bgcolor=ft.Colors.RED,
        controls=[
            ft.Text("Emergencia", size=60,color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            ft.Button(
                "Regresar al menú",
                on_click=lambda _: page.navigate("/"),
            ),
        ],
    )