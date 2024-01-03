from fastapi import Depends,FastAPI, Body, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.employee import Employee as EmployeeModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()
app.title = "Base de Datos Trabajadores"
app.version = "0.0.3"

Base.metadata.create_all(bind=engine)

@app.get('/')

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth =  await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'admin@admin':
            raise HTTPException(status_code=403, details="Credenciales son invalidas")

class User(BaseModel):
    email: str
    password: str

class Employee(BaseModel):
    id: Optional [int] = None
    employee_id: int = Field(ge=1000)
    name: str = Field(min_length=3, max_length= 50)
    dob: str  = Field(min_length=3, max_length= 25)
    date_of_admission: str  = Field(min_length=3, max_length= 25) 
    department: str  = Field(min_length=3, max_length= 25)
    campaign: Optional [str] = None
    position: str  = Field(min_length=3, max_length= 30)
    supervisor:str  = Field(min_length=3, max_length= 25)
    salary: float = Field(ge=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "employee_id":1000 ,
                "name": "Nombre",
                "dob": "Fecha de Nacimiento",
                "date_of_admission": "Fecha de Ingreso",
                "department": "Departamento",
                "campaign": "Campaña",
                "position": "Puesto",
                "supervisor": "Supervisor",
                "salary": 100

            }
        }

#lista de productos
employees = [
    {
        "id": 1,
        "employee_id": 1935,
        "name": "Andrea Diaz Covarrubias Lopez",
        "dob": "7/10/1996",
        "date_of_admission": "28/03/2022",
        "department": "Administration",
        "campaign": "",
        "position": "Rios Assistant",
        "supervisor": "Christian Peña",
        "salary": 800.00
    },
    {
        "id": 2,
        "employee_id": 1900,
        "name": "Joel de Jesus Hernandez Izquierdo",
        "dob": "10/12/1988",
        "date_of_admission": "28/02/2022",
        "department": "Billing",
        "campaign": "Aging",
        "position": "Biller",
        "supervisor": "Dorian Gallardo",
        "salary": 500.00
    },
    {
        "id": 3,
        "employee_id": 1883,
        "name": "Sofia Labrada Sanchez ",
        "dob": "7/10/1996",
        "date_of_admission": "14/02/2022",
        "department": "MSO",
        "campaign": "Credentialing",
        "position": "Agent",
        "supervisor": "Christian Peña",
        "salary": 1500.00
    },
    {
        "id": 4,
        "employee_id": 1209,
        "name": "Eleazar Eduardo Leal Gómez",
        "dob": "15/09/1987",
        "date_of_admission": "30/04/2018",
        "department": "IT",
        "campaign": "",
        "position": "Supervisor",
        "supervisor": "Christian Peña",
        "salary": 1200.00
    },
    {
        "id": 5,
        "employee_id": 1793,
        "name": "Efrain Rabago Pérez",
        "dob": "18/05/1995",
        "date_of_admission": "01/11/2021",
        "department": "Clients",
        "campaign": "Stockton",
        "position": "Agent",
        "supervisor": "Omar Acosta",
        "salary": 500.00
    },
]

#Rutas
@app.get('/', tags=['home'])

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == 'admin@admin' and user.password == 'admin':
        token: str = create_token(user.dict())
    return JSONResponse(status_code=200, content=token)

#mostrar empleado
@app.get('/employees', tags=['employees'], response_model=List[Employee], status_code=200, dependencies=[Depends(JWTBearer())])
def get_employee() -> List[Employee]:
    db = Session()
    result = db.query(EmployeeModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#mostrar empleado por ID
@app.get('/employees/{employee_id}', tags=['employees'], response_model=Employee, dependencies=[Depends(JWTBearer())])
def get_employee(employee_id: int = Path(ge=1000)) -> Employee:
    db = Session()
    result = db.query(EmployeeModel).filter(EmployeeModel.employee_id == employee_id).first()
    if not result:
        return JSONResponse(status_code=404, content = {"message": "Número de empleado no encontrado."})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#filtrar por departamento
@app.get("/employees/", tags=['employees'], response_model=List[Employee], dependencies=[Depends(JWTBearer())])
def get_employess_by_department(department: str = Query(min_length=5, max_length=25)) -> List[Employee]:
    db = Session()
    result = db.query(EmployeeModel).filter(EmployeeModel.department == department).all()
    if not result:
        return JSONResponse(status_code=404, content={"message": "Departamento no encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result)) 

#Agrega un nuevo empleado
@app.post('/employees', tags=['employees'], response_model=dict, status_code=201, dependencies=[Depends(JWTBearer())])
def create_employee(employee: Employee) -> dict:
    db = Session()
    new_employee = EmployeeModel(**employee.dict())
    db.add(new_employee)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha registrado correctamente al trabajador."})

#Modificar empleado
@app.put('/employees/{employee_id}', tags=['employees'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def update_employee(employee_id: int, employee: Employee) -> dict:
    db = Session()
    result = db.query(EmployeeModel).filter(EmployeeModel.employee_id == employee_id).first()
    if not result:
        return JSONResponse(status_code=404, content = {"message": "Número de empleado no encontrado."})
    result.name = employee.name
    result.dob = employee.dob
    result.date_of_admission = employee.date_of_admission
    result.department = employee.department
    result.campaign = employee.campaign
    result.position = employee.position
    result.supervisor = employee.supervisor
    result.salary = employee.salary
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha modificado correctamente al trabajador."})

#Eliminar empleado
@app.delete('/employees/{employee_id}', tags=['employees'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def delete_movie(employee_id: int) -> dict:
    db = Session()
    result = db.query(EmployeeModel).filter(EmployeeModel.employee_id == employee_id).first()
    if not result:
        return JSONResponse(status_code=404, content = {"message": "Número de empleado no encontrado."})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado correctamente al trabajador."})