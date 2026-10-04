from fastapi import FastAPI

# Instancia principal de la aplicación
app = FastAPI(title="cicd-practica", version="0.1.0")


@app.get("/")
def raiz():
    """Endpoint raíz: devuelve un saludo."""
    return {"mensaje": "¡Hola desde cicd-practica!"}


@app.get("/health")
def health():
    """Comprobación de salud: la usarán el pipeline y los despliegues."""
    return {"status": "ok"}
