"""
ImaraFund Intelligent Matching Algorithm
40/30/20/10 weighted scoring system with enhanced error handling
"""

from typing import List, Tuple, Dict
from sqlalchemy.orm import Session
from app.models import Grant, Company
import logging

logger = logging.getLogger(__name__)

class IntelligentMatcher:
    """
    ImaraFund Intelligent Matching Algorithm
    40/30/20/10 weighted scoring system
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_matches(self, company_id: int, top_n: int = 5) -> Tuple[Company, List[Dict]]:
        """Find best matching grants using 40/30/20/10 scoring algorithm"""
        company = self.db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise ValueError(f"Company with ID {company_id} not found")

        grants = self.db.query(Grant).all()
        matches = []
        
        logger.info(f"Evaluating {len(grants)} grants for company: {company.company_name}")
        
        for grant in grants:
            try:
                score, breakdown = self._calculate_match_score(company, grant)
                
                if score > 30:  # Quality threshold
                    # ✅ COMPLETE: Include ALL required fields with safe defaults
                    match_dict = {
                        'grant': grant,
                        'program_name': str(grant.program_name or 'Unknown Program'),
                        'institution': str(grant.institution_name or 'Unknown Institution'),
                        'country': str(grant.country or 'Unknown'),
                        'funding_amount': float(grant.estimated_value_amount or 0),
                        'match_score': round(float(score), 1),
                        'score_breakdown': breakdown,
                        'target_sectors': str(grant.target_sectors or 'General'),
                        'website': grant.website_url,  # Can be None
                        'repayment_required': str(grant.repayment_required) if grant.repayment_required is not None else 'Unknown'
                    }
                    matches.append(match_dict)
                    
            except Exception as e:
                logger.error(f"Error processing grant {grant.id}: {str(e)}")
                continue  # Skip problematic grants

        matches_sorted = sorted(matches, key=lambda x: x['match_score'], reverse=True)[:top_n]
        logger.info(f"Found {len(matches_sorted)} matches above threshold for {company.company_name}")
        return company, matches_sorted

    def _calculate_match_score(self, company: Company, grant: Grant) -> Tuple[float, Dict]:
        """Calculate comprehensive match score using 40/30/20/10 weighting"""
        score = 0.0
        breakdown = {}

        # 1. Geographic Match (40 points) - Most important
        geo_score = self._score_geography(company, grant)
        score += geo_score
        breakdown['geographic'] = float(geo_score)

        # 2. Sector Match (30 points)
        sector_score = self._score_sector(company, grant)
        score += sector_score
        breakdown['sector'] = float(sector_score)

        # 3. Funding Amount Fit (20 points)
        amount_score = self._score_funding_amount(company, grant)
        score += amount_score
        breakdown['amount_fit'] = float(amount_score)

        # 4. Stage Bonus (10 points)
        stage_score = self._score_business_stage(company, grant)
        score += stage_score
        breakdown['stage'] = float(stage_score)

        return min(100.0, score), breakdown

    def _score_geography(self, company: Company, grant: Grant) -> float:
        """Score geographic eligibility (0-40 points)"""
        company_country = str(company.nationality or '').lower().strip()
        grant_scope = str(grant.geographic_scope or '').lower().strip()
        grant_country = str(grant.country or '').lower().strip()

        # Global programs get full points
        if 'global' in grant_scope:
            return 40.0

        # Exact country match
        if company_country in grant_country or company_country in grant_scope:
            return 40.0

        # Regional matches for African countries
        africa_countries = [
            'nigeria', 'kenya', 'south africa', 'ghana', 'uganda', 'egypt',
            'tanzania', 'rwanda', 'ethiopia', 'senegal', 'botswana', 'zambia'
        ]

        if company_country in africa_countries:
            if 'africa' in grant_scope or 'african' in grant_scope:
                return 35.0

        return 0.0

    def _score_sector(self, company: Company, grant: Grant) -> float:
        """Score sector alignment (0-30 points)"""
        company_sector = str(company.sector or '').lower().strip()
        target_sectors = str(grant.target_sectors or '').lower().strip()

        # All sectors accepted
        if any(keyword in target_sectors for keyword in ['all', 'general', 'any']):
            return 25.0

        # Exact sector match
        if company_sector in target_sectors:
            return 30.0

        # Partial match
        sector_words = company_sector.split()
        if any(word in target_sectors for word in sector_words if len(word) > 3):
            return 20.0

        return 10.0

    def _score_funding_amount(self, company: Company, grant: Grant) -> float:
        """Score funding amount fit (0-20 points)"""
        need = float(company.funding_need_usd or 0.0)
        available = float(grant.estimated_value_amount or 0.0)

        if available == 0 or need == 0:
            return 15.0  # Unknown amount gets partial credit

        ratio = need / available

        # Perfect fit: need is 10%-200% of available
        if 0.1 <= ratio <= 2.0:
            return 20.0
        # Good fit: need is 5%-500% of available
        elif 0.05 <= ratio <= 5.0:
            return 15.0
        # Poor fit but not impossible
        else:
            return 8.0

    def _score_business_stage(self, company: Company, grant: Grant) -> float:
        """Score business stage fit (0-10 points)"""
        stage = str(company.business_stage or '').lower().strip()

        if stage in ['startup', 'early growth']:
            return 10.0
        elif stage == 'idea':
            return 8.0
        elif stage in ['growth', 'scale-up', 'expansion']:
            return 9.0
        else:
            return 7.0
