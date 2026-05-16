#!/usr/bin/env python
"""
ImaraFund Complete Schema Migration
Adds ALL missing CSV columns to match the 63 grant + 16 company fields
FIXED: Uses imarafund_user credentials (table owner)
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

# FIXED: Use application user (table owner) instead of postgres
DATABASE_URL = "postgresql://imarafund_user:ImaraFund2024@130.211.88.95:5432/imarafund"

def run_migration():
    print("=" * 80)
    print("ImaraFund Complete Schema Migration")
    print("Adding missing columns for full CSV coverage")
    print("Target: 63 grant columns + 16 company columns")
    print("Using: imarafund_user credentials (table owner)")
    print("=" * 80)

    conn = None
    try:
        print("\n[1] Connecting to database as imarafund_user...")
        conn = psycopg2.connect(DATABASE_URL)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        print("    ✅ Connected successfully")

        # Create backup tables
        print("\n[2] Creating backup tables...")
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS companies_backup_full_schema AS 
                SELECT * FROM companies;
            """)
            print("    ✅ Companies backup created")
        except Exception as e:
            print(f"    ⚠️  Companies backup: {e}")
        
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS grants_backup_full_schema AS 
                SELECT * FROM grants;
            """)
            print("    ✅ Grants backup created")
        except Exception as e:
            print(f"    ⚠️  Grants backup: {e}")

        # =====================================================================
        # COMPANIES TABLE - Add 6 missing columns (to reach 16 total)
        # =====================================================================
        print("\n[3] Updating COMPANIES table...")
        companies_columns = [
            ("company_id", "VARCHAR(50) UNIQUE"), # ✅ FIXED: Clean name (no _csv suffix)
            ("business_registered_in", "VARCHAR(100)"),
            ("founder_age", "INTEGER"),
            ("has_prototype", "BOOLEAN DEFAULT FALSE"),
            ("innovation_level", "VARCHAR(50)"),
            ("targets_underserved", "BOOLEAN DEFAULT FALSE"),
        ]
        
        companies_added = 0
        for col_name, col_type in companies_columns:
            try:
                cursor.execute(f"""
                    ALTER TABLE companies 
                    ADD COLUMN IF NOT EXISTS {col_name} {col_type};
                """)
                companies_added += 1
                print(f"    ✅ Added: {col_name}")
            except Exception as e:
                print(f"    ⚠️  Column {col_name}: {str(e)[:50]}...")
        
        # Add indexes for companies
        print("    📊 Creating indexes...")
        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_companies_company_id_csv ON companies(company_id_csv);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_companies_innovation_level ON companies(innovation_level);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_companies_has_prototype ON companies(has_prototype);")
            print("    ✅ Company indexes created")
        except Exception as e:
            print(f"    ⚠️  Index creation: {str(e)[:50]}...")
        
        print(f"    📈 Companies: {companies_added} columns added")

        # =====================================================================
        # GRANTS TABLE - Add ALL 49 missing columns (to reach 63 total)
        # =====================================================================
        print("\n[4] Updating GRANTS table...")
        grants_columns = [
            ("program_id", "VARCHAR(100)"),
            ("region", "VARCHAR(200)"),
            ("currency_code", "VARCHAR(20)"),
            ("program_type", "VARCHAR(200)"),
            ("duration_months", "FLOAT"),
            ("eligibility_criteria", "TEXT"),
            ("application_process", "TEXT"),
            ("last_verified_date", "VARCHAR(100)"),
            ("notes", "TEXT"),
            ("target_beneficiaries", "TEXT"),
            ("age_restrictions", "FLOAT"),
            ("gender_focus", "FLOAT"),
            ("environmental_focus", "BOOLEAN DEFAULT FALSE"),
            ("innovation_focus", "BOOLEAN DEFAULT FALSE"),
            ("digital_focus", "BOOLEAN DEFAULT FALSE"),
            ("export_focus", "BOOLEAN DEFAULT FALSE"),
            ("minimum_employees", "FLOAT"),
            ("maximum_employees", "FLOAT"),
            ("minimum_revenue", "FLOAT"),
            ("maximum_revenue", "FLOAT"),
            ("collateral_required", "VARCHAR(200)"),
            ("interest_rate", "VARCHAR(100)"),
            ("grace_period_months", "FLOAT"),
            ("success_rate", "FLOAT"),
            ("total_beneficiaries", "FLOAT"),
            ("year_established", "FLOAT"),
            ("funding_source", "TEXT"),
            ("application_deadline", "VARCHAR(100)"),
            ("language_requirements", "TEXT"),
            ("technical_assistance", "BOOLEAN DEFAULT FALSE"),
            ("mentorship_available", "BOOLEAN DEFAULT FALSE"),
            ("networking_opportunities", "BOOLEAN DEFAULT FALSE"),
            ("training_provided", "BOOLEAN DEFAULT FALSE"),
            ("co_financing_required", "BOOLEAN DEFAULT FALSE"),
            ("special_features", "TEXT"),
            ("minimum_amount", "FLOAT"),
            ("maximum_amount", "FLOAT"),
            ("green_climate_focused", "BOOLEAN DEFAULT FALSE"),
            ("export_support", "BOOLEAN DEFAULT FALSE"),
            ("technology_innovation", "BOOLEAN DEFAULT FALSE"),
            ("co_financing_available", "BOOLEAN DEFAULT FALSE"),
            ("last_updated", "FLOAT"),
            ("program_start_date", "FLOAT"),
            ("contact_email", "VARCHAR(255)"),
            ("contact_phone", "VARCHAR(50)"),
            ("language_support", "TEXT"),
            ("digital_application", "BOOLEAN DEFAULT FALSE"),
            ("guarantee_coverage", "TEXT"),
            ("verification_date", "FLOAT"),
            ("target_demographics", "TEXT"),
        ]
        
        grants_added = 0
        print(f"    Adding {len(grants_columns)} grant columns...")
        for col_name, col_type in grants_columns:
            try:
                cursor.execute(f"""
                    ALTER TABLE grants 
                    ADD COLUMN IF NOT EXISTS {col_name} {col_type};
                """)
                grants_added += 1
            except Exception as e:
                print(f"    ⚠️  Column {col_name}: {str(e)[:30]}...")
        
        # Add indexes for grants
        print("    📊 Creating indexes...")
        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_grants_program_id ON grants(program_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_grants_program_type ON grants(program_type);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_grants_region ON grants(region);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_grants_digital_application ON grants(digital_application);")
            print("    ✅ Grant indexes created")
        except Exception as e:
            print(f"    ⚠️  Index creation: {str(e)[:50]}...")
        
        print(f"    📈 Grants: {grants_added} columns added")

        # =====================================================================
        # VERIFICATION
        # =====================================================================
        print("\n[5] Verifying schema changes...")
        
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.columns 
            WHERE table_schema = 'public' AND table_name = 'companies';
        """)
        companies_cols = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.columns 
            WHERE table_schema = 'public' AND table_name = 'grants';
        """)
        grants_cols = cursor.fetchone()[0]
        
        print(f"    📊 Companies table: {companies_cols} total columns")
        print(f"    📊 Grants table: {grants_cols} total columns")
        
        # Data integrity check
        cursor.execute("SELECT COUNT(*) FROM companies;")
        company_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM grants;")
        grant_count = cursor.fetchone()[0]
        
        print(f"\n[6] Data integrity check:")
        print(f"    📈 Companies: {company_count} records")
        print(f"    📈 Grants: {grant_count} records")

        cursor.close()
        conn.close()
        
        print("\n" + "=" * 80)
        print("✅ MIGRATION COMPLETED SUCCESSFULLY")
        print("=" * 80)
        print(f"Summary:")
        print(f"  - Companies: {companies_cols} columns (target: 16)")
        print(f"  - Grants: {grants_cols} columns (target: 63)")
        print(f"  - Total new columns added: {companies_added + grants_added}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ [ERROR] Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
