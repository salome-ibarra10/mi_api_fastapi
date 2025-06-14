from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# Crea la aplicación FastAPI
app = FastAPI()

# Modelo de datos para usuarios (usando Pydantic)
class Usuario(BaseModel):
    nombre: str
    edad: int
    email: str
    activo: Optional[bool] = True

class UsuarioActualizar(BaseModel):
    nombre: Optional[str] = None
    edad: Optional[int] = None
    email: Optional[str] = None
    activo: Optional[bool] = None

# Base de datos simulada en memoria
usuarios_db = []
contador_id = 1

# ========== ENDPOINTS EXISTENTES ==========
# Ruta GET en la raíz: http://localhost:8000/
@app.get("/")
def hola_mundo():
    return {"mensaje": "¡Hola jóvenes! Bienvenidos a FastAPI"}

# Ruta GET personalizada: http://localhost:8000/saludo/{nombre}
@app.get("/saludo/{nombre}")
def saludar(nombre: str):
    return {"saludo": f"¡Hola {nombre}! ¿Cómo estás?"}

# ========== NUEVOS ENDPOINTS CRUD ==========

# 📖 GET - Obtener todos los usuarios
@app.get("/usuarios")
def obtener_usuarios():
    """Obtiene la lista de todos los usuarios"""
    return {
        "total": len(usuarios_db),
        "usuarios": usuarios_db
    }

# 📖 GET - Obtener un usuario específico por ID
@app.get("/usuarios/{usuario_id}")
def obtener_usuario(usuario_id: int):
    """Obtiene un usuario específico por su ID"""
    for usuario in usuarios_db:
        if usuario["id"] == usuario_id:
            return usuario
    return {"error": f"Usuario con ID {usuario_id} no encontrado"}

# ➕ POST - Crear un nuevo usuario
@app.post("/usuarios")
def crear_usuario(usuario: Usuario):
    """Crea un nuevo usuario"""
    global contador_id
    
    nuevo_usuario = {
        "id": contador_id,
        "nombre": usuario.nombre,
        "edad": usuario.edad,
        "email": usuario.email,
        "activo": usuario.activo
    }
    
    usuarios_db.append(nuevo_usuario)
    contador_id += 1
    
    return {
        "mensaje": "Usuario creado exitosamente",
        "usuario": nuevo_usuario
    }

# ✏️ PUT - Actualizar un usuario completo
@app.put("/usuarios/{usuario_id}")
def actualizar_usuario_completo(usuario_id: int, usuario: Usuario):
    """Actualiza completamente un usuario existente"""
    for i, user in enumerate(usuarios_db):
        if user["id"] == usuario_id:
            usuarios_db[i] = {
                "id": usuario_id,
                "nombre": usuario.nombre,
                "edad": usuario.edad,
                "email": usuario.email,
                "activo": usuario.activo
            }
            return {
                "mensaje": "Usuario actualizado completamente",
                "usuario": usuarios_db[i]
            }
    
    return {"error": f"Usuario con ID {usuario_id} no encontrado"}

# ✏️ PATCH - Actualizar parcialmente un usuario
@app.patch("/usuarios/{usuario_id}")
def actualizar_usuario_parcial(usuario_id: int, usuario: UsuarioActualizar):
    """Actualiza parcialmente un usuario existente"""
    for i, user in enumerate(usuarios_db):
        if user["id"] == usuario_id:
            # Solo actualiza los campos que no son None
            if usuario.nombre is not None:
                usuarios_db[i]["nombre"] = usuario.nombre
            if usuario.edad is not None:
                usuarios_db[i]["edad"] = usuario.edad
            if usuario.email is not None:
                usuarios_db[i]["email"] = usuario.email
            if usuario.activo is not None:
                usuarios_db[i]["activo"] = usuario.activo
            
            return {
                "mensaje": "Usuario actualizado parcialmente",
                "usuario": usuarios_db[i]
            }
    
    return {"error": f"Usuario con ID {usuario_id} no encontrado"}

# 🗑️ DELETE - Eliminar un usuario
@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    """Elimina un usuario por su ID"""
    for i, user in enumerate(usuarios_db):
        if user["id"] == usuario_id:
            usuario_eliminado = usuarios_db.pop(i)
            return {
                "mensaje": "Usuario eliminado exitosamente",
                "usuario_eliminado": usuario_eliminado
            }
    
    return {"error": f"Usuario con ID {usuario_id} no encontrado"}

# 🗑️ DELETE - Eliminar todos los usuarios
@app.delete("/usuarios")
def eliminar_todos_usuarios():
    """Elimina todos los usuarios (¡Cuidado!)"""
    global contador_id
    total_eliminados = len(usuarios_db)
    usuarios_db.clear()
    contador_id = 1
    
    return {
        "mensaje": f"Se eliminaron {total_eliminados} usuarios",
        "usuarios_restantes": len(usuarios_db)
    }

