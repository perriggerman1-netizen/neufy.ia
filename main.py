from fastapi import FastAPI

app = FastAPI()

@app.get("/hola")
def hola():
    return {"mensaje": "Hola, soy el backend de Neufy"}