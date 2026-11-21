from io import BytesIO
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, ConfusionMatrixDisplay, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import os
import flet as ft


def _figure_to_png(fig: plt.Figure) -> bytes:
    image = BytesIO()
    fig.savefig(image, format="png", bbox_inches="tight")
    plt.close(fig)
    return image.getvalue()


def load_and_preprocess_alzheimer_data() -> tuple[bytes, bytes]:
    # Obtiene la ruta exacta de la carpeta donde está estadistica.py
    ruta_carpeta = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(ruta_carpeta, "alzheimer.csv")

    subir = pd.read_csv(ruta_csv)
    # `subir` ya es un DataFrame; no es contenido binario para BytesIO.
    df = subir.copy()
    # Eliminar 'Converted' directamente de df y crear df2
    df2 = df[df['Group'] != 'Converted'].copy()

    # Imputar valores faltantes en SES y MMSE correctamente
    imputer = SimpleImputer(strategy='median')
    df2[['SES', 'MMSE']] = imputer.fit_transform(df2[['SES', 'MMSE']])

    # Convertir Group (0 = Demented, 1 = Nondemented) y M/F (0 = F, 1 = M) a números
    df2_encoded = pd.get_dummies(df2, columns=['Group', 'M/F'], drop_first=True, dtype=int)

    print(df2_encoded.head())
    # Asegurar que M/F esté convertido a numérico (0 y 1) si aún es texto
    if 'M/F' in df2_encoded.columns:
        df2_encoded = pd.get_dummies(df2_encoded, columns=['M/F'], drop_first=True, dtype=int)

    # X son todas las columnas excepto la variable dependiente 'Group_Nondemented'
    X_synth = df2_encoded.drop(columns=['Group_Nondemented'])

    # y es la única columna dependiente (0 = Demented, 1 = Nondemented)
    y_synth = df2_encoded['Group_Nondemented']

    # Dividir en entrenamiento (80%) y prueba (20%) a traves de la regla de parento
    X_train_synth, X_test_synth, y_train_synth, y_test_synth = train_test_split(
        X_synth, y_synth, test_size=0.2, random_state=42
    )

    # Escalar las características
    scaler = StandardScaler()
    X_train_scaled_synth = scaler.fit_transform(X_train_synth)
    X_test_scaled_synth = scaler.transform(X_test_synth)
    from sklearn.linear_model import LogisticRegression

    # 1. Instanciar el modelo de regresión logística
    log_reg_synth = LogisticRegression(random_state=42)

    # 2. Ajustar el modelo con los datos de entrenamiento escalados
    log_reg_synth.fit(X_train_scaled_synth, y_train_synth)

    # 3. Realizar predicciones sobre el conjunto de prueba
    y_pred_synth = log_reg_synth.predict(X_test_scaled_synth)

    cm_synth = confusion_matrix(y_test_synth, y_pred_synth)

    fig_cm, ax_cm = plt.subplots(figsize=(6, 5))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm_synth, display_labels=['Demented', 'Nondemented'])
    disp.plot(ax=ax_cm, cmap='Oranges', values_format='n')
    ax_cm.set_title('Matriz de Confusión - Alzheimer (Demented vs Nondemented)')
    ax_cm.grid(False)
    imagen_matriz = _figure_to_png(fig_cm)

    print("--- Reporte de Clasificación ---")
    print(classification_report(y_test_synth, y_pred_synth, target_names=['Demented', 'Nondemented']))

    # Tabla de coeficientes
    coeficientes = log_reg_synth.coef_[0]
    importancia_coef = pd.DataFrame({
        'Característica': X_synth.columns,
        'Coeficiente': coeficientes,
        'Impacto Absoluto': abs(coeficientes)
    }).sort_values(by='Coeficiente', ascending=False)

    print(f"Intercepto (Sesgo): {log_reg_synth.intercept_[0]:.4f}\n")
    print(importancia_coef.to_string(index=False))
    from sklearn.model_selection import cross_val_score

    # Instanciamos el modelo ajustado para evitar sobreajuste en muestras médicas pequeñas
    modelo_rf = RandomForestClassifier(
        n_estimators=200,        # Número de árboles en el bosque
        max_depth=5,             # Limita la profundidad para que no memorice los datos
        min_samples_split=5,     # Mínimo de pacientes para dividir un nodo
        class_weight='balanced', # Compensa el ligero desbalance entre Demented y Nondemented
        random_state=42
    )

    # Validación cruzada (5 pliegues) sobre el entrenamiento para medir estabilidad real
    scores_cv = cross_val_score(modelo_rf, X_train_synth, y_train_synth, cv=5, scoring='accuracy')
    print(f"Exactitud promedio en Validación Cruzada (5-fold): {scores_cv.mean():.2f} (+/- {scores_cv.std():.2f})")

    # Entrenamos el modelo con los datos de Alzheimer (sin escalar)
    modelo_rf.fit(X_train_synth, y_train_synth)
    print("¡Modelo Random Forest de Alzheimer entrenado con éxito!")
    importancias = pd.DataFrame({
        'Característica': X_train_synth.columns,
        'Importancia': modelo_rf.feature_importances_
    }).sort_values(by='Importancia', ascending=False)

    print("--- Importancia de Variables en Random Forest ---")
    print(importancias.to_string(index=False))

    # Gráfica de barras de importancia
    fig_importancias, ax_importancias = plt.subplots(figsize=(8, 4))
    sns.barplot(data=importancias, x='Importancia', y='Característica', palette='viridis', ax=ax_importancias)
    ax_importancias.set_title('Importancia de las Características - Random Forest')
    fig_importancias.tight_layout()
    imagen_importancias = _figure_to_png(fig_importancias)

    return imagen_matriz, imagen_importancias


def build_view(page: ft.Page) -> ft.View:
    imagen_matriz, imagen_importancias = load_and_preprocess_alzheimer_data()

    return ft.View(
        route="/matrizbarra",
        bgcolor=ft.Colors.WHITE,
        scroll="auto",
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text("Estadísticas", size=32, color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD),
            ft.Text("Matriz de confusión", size=20, color=ft.Colors.BLACK),
            ft.Button(
                "Regresar al menú",
                on_click=lambda _: page.navigate("/"),
            ),
            ft.Image(
                src=imagen_matriz,
                width=350,
                height=290,
                fit=ft.BoxFit.CONTAIN,
                semantics_label="Matriz de confusión del modelo",
            ),
            ft.Text("Importancia de las características", size=20, color=ft.Colors.BLACK),
            ft.Image(
                src=imagen_importancias,
                width=350,
                height=220,
                fit=ft.BoxFit.CONTAIN,
                semantics_label="Importancia de las características del modelo",
            ),
        ],
    )