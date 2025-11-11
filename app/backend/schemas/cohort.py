"""Cohort schemas"""
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List, Union
from datetime import date, datetime
from app.backend.models.cohort import CohortRole


class CohortCreate(BaseModel):
    """Schema for creating a cohort"""
    name: str = Field(..., max_length=100, description="Cohort name")
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: bool = True
    
    @field_validator('start_date', 'end_date', mode='before')
    @classmethod
    def empty_string_to_none(cls, v: Union[str, date, None]) -> Optional[date]:
        """Convert empty strings to None for date fields"""
        if v == '' or v is None:
            return None
        if isinstance(v, str):
            # Let Pydantic handle the date parsing
            return v
        return v
    
    @field_validator('start_date')
    @classmethod
    def validate_start_date(cls, v: Optional[date]) -> Optional[date]:
        """Validate start date is not in the past"""
        if v is not None:
            today = date.today()
            if v < today:
                raise ValueError(f"Start date cannot be before today ({today})")
        return v
    
    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v: Optional[date]) -> Optional[date]:
        """Validate end date is not before today"""
        if v is not None:
            today = date.today()
            if v < today:
                raise ValueError(f"End date cannot be before today ({today})")
        return v
    
    @model_validator(mode='after')
    def validate_dates(self):
        """Validate date relationships"""
        today = date.today()
        
        # Validate start_date is not in the past
        if self.start_date is not None and self.start_date < today:
            raise ValueError(f"Start date cannot be before today ({today})")
        
        # Validate end_date is not before today
        if self.end_date is not None and self.end_date < today:
            raise ValueError(f"End date cannot be before today ({today})")
        
        # Validate end_date is not before start_date
        if self.start_date is not None and self.end_date is not None:
            if self.end_date < self.start_date:
                raise ValueError("End date cannot be before start date")
        
        return self


class CohortUpdate(BaseModel):
    """Schema for updating a cohort"""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: Optional[bool] = None
    
    @field_validator('start_date', 'end_date', mode='before')
    @classmethod
    def empty_string_to_none(cls, v: Union[str, date, None]) -> Optional[date]:
        """Convert empty strings to None for date fields"""
        if v == '' or v is None:
            return None
        if isinstance(v, str):
            # Let Pydantic handle the date parsing
            return v
        return v
    
    @field_validator('start_date')
    @classmethod
    def validate_start_date(cls, v: Optional[date]) -> Optional[date]:
        """Validate start date is not in the past"""
        if v is not None:
            today = date.today()
            if v < today:
                raise ValueError(f"Start date cannot be before today ({today})")
        return v
    
    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v: Optional[date]) -> Optional[date]:
        """Validate end date is not before today"""
        if v is not None:
            today = date.today()
            if v < today:
                raise ValueError(f"End date cannot be before today ({today})")
        return v
    
    @model_validator(mode='after')
    def validate_dates(self):
        """Validate date relationships"""
        today = date.today()
        
        # Validate start_date is not in the past
        if self.start_date is not None and self.start_date < today:
            raise ValueError(f"Start date cannot be before today ({today})")
        
        # Validate end_date is not before today
        if self.end_date is not None and self.end_date < today:
            raise ValueError(f"End date cannot be before today ({today})")
        
        # Validate end_date is not before start_date
        if self.start_date is not None and self.end_date is not None:
            if self.end_date < self.start_date:
                raise ValueError("End date cannot be before start date")
        
        return self


class CohortMemberCreate(BaseModel):
    """Schema for adding a member to a cohort"""
    user_id: int
    role: CohortRole = CohortRole.STUDENT


class CohortMemberResponse(BaseModel):
    """Schema for cohort member response"""
    id: int
    cohort_id: int
    user_id: int
    role: str
    joined_at: datetime
    user: Optional[dict] = None  # Will include user details
    
    class Config:
        from_attributes = True


class CohortResponse(BaseModel):
    """Schema for cohort response"""
    id: int
    name: str
    description: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    is_active: bool
    cancelled_at: Optional[datetime] = None
    created_by: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
    members: List[CohortMemberResponse] = []
    member_count: int = 0
    student_count: int = 0
    instructor_count: int = 0
    
    class Config:
        from_attributes = True


class CohortListResponse(BaseModel):
    """Schema for list of cohorts"""
    cohorts: List[CohortResponse]
    total: int

