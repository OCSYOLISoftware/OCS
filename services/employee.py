from models.employee import Employee as EmployeeModel
from schemas.employee import Employee

class EmployeeService():

    def __init__(self, db) -> None:
        self.db = db
    #Consulta de registros
    def get_employees(self):
        result = self.db.query(EmployeeModel).all()
        return result

    #Filtrar por ID
    def get_employee(self, employee_id):
        result = self.db.query(EmployeeModel).filter(EmployeeModel.employee_id == employee_id).first()
        return result

    #Filtrar por Departamento
    def get_employees_by_department(self, department):
        result = self.db.query(EmployeeModel).filter(EmployeeModel.department == department).all()
        return result

    #Filtrar por Departamento
    def get_employees_by_department(self, department):
        result = self.db.query(EmployeeModel).filter(EmployeeModel.department == department).all()
        return result

    #Crear un empleado nuevo
    def create_employee(self, employee: Employee):
        new_employee = EmployeeModel(**employee.dict())
        self.db.add(new_employee)
        self.db.commit()
        return 

    #Actualizar empleado
    def update_employee(self, employee_id: int, data: Employee):
        employee = self.db.query(EmployeeModel).filter(EmployeeModel.employee_id == employee_id).first()
        employee.name = data.name
        employee.dob = data.dob
        employee.date_of_admission = data.date_of_admission
        employee.department = data.department
        employee.campaign = data.campaign
        employee.position = data.position
        employee.supervisor = data.supervisor
        employee.salary = data.salary
        self.db.commit()
        return

    def delete_employee(self, employee_id):
        self.db.query(EmployeeModel).filter(EmployeeModel.employee_id == employee_id).delete()
        self.db.commit()
        return