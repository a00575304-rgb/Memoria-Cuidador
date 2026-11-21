import flet as ft


def build_view(page: ft.Page) -> ft.View:
    return ft.View(
        route="/family",
        bgcolor=ft.Colors.WHITE,
        controls=[
            ft.Text("Familia", size=30,color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD),
            ft.Button("Agregar miembro", on_click=lambda _: page.navigate("/family_add")),
            ft.Button(
                "Regresar al menú",
                on_click=lambda _: page.navigate("/"),
            ),
        ],
    )
