"""
ImaraFund Google Gemini AI Integration - Tier 1 Professional
OPTIMIZED: Hybrid AI + Enhanced Fallback System for Consistent Quality
Women Techsters Fellowship 2025 - NexusTeam
Language-Aware Conversational Advisory with Unique Match Analysis
"""

import google.generativeai as genai
import os
import logging
import time
from typing import Dict, Optional, Any
from functools import wraps
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

def retry_on_error(max_retries=1, delay=0.5):
    """Minimal retry to prevent API exhaustion"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries:
                        logger.warning(f"⚠️ Retry {attempt + 1}/{max_retries}")
                        time.sleep(delay)
                        continue
                    raise
            return None
        return wrapper
    return decorator

class GeminiAdvisor:
    """
    Hybrid AI advisory system: Gemini AI + Enhanced Deterministic Fallback
    Design: Use AI when excellent, fallback for consistency
    Language-aware: Responds in user's preferred language with unique match analysis
    """
    
    def __init__(self):
        """Initialize Gemini AI with robust model testing"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL", "models/gemini-2.5-flash")
        self.enabled = False
        self.model = None
        self.generation_count = 0
        self.tier = "Tier 1 Professional - Hybrid Optimized + Unique Match Analysis"
        
        logger.info("=" * 60)
        logger.info("🔧 GEMINI AI INITIALIZATION - HYBRID OPTIMIZED")
        logger.info("=" * 60)
        
        if not self.api_key:
            logger.error("❌ GEMINI_API_KEY not found!")
            return
        
        logger.info(f"✅ API Key: {self.api_key[:10]}...{self.api_key[-4:]}")
        
        if not self.api_key.startswith("AIza"):
            logger.error("❌ Invalid API key format")
            return
        
        try:
            genai.configure(api_key=self.api_key)
            logger.info("✅ Gemini API configured")
            
            # Use verified working models
            model_attempts = [
                "models/gemini-2.5-flash",
                "models/gemini-flash-latest", 
                "models/gemini-pro-latest",
            ]
            
            for model in model_attempts:
                try:
                    logger.info(f"🔄 Testing: {model}")
                    self.model = genai.GenerativeModel(model)
                    
                    test_response = self.model.generate_content(
                        "System test: respond 'OPERATIONAL' if working correctly.",
                        generation_config=genai.types.GenerationConfig(
                            max_output_tokens=50,
                            temperature=0.1
                        )
                    )
                    
                    if self._validate_response(test_response):
                        self.model_name = model
                        self.enabled = True
                        logger.info(f"✅ ACTIVE: {model}")
                        logger.info("📊 Hybrid System: AI + Enhanced Fallback")
                        logger.info("=" * 60)
                        return
                        
                except Exception as e:
                    logger.warning(f"⚠️ {model}: {str(e)[:100]}")
                    continue
            
            logger.error("❌ All models failed - fallback-only mode")
            self.enabled = False
            
        except Exception as e:
            logger.error(f"❌ Init failed: {str(e)}")
            self.enabled = False
    
    def _validate_response(self, response) -> bool:
        """Validate response can be extracted"""
        if not response:
            return False
        try:
            text = self._extract_text_from_response(response)
            return bool(text and len(text.strip()) > 0)
        except:
            return False
    
    def _extract_text_from_response(self, response) -> Optional[str]:
        """Comprehensive text extraction with error handling"""
        if not response:
            return None
        
        try:
            # Method 1: Direct text access
            if hasattr(response, 'text'):
                try:
                    text = response.text.strip()
                    if text:
                        return text
                except Exception:
                    pass
            
            # Method 2: Candidates structure
            if hasattr(response, 'candidates') and response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate, 'content') and candidate.content:
                        if hasattr(candidate.content, 'parts') and candidate.content.parts:
                            for part in candidate.content.parts:
                                if hasattr(part, 'text') and part.text:
                                    text = part.text.strip()
                                    if text:
                                        return text
            return None
            
        except Exception as e:
            logger.debug(f"Text extraction error: {e}")
            return None
    
    def _get_language_name(self, language_code: str) -> str:
        """Convert language code to full language name for AI prompt"""
        language_map = {
            "en": "English", "es": "Spanish", "fr": "French", "de": "German",
            "it": "Italian", "pt": "Portuguese", "zh": "Chinese", "ja": "Japanese",
            "ko": "Korean", "ar": "Arabic", "hi": "Hindi", "ru": "Russian",
            "sw": "Swahili", "am": "Amharic", "yo": "Yoruba", "ha": "Hausa", "ig": "Igbo"
        }
        return language_map.get(language_code.lower(), "English")
    
    def _get_score_label(self, category: str, score: int) -> str:
        """Generate categorical labels for score breakdown display"""
        if category == 'geographic':
            if score >= 35: return "PERFECT"
            elif score >= 20: return "PARTIAL"
            elif score > 0: return "WEAK"
            else: return "NO MATCH"
        elif category == 'sector':
            if score >= 25: return "PERFECT"
            elif score >= 15: return "GOOD"
            else: return "WEAK"
        elif category == 'amount_fit':
            if score >= 18: return "PERFECT"
            elif score >= 12: return "GOOD"
            else: return "OKAY"
        elif category == 'stage':
            if score >= 8: return "GOOD"
            else: return "OKAY"
        return "N/A"
    
    @retry_on_error(max_retries=1, delay=0.5)
    def generate_match_advice(
        self, 
        company_name: str,
        company_sector: str,
        company_country: str,
        funding_need_usd: float,
        grant_name: str,
        grant_institution: str,
        grant_country: str,
        grant_sectors: str,
        grant_amount: float,
        match_score: float,
        score_breakdown: Dict,
        language: str = "en"
    ) -> Optional[str]:
        """
        Generate strategic advisory with hybrid AI + fallback approach
        STRATEGY: High quality threshold forces consistent fallback usage
        Language-aware: Responds in user's preferred language with unique match analysis
        """
        # Get score labels for prompt
        geo_score = score_breakdown.get('geographic', 0)
        sec_score = score_breakdown.get('sector', 0)
        amt_score = score_breakdown.get('amount_fit', 0)
        stg_score = score_breakdown.get('stage', 0)
        
        geo_label = self._get_score_label('geographic', geo_score)
        sec_label = self._get_score_label('sector', sec_score)
        amt_label = self._get_score_label('amount_fit', amt_score)
        stg_label = self._get_score_label('stage', stg_score)
        
        # ✅ STRATEGIC DECISION: Try AI first, but use high quality bar
        if self.enabled:
            # Unique Match Analysis Conversational Prompt
            prompt = f"""You are a friendly business advisor explaining a specific funding opportunity to {company_name}. Focus on the UNIQUE aspects of THIS match - not just the overall score.

IMPORTANT: Write in {self._get_language_name(language)} language.

ABOUT THE BUSINESS:
{company_name} does {company_sector} work in {company_country} and needs ${funding_need_usd:,.0f}.

THIS SPECIFIC OPPORTUNITY:
{grant_name} from {grant_institution} ({grant_country}) offers ${grant_amount:,.0f} for {grant_sectors} businesses.

THE MATCH BREAKDOWN:
Total: {match_score}/100
- Location: {geo_score}/40 → {geo_label}
- Industry: {sec_score}/30 → {sec_label}
- Money: {amt_score}/20 → {amt_label}
- Stage: {stg_score}/10 → {stg_label}

Write 4 natural paragraphs. DON'T start by mentioning the overall score. Instead, START with the most interesting or surprising aspect of THIS specific match. What makes THIS opportunity different from others?

PARAGRAPH 1:
Look at the breakdown above. What's the STORY here? Is it "perfect location but wrong industry"? "Great industry match but you're in the wrong country"? "Everything aligns except the money"? Lead with whatever makes THIS match unique. Don't say "Your score is X/100" first - say something about the actual situation, THEN mention the score if relevant.

PARAGRAPH 2:
Focus on whatever scored HIGHEST in the breakdown. Don't list all strengths generically. Pick the TOP strength and explain why it matters FOR THIS SPECIFIC GRANT and THIS SPECIFIC COMPANY. What does {grant_institution} care most about? How does {company_name}'s situation match that? Be concrete about THIS situation, not general advice.

PARAGRAPH 3:
Look at the LOWEST score. Explain what that specific gap means for THIS application. If geography is 0, the advice is completely different than if sector is 10. Don't use generic phrases - address the specific barrier. What would it take to overcome THIS particular weakness with THIS particular funder?

PARAGRAPH 4:
Based on the SPECIFIC pattern of scores (not just the total), what's the strategy? A 60/100 from (40 geo + 10 sector + 10 money) requires TOTALLY different advice than a 60/100 from (0 geo + 30 sector + 20 money + 10 stage). Tailor the game plan to THIS unique situation.

ANTI-REPETITION RULES:
- NEVER start with "Let's be realistic/honest about this [score]..."
- NEVER use the phrase "You're not just asking for money..."
- NEVER say "This isn't about faking anything..."
- NEVER end with "You've got a real shot at this..."
- DO start each recommendation differently based on what's most notable about THAT match
- DO use completely different language for matches with the same total but different breakdowns
- DO let the specific numbers (not just the total) drive what you say

EXAMPLES OF GOOD OPENINGS (use these as inspiration, don't copy):
- "The interesting thing about {grant_name} is..."
- "{grant_institution} is looking for exactly what you have in [specific area]..."
- "Here's the challenge with this one: [specific gap]..."
- "You're going to love this - [specific strength]..."
- "This match has an unusual pattern: [describe breakdown]..."

Write like you're analyzing THIS specific situation, not filling in a template based on score ranges.

Remember: Write everything in {self._get_language_name(language)} language."""

            try:
                logger.info(f"🤖 Attempting AI generation #{self.generation_count + 1}: {company_name} (Language: {language})")
                
                # Rate limiting protection
                if self.generation_count > 0:
                    time.sleep(0.4)
                
                # Enhanced config for natural variation while maintaining quality
                generation_config = genai.types.GenerationConfig(
                    max_output_tokens=1200,
                    temperature=0.85,  # Higher for unique analysis
                    top_p=0.95,
                    candidate_count=1
                )
                
                response = self.model.generate_content(prompt, generation_config=generation_config)
                self.generation_count += 1
                
                advice = self._extract_text_from_response(response)
                
                if advice:
                    length = len(advice)
                    logger.info(f"📊 AI response: {length} chars")
                    
                    # ✅ THRESHOLD: Balanced for conversational style while maintaining quality
                    if length >= 700 and advice.strip()[-1] in ['.', '!', '?', '。', '！', '？']:
                        logger.info(f"✅ High-quality AI response accepted ({length} chars)")
                        return advice.strip()
                    else:
                        logger.info(f"⚠️ AI response insufficient ({length} chars) - using optimized fallback")
                        # Fall through to fallback
                else:
                    logger.info("⚠️ Empty AI response - using optimized fallback")
                    # Fall through to fallback
                    
            except Exception as e:
                logger.info(f"⚠️ AI generation failed - using optimized fallback: {str(e)[:50]}")
                # Fall through to fallback
        
        # ✅ PRIMARY QUALITY SOURCE: Enhanced deterministic fallback with unique match analysis
        return self._generate_unique_match_fallback(
            company_name, company_sector, company_country, grant_country,
            funding_need_usd, grant_name, grant_institution, grant_sectors,
            grant_amount, match_score, score_breakdown, language  # ✅ FIXED: Added grant_amount
        )
    
    def _generate_unique_match_fallback(
        self, 
        company_name: str, 
        company_sector: str, 
        company_country: str,
        grant_country: str,
        funding_need_usd: float, 
        grant_name: str, 
        grant_institution: str,
        grant_sectors: str,
        grant_amount: float,  # ✅ FIXED: Added missing parameter
        match_score: float, 
        score_breakdown: Dict,
        language: str = "en"
    ) -> str:
        """
        Enhanced conversational fallback focused on unique match characteristics
        OPTIMIZED: Analyzes score patterns, not just totals with natural storytelling
        Language-aware: Returns advice in specified language (English fallback for now)
        """
        # Extract scores
        geo = score_breakdown.get('geographic', 0)
        sec = score_breakdown.get('sector', 0)
        amt = score_breakdown.get('amount_fit', 0)
        stg = score_breakdown.get('stage', 0)
        
        # Identify highest and lowest scoring areas for targeted advice
        score_items = [
            ('geographic', geo, 'location'),
            ('sector', sec, 'industry'),
            ('amount_fit', amt, 'funding size'),
            ('stage', stg, 'business stage')
        ]
        score_items_sorted = sorted(score_items, key=lambda x: x[1], reverse=True)
        highest_area = score_items_sorted[0]
        lowest_area = score_items_sorted[-1]
        
        # Generate unique narrative hook based on score pattern
        hook_variations = []
        
        if geo >= 35 and sec >= 25:
            hook_variations = [
                f"What jumps out about {grant_name} is how perfectly aligned you are - both your {company_country} location and {company_sector} focus hit exactly what {grant_institution} prioritizes",
                f"This is one of those rare situations where {grant_institution} seems designed for businesses exactly like {company_name} - the geography and industry alignment is remarkable",
                f"The standout feature here is the double advantage: you're in {company_country} where they want to invest, doing {company_sector} work which is their core focus"
            ]
        elif geo >= 35 and sec < 15:
            hook_variations = [
                f"Here's the interesting twist with {grant_name}: your {company_country} location is perfect for them, but your {company_sector} work sits outside their usual {grant_sectors} comfort zone",
                f"This opportunity has a fascinating dynamic - {grant_institution} clearly wants to support {company_country}, but they'll need convincing about the {company_sector} angle",
                f"The story here is geographic alignment versus sector stretch: you're exactly where they want to invest, but not quite doing what they typically fund"
            ]
        elif geo < 20 and sec >= 25:
            hook_variations = [
                f"What makes {grant_name} intriguing is that you have exactly the {company_sector} expertise they're seeking, but the {company_country} to {grant_country} geographic gap creates an interesting challenge",
                f"This match has a compelling contradiction: {grant_institution} prioritizes {company_sector} work like yours, but they typically focus on {grant_country} rather than {company_country}",
                f"The unique aspect of this opportunity is strong sector alignment despite geographic distance - you do exactly what they fund, just not where they usually fund it"
            ]
        elif amt >= 18 and match_score < 75:
            hook_variations = [
                f"The curious thing about {grant_name} is that your ${funding_need_usd:,.0f} funding need fits their ${grant_amount:,.0f} program perfectly, but other factors complicate the match",
                f"This opportunity presents an interesting puzzle: the money side aligns beautifully, but the overall fit requires more creative positioning",
                f"What's notable here is the financial harmony - your funding request matches their grant size well - while other dimensions need more work"
            ]
        else:
            hook_variations = [
                f"The pattern with {grant_name} is more nuanced than most opportunities - you have clear strengths in {highest_area[2]}, but the overall picture requires strategic thinking",
                f"This match tells an interesting story when you look beyond the total score - your {highest_area[2]} strength creates opportunity, but success depends on addressing other gaps",
                f"What's distinctive about this {grant_institution} opportunity is how your {highest_area[2]} advantage could overcome challenges in other areas"
            ]
        
        # Select hook based on company name hash for consistency
        selected_hook = hook_variations[hash(company_name) % len(hook_variations)]
        
        # Build strength explanation with specificity
        strength_explanations = {
            'geographic': {
                'high': f"Your {company_country} base is your strongest asset here. {grant_institution} specifically targets this region, which means you're competing with other local businesses rather than trying to justify why distance doesn't matter. They've already decided {company_country} is where they want impact - you just need to show you're the right local partner to deliver it",
                'medium': f"Being in {company_country} gives you regional credibility that {grant_institution} values. While you're not in their primary target area, you're close enough that reviewers will see geographic logic rather than geographic stretch. Frame this as regional expertise rather than trying to overcome distance"
            },
            'sector': {
                'high': f"Your {company_sector} focus is precisely what {grant_institution} prioritizes. They've already decided this sector deserves funding - you don't need to convince them it matters. Instead, show why {company_name} specifically represents the best {company_sector} investment opportunity in this funding cycle",
                'medium': f"The {company_sector} work you do overlaps meaningfully with their {grant_sectors} priorities. You're not perfectly aligned, but you're close enough that emphasizing the right aspects of your business will resonate with reviewers who understand this space"
            },
            'amount_fit': {
                'high': f"Your ${funding_need_usd:,.0f} request hits their funding sweet spot perfectly. This isn't too ambitious or too modest - it's exactly the scale {grant_institution} designed this program to support. Your budget immediately looks credible to reviewers familiar with realistic project costs",
                'medium': f"The funding amount you need falls within their reasonable range. While not perfectly aligned, it's close enough that a well-justified budget explanation will work. Focus on showing exactly what outcomes each dollar produces"
            },
            'stage': {
                'high': f"Your business maturity level matches exactly what they prefer to fund. You're established enough to manage funds responsibly but still growing enough to benefit significantly from their investment. This reduces their risk while maximizing their impact potential",
                'medium': f"Your operational stage fits within their comfort zone. You have enough track record to be credible but enough growth potential to justify their investment. This positions you as a reliable choice for reviewers"
            }
        }
        
        strength_level = 'high' if highest_area[1] >= (30 if highest_area[0] == 'geographic' else 20 if highest_area[0] == 'sector' else 15 if highest_area[0] == 'amount_fit' else 8) else 'medium'
        strength_detail = strength_explanations[highest_area[0]][strength_level]
        
        # Build weakness-specific actionable advice
        weakness_strategies = {
            'geographic': {
                'severe': f"The geographic barrier is significant since {grant_institution} focuses on {grant_country} and you're in {company_country}. You need concrete evidence of cross-border impact. This week, identify potential {grant_country} partners, document any existing connections to their region, or research how your success creates measurable benefits in their target area",
                'moderate': f"Location isn't your strongest point, but it's not fatal. Research {grant_institution}'s past funding patterns - if they've supported similar cross-regional projects, reference those precedents. If not, build a compelling case for why your {company_country} base actually enhances your ability to serve their {grant_country} priorities"
            },
            'sector': {
                'severe': f"The sector mismatch is substantial - your {company_sector} focus doesn't align closely with their {grant_sectors} priorities. You have three options: reframe your business to emphasize aspects that do connect, find genuine interdisciplinary bridges between your work and their focus, or honestly consider whether better-matched opportunities exist",
                'moderate': f"Industry alignment needs work but isn't impossible. Study {grant_institution}'s funded projects and identify which aspects of your {company_sector} business most closely mirror their priorities. Restructure your application to lead with those elements rather than presenting your full scope equally"
            },
            'amount_fit': {
                'severe': f"Your ${funding_need_usd:,.0f} request doesn't align well with their typical ${grant_amount:,.0f} grants. If asking for significantly more, prepare exceptional impact justifications. If asking for less, consider expanding project scope or explain why a smaller investment makes strategic sense for this particular initiative",
                'moderate': f"The funding size requires some justification but isn't prohibitive. Create budget scenarios showing flexibility - what could you accomplish at 75%, 100%, and 125% of your request? This demonstrates thoughtful planning and gives reviewers options"
            },
            'stage': {
                'severe': f"Business maturity concerns will require substantial documentation. Gather comprehensive evidence: audited financials, multi-year operational history, governance structures, team credentials, and risk management systems. Without this proof of stability, even strong scores elsewhere won't overcome maturity concerns",
                'moderate': f"Your business stage needs some reinforcement but isn't disqualifying. Compile a credibility portfolio: business registration, financial records from the past year, key team qualifications, and customer testimonials that demonstrate operational reliability"
            }
        }
        
        weakness_severity = 'severe' if lowest_area[1] <= (15 if lowest_area[0] == 'geographic' else 10 if lowest_area[0] == 'sector' else 8 if lowest_area[0] == 'amount_fit' else 4) else 'moderate'
        weakness_detail = weakness_strategies[lowest_area[0]][weakness_severity]
        
        # Generate strategy based on specific score pattern
        if match_score >= 85:
            if geo >= 35 and sec >= 25:
                strategy = f"With both location and industry strongly aligned, your strategy is 'Proven Partnership.' Position {company_name} as the obvious local choice - an established {company_sector} operator already embedded where {grant_institution} wants impact. Emphasize immediate deployment capability rather than needing to build credibility or infrastructure"
            else:
                strategy = f"At {match_score}/100, you're operating from strength. Focus on 'Excellence in Execution' - show superior operational quality, proven results, and risk mitigation that makes you the safer choice compared to other competitive applicants. Your high score means they like what you do; now prove you do it better than others"
        elif match_score >= 70:
            strategy = f"Your {match_score}/100 puts you in serious consideration territory. The strategy is 'Strategic Bridge Building' - actively connect your {highest_area[2]} strength to their core mission, then proactively address your {lowest_area[2]} gap with concrete mitigation plans. Don't assume they'll see the connections; make them explicit"
        else:
            strategy = f"At {match_score}/100, this requires 'Differentiation Through Innovation.' Since you don't fit their standard profile, position yourself as the strategic outlier that brings unique value to their portfolio. Acknowledge the unconventional fit while making a compelling case for why that's actually an advantage"
        
        # Varied closing based on match strength
        closing_options = [
            "Start mapping out your narrative this week while the opportunity details are fresh",
            "Begin gathering supporting evidence now - strong applications need time to develop properly",
            "Take the first step by outlining how your specific situation serves their mission"
        ]
        closing = closing_options[int(match_score) % 3]
        
        return f"""{selected_hook}. The {match_score}/100 breakdown reveals the real story: {geo}/40 on location, {sec}/30 on industry alignment, {amt}/20 on funding size, and {stg}/10 on business readiness. These specific numbers matter more than the total because they show exactly where you're competitive and where you'll face scrutiny.

{strength_detail}. This is your competitive advantage - the foundation everything else builds on. Make this strength the centerpiece of your application narrative, using it to establish credibility before addressing other dimensions.

{weakness_detail}. Reviewers will notice this gap, so your application must address it directly rather than hoping they focus only on strengths. The difference between funded and rejected applications often comes down to how convincingly you handle your weakest area.

{strategy}. Remember that {grant_institution} receives numerous {grant_name} applications - your job is demonstrating why funding {company_name}'s {company_sector} work in {company_country} advances their mission better than alternative investments. {closing}."""
    
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive AI service status for technical reporting"""
        return {
            "enabled": self.enabled,
            "model": self.model_name if self.enabled else None,
            "tier": self.tier,
            "generation_count": self.generation_count,
            "optimization_strategy": "Hybrid AI + Unique Match Pattern Analysis Fallback",
            "language_support": "Multi-language AI prompts with English fallback",
            "quality_assurance": [
                "700+ character minimum threshold (conversational style)",
                "Complete sentence validation", 
                "4-paragraph unique match analysis format",
                "Score pattern-based opening generation with multiple variations",
                "Highest/lowest dimension-specific advice with severity levels",
                "Anti-template language enforcement with hash-based consistency",
                "Multilingual punctuation support",
                "Language-aware response generation",
                "Natural storytelling approach with strategic depth"
            ],
            "api_key_configured": bool(self.api_key),
            "api_key_format_valid": self.api_key.startswith("AIza") if self.api_key else False,
            "limits": {
                "requests_per_minute": "1,000",
                "tokens_per_minute": "4,000,000", 
                "requests_per_day": "50,000"
            }
        }
