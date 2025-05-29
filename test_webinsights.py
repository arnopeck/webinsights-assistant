"""
WebInsights Assistant - Test Suite

Questo script esegue una serie di test per verificare il corretto funzionamento
del sistema WebInsights Assistant.
"""

import logging
import os
import sys
import unittest
from datetime import datetime, timedelta

# Aggiungi la directory principale al path per l'importazione dei moduli
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestration_agent import create_orchestration_agent
from data_extraction_agent import create_data_extraction_agent
from data_processing_agent import create_data_processing_agent
from insight_generation_agent import create_insight_generation_agent
from visualization_agent import create_visualization_agent
from google_analytics_integration import create_google_analytics_integration
from webinsights_integration import create_webinsights_assistant

from google.adk.orchestration import AgentContext

# Configurazione del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("WebInsightsTest")

class TestWebInsightsAssistant(unittest.TestCase):
    """Test suite per il sistema WebInsights Assistant."""
    
    def setUp(self):
        """Inizializza le risorse necessarie per i test."""
        logger.info("Inizializzazione dei test")
        
        # Crea istanze degli agenti per i test
        self.orchestration_agent = create_orchestration_agent()
        self.data_extraction_agent = create_data_extraction_agent()
        self.data_processing_agent = create_data_processing_agent()
        self.insight_generation_agent = create_insight_generation_agent()
        self.visualization_agent = create_visualization_agent()
        
        # Crea istanza dell'integrazione Google Analytics
        self.ga_integration = create_google_analytics_integration()
        
        # Crea istanza del WebInsights Assistant
        self.assistant = create_webinsights_assistant()
        
        # Dati di esempio per i test
        self.sample_property_id = "GA4_PROPERTY_ID"
        self.sample_start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        self.sample_end_date = datetime.now().strftime("%Y-%m-%d")
        
    def test_orchestration_agent(self):
        """Testa il funzionamento dell'Orchestration Agent."""
        logger.info("Test dell'Orchestration Agent")
        
        # Verifica che l'agente sia stato creato correttamente
        self.assertIsNotNone(self.orchestration_agent)
        
        # Testa la registrazione degli agenti
        self.orchestration_agent.register_agent("test_agent", self.data_extraction_agent)
        
        # Testa la risposta dell'agente a una richiesta semplice
        response = self.orchestration_agent.process(AgentContext("Test request"))
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.response)
        
    def test_data_extraction_agent(self):
        """Testa il funzionamento del Data Extraction Agent."""
        logger.info("Test del Data Extraction Agent")
        
        # Verifica che l'agente sia stato creato correttamente
        self.assertIsNotNone(self.data_extraction_agent)
        
        # Testa la generazione di dati di esempio
        sample_data = self.data_extraction_agent._get_sample_data()
        self.assertIsNotNone(sample_data)
        self.assertIn("report_name", sample_data)
        self.assertIn("metrics", sample_data)
        
        # Testa la risposta dell'agente a una richiesta semplice
        response = self.data_extraction_agent.process(AgentContext("Test request"))
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.data)
        
    def test_data_processing_agent(self):
        """Testa il funzionamento del Data Processing Agent."""
        logger.info("Test del Data Processing Agent")
        
        # Verifica che l'agente sia stato creato correttamente
        self.assertIsNotNone(self.data_processing_agent)
        
        # Crea dati di esempio per il test
        sample_data = self.data_extraction_agent._get_sample_data()
        
        # Testa la risposta dell'agente con i dati di esempio
        response = self.data_processing_agent.process(AgentContext(sample_data))
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.data)
        
    def test_insight_generation_agent(self):
        """Testa il funzionamento dell'Insight Generation Agent."""
        logger.info("Test dell'Insight Generation Agent")
        
        # Verifica che l'agente sia stato creato correttamente
        self.assertIsNotNone(self.insight_generation_agent)
        
        # Crea dati elaborati di esempio per il test
        sample_data = self.data_extraction_agent._get_sample_data()
        processed_data = self.data_processing_agent.process(AgentContext(sample_data)).data
        
        # Testa la risposta dell'agente con i dati elaborati
        response = self.insight_generation_agent.process(AgentContext(processed_data))
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.data)
        
    def test_visualization_agent(self):
        """Testa il funzionamento del Visualization Agent."""
        logger.info("Test del Visualization Agent")
        
        # Verifica che l'agente sia stato creato correttamente
        self.assertIsNotNone(self.visualization_agent)
        
        # Crea dati e insight di esempio per il test
        sample_data = self.data_extraction_agent._get_sample_data()
        processed_data = self.data_processing_agent.process(AgentContext(sample_data)).data
        insights = self.insight_generation_agent.process(AgentContext(processed_data)).data
        
        # Prepara l'input per il Visualization Agent
        visualization_input = {
            "processed_data": processed_data,
            "insights": insights
        }
        
        # Testa la risposta dell'agente con i dati e gli insight
        response = self.visualization_agent.process(AgentContext(visualization_input))
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.data)
        
    def test_google_analytics_integration(self):
        """Testa l'integrazione con Google Analytics."""
        logger.info("Test dell'integrazione con Google Analytics")
        
        # Verifica che l'integrazione sia stata creata correttamente
        self.assertIsNotNone(self.ga_integration)
        
        # Testa l'autenticazione
        auth_result = self.ga_integration.authenticate()
        self.assertTrue(auth_result)
        
        # Testa l'estrazione dei dati
        traffic_data = self.ga_integration.get_website_traffic(
            self.sample_property_id, self.sample_start_date, self.sample_end_date
        )
        self.assertIsNotNone(traffic_data)
        self.assertIn("report_name", traffic_data)
        self.assertIn("metrics", traffic_data)
        
    def test_webinsights_assistant(self):
        """Testa il funzionamento completo del WebInsights Assistant."""
        logger.info("Test del WebInsights Assistant")
        
        # Verifica che l'assistente sia stato creato correttamente
        self.assertIsNotNone(self.assistant)
        
        # Testa l'autenticazione
        auth_result = self.assistant.authenticate_google_analytics()
        self.assertTrue(auth_result)
        
        # Testa l'analisi dei dati
        results = self.assistant.analyze_website_data(
            self.sample_property_id, self.sample_start_date, self.sample_end_date
        )
        self.assertIsNotNone(results)
        self.assertIn("raw_data", results)
        self.assertIn("processed_data", results)
        self.assertIn("insights", results)
        self.assertIn("visualizations", results)
        
        # Testa la generazione del report HTML
        html_report = self.assistant.generate_collaborative_report(results, "html")
        self.assertIsNotNone(html_report)
        self.assertTrue(os.path.exists(html_report))
        
        # Testa la generazione del report JSON
        json_report = self.assistant.generate_collaborative_report(results, "json")
        self.assertIsNotNone(json_report)
        self.assertTrue(os.path.exists(json_report))
        
    def test_end_to_end_workflow(self):
        """Testa il flusso di lavoro completo dall'estrazione alla visualizzazione."""
        logger.info("Test del flusso di lavoro completo")
        
        # Estrai dati di esempio
        sample_data = self.data_extraction_agent._get_sample_data()
        self.assertIsNotNone(sample_data)
        
        # Elabora i dati
        processed_data = self.data_processing_agent.process(AgentContext(sample_data)).data
        self.assertIsNotNone(processed_data)
        
        # Genera insight
        insights = self.insight_generation_agent.process(AgentContext(processed_data)).data
        self.assertIsNotNone(insights)
        
        # Crea visualizzazioni
        visualization_input = {
            "processed_data": processed_data,
            "insights": insights
        }
        visualizations = self.visualization_agent.process(AgentContext(visualization_input)).data
        self.assertIsNotNone(visualizations)
        
        # Verifica che il flusso completo funzioni
        self.assertIn("sommario", insights)
        self.assertIn("dashboard", visualizations)
        
    def tearDown(self):
        """Pulisce le risorse utilizzate dai test."""
        logger.info("Pulizia dopo i test")
        
        # Rimuovi eventuali file di report generati durante i test
        for file_path in ["webinsights_report.html", "webinsights_report.json"]:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    logger.info(f"File rimosso: {file_path}")
                except Exception as e:
                    logger.warning(f"Errore durante la rimozione del file {file_path}: {e}")

if __name__ == "__main__":
    unittest.main()
