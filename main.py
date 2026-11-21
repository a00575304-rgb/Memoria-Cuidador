# Modelo de cuidador para la aplicación de sanación
import flet as ft
#Version de Flet 1.1.2 
from family import build_view as family_view
from family_add import build_view as family_add_view
from medicine_table import build_view as medicine_table_view
from localizador import build_view as localizador
from Emergencia import build_view as emergencia_view
from estadistica import build_view as estadistica_view
async def cerrar_app(e):
    await e.page.window.close()
async def ir_a_family(e):
    e.page.navigate("/family")
async def ir_a_localizador(e):
    e.page.navigate("/localizador")
async def ir_a_medicina(e):
    e.page.navigate("/medicine_table")
async def ir_a_emergencia(e):
    e.page.navigate("/emergencia")
async def ir_a_estadistica(e):
    e.page.navigate("/matrizbarra")

async def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = "Memoria - Menu principal"
    page.bgcolor = ft.Colors.WHITE
    page.window.width = 390
    page.window.height = 844
    page.window.resizable = False
    await page.window.center()

    mi_boton = ft.Button(
        content="Salir",
        bgcolor=ft.Colors.RED_600,
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=15,
        ),
        on_click=cerrar_app,
    )
    boton_familia = ft.Button(
        content="Mi Familia",
        bgcolor=ft.Colors.PURPLE_500,
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=15,
        ),
        width=200,
        height=100,
        on_click=ir_a_family,
    )
    boton_localizador = ft.Button(
        content="Localizador",
        bgcolor=ft.Colors.ORANGE_600,
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=15,
        ),
        width=200,
        height=100,
        on_click=ir_a_localizador,
    )
    boton_medicina = ft.Button(
        content="Medicina",
        bgcolor=ft.Colors.INDIGO,
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=15,
        ),
        width=200,
        height=100,
        on_click=ir_a_medicina,
    )
    boton_emergencia = ft.Button(
        content="Emergencia",
        bgcolor=ft.Colors.RED_600,
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=15,
        ),
        width=200,
        height=100,
        on_click=ir_a_emergencia,
    )
    boton_estadistica = ft.Button(
        content="Estadistica",
        bgcolor=ft.Colors.PURPLE,
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=15,
        ),
        width=200,
        height=100,
        on_click=ir_a_estadistica,
    )
    def home_view() -> ft.View:
        return ft.View(
            bgcolor=ft.Colors.WHITE,
            route="/",
            controls=[
                ft.Text(
                    "Memoria cuidador",
                    color=ft.Colors.BLACK,
                    size=30,
                    weight=ft.FontWeight.BOLD,
                ),
                boton_familia,
                boton_localizador,
                boton_medicina,
                boton_estadistica,
                boton_emergencia,
                mi_boton,
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def route_change(e=None):
        page.views.clear()
        page.views.append(home_view())

        if page.route == "/family":
            page.views.append(family_view(page))
        elif page.route == "/family_add":
            page.views.append(family_view(page))
            page.views.append(family_add_view(page))
        elif page.route == "/localizador":
            page.views.append(localizador(page))
        elif page.route == "/medicine_table":
            page.views.append(medicine_table_view(page))
        elif page.route == "/emergencia":
            page.views.append(emergencia_view(page))
        elif page.route == "/matrizbarra":
            page.views.append(estadistica_view(page))
        page.update()

    page.on_route_change = route_change
    route_change()


if __name__ == "__main__":
    ft.run(main, view=ft.AppView.FLET_APP)