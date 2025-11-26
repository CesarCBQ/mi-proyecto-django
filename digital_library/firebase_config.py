# digital_library/firebase_config.py

import firebase_admin
from firebase_admin import credentials, firestore
from digital_library.settings import FIREBASE_KEY_PATH 
import os # <-- Importamos os

# Inicializa las credenciales
# 💥 VERIFICACIÓN DE EXISTENCIA ANTES DE INTENTAR CARGAR 💥
if os.path.exists(FIREBASE_KEY_PATH):
    cred = credentials.Certificate(FIREBASE_KEY_PATH)

    # Inicializa la aplicación de Firebase
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        
    def get_firebase_db():
        """Retorna la instancia del cliente de Firestore."""
        return db
else:
    # Definir una función de fallback si el archivo no se encuentra
    print("ADVERTENCIA: Archivo firebase_key.json no encontrado. Las vistas de Firebase no funcionarán.")
    def get_firebase_db():
        raise FileNotFoundError("firebase_key.json no encontrado. Verifique la ruta en settings.py.")