from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.employee import Employee as EmployeeModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.employee import EmployeeService
from schemas.employee import Employee

employee_router = APIRouter()

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

#mostrar empleado
@employee_router.get('/employees', tags=['employees'], response_model=List[Employee], status_code=200, dependencies=[Depends(JWTBearer())])
def get_employees() -> List[Employee]:
    db = Session()
    result = EmployeeService(db).get_employees()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#mostrar empleado por ID
@employee_router.get('/employees/{employee_id}', tags=['employees'], response_model=Employee, dependencies=[Depends(JWTBearer())])
def get_employee(employee_id: int = Path(ge=1000)) -> Employee:
    db = Session()
    result = EmployeeService(db).get_employee(employee_id)
    if not result:
        return JSONResponse(status_code=404, content = {"message": "Número de empleado no encontrado."})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#filtrar por departamento
@employee_router.get("/employees/", tags=['employees'], response_model=List[Employee], dependencies=[Depends(JWTBearer())])
def get_employees_by_department(department: str = Query(min_length=5, max_length=25)) -> List[Employee]:
    db = Session()
    result = EmployeeService(db).get_employees_by_department(department)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Departamento no encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result)) 

#Agrega un nuevo empleado
@employee_router.post('/employees', tags=['employees'], response_model=dict, status_code=201, dependencies=[Depends(JWTBearer())])
def create_employee(employee: Employee) -> dict:
    db = Session()
    EmployeeService(db).create_employee(employee)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado correctamente al trabajador."})

#Modificar empleado
@employee_router.put('/employees/{employee_id}', tags=['employees'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def update_employee(employee_id: int, employee: Employee) -> dict:
    db = Session()
    result = EmployeeService(db).get_employee(employee_id)
    if not result:
        return JSONResponse(status_code=404, content = {"message": "Número de empleado no encontrado."})
    EmployeeService(db).update_employee(employee_id, employee)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado correctamente al trabajador."})

#Eliminar empleado
@employee_router.delete('/employees/{employee_id}', tags=['employees'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def delete_employee(employee_id: int) -> dict:
    db = Session()
    result: EmployeeModel = db.query(EmployeeModel).filter(EmployeeModel.employee_id == employee_id).first()
    if not result:
        return JSONResponse(status_code=404, content = {"message": "Número de empleado no encontrado."})
    EmployeeService(db).delete_employee(employee_id)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado correctamente al trabajador."})