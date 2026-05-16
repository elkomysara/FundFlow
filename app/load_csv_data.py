#!/usr/bin/env python
"""
ImaraFund Complete CSV Data Loader
Loads ALL 63 grant fields + 16 company fields with intelligent error handling
"""

import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Cross-platform path resolution
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def clean_value(value, target_type='string'):
    """Universal value cleaner with intelligent type conversion"""
    if pd.isna(value) or value == "" or value is None:
        return None
    
    try:
        if target_type == 'float':
            if isinstance(value, (int, float)):
                return float(value) if not pd.isna(value) else None
            cleaned = str(value).replace("$", "").replace(",", "").strip()
            return float(cleaned) if cleaned else None
        elif target_type == 'integer':
            return int(float(value)) if not pd.isna(value) else None
        elif target_type == 'boolean':
            if isinstance(value, bool):
                return value
            str_val = str(value).lower().strip()
            return str_val in ["true", "yes", "1", "y", "on", "t"]
        else:  # string
            return str(value).strip() if str(value).strip() else None
    except (ValueError, TypeError):
        return None

def load_csv_data():
    """Load both CSV files into database with complete field support"""
    
    # Get database connection
    db_url = os.getenv('DATABASE_URL', 'sqlite:///./imarafund.db')
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    print("🔄 Loading CSV data into database...")
    print(f"📁 Data directory: {DATA_DIR}")
    
    try:
        # ============================================================================
        # COMPANIES - ALL 16 FIELDS
        # ============================================================================
        company_csv = os.path.join(DATA_DIR, "synthetic_companies.csv")
        
        if os.path.exists(company_csv):
            print(f"\n📂 Loading companies from: {company_csv}")
            df = pd.read_csv(company_csv)
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
            print(f"   📊 Found {len(df)} companies in CSV")
            
            # Clear existing companies
            session.execute(text("DELETE FROM companies"))
            
            loaded = 0
            for _, row in df.iterrows():
                try:
                    insert_sql = """
                        INSERT INTO companies (
                            company_id, company_name, sector, nationality,
                            business_registered_in, founder_age, founder_gender,
                            business_age_months, annual_revenue_usd, employees,
                            business_stage, funding_need_usd, has_prototype,
                            innovation_level, targets_underserved
                        ) VALUES (
                            :company_id, :company_name, :sector, :nationality,
                            :business_registered_in, :founder_age, :founder_gender,
                            :business_age_months, :annual_revenue_usd, :employees,
                            :business_stage, :funding_need_usd, :has_prototype,
                            :innovation_level, :targets_underserved
                        )
                    """
                    
                    session.execute(text(insert_sql), {
                        'company_id': clean_value(row.get('company_id')),
                        'company_name': clean_value(row.get('company_name')) or f'Company {loaded}',
                        'sector': clean_value(row.get('sector')) or 'General',
                        'nationality': clean_value(row.get('nationality')) or 'Unknown',
                        'business_registered_in': clean_value(row.get('business_registered_in')),
                        'founder_age': clean_value(row.get('founder_age'), 'integer'),
                        'founder_gender': clean_value(row.get('founder_gender')),
                        'business_age_months': clean_value(row.get('business_age_months'), 'integer'),
                        'annual_revenue_usd': clean_value(row.get('annual_revenue_usd'), 'float'),
                        'employees': clean_value(row.get('employees'), 'integer'),
                        'business_stage': clean_value(row.get('business_stage')) or 'Unknown',
                        'funding_need_usd': clean_value(row.get('funding_need_usd'), 'float') or 0.0,
                        'has_prototype': clean_value(row.get('has_prototype'), 'boolean'),
                        'innovation_level': clean_value(row.get('innovation_level')),
                        'targets_underserved': clean_value(row.get('targets_underserved'), 'boolean')
                    })
                    loaded += 1
                except Exception as e:
                    print(f"    ⚠️  Skipped company row {loaded}: {str(e)[:80]}")
            
            session.commit()
            print(f"    ✅ Successfully loaded {loaded} companies")
        else:
            print(f"    ❌ Company CSV not found at: {company_csv}")
        
        # ============================================================================
        # GRANTS - ALL 63 FIELDS (COMPLETE MAPPING)
        # ============================================================================
        grant_csv = os.path.join(DATA_DIR, "grants_cleaned_latest.csv")
        
        if os.path.exists(grant_csv):
            print(f"\n📂 Loading grants from: {grant_csv}")
            df = pd.read_csv(grant_csv)
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
            print(f"   📊 Found {len(df)} grants in CSV")
            
            # Clear existing grants
            session.execute(text("DELETE FROM grants"))
            
            loaded = 0
            for _, row in df.iterrows():
                try:
                    # ✅ COMPLETE 63-FIELD MAPPING (organized by category)
                    grant_data = {
                        # Core Identity & Program Info (12 fields)
                        'program_id': clean_value(row.get('program_id')),
                        'program_name': clean_value(row.get('program_name')) or f'Grant {loaded}',
                        'institution_name': clean_value(row.get('institution_name')),
                        'country': clean_value(row.get('country')),
                        'region': clean_value(row.get('region')),
                        'currency_code': clean_value(row.get('currency_code')),
                        'program_type': clean_value(row.get('program_type')),
                        'target_sectors': clean_value(row.get('target_sectors')),
                        'geographic_scope': clean_value(row.get('geographic_scope')),
                        'funding_source': clean_value(row.get('funding_source')),
                        'year_established': clean_value(row.get('year_established'), 'float'),
                        'verified': clean_value(row.get('verified'), 'boolean'),
                        
                        # Financial Information (8 fields)
                        'estimated_value_amount': clean_value(row.get('estimated_value_amount'), 'float'),
                        'minimum_amount': clean_value(row.get('minimum_amount'), 'float'),
                        'maximum_amount': clean_value(row.get('maximum_amount'), 'float'),
                        'repayment_required': clean_value(row.get('repayment_required')),
                        'interest_rate': clean_value(row.get('interest_rate')),
                        'collateral_required': clean_value(row.get('collateral_required')),
                        'grace_period_months': clean_value(row.get('grace_period_months'), 'float'),
                        'guarantee_coverage': clean_value(row.get('guarantee_coverage')),
                        
                        # Program Timeline & Deadlines (4 fields)
                        'duration_months': clean_value(row.get('duration_months'), 'float'),
                        'program_start_date': clean_value(row.get('program_start_date'), 'float'),
                        'application_deadline': clean_value(row.get('application_deadline')),
                        'last_updated': clean_value(row.get('last_updated'), 'float'),
                        
                        # Eligibility & Requirements (9 fields)
                        'eligibility_criteria': clean_value(row.get('eligibility_criteria')),
                        'target_beneficiaries': clean_value(row.get('target_beneficiaries')),
                        'target_demographics': clean_value(row.get('target_demographics')),
                        'age_restrictions': clean_value(row.get('age_restrictions'), 'float'),
                        'gender_focus': clean_value(row.get('gender_focus'), 'float'),
                        'minimum_employees': clean_value(row.get('minimum_employees'), 'float'),
                        'maximum_employees': clean_value(row.get('maximum_employees'), 'float'),
                        'minimum_revenue': clean_value(row.get('minimum_revenue'), 'float'),
                        'maximum_revenue': clean_value(row.get('maximum_revenue'), 'float'),
                        
                        # Focus Areas (10 boolean fields)
                        'women_focused': clean_value(row.get('women_focused'), 'boolean'),
                        'youth_focused': clean_value(row.get('youth_focused'), 'boolean'),
                        'agriculture_focused': clean_value(row.get('agriculture_focused'), 'boolean'),
                        'environmental_focus': clean_value(row.get('environmental_focus'), 'boolean'),
                        'green_climate_focused': clean_value(row.get('green_climate_focused'), 'boolean'),
                        'innovation_focus': clean_value(row.get('innovation_focus'), 'boolean'),
                        'technology_innovation': clean_value(row.get('technology_innovation'), 'boolean'),
                        'digital_focus': clean_value(row.get('digital_focus'), 'boolean'),
                        'export_focus': clean_value(row.get('export_focus'), 'boolean'),
                        'export_support': clean_value(row.get('export_support'), 'boolean'),
                        
                        # Support Services (6 boolean fields)
                        'technical_assistance': clean_value(row.get('technical_assistance'), 'boolean'),
                        'mentorship_available': clean_value(row.get('mentorship_available'), 'boolean'),
                        'networking_opportunities': clean_value(row.get('networking_opportunities'), 'boolean'),
                        'training_provided': clean_value(row.get('training_provided'), 'boolean'),
                        'co_financing_required': clean_value(row.get('co_financing_required'), 'boolean'),
                        'co_financing_available': clean_value(row.get('co_financing_available'), 'boolean'),
                        
                        # Application & Contact Info (8 fields)
                        'application_process': clean_value(row.get('application_process')),
                        'website_url': clean_value(row.get('website_url')),
                        'data_source_url': clean_value(row.get('data_source_url')),
                        'contact_email': clean_value(row.get('contact_email')),
                        'contact_phone': clean_value(row.get('contact_phone')),
                        'language_requirements': clean_value(row.get('language_requirements')),
                        'language_support': clean_value(row.get('language_support')),
                        'digital_application': clean_value(row.get('digital_application'), 'boolean'),
                        
                        # Tracking & Verification (6 fields)
                        'last_verified_date': clean_value(row.get('last_verified_date')),
                        'verification_date': clean_value(row.get('verification_date'), 'float'),
                        'success_rate': clean_value(row.get('success_rate'), 'float'),
                        'total_beneficiaries': clean_value(row.get('total_beneficiaries'), 'float'),
                        'notes': clean_value(row.get('notes')),
                        'special_features': clean_value(row.get('special_features'))
                    }
                    
                    # Build dynamic INSERT statement
                    columns = ', '.join(grant_data.keys())
                    placeholders = ', '.join([f':{k}' for k in grant_data.keys()])
                    insert_sql = f"INSERT INTO grants ({columns}) VALUES ({placeholders})"
                    
                    session.execute(text(insert_sql), grant_data)
                    loaded += 1
                    
                    # Progress indicator for large datasets
                    if loaded % 100 == 0:
                        print(f"    📈 Processed {loaded} grants...")
                    
                except Exception as e:
                    print(f"    ⚠️  Skipped grant row {loaded}: {str(e)[:100]}")
            
            session.commit()
            print(f"    ✅ Successfully loaded {loaded} grants")
        else:
            print(f"    ❌ Grant CSV not found at: {grant_csv}")
        
        session.close()
        print(f"\n🎉 CSV data loading complete!")
        print(f"📊 Database is now populated and ready for matching algorithm")
        return True
        
    except Exception as e:
        session.rollback()
        session.close()
        print(f"\n❌ CSV loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 80)
    print("🚀 ImaraFund Data Loader - Complete 63+16 Field Support")
    print("=" * 80)
    load_csv_data()
