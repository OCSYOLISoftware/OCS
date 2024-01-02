from config.database import Base
from sqlalchemy import Column, Integer, String, Float

class Employee(Base):

    __tablename__ = 'employees'

    id = Column(Integer, primary_key = True)
    employee_id = Column(Integer)
    name = Column(String)
    dob = Column(String)
    date_of_admission = Column(String)
    department = Column(String)
    campaign = Column(String)
    position = Column(String)
    supervisor = Column(String)
    salary = Column(Float)


