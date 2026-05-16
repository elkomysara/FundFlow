from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime

# ============================================================================
# COMPANY SCHEMAS - 16 CSV COLUMNS (COMPLETE & FIXED)
# ============================================================================

class CompanyCreate(BaseModel):
    """Complete 16-column company creation schema with all CSV fields"""
    
    # Required fields (5)
    company_name: str = Field(..., min_length=1, max_length=500)
    sector: str = Field(..., min_length=1, max_length=200)
    nationality: str = Field(..., min_length=1, max_length=100)
    business_stage: str = Field(...)
    funding_need_usd: float = Field(..., gt=0)
    
    # Optional demographic fields (4)
    founder_gender: Optional[str] = Field(None, max_length=50)
    business_age_months: Optional[int] = Field(None, ge=0)
    annual_revenue_usd: Optional[float] = Field(None, ge=0)
    employees: Optional[int] = Field(None, ge=0)
    
    # Extended CSV fields (6)
    company_id: Optional[str] = Field(None, max_length=100)
    business_registered_in: Optional[str] = Field(None, max_length=100)
    founder_age: Optional[int] = Field(None, ge=18, le=100)
    innovation_level: Optional[str] = Field(None, max_length=100)
    has_prototype: Optional[bool] = None
    targets_underserved: Optional[bool] = None
    
    # Original CSV timestamp field (1)
    #created_date: Optional[str] = Field(None, max_length=100)
    
    # ✅ Pydantic v2 field validators
    @field_validator("business_stage", mode="before")
    @classmethod
    def validate_business_stage(cls, v: Any) -> Any:
        """Accept any business stage value to prevent crashes on legacy data"""
        if v is None or v == "":
            return "Unknown"
        return str(v)

    @field_validator("innovation_level", mode="before")
    @classmethod
    def validate_innovation_level(cls, v: Any) -> Any:
        """Accept any innovation level value"""
        return str(v) if v is not None else None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "company_id": "COMP052",
                "company_name": "EcoFarm Solutions",
                "sector": "Agriculture", 
                "nationality": "Kenya",
                "business_stage": "Growth",
                "funding_need_usd": 125000,
                "has_prototype": True,
                "innovation_level": "High"
            }
        }
    )


class CompanyResponse(CompanyCreate):
    """Complete 16-column company response schema - inherits all fields"""
    
    # Database-specific fields
    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


# ============================================================================
# GRANT SCHEMAS - ALL 63 CSV COLUMNS (COMPLETE)
# ============================================================================

class GrantCreate(BaseModel):
    """Complete 63-column grant creation schema matching exact CSV analysis"""
    
    # Required field (1)
    program_name: str = Field(..., min_length=1, max_length=500)
    
    # Core matching fields used by algorithm (12)
    institution_name: Optional[str] = Field(None, max_length=500)
    country: Optional[str] = Field(None, max_length=200)
    geographic_scope: Optional[str] = Field(None, max_length=200)
    target_sectors: Optional[str] = None
    estimated_value_amount: Optional[float] = Field(None, ge=0)
    repayment_required: Optional[str] = Field(None, max_length=50)  # String for flexibility
    website_url: Optional[str] = Field(None, max_length=500)
    data_source_url: Optional[str] = Field(None, max_length=500)
    women_focused: Optional[bool] = False
    youth_focused: Optional[bool] = False
    agriculture_focused: Optional[bool] = False
    verified: Optional[bool] = False
    
    # ALL 50 Extended CSV fields (matching your schema analysis exactly)
    program_id: Optional[str] = Field(None, max_length=100)
    region: Optional[str] = Field(None, max_length=200)
    currency_code: Optional[str] = Field(None, max_length=50)
    program_type: Optional[str] = Field(None, max_length=200)
    duration_months: Optional[float] = Field(None, ge=0)
    eligibility_criteria: Optional[str] = None
    application_process: Optional[str] = None
    last_verified_date: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None
    target_beneficiaries: Optional[str] = None
    age_restrictions: Optional[float] = None
    gender_focus: Optional[float] = None
    environmental_focus: Optional[bool] = False
    innovation_focus: Optional[bool] = False
    digital_focus: Optional[bool] = False
    export_focus: Optional[bool] = False
    minimum_employees: Optional[float] = None
    maximum_employees: Optional[float] = None
    minimum_revenue: Optional[float] = None
    maximum_revenue: Optional[float] = None
    collateral_required: Optional[str] = Field(None, max_length=200)
    interest_rate: Optional[str] = Field(None, max_length=100)
    grace_period_months: Optional[float] = None
    success_rate: Optional[float] = None
    total_beneficiaries: Optional[float] = None
    year_established: Optional[float] = None
    funding_source: Optional[str] = None
    application_deadline: Optional[str] = Field(None, max_length=100)
    language_requirements: Optional[str] = None
    technical_assistance: Optional[bool] = False
    mentorship_available: Optional[bool] = False
    networking_opportunities: Optional[bool] = False
    training_provided: Optional[bool] = False
    co_financing_required: Optional[bool] = False
    special_features: Optional[str] = None
    minimum_amount: Optional[float] = Field(None, ge=0)
    maximum_amount: Optional[float] = Field(None, ge=0)
    green_climate_focused: Optional[bool] = False
    export_support: Optional[bool] = False
    technology_innovation: Optional[bool] = False
    co_financing_available: Optional[bool] = False
    last_updated: Optional[float] = None
    program_start_date: Optional[float] = None
    
    # ✅ CRITICAL: Handle NaN values from CSV analysis correctly
    contact_email: Optional[str] = Field(None, max_length=255)  # String despite CSV showing Float (NaN handling)
    contact_phone: Optional[str] = Field(None, max_length=100)
    language_support: Optional[str] = None  # String despite CSV showing Float (NaN handling)
    
    digital_application: Optional[bool] = False
    guarantee_coverage: Optional[str] = None
    verification_date: Optional[float] = None
    target_demographics: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "program_id": "GRANT001",
                "program_name": "African Innovation Fund",
                "institution_name": "African Development Bank",
                "country": "Kenya",
                "region": "East Africa",
                "target_sectors": "Technology, Agriculture",
                "estimated_value_amount": 500000,
                "repayment_required": "No",
                "women_focused": True,
                "youth_focused": True
            }
        }
    )


class GrantResponse(GrantCreate):
    """Complete 63-column grant response schema - inherits all fields"""
    
    # Database-specific fields
    id: int
    created_at: datetime
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


# ============================================================================
# MATCHING SCHEMAS (PRESERVED & ENHANCED)
# ============================================================================

class ScoreBreakdown(BaseModel):
    """Detailed breakdown of matching algorithm scores (40/30/20/10 system)"""
    geographic: float = Field(..., ge=0, le=40, description="Geographic alignment score")
    sector: float = Field(..., ge=0, le=30, description="Sector matching score")
    amount_fit: float = Field(..., ge=0, le=20, description="Funding amount compatibility")
    stage: float = Field(..., ge=0, le=10, description="Business stage alignment")
    
    model_config = ConfigDict(from_attributes=True)


class MatchResult(BaseModel):
    """Individual grant match result with AI advice"""
    grant: GrantResponse
    match_score: float = Field(..., ge=0, le=100, description="Total match score (0-100)")
    match_breakdown: Dict[str, float]  # Flexible dict for backward compatibility
    ai_advice: Optional[str] = Field(None, description="AI-generated application advice")

    model_config = ConfigDict(from_attributes=True)


class MatchResponse(BaseModel):
    """Complete matching response with AI summary"""
    matches: List[MatchResult] = Field(..., description="List of matched grants")
    total_matches_found: int = Field(..., ge=0, description="Total number of matches found")
    company_name: str = Field(..., description="Name of the company being matched")
    ai_summary: Optional[str] = Field(None, description="AI-generated overall recommendation")
    
    model_config = ConfigDict(from_attributes=True)
