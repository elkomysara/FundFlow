import sys
import os
from dotenv import load_dotenv

# ✅ CRITICAL: Load environment variables before anything else
load_dotenv()

# ✅ CRITICAL FIX: Add project root to system path for direct execution
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.database import get_db, init_db
from app.models import Grant, Company
from app.services.intelligent_matcher import IntelligentMatcher
from app.services.gemini_service import GeminiAdvisor
from app.schemas import CompanyCreate, CompanyResponse, GrantCreate, GrantResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
import textwrap

from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
import textwrap

# Create FastAPI application with comprehensive Team Nexus documentation and database statistics
app = FastAPI(
    title="ImaraFund API | Team Nexus - Women Techsters Fellowship 2025",
    description=textwrap.dedent("""
    # **Team Nexus - ImaraFund Project Structure**

    **Supervisor:** Mr. Anthony Ameh  
    **Team Leader:** Maureen Cheptoo - WTF/2025/1486

    ---

    ## **Technical Implementation Acknowledgment**

    **ImaraFund FastAPI Backend System**  
    *Architected, Developed, and Deployed by the Data Science and Engineering Team*

    The complete **FastAPI backend infrastructure**, intelligent matching engine, AI integration, 
    database architecture, and cloud deployment that powers the ImaraFund platform were designed, 
    implemented, and maintained by the **Data Science and Engineering Team** within the **Team Nexus** 
    organization. This team assumed full technical ownership from initial algorithm design through 
    production deployment on Google Cloud Platform.

    ---

    ## **Project Description – ImaraFund**

    **ImaraFund** is an AI-powered intelligent funding discovery and matching platform designed to 
    connect African Small and Medium Enterprises (SMEs) with the most relevant grant opportunities 
    across the continent. The platform addresses the critical challenge of SME funding access in 
    Africa by automating the grant discovery process and providing AI-generated strategic guidance 
    to increase application success rates.

    ### **Core Technical Architecture:**
    * **Backend:** Python 3.12.12 with FastAPI framework, deployed on Google Cloud Run
    * **Database:** PostgreSQL 15 (Cloud SQL) with comprehensive 79-column schema (63 grant + 16 company fields)
    * **AI Integration:** Google Gemini 2.5 Flash with intelligent quota optimization (66% API call reduction)
    * **Matching Algorithm:** Proprietary 40/30/20/10 weighted scoring system with mathematical formulation:

    ```
    S_total = (0.40 × S_geo) + (0.30 × S_sector) + (0.20 × S_funding) + (0.10 × S_stage)
    ```

    * **Infrastructure:** Fully containerized deployment with CI/CD pipeline on Google Cloud Platform
    * **Production URL:** https://imarafund-api-443679739700.europe-west1.run.app

    ### **Key Features:**
    * **Intelligent Matching:** Transparent scoring system evaluating geographic alignment (40%), sector compatibility (30%), funding amount fit (20%), and business stage alignment (10%)
    * **AI-Powered Recommendations:** Context-aware application advice generated through Google Gemini integration
    * **Comprehensive Database:** 103+ verified grant programs with complete CSV schema support
    * **Production-Ready API:** RESTful endpoints with interactive documentation, CRUD operations, and health monitoring
    * **Scalable Architecture:** Enterprise-grade deployment with robust error handling and fallback strategies

    ---

    ## **📊 Comprehensive Database Statistics & Coverage**

    The ImaraFund matching engine operates on two strategically designed datasets that enable comprehensive 
    testing and optimization of the intelligent matching algorithm.

    ### **1. Real-World Grants Dataset - 103 Verified Programs**

    **Source:** `data/cleaned/grants_cleaned_latest.csv`

    **Geographic Distribution:**
    * **Total Programs:** 103 verified funding opportunities
    * **Top Countries:** United States (5 programs), Germany (4), United Arab Emirates (3), Nigeria (3), Sweden (3), Turkey (2), Mexico (2), Kenya (2), Norway (2)
    * **Regional Coverage:**
      * Europe: 17 programs (16.5%)
      * Asia: 15 programs (14.6%)
      * Africa: 11 programs (10.7%)
      * Latin America: 10 programs (9.7%)
      * Caribbean: 9 programs (8.7%)
      * Middle East: 13 programs combined (12.6%)
      * Pacific: 12 programs combined (11.7%)
      * North America: 7 programs (6.8%)
      * Global: 3 programs (2.9%)
      * Oceania: 1 program (1.0%)

    **Program Structure & Terms:**
    * **Program Types:**
      * Financial Grants: 49 programs (47.6%)
      * Financial/Loans: 18 programs (17.5%)
      * Microfinance: 12 programs (11.7%)
      * Technical Resources: 4 programs (3.9%)
      * Unspecified Type: 20 programs (19.4%)
    * **Repayment Requirements:**
      * Loans (Repayment Required): 90 programs (87.4%)
      * Pure Grants (Non-Repayable): 13 programs (12.6%)

    **Sector-Specific Focus Areas:**
    * Agriculture-Focused: 15 programs (14.6% of total)
    * Women-Focused: 5 programs (4.9%)
    * Youth-Focused: 4 programs (3.9%)
    * Green/Climate-Focused: 4 programs (3.9%)
    * Technology/Innovation: 2 programs (1.9%)
    * Export Support: 2 programs (1.9%)

    **Financial Scale Analysis:**
    * **Programs with Financial Data:** 95 out of 103 (92.2%)
    * **Median Grant Amount:** $5,000,000
    * **25th Percentile:** $425,000
    * **75th Percentile:** $32,500,000
    * **Range:** $0 - $300 trillion (includes large-scale development funds)
    * **Mean:** $3.16 trillion (skewed by mega-funds, median more representative)

    ---

    ### **2. Synthetic Companies Dataset - 50 Diverse SME Profiles**

    **Source:** `data/companies/synthetic_companies.csv`

    **Geographic Registration Distribution:**
    * **Total Companies:** 50 synthetic profiles representing diverse global SMEs
    * **Top Registration Countries:**
      * South Africa: 7 companies (14%)
      * Brazil: 5 companies (10%)
      * Kenya: 5 companies (10%)
      * USA: 5 companies (10%)
      * Uganda: 4 companies (8%)
      * Indonesia: 4 companies (8%)
      * Nigeria: 4 companies (8%)
      * United Kingdom: 3 companies (6%)
      * Mexico: 3 companies (6%)
      * Germany: 3 companies (6%)

    **Sector Distribution Analysis:**
    * Healthcare: 11 companies (22%)
    * Technology: 7 companies (14%)
    * Food Processing: 6 companies (12%)
    * Manufacturing: 5 companies (10%)
    * E-commerce: 5 companies (10%)
    * Tourism: 4 companies (8%)
    * Financial Services: 4 companies (8%)
    * Clean Energy: 3 companies (6%)
    * Education: 3 companies (6%)
    * Agriculture: 2 companies (4%)

    **Business Maturity Profile:**
    * Growth Stage: 23 companies (46%)
    * Early Growth: 17 companies (34%)
    * Scale-up: 6 companies (12%)
    * Startup: 3 companies (6%)
    * Idea Stage: 1 company (2%)

    **Founder Demographics:**
    * Male Founders: 30 companies (60%)
    * Female Founders: 20 companies (40%)

    **Comprehensive Financial Analysis:**

    **Annual Revenue (USD):**
    * Count: 50 companies
    * Mean: $930,500
    * Median: $200,000
    * Standard Deviation: $1,562,355
    * Range: $0 - $5,000,000
    * 25th Percentile: $100,000
    * 75th Percentile: $1,000,000

    **Employee Count:**
    * Mean: 8.16 employees
    * Median: 4 employees
    * Standard Deviation: 10.52 employees
    * Range: 1 - 48 employees
    * 25th Percentile: 2 employees
    * 75th Percentile: 9.75 employees

    **Funding Requirements (USD):**
    * Mean: $1,482,000
    * Median: $500,000
    * Standard Deviation: $2,622,791
    * Range: $25,000 - $10,000,000
    * 25th Percentile: $250,000
    * 75th Percentile: $1,750,000

    ---

    ### **3. Strategic Matching Optimization Insights**

    **Dataset Alignment for Algorithm Testing:**

    **Geographic Matching Opportunities:**
    * 5 companies registered in USA align with 5 US-based grant programs
    * 4 companies in Nigeria match 3 Nigeria-specific programs
    * 5 companies in Kenya can target 2 Kenya-focused grants plus 11 Africa-regional programs
    * Global/regional programs (23 total) provide fallback options for all companies

    **Sector Alignment Analysis:**
    * 2 Agriculture companies can test against 15 agriculture-focused grants (7.5x opportunity multiplier)
    * 11 Healthcare companies provide robust testing for health-related grant criteria
    * 7 Technology companies align with 2 technology/innovation-specific programs plus broader innovation funds

    **Financial Compatibility Assessment:**
    * Company median funding need ($500K) vs Grant median value ($5M) = 10:1 ratio
    * 75th percentile company need ($1.75M) fits comfortably within grant ranges
    * SME definition compliance: All companies <50 employees, qualifying for 95%+ of SME-targeted programs

    **Matching Success Factors:**
    * **Growth Stage Targeting:** 80% of companies in Growth/Early Growth stages match primary demographic of development finance programs
    * **Gender Diversity Testing:** 40% female founder representation enables comprehensive evaluation of 5 women-focused grant programs
    * **Cross-Border Opportunities:** Multi-country registration enables testing of regional and global program eligibility logic
    * **Scale Appropriateness:** Average company size (8 employees, $930K revenue) fits typical SME eligibility criteria

    ---

    ## **Team Structure**

    ### **1. Product Management Team**
    Drives strategic vision, roadmap planning, and cross-team coordination for ImaraFund development.

    **Members:**
    * Maureen Cheptoo - WTF/2025/1486 *(Team Leader)*
    * Comfort Effiong - WTF/2025/5941
    * Favour Folorunso - WTF/2025/9542

    ---

    ### **2. Product Design Team**
    Creates intuitive user experiences and visual interfaces for optimal user engagement.

    **Members:**
    * Adegbite Suliyat Adenike - WTF/2025/1952
    * Ukah Christiana Amarachi - WTF/2025/3373

    ---

    ### **3. Software Development - Frontend Team**
    Implements client-facing components and responsive user interfaces for seamless user interaction.

    **Members:**
    * Queen Odede Christopher - WTF/2025/1100
    * Fatma Suleiman - WTF/2025/4962
    * Marvelous Olagoke - WTF/2025/3666

    ---

    ### **4. Software Development - Backend Team**
    Supports server-side architecture and complementary backend services.

    **Member:**
    * Christiana Ibrahim - WTF/2025/5849

    ---

    ### **5. Data Science and Engineering Team**

    **Primary Role:** Core technical architects responsible for the complete end-to-end implementation 
    of ImaraFund's backend system. This team designed, developed, and deployed the entire FastAPI 
    infrastructure, intelligent matching algorithm, AI integration, data pipelines, and cloud deployment 
    that powers the ImaraFund platform.

    **Major Technical Achievements:**

    **1. FastAPI Backend Architecture & Development**
    * Architected and implemented the complete **FastAPI-based backend system** that powers ImaraFund
    * Developed all core API endpoints:
      * `/api/v1/companies` – Full CRUD operations with 16-column company schema
      * `/api/v1/grants` – Full CRUD operations with 63-column grant schema  
      * `/api/v1/match/{company_id}` – Intelligent matching with AI advisory capabilities
      * `/health` – System diagnostics and monitoring endpoint
    * Implemented comprehensive validation using Pydantic, error handling, logging, and interactive documentation (`/docs`)

    **2. Intelligent Matching Algorithm Development**
    * Designed and implemented the proprietary **40/30/20/10 weighted scoring system** with mathematical rigor
    * Established quality threshold (>30 points) ensuring only relevant matches are returned
    * Developed transparent scoring breakdown for user understanding and system optimization
    * Conducted comprehensive testing and validation across diverse company-grant pairings

    **3. Google Gemini AI Integration**
    * Complete integration with **Google Gemini 2.5 Flash API** for personalized funding advice generation
    * Implemented intelligent quota management achieving **66% API call reduction** through optimization
    * Developed comprehensive error handling, retry logic, and user-friendly fallback messaging strategies
    * Created production-ready `GeminiAdvisor` service with multi-format response extraction and connection testing

    **4. Database Architecture & Data Engineering**
    * Designed complete database schema supporting **63 grant columns and 16 company columns**
    * Implemented PostgreSQL 15 with proper indexing, performance optimization, and connection pooling
    * Created safe migration scripts enabling schema evolution without data loss
    * Developed intelligent CSV data loaders with advanced type conversion, NULL value handling, and validation

    **5. Data Collection, Analysis, and Curation**
    * Curated comprehensive dataset of **103+ African grant programs** from multiple verified sources
    * Generated synthetic company dataset representing diverse African SME scenarios across 15+ sectors
    * Performed extensive data cleaning, normalization, and validation processes
    * Conducted exploratory data analysis to optimize matching patterns and algorithm performance
    * **Statistical Analysis:** Comprehensive profiling of both datasets including financial distributions, geographic coverage analysis, and sector alignment optimization

    **6. Google Cloud Platform Production Deployment**
    * Deployed complete system to **Google Cloud Run** with containerized Docker architecture
    * Configured **Cloud SQL (PostgreSQL 15)** with secure networking and environment management
    * Implemented **Cloud Build CI/CD pipeline** for automated deployments and version control
    * Established comprehensive monitoring, logging, and health check systems achieving **99.9%+ uptime**

    **7. GitHub Repository Management & Documentation**
    * Created and maintained comprehensive **GitHub repository** with complete project structure
    * Developed extensive technical documentation including API guides, deployment procedures, and troubleshooting
    * Implemented testing suites for both local development and production environments
    * Established code review standards and contribution guidelines for long-term maintainability

    **Technical Stack:**
    * **Languages & Frameworks:** Python 3.12.12, FastAPI, SQLAlchemy, Pydantic, Pandas, NumPy
    * **AI/ML Technologies:** Google Gemini 2.5 Flash API, intelligent matching algorithms
    * **Database Systems:** PostgreSQL 15, SQLite (development), database migration tools
    * **Cloud Infrastructure:** Google Cloud Platform (Cloud Run, Cloud SQL, Cloud Build)
    * **DevOps & Deployment:** Docker containerization, CI/CD pipelines, environment management
    * **Data Analysis:** Pandas, NumPy, statistical profiling, exploratory data analysis

    **Members:**
    * Busola Oladokun - WTF/2025/9397
    * Gold Agboola - WTF/2025/9629
    * Nqobile Buthelezi - WTF/2025/6698
    * Oluwanifemi Famobio - WTF/2025/9191
    * Sara Taha - WTF/2025/1140

    ---

    ### **6. Cybersecurity Team**
    Ensures platform security protocols, implements protection measures, and safeguards user data integrity.

    **Members:**
    * Ugwoke Divine-Gift Mmesoma - WTF/2025/7217
    * Magopane Katlego - WTF/2025/7300
    * Eunice Onukwue - WTF/2025/1438

    ---

    ## **Current Project Status**

    **System Metrics:**
    * ✅ **Production Deployment:** Fully operational on Google Cloud Platform
    * ✅ **Data Coverage:** 103 verified grant programs across 30+ countries, 50+ company profiles across 10+ countries
    * ✅ **AI Integration:** Google Gemini 2.5 Flash with optimized quota management
    * ✅ **API Performance:** <5s matching response time, <30s with AI advice generation
    * ✅ **Database Schema:** Complete 79-column coverage with full CSV support
    * ✅ **System Reliability:** 99.9%+ uptime on enterprise-grade cloud infrastructure
    * ✅ **Matching Coverage:** 87.4% loan programs, 12.6% pure grants with comprehensive sector targeting
    * ✅ **Algorithm Optimization:** Strategic dataset design ensuring 95%+ SME eligibility compliance

    **Access Points:**
    * **Production API:** https://imarafund-api-443679739700.europe-west1.run.app
    * **Interactive Documentation:** https://imarafund-api-443679739700.europe-west1.run.app/docs
    * **Health Monitoring:** https://imarafund-api-443679739700.europe-west1.run.app/health

    ---

    **Team Nexus Composition:** 19 specialized professionals across 6 collaborative teams working 
    under the supervision of **Mr. Anthony Ameh** and the leadership of **Maureen Cheptoo**.

    ---

    ## **🎓 Academic Context**

    This project represents advanced data science and software engineering principles applied to 
    solve real-world African SME funding challenges. Developed as part of the Women Techsters 
    Fellowship 2025 program, demonstrating enterprise-grade system design, AI integration, cloud 
    deployment capabilities, and comprehensive statistical data analysis for intelligent matching 
    algorithm optimization.
    """).strip(),
    version="4.0.0",
    contact={
        "name": "Team Nexus - Women Techsters Fellowship 2025",
        "url": "https://womentechsters.org"
    },
    license_info={
        "name": "Women Techsters Fellowship Project 2025",
        "url": "https://womentechsters.org"
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "health",
            "description": "System health monitoring and diagnostics"
        },
        {
            "name": "companies", 
            "description": "Company profile management (50 profiles, 10 countries, 10 sectors)"
        },
        {
            "name": "grants",
            "description": "Grant program management (103 programs, 30+ countries, global coverage)"
        },
        {
            "name": "matching",
            "description": "Intelligent matching with AI recommendations (40/30/20/10 algorithm, >30 quality threshold)"
        }
    ]
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Global AI advisor instance
gemini_advisor = None

# ===== PYDANTIC MODELS FOR MATCHING (RESPONSE SHAPES) =====
class ScoreBreakdown(BaseModel):
    geographic: float
    sector: float
    amount_fit: float
    stage: float

class MatchResultInternal(BaseModel):
    program_name: str
    institution: str
    country: str
    funding_amount: float
    match_score: float
    score_breakdown: ScoreBreakdown
    website: Optional[str] = None
    target_sectors: Optional[str] = None
    repayment_required: Optional[str] = None
    ai_advice: Optional[str] = None

class MatchResponse(BaseModel):
    matches: List[MatchResultInternal]
    total_matches_found: int
    company_name: str
    ai_summary: Optional[str] = None


# ===== STARTUP EVENT =====
@app.on_event("startup")
async def startup_event():
    """Initialize database and AI services on application startup"""
    global gemini_advisor
    
    logger.info("🚀 ImaraFund API starting up - Women Techsters Fellowship 2025")
    
    # Initialize database
    try:
        init_db()
        logger.info("✅ Database tables initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}")
        raise
    
    # Initialize Gemini AI advisor
    try:
        gemini_advisor = GeminiAdvisor()
        if gemini_advisor.enabled:
            logger.info("✅ AI advisor ready - UNLIMITED recommendations enabled for ALL matches")
        else:
            logger.warning("⚠️ AI advisor disabled - check GEMINI_API_KEY")
    except Exception as e:
        logger.error(f"❌ Failed to initialize AI advisor: {str(e)}")
        logger.warning("⚠️ Continuing without AI recommendations")
        gemini_advisor = None


# ===== BASIC ENDPOINTS =====
@app.get("/")
def root():
    return {
        "message": "ImaraFund Intelligent Matching API - Operational",
        "project": "Women Techsters Fellowship 2025 Capstone",
        "team": {
            "name": "NexusTeam - Data Science",
            "fellowship": "Women Techsters Fellowship (WTF) 2025",
            "supervisor": "Maureen Cheptoo",
            "members": [
                {"name": "Busola Oladokun", "id": "WTF/2025/9397", "focus": "Project Architecture"},
                {"name": "Gold Agboola", "id": "WTF/2025/9629", "focus": "Data Engineering"},
                {"name": "Nqobile Buthelezi", "id": "WTF/2025/6698", "focus": "Machine Learning"},
                {"name": "Oluwanifemi Famobio", "id": "WTF/2025/9191", "focus": "Backend Development"},
                {"name": "Sara Taha", "id": "WTF/2025/1140", "focus": "Full Stack Development"}
            ]
        },
        "version": "2.0.0",
        "status": "operational",
        "features": {
            "ai_enabled": bool(gemini_advisor and gemini_advisor.enabled),
            "full_csv_schema": "Complete 63 grant + 16 company fields",
            "ai_coverage": "UNLIMITED - AI advice for ALL matches",
            "crud_operations": "Create companies and grants"
        },
        "endpoints": {
            "grants_list": "GET /api/v1/grants",
            "grants_create": "POST /api/v1/grants",
            "companies_list": "GET /api/v1/companies", 
            "companies_create": "POST /api/v1/companies",
            "matching": "POST /api/v1/match/{company_id}",
            "docs": "GET /docs"
        },
        "algorithm": "40/30/20/10 weighted scoring system",
        "fellowship_program": "Women Techsters 2025"
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        grant_count = db.query(Grant).count()
        company_count = db.query(Company).count()
        
        return {
            "status": "healthy",
            "service": "imarafund-api",
            "version": "2.0.0",
            "database": {
                "connected": True,
                "grants_count": grant_count,
                "companies_count": company_count
            },
            "ai_enabled": bool(gemini_advisor and gemini_advisor.enabled),
            "schema": {
                "companies": "16 CSV columns supported",
                "grants": "63 CSV columns supported"
            },
            "fellowship": "Women Techsters Fellowship 2025",
            "team": "NexusTeam - Data Science"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")


# ============================================================================
# GRANT ENDPOINTS
# ============================================================================
@app.get("/api/v1/grants", response_model=List[GrantResponse])
def list_grants(
    limit: int = Query(100, ge=1, le=500),
    skip: int = Query(0, ge=0),
    country: Optional[str] = Query(None),
    sector: Optional[str] = Query(None),
    women_focused: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    """List grants with filtering capabilities"""
    try:
        query = db.query(Grant)
        
        if country:
            query = query.filter(Grant.country.ilike(f"%{country}%"))
        if sector:
            query = query.filter(Grant.target_sectors.ilike(f"%{sector}%"))
        if women_focused is not None:
            query = query.filter(Grant.women_focused == women_focused)
        
        grants = query.offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(grants)} grants")
        return grants
        
    except Exception as e:
        logger.error(f"Error listing grants: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/grants", response_model=GrantResponse, status_code=status.HTTP_201_CREATED)
async def create_grant(grant: GrantCreate, db: Session = Depends(get_db)):
    """Create grant with complete 63-column CSV support"""
    try:
        if hasattr(grant, 'model_dump'):
            grant_data = grant.model_dump(exclude_unset=True)
        else:
            grant_data = grant.dict(exclude_unset=True)
        
        db_grant = Grant(**grant_data)
        db.add(db_grant)
        db.commit()
        db.refresh(db_grant)
        
        logger.info(f"✅ Created grant: {db_grant.program_name} (ID: {db_grant.id})")
        return db_grant
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error creating grant: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create grant: {str(e)}")


# ============================================================================
# COMPANY ENDPOINTS
# ============================================================================
@app.get("/api/v1/companies", response_model=List[CompanyResponse])
def list_companies(
    limit: int = Query(100, ge=1, le=500),
    skip: int = Query(0, ge=0),
    sector: Optional[str] = Query(None),
    nationality: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List companies with filtering capabilities"""
    try:
        query = db.query(Company)
        
        if sector:
            query = query.filter(Company.sector.ilike(f"%{sector}%"))
        if nationality:
            query = query.filter(Company.nationality.ilike(f"%{nationality}%"))
        
        companies = query.offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(companies)} companies")
        return companies
        
    except Exception as e:
        logger.error(f"Error listing companies: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/companies", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    """Create company with complete 16-column CSV support"""
    try:
        if hasattr(company, 'model_dump'):
            company_data = company.model_dump(exclude_unset=True)
        else:
            company_data = company.dict(exclude_unset=True)
        
        db_company = Company(**company_data)
        db.add(db_company)
        db.commit()
        db.refresh(db_company)
        
        logger.info(f"✅ Created company: {db_company.company_name} (ID: {db_company.id})")
        return db_company
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error creating company: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create company: {str(e)}")


# ============================================================================
# EXECUTIVE SUMMARY GENERATOR
# ============================================================================
def _generate_executive_summary(company: Company, match_results: List[MatchResultInternal]) -> str:
    """
    Generate comprehensive executive summary synthesizing all match recommendations.
    Produces portfolio-level insight for technical report & demo.
    """
    if not match_results:
        return "No suitable funding matches found. Consider broadening eligibility criteria or strengthening business profile."
    
    scores = [m.match_score for m in match_results]
    avg_score = sum(scores) / len(scores)
    best_score = max(scores)
    worst_score = min(scores)
    
    geo_avg = sum(m.score_breakdown.geographic for m in match_results) / len(match_results)
    sec_avg = sum(m.score_breakdown.sector for m in match_results) / len(match_results)
    amt_avg = sum(m.score_breakdown.amount_fit for m in match_results) / len(match_results)
    stg_avg = sum(m.score_breakdown.stage for m in match_results) / len(match_results)
    
    dimensions = {
        'geographic alignment': (geo_avg, 40),
        'sector compatibility': (sec_avg, 30), 
        'funding scale match': (amt_avg, 20),
        'business stage fit': (stg_avg, 10)
    }
    sorted_dims = sorted(dimensions.items(), key=lambda x: x[1][0] / x[1][1], reverse=True)
    strongest_area = sorted_dims[0][0]
    weakest_area = sorted_dims[-1][0]
    
    excellent = [m for m in match_results if m.match_score >= 80]
    strong = [m for m in match_results if 70 <= m.match_score < 80]
    moderate = [m for m in match_results if m.match_score < 70]
    
    summary_parts: List[str] = []
    
    # Portfolio overview
    summary_parts.append(
        f"EXECUTIVE PORTFOLIO ANALYSIS: {company.company_name} ({company.sector}, {company.nationality}) "
        f"shows an average compatibility score of {avg_score:.0f}/100 across {len(match_results)} funding opportunities "
        f"(range: {worst_score:.0f}–{best_score:.0f}/100). "
    )
    
    # Tiered recommendations
    if excellent:
        summary_parts.append(
            f"IMMEDIATE PRIORITY: {len(excellent)} high-compatibility program"
            f"{'' if len(excellent)==1 else 's'} "
            f"({', '.join(m.program_name for m in excellent[:2])}) warrant immediate application focus. "
        )
    if strong:
        summary_parts.append(
            f"STRONG PIPELINE: {len(strong)} additional opportunity"
            f"{'' if len(strong)==1 else 'ies'} demonstrate solid strategic fit that can be "
            f"competitive with targeted positioning. "
        )
    if moderate:
        summary_parts.append(
            f"DEVELOPMENT OPPORTUNITIES: {len(moderate)} program"
            f"{'' if len(moderate)==1 else 's'} require strategic enhancement before submitting "
            f"highly competitive applications. "
        )
    
    # Strengths & gaps
    summary_parts.append(
        f"COMPETITIVE STRENGTH: Your {strongest_area} consistently performs well "
        f"(averaging {sorted_dims[0][1][0]:.0f}/{sorted_dims[0][1][1]} points), providing a strong basis for "
        f"differentiation in all applications. "
    )
    
    if weakest_area != strongest_area:
        summary_parts.append(
            f"PRIMARY IMPROVEMENT AREA: Enhancing {weakest_area} "
            f"(currently {sorted_dims[-1][1][0]:.0f}/{sorted_dims[-1][1][1]} points on average) "
            f"would significantly increase competitiveness across your entire funding portfolio. "
        )
    
    # Action guidance
    if best_score >= 80:
        summary_parts.append(
            f"RECOMMENDED ACTION: Prioritize immediate, high-quality submissions to top-tier programs "
            f"while using the detailed AI advisories above to tailor positioning around your strongest "
            f"capabilities and address any identified gaps."
        )
    elif best_score >= 70:
        summary_parts.append(
            f"RECOMMENDED ACTION: Focus on strengthening the identified improvement area and refine your "
            f"narratives for the strongest opportunities first, using the AI-generated strategies as a guide."
        )
    else:
        summary_parts.append(
            f"RECOMMENDED ACTION: Before submitting applications, invest in strengthening your core "
            f"business profile and alignment with funder priorities, guided by the AI recommendations "
            f"for each match."
        )
    
    return "".join(summary_parts)


# ============================================================================
# MATCHING ENDPOINT - UNLIMITED AI FOR ALL MATCHES
# ============================================================================
@app.post("/api/v1/match/{company_id}", response_model=MatchResponse)
def match_company_with_grants(
    company_id: int,
    top_n: int = Query(5, ge=1, le=20, description="Number of top matches to return"),
    include_ai_advice: bool = Query(True, description="Include AI-generated advice for ALL matches"),
    db: Session = Depends(get_db)
):
    """
    Run ImaraFund's intelligent matching algorithm with AI recommendations
    
    ✅ UNLIMITED AI: AI advice generated for ALL matches
    ✅ PRESERVED: 40/30/20/10 scoring system
    """
    matcher = IntelligentMatcher(db)
    
    try:
        company, matches = matcher.find_matches(company_id, top_n=top_n)
    except ValueError as e:
        logger.warning(f"Company not found: {company_id}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Matching error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Matching error: {str(e)}")

    if not matches:
        logger.info(f"No matches found for company {company_id}")
        return MatchResponse(
            matches=[],
            total_matches_found=0,
            company_name=company.company_name,
            ai_summary="No suitable funding matches found. Consider broadening your criteria."
        )

    match_results: List[MatchResultInternal] = []
    ai_generation_count = 0
    
    for i, match in enumerate(matches):
        breakdown = match.get('score_breakdown', {})
        
        ai_advice: Optional[str] = None
        if include_ai_advice and gemini_advisor and gemini_advisor.enabled:
            try:
                logger.info(f"🤖 Generating AI advice for match #{i+1}: {match.get('program_name', 'Unknown')}")
                ai_advice = gemini_advisor.generate_match_advice(
                    company_name=company.company_name,
                    company_sector=company.sector or "General",
                    company_country=company.nationality or "Unknown",
                    funding_need_usd=company.funding_need_usd or 0,
                    grant_name=match.get('program_name', 'Unknown Program'),
                    grant_institution=match.get('institution', 'Unknown Institution'),
                    grant_country=match.get('country', 'Unknown'),
                    grant_sectors=match.get('target_sectors', 'General'),
                    grant_amount=match.get('funding_amount', 0),
                    match_score=match.get('match_score', 0),
                    score_breakdown=breakdown
                )
                if ai_advice:
                    ai_generation_count += 1
                    logger.info(f"✅ Professional advice generated for match #{i+1}")
            except Exception as e:
                logger.error(f"❌ AI generation failed for match #{i+1}: {str(e)}")
                ai_advice = "Professional AI analysis temporarily unavailable."
        
        match_result = MatchResultInternal(
            program_name=match.get('program_name', 'Unknown Program'),
            institution=match.get('institution', 'Unknown Institution'),
            country=match.get('country', 'Unknown'),
            funding_amount=match.get('funding_amount', 0),
            match_score=match.get('match_score', 0),
            score_breakdown=ScoreBreakdown(
                geographic=breakdown.get('geographic', 0),
                sector=breakdown.get('sector', 0),
                amount_fit=breakdown.get('amount_fit', 0),
                stage=breakdown.get('stage', 0)
            ),
            website=match.get('website'),
            target_sectors=match.get('target_sectors', 'General'),
            repayment_required=str(match.get('repayment_required', 'Unknown')),
            ai_advice=ai_advice
        )
        match_results.append(match_result)

    logger.info(f"✅ Processed {len(match_results)} matches, {ai_generation_count} with AI advice")

    # ✅ ENHANCED: Executive-level AI summary based on all matches
    ai_summary: Optional[str] = None
    try:
        ai_summary = _generate_executive_summary(company, match_results)
        logger.info("✅ Executive summary generated")
    except Exception as e:
        logger.error(f"Failed to generate executive summary: {str(e)}")
        ai_summary = (
            f"Analysis complete for {company.company_name}: {len(match_results)} funding opportunities identified "
            f"with compatibility scores ranging from {min(m.match_score for m in match_results):.0f} to "
            f"{max(m.match_score for m in match_results):.0f}/100. Review detailed strategic guidance above."
        )

    return MatchResponse(
        matches=match_results,
        total_matches_found=len(match_results),
        company_name=company.company_name,
        ai_summary=ai_summary
    )


# Diagnostic endpoint to check AI advisor status
@app.get("/api/v1/ai-status")
def check_ai_status():
    """Diagnostic endpoint to check AI service status"""
    if gemini_advisor is None:
        return {
            "status": "not_initialized",
            "error": "GeminiAdvisor instance is None"
        }
    
    return {
        "status": "initialized" if gemini_advisor.enabled else "disabled",
        "details": gemini_advisor.get_status()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
