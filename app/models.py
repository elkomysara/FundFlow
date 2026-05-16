from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.sql import func
from datetime import datetime
# ✅ CRITICAL FIX: Import Base from database.py so init_db() can find these tables
from app.database import Base

class Grant(Base):
    """Grant model - COMPLETE 63-column CSV schema"""
    __tablename__ = "grants"
    
     # Database fields
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # ALL 63 CSV COLUMNS (matching your schema analysis exactly)
    program_id = Column(String(100), index=True)
    program_name = Column(String(500), nullable=False, index=True)
    institution_name = Column(String(500))
    country = Column(String(200), index=True)
    region = Column(String(200))
    currency_code = Column(String(50))
    estimated_value_amount = Column(Float)
    repayment_required = Column(String(50))  # Flexible string type
    program_type = Column(String(200))
    target_sectors = Column(Text)
    duration_months = Column(Float)
    geographic_scope = Column(String(200))
    eligibility_criteria = Column(Text)
    application_process = Column(Text)
    website_url = Column(String(500))
    last_verified_date = Column(String(100))
    notes = Column(Text)
    target_beneficiaries = Column(Text)
    age_restrictions = Column(Float)
    gender_focus = Column(Float)
    environmental_focus = Column(Boolean, default=False)
    innovation_focus = Column(Boolean, default=False)
    digital_focus = Column(Boolean, default=False)
    export_focus = Column(Boolean, default=False)
    minimum_employees = Column(Float)
    maximum_employees = Column(Float)
    minimum_revenue = Column(Float)
    maximum_revenue = Column(Float)
    collateral_required = Column(String(200))
    interest_rate = Column(String(100))
    grace_period_months = Column(Float)
    success_rate = Column(Float)
    total_beneficiaries = Column(Float)
    year_established = Column(Float)
    funding_source = Column(Text)
    application_deadline = Column(String(100))
    language_requirements = Column(Text)
    technical_assistance = Column(Boolean, default=False)
    mentorship_available = Column(Boolean, default=False)
    networking_opportunities = Column(Boolean, default=False)
    training_provided = Column(Boolean, default=False)
    co_financing_required = Column(Boolean, default=False)
    verified = Column(Boolean, default=False)
    special_features = Column(Text)
    minimum_amount = Column(Float)
    maximum_amount = Column(Float)
    women_focused = Column(Boolean, default=False)
    youth_focused = Column(Boolean, default=False)
    agriculture_focused = Column(Boolean, default=False)
    green_climate_focused = Column(Boolean, default=False)
    export_support = Column(Boolean, default=False)
    technology_innovation = Column(Boolean, default=False)
    co_financing_available = Column(Boolean, default=False)
    last_updated = Column(Float)
    program_start_date = Column(Float)
    contact_email = Column(String(255))  # String despite CSV analysis (NaN handling)
    contact_phone = Column(String(100))
    language_support = Column(Text)
    digital_application = Column(Boolean, default=False)
    guarantee_coverage = Column(Text)
    verification_date = Column(Float)
    target_demographics = Column(Text)
    data_source_url = Column(String(500))

class Company(Base):
    """Company model - COMPLETE 16-column CSV schema"""
    __tablename__ = "companies"
    
     # Database fields
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # ALL 16 CSV COLUMNS (matching your schema analysis exactly)
    company_id = Column(String(100), index=True)
    company_name = Column(String(500), nullable=False, index=True)
    sector = Column(String(200), nullable=False, index=True)
    nationality = Column(String(100), nullable=False, index=True)
    business_registered_in = Column(String(100))
    founder_age = Column(Integer)
    founder_gender = Column(String(50))
    business_age_months = Column(Integer)
    annual_revenue_usd = Column(Float)
    employees = Column(Integer)
    business_stage = Column(String(100), nullable=False)
    funding_need_usd = Column(Float, nullable=False)
    has_prototype = Column(Boolean, default=False, index=True)
    innovation_level = Column(String(100), index=True)
    targets_underserved = Column(Boolean, default=False, index=True)
    #created_date = Column(String(100))  # Original CSV field