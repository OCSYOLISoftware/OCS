from pydantic import BaseModel, Field
from typing import Optional, List

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
