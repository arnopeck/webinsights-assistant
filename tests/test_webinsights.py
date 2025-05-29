"""
WebInsights Assistant - Test Suite

This script runs the full test suite for the WebInsights Assistant system.
Moved from src/ to tests/ for best practice.
"""

import logging
import os
import sys
import unittest
import asyncio
from datetime import datetime, timedelta

# Add the src directory to the path for module imports
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from orchestration_agent import create_orchestration_agent
from data_extraction_agent import create_data_extraction_agent
from data_processing_agent import create_data_processing_agent
from insight_generation_agent import create_insight_generation_agent
from visualization_agent import create_visualization_agent
from google_analytics_integration import create_google_analytics_integration
from webinsights_integration import create_webinsights_assistant

try:
    from google.adk import AgentContext
except ImportError:
    from adk_compatibility import AgentContext

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("WebInsightsTest")

class TestWebInsightsAssistant(unittest.TestCase):
    """Test suite for the WebInsights Assistant system."""

    def setUp(self):
        """
        Initialize resources for each test.
        Creates agent instances and sets up sample data for testing.
        """
        logger.info("Initializing test resources")
        self.orchestration_agent = create_orchestration_agent()
        self.data_extraction_agent = create_data_extraction_agent()
        self.data_processing_agent = create_data_processing_agent()
        self.insight_generation_agent = create_insight_generation_agent()
        self.visualization_agent = create_visualization_agent()
        self.ga_integration = create_google_analytics_integration()
        self.assistant = create_webinsights_assistant()
        self.sample_property_id = "GA4_PROPERTY_ID"
        self.sample_start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        self.sample_end_date = datetime.now().strftime("%Y-%m-%d")

    def test_orchestration_agent(self):
        """
        Test the Orchestration Agent's ability to register and process a request.
        """
        logger.info("Testing Orchestration Agent")
        self.assertIsNotNone(self.orchestration_agent)
        self.orchestration_agent.register_agent("test_agent", self.data_extraction_agent)
        state = {"request_data": "Test request", "timestamp": "2025-05-29T00:00:00"}
        result = asyncio.run(self.orchestration_agent.run(state))
        self.assertIsInstance(result, dict)
        self.assertIn("orchestration", result)

    def test_data_extraction_agent(self):
        """
        Test the Data Extraction Agent's ability to extract data from a simulated request.
        """
        logger.info("Testing Data Extraction Agent")
        self.assertIsNotNone(self.data_extraction_agent)
        state = {"request_data": {"property_id": self.sample_property_id}}
        result = asyncio.run(self.data_extraction_agent.run(state))
        self.assertIn("extracted_data", result)
        self.assertIn("metrics", result["extracted_data"])
        self.assertIn("dimensions", result["extracted_data"])

    def test_data_processing_agent(self):
        """
        Test the Data Processing Agent's ability to process extracted data.
        """
        logger.info("Testing Data Processing Agent")
        self.assertIsNotNone(self.data_processing_agent)
        extracted_data = {"metrics": {"users": 100}, "dimensions": {"date": ["2025-05-29"]}}
        state = {"extracted_data": extracted_data}
        result = asyncio.run(self.data_processing_agent.run(state))
        self.assertIn("processed_data", result)

    def test_insight_generation_agent(self):
        """
        Test the Insight Generation Agent's ability to generate insights from processed data.
        """
        logger.info("Testing Insight Generation Agent")
        self.assertIsNotNone(self.insight_generation_agent)
        processed_data = {"users": 100, "trend": "up"}
        state = {"processed_data": processed_data}
        result = asyncio.run(self.insight_generation_agent.run(state))
        self.assertIn("insights", result)

    def test_visualization_agent(self):
        """
        Test the Visualization Agent's ability to generate visualizations from processed data and insights.
        """
        logger.info("Testing Visualization Agent")
        self.assertIsNotNone(self.visualization_agent)
        processed_data = {"users": 100}
        insights = {"summary": "ok"}
        state = {"processed_data": processed_data, "insights": insights}
        result = asyncio.run(self.visualization_agent.run(state))
        self.assertIn("visualizations", result)

    def test_google_analytics_integration(self):
        """
        Test the Google Analytics integration for authentication and data extraction.
        """
        logger.info("Testing Google Analytics Integration")
        self.assertIsNotNone(self.ga_integration)
        auth_result = self.ga_integration.authenticate()
        self.assertTrue(auth_result)
        traffic_data = self.ga_integration.get_website_traffic(
            self.sample_property_id, self.sample_start_date, self.sample_end_date
        )
        self.assertIsNotNone(traffic_data)
        self.assertIn("report_name", traffic_data)
        self.assertIn("metrics", traffic_data)

    def test_webinsights_assistant(self):
        """
        Test the full workflow of the WebInsights Assistant, including authentication, analysis, and report generation.
        """
        logger.info("Testing WebInsights Assistant end-to-end")
        self.assertIsNotNone(self.assistant)
        auth_result = self.assistant.authenticate_google_analytics()
        self.assertTrue(auth_result)
        results = self.assistant.analyze_website_data(
            self.sample_property_id, self.sample_start_date, self.sample_end_date
        )
        self.assertIsNotNone(results)
        self.assertIn("raw_data", results)
        self.assertIn("processed_data", results)
        self.assertIn("insights", results)
        self.assertIn("visualizations", results)
        html_report = self.assistant.generate_collaborative_report(results, "html")
        self.assertIsNotNone(html_report)
        self.assertTrue(os.path.exists(html_report))
        json_report = self.assistant.generate_collaborative_report(results, "json")
        self.assertIsNotNone(json_report)
        self.assertTrue(os.path.exists(json_report))

    def test_end_to_end_workflow(self):
        """
        Test the complete workflow from data extraction to visualization using all agents in sequence.
        """
        logger.info("Testing end-to-end workflow")
        state = {"request_data": {"property_id": self.sample_property_id}}
        state = asyncio.run(self.data_extraction_agent.run(state))
        self.assertIn("extracted_data", state)
        state = asyncio.run(self.data_processing_agent.run(state))
        self.assertIn("processed_data", state)
        state = asyncio.run(self.insight_generation_agent.run(state))
        self.assertIn("insights", state)
        state = asyncio.run(self.visualization_agent.run(state))
        self.assertIn("visualizations", state)

    def tearDown(self):
        """
        Clean up resources after each test.
        Removes any generated report files.
        """
        logger.info("Cleaning up after tests")
        for file_path in ["webinsights_report.html", "webinsights_report.json"]:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    logger.info(f"Removed file: {file_path}")
                except Exception as e:
                    logger.warning(f"Error removing file {file_path}: {e}")

if __name__ == "__main__":
    unittest.main()
