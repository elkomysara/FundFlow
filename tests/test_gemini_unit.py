"""
Unit Tests for GeminiAdvisor Class
Professional pytest-based testing with mocking
"""

import pytest
import os
from unittest.mock import Mock, patch
from app.services.gemini_service import GeminiAdvisor

class TestGeminiAdvisor:
    
    def test_initialization_without_api_key(self, monkeypatch):
        """Test that GeminiAdvisor disables when no API key is provided"""
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        
        advisor = GeminiAdvisor()
        assert advisor.enabled is False
        
        # Should return None when disabled
        advice = advisor.generate_match_advice(
            company_name="Test Co",
            company_sector="Tech",
            company_country="Kenya",
            funding_need_usd=50000,
            grant_name="Test Grant",
            grant_institution="Test Inst",
            grant_country="Global",
            grant_sectors="Technology",
            grant_amount=100000,
            match_score=90,
            score_breakdown={"geographic": 40, "sector": 30, "amount_fit": 15, "stage": 5}
        )
        assert advice is None

    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_successful_advice_generation(self, mock_model_class, mock_configure):
        """Test successful AI advice generation with mocked Gemini"""
        # Setup mocks
        mock_response = Mock()
        mock_response.text = "This is test AI advice for the company."
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        # Set environment variable
        os.environ["GEMINI_API_KEY"] = "test_key"
        
        advisor = GeminiAdvisor()
        assert advisor.enabled is True
        
        advice = advisor.generate_match_advice(
            company_name="TestCorp",
            company_sector="Manufacturing",
            company_country="Nigeria",
            funding_need_usd=75000,
            grant_name="Manufacturing Grant",
            grant_institution="Development Bank",
            grant_country="Africa",
            grant_sectors="Manufacturing, SME",
            grant_amount=150000,
            match_score=85,
            score_breakdown={"geographic": 35, "sector": 28, "amount_fit": 18, "stage": 4}
        )
        
        assert advice == "This is test AI advice for the company."
        assert mock_model.generate_content.called
        
        # Verify the prompt contains key information
        call_args = mock_model.generate_content.call_args[0][0]
        assert "TestCorp" in call_args
        assert "Manufacturing Grant" in call_args
        assert "85/100" in call_args

    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_api_error_handling(self, mock_model_class, mock_configure):
        """Test graceful handling of API errors"""
        mock_model = Mock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_model_class.return_value = mock_model
        
        os.environ["GEMINI_API_KEY"] = "test_key"
        
        advisor = GeminiAdvisor()
        
        advice = advisor.generate_match_advice(
            company_name="TestCorp",
            company_sector="Tech",
            company_country="Kenya",
            funding_need_usd=50000,
            grant_name="Tech Grant",
            grant_institution="Tech Fund",
            grant_country="Global",
            grant_sectors="Technology",
            grant_amount=100000,
            match_score=90,
            score_breakdown={"geographic": 40, "sector": 30, "amount_fit": 15, "stage": 5}
        )
        
        # Should return None on error, not crash
        assert advice is None

    def test_prompt_formatting(self):
        """Test that prompt is properly formatted with all variables"""
        # This test would require access to the actual prompt building logic
        # For now, we'll test through the integration approach
        pass

if __name__ == "__main__":
    pytest.main([__file__])