import sqlite3
from contextlib import closing
from pathlib import Path

import flet as ft


DATABASE_PATH = Path.home() / ".modelo_cuidador" / "familia.db"


def _inicializar_base_datos():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(DATABASE_PATH)) as conexion:
        with conexion:
            conexion.execute(
                """
                CREATE TABLE IF NOT EXISTS familia (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    edad TEXT,
                    relacion TEXT,
                    detalles TEXT,
                    imagen_path TEXT
                )
                """
            )

def obtener_datos():
    # Conexión y consulta a la base de datos
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, edad, relacion, detalles, imagen_path FROM familia")
    registros = cursor.fetchall()
    conn.close()
    return registros

def build_view(page: ft.Page) -> ft.View:
    file_picker = ft.FilePicker()
    page.services.append(file_picker)

    txt_nombre = ft.TextField(
        label="Nombre del miembro",
        width=300,
        color=ft.Colors.BLACK,
    )
    txt_edad = ft.TextField(
        label="Edad",
        width=300,
        color=ft.Colors.BLACK,
        #keyboard_type=ft.KeyboardType.NUMBER,
    )
    txt_relacion = ft.TextField(
        label="Relación",
        width=300,
        color=ft.Colors.BLACK,
    )
    txt_detalles = ft.TextField(
        label="Detalles extra:",
        width=300,
        color=ft.Colors.BLACK,
        multiline=True,
    )
    estado = ft.Text()
    ruta_imagen = None

    imagen_mostrada = ft.Image(
        src="",
        width=150,
        height=150,
        fit=ft.BoxFit.CONTAIN,
        visible=False,
    )

    async def seleccionar_imagen(e):
        nonlocal ruta_imagen
        archivos = await file_picker.pick_files(
            dialog_title="Selecciona una imagen",
            file_type=ft.FilePickerFileType.IMAGE,
            allow_multiple=False,
        )

        if archivos:
            ruta_imagen = archivos[0].path
            imagen_mostrada.src = ruta_imagen
            imagen_mostrada.visible = True
            page.update()
    def guardar_miembro(e):
        nombre = (txt_nombre.value or "").strip()
        edad_texto = (txt_edad.value or "").strip()
        relacion = (txt_relacion.value or "").strip()
        detalles = (txt_detalles.value or "").strip()

        if not nombre:
            estado.value = "Escribe el nombre del familiar."
            page.update()
            return

        try:
            edad = int(edad_texto) if edad_texto else None
        except ValueError:
            estado.value = "La edad debe ser un número entero."
            page.update()
            return

        try:
            _inicializar_base_datos()
            with closing(sqlite3.connect(DATABASE_PATH)) as conexion:
                with conexion:
                    conexion.execute(
                        """
                        INSERT INTO familia
                            (nombre, edad, relacion, detalles, imagen_path)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (nombre, edad, relacion, detalles, ruta_imagen),
                    )
        except (OSError, sqlite3.Error) as error:
            estado.value = f"No se pudo guardar el miembro: {error}"
            page.update()
            return
        estado.value = "Miembro guardado."
        page.update()

    return ft.View(
        route="/family_add",
        bgcolor=ft.Colors.WHITE,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text("Agregar miembro",color=ft.Colors.BLACK, size=30),
            ft.Button(
                content="Insertar imagen",
                icon=ft.Icons.ADD_PHOTO_ALTERNATE,
                on_click=seleccionar_imagen,
            ),ft.Button("Guardar miembro", on_click=guardar_miembro),
            ft.Button("Regresar a Familia",
                on_click=lambda _: page.navigate("/family"),
            ),
            txt_nombre,
            txt_edad,
            txt_relacion,
            txt_detalles,
            imagen_mostrada,
            estado,
        ],
    )
