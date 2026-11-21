import flet as ft
import flet as ft
import flet_map as ftm


def build_view(page: ft.Page) -> ft.View:
    page.title = "Google Maps en Flet 1.1.2"
    page.padding = 0

    mapa = ftm.Map(
        expand=True,
        initial_center=ftm.MapLatitudeLongitude(21.1220, -101.6820), # Ej. León, Gto.
        initial_zoom=13,
        layers=[
            ftm.TileLayer(
                # lyrs=m (mapa estándar), s (satélite), y (híbrido), t (terreno)
                url_template="https://google.com{x}&y={y}&z={z}",
                user_agent_package_name="com.tuapp.ejemplo",
            ),
            ftm.MarkerLayer(
                markers=[
                    ftm.Marker(
                        content=ft.Icon(ft.Icons.LOCATION_ON, color=ft.Colors.RED, size=40),
                        coordinates=ftm.MapLatitudeLongitude(21.1220, -101.6820),
                    )
                ]
            ),
            ftm.SimpleAttribution(text="Google Maps"),
        ],
    )

    page.add(ft.SafeArea(expand=True, content=mapa))
    page.update()
    def regresar_al_menu(e):
        page.navigate("/")

    vista = ft.View(
#        route="/localizador",
        bgcolor=ft.Colors.WHITE,
        controls=[
            ft.Text("Localizador en Maps", size=24,color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD),
            ft.Button(
                "Regresar al menú",
                on_click=regresar_al_menu,
            ),
            mapa,
        ],
    )
    return vista