from typing import Optional
from pydantic import BaseModel

class CustomerData(BaseModel):
    incident_type: Optional[str]=None
    incident_date: Optional[str] = None
    incident_location: Optional[str] = None
    hospitalized: Optional[bool] = None
    hospital_name: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    estimated_amount: Optional[float] = None
    description: Optional[str] = None

    