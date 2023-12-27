from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()
app.title = "Base de Datos Trabajadores"
app.version = "0.0.3"

@app.get('/')

class Employee(BaseModel):
    id: int
    employee_id: int = Field(ge=1000)
    name: str = Field(min_length=3, max_length= 25)
    dob: str  = Field(min_length=3, max_length= 25)
    date_of_admission: str  = Field(min_length=3, max_length= 25) 
    department: str  = Field(min_length=3, max_length= 25)
    campaign: Optional [str] = Field(min_length=3, max_length= 25)
    position: str  = Field(min_length=3, max_length= 25)
    supervisor:str  = Field(min_length=3, max_length= 25)
    salary: float = Field(ge=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "Número de Empleado",
                "employee_id": "Número de Empleado",
                "name": "Nombre",
                "dob": "Fecha de Nacimiento",
                "date_of_admission": "Fecha de Ingreso",
                "department": "Departamento",
                "campaign": "Campaña",
                "position": "Puesto",
                "supervisor": "Supervisor",
                "salary": "Sueldo Diario"

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
        "position": "Rios Asistant",
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
#mostrar productos
@app.get('/employees', tags=['employees'])
def get_employee():
    return employees

#mostrar producto por ID
@app.get('/employees/{employee_id}', tags=['employees'])
def get_employee(employee_id: int):
    for employee in employees:
        if employee ["employee_id"] == employee_id:
            return employee
    return []

#filtrar por departamento y campaña
@app.get("/employees/", tags=['employees'])
def get_employess_by_department(department: str):
    return [employee for employee in employees if employee['department'] == department]

#Agrega una nueva lista
@app.post('/employees', tags=['employees'])
def create_employee(employee: Employee):
    employees.append(employee)
    return employees

#Modificar empleado
@app.put('/employees/{employee_id}', tags=['employees'])
def update_employee(employee_id: int, employee: Employee):
    for employee in employees:
        if employee['employee_id'] == Employee.employee_id:
            employee['employee_id'] = Employee.employee_id
            employee['dob'] = Employee.dob
            employee['date_of_admission'] = Employee.date_of_admission
            employee['department'] = Employee.department
            employee['campaign'] = Employee.campaign
            employee['position'] = Employee.position
            employee['supervisor'] = Employee.supervisor
            employee['salary'] = Employee.salary
            return employees

#Eliminar empleado
@app.delete('/employees/{employee_id}', tags=['employees'])
def delete_movie(employee_id: int):
    for employee in employees:
        if employee['employee_id'] == employee_id:
            employees.remove(employee)
            return employees