import sqlite3
from contextlib import closing
from pathlib import Path

import flet as ft


DATABASE_PATH = Path.home() / ".modelo_cuidador" / "medicamentos.db"


def _inicializar_base_datos():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(DATABASE_PATH)) as conexion:
        with conexion:
            conexion.execute(
                """
                CREATE TABLE IF NOT EXISTS medicamentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT  NULL,
                    dosis TEXT NOT NULL,
                    horario TEXT NOT NULL
                )
                """
            )

def _cargar_medicamentos():
    with closing(sqlite3.connect(DATABASE_PATH)) as conexion:
        return conexion.execute(
            "SELECT id, nombre, dosis, horario FROM medicamentos ORDER BY id"
        ).fetchall()


def build_view(page: ft.Page) -> ft.View:
    page.title = "Registro en Tabla"

    txt_medicina = ft.TextField(
        label="Nombre",
        width=175,
        color=ft.Colors.BLACK,
    )
    txt_dosis = ft.TextField(
        label="Dosis",
        width=95,
        color=ft.Colors.BLACK,
    )
    txt_horario = ft.TextField(
        label="Horario",
        width=145,
        color=ft.Colors.BLACK,
    )
    estado = ft.Text(color=ft.Colors.RED_700)

    def texto_celda(texto, ancho):
        return ft.Container(
            width=ancho,
            content=ft.Text(
                texto or "",
                color=ft.Colors.WHITE,
                size=11,
                max_lines=1,
                overflow=ft.TextOverflow.ELLIPSIS,
            ),
        )

    def crear_fila(id_medicamento, nombre, dosis, horario):
        return ft.DataRow(
            cells=[
                ft.DataCell(texto_celda(nombre, 78)),
                ft.DataCell(texto_celda(dosis, 58)),
                ft.DataCell(texto_celda(horario, 68)),
                ft.DataCell(
                    ft.Button(
                        "X",
                        tooltip="Eliminar",
                        width=38,
                        height=32,
                        style=ft.ButtonStyle(padding=0),
                        on_click=lambda e, mid=id_medicamento: eliminar_fila(mid),
                    )
                ),
            ]
        )

    tabla = ft.DataTable(
        width=350,
        bgcolor=ft.Colors.BLACK,
        heading_row_color=ft.Colors.BLACK,
        data_row_color=ft.Colors.BLACK,
        horizontal_margin=6,
        column_spacing=6,
        heading_row_height=40,
        data_row_min_height=40,
        data_row_max_height=44,
        heading_text_style=ft.TextStyle(
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD,
            size=11,
        ),
        data_text_style=ft.TextStyle(color=ft.Colors.WHITE, size=11),
        columns=[
            ft.DataColumn(texto_celda("Nombre", 78)),
            ft.DataColumn(texto_celda("Dosis", 58)),
            ft.DataColumn(texto_celda("Horario", 68)),
            ft.DataColumn(texto_celda("Acción", 38)),
        ],
        rows=[],
    )

    def cargar_filas():
        tabla.rows = [
            crear_fila(id_medicamento, nombre, dosis, horario)
            for id_medicamento, nombre, dosis, horario in _cargar_medicamentos()
        ]

    try:
        _inicializar_base_datos()
        cargar_filas()
    except (OSError, sqlite3.Error) as error:
        estado.value = f"No se pudieron cargar los medicamentos: {error}"

    def eliminar_fila(id_medicamento):
        try:
            with closing(sqlite3.connect(DATABASE_PATH)) as conexion:
                with conexion:
                    conexion.execute(
                        "DELETE FROM medicamentos WHERE id = ?",
                        (id_medicamento,),
                    )
            cargar_filas()
        except (OSError, sqlite3.Error) as error:
            estado.value = f"No se pudo eliminar el medicamento: {error}"
        page.update()

    def agregar_fila(e):
        nombre = (txt_medicina.value or "").strip()
        dosis = (txt_dosis.value or "").strip()
        horario = (txt_horario.value or "").strip()
        if not nombre or not dosis or not horario:
            estado.value = "Completa nombre, dosis y horario."
            page.update()
            return

        try:
            with closing(sqlite3.connect(DATABASE_PATH)) as conexion:
                with conexion:
                    cursor = conexion.execute(
                        """
                        INSERT INTO medicamentos (nombre, dosis, horario)
                        VALUES (?, ?, ?)
                        """,
                        (nombre, dosis, horario),
                    )
        except (OSError, sqlite3.Error) as error:
            estado.value = f"No se pudo guardar el medicamento: {error}"
            page.update()
            return

        tabla.rows.append(
            crear_fila(cursor.lastrowid, nombre, dosis, horario)
        )
        txt_medicina.value = ""
        txt_dosis.value = ""
        txt_horario.value = ""
        estado.value = "Medicamento guardado."
        page.update()

    btn_guardar = ft.Button("Agregar", on_click=agregar_fila)

    return ft.View(
        route="/medicine_table",
        bgcolor=ft.Colors.WHITE,
        controls=[
            ft.Text(
                "Tabla de Medicina",
                color=ft.Colors.BLACK,
                size=30,
            ),
            ft.Row([txt_medicina, txt_dosis], spacing=8, wrap=True),
            ft.Row([txt_horario, btn_guardar], spacing=8, wrap=True),
            estado,
            ft.Button(
                "Regresar al menú",
                on_click=lambda _: page.navigate("/"),
            ),
            tabla,
        ],
    )
