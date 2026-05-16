"""
Direct AI Prompt Testing - Bypasses API and Database
Tests the GeminiAdvisor class directly with controlled inputs
"""

import sys
import os
import logging

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.gemini_service import GeminiAdvisor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_high_quality_match():
    """Test AI advice for a high-quality match scenario"""
    print("\n🤖 INITIALIZING GEMINI ADVISOR...")
    advisor = GeminiAdvisor()
    
    if not advisor.enabled:
        print("❌ AI Service disabled. Check GEMINI_API_KEY.")
        return False

    print(f"✅ Service Active. Model: {advisor.model_name}")

    # High-quality match scenario
    print("\n🧪 TEST CASE: High-Quality Match (Kenyan Agri-Tech → Global Agriculture Fund)")
    
    advice = advisor.generate_match_advice(
        company_name="GreenHarvest Kenya",
        company_sector="Agriculture Technology", 
        company_country="Kenya",
        funding_need_usd=75000.0,
        grant_name="Global Agriculture Innovation Fund",
        grant_institution="World Bank",
        grant_country="Global",
        grant_sectors="Agriculture, Technology, Sustainability",
        grant_amount=150000.0,
        match_score=95.0,
        score_breakdown={
            'geographic': 40.0,  # Perfect global eligibility
            'sector': 30.0,      # Perfect sector match
            'amount_fit': 18.0,  # Good amount fit (75k need vs 150k available)
            'stage': 7.0         # Good stage fit
        }
    )

    print("\n" + "="*60)
    print("🧠 AI GENERATED ADVICE:")
    print("="*60)
    print(advice)
    print("="*60)

    # Quality validation checks
    if advice:
        checks = {
            "Has content": len(advice) > 50,
            "Reasonable length": len(advice) < 2000,
            "Mentions company": "GreenHarvest" in advice or "Kenya" in advice,
            "Mentions grant": "Global Agriculture" in advice or "World Bank" in advice,
            "Contains actionable advice": any(word in advice.lower() for word in ['should', 'recommend', 'focus', 'prepare', 'apply']),
            "Professional tone": not any(word in advice.lower() for word in ['lol', 'omg', 'awesome', 'amazing'])
        }
        
        print("\n✅ QUALITY VALIDATION:")
        all_passed = True
        for check, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"{status} {check}: {passed}")
            if not passed:
                all_passed = False
        
        return all_passed
    else:
        print("❌ No advice generated")
        return False

def test_weak_match_scenario():
    """Test AI advice for a weak match to ensure it identifies problems"""
    print("\n🧪 TEST CASE: Weak Match (FinTech → Health Grant)")
    
    advisor = GeminiAdvisor()
    if not advisor.enabled:
        return False
    
    advice = advisor.generate_match_advice(
        company_name="PayQuick Nigeria",
        company_sector="FinTech",
        company_country="Nigeria", 
        funding_need_usd=25000.0,
        grant_name="Global Health Infrastructure Fund",
        grant_institution="WHO",
        grant_country="Global",
        grant_sectors="Healthcare, Medical Equipment, Hospitals",
        grant_amount=500000.0,
        match_score=38.0,  # Just above threshold
        score_breakdown={
            'geographic': 25.0,  # Partial geographic fit
            'sector': 3.0,       # Poor sector match
            'amount_fit': 5.0,   # Poor amount fit
            'stage': 5.0         # Poor stage fit
        }
    )
    
    print("\n" + "="*50)
    print("🧠 WEAK MATCH ADVICE:")
    print("="*50)
    print(advice)
    print("="*50)
    
    # The AI should identify the sector mismatch or suggest improvements
    if advice:
        weakness_indicators = ['sector', 'mismatch', 'gap', 'challenge', 'improve', 'strengthen', 'address']
        identifies_weakness = any(indicator in advice.lower() for indicator in weakness_indicators)
        
        if identifies_weakness:
            print("✅ SUCCESS: AI identified the match weaknesses")
            return True
        else:
            print("⚠️ WARNING: AI did not explicitly address the weaknesses")
            return False
    else:
        print("❌ No advice generated")
        return False

def test_variable_injection():
    """Test that all variables are properly injected into the prompt"""
    print("\n🧪 TEST CASE: Variable Injection Verification")
    
    advisor = GeminiAdvisor()
    if not advisor.enabled:
        return False
    
    # Use distinctive values to easily spot in output
    advice = advisor.generate_match_advice(
        company_name="TESTCOMPANY_12345",
        company_sector="TESTSECTOR_67890", 
        company_country="TESTCOUNTRY_ABCDE",
        funding_need_usd=99999.0,
        grant_name="TESTGRANT_FGHIJ",
        grant_institution="TESTINSTITUTION_KLMNO",
        grant_country="TESTLOCATION_PQRST",
        grant_sectors="TESTTARGETS_UVWXY",
        grant_amount=88888.0,
        match_score=77.0,
        score_breakdown={'geographic': 30, 'sector': 25, 'amount_fit': 15, 'stage': 7}
    )
    
    if advice:
        # Check if our test values appear in the advice
        test_values = ["TESTCOMPANY_12345", "TESTSECTOR_67890", "TESTGRANT_FGHIJ"]
        injection_success = any(value in advice for value in test_values)
        
        if injection_success:
            print("✅ SUCCESS: Variables properly injected into prompt")
            return True
        else:
            print("⚠️ WARNING: Variables may not be properly injected")
            print(f"Advice preview: {advice[:200]}...")
            return False
    else:
        print("❌ No advice generated")
        return False

if __name__ == "__main__":
    print("🚀 ImaraFund Direct AI Prompt Testing")
    print("=" * 60)
    
    results = []
    results.append(("High Quality Match", test_high_quality_match()))
    results.append(("Weak Match Scenario", test_weak_match_scenario()))
    results.append(("Variable Injection", test_variable_injection()))
    
    print("\n" + "=" * 60)
    print("📊 DIRECT TESTING RESULTS:")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    total_passed = sum(1 for _, passed in results if passed)
    print(f"\nTotal: {total_passed}/{len(results)} tests passed")
    
    if total_passed >= 2:
        print("🎉 Direct AI testing successful!")
    else:
        print("⚠️ AI prompt issues detected - review configuration")
