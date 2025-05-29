"""
WebInsights Assistant - Main Application

Questo modulo implementa l'applicazione principale che coordina tutti gli agenti
del sistema WebInsights Assistant.
"""

import logging
from google.adk.orchestration import AgentApp
from .orchestration_agent import create_orchestration_agent

# Configurazione del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("WebInsightsApp")

class WebInsightsApp(AgentApp):
    """
    Applicazione principale del WebInsights Assistant che utilizza l'architettura ADK
    per orchestrare i diversi agenti specializzati.
    """
    
    def __init__(self):
        """Inizializza l'applicazione WebInsights Assistant."""
        super().__init__()
        logger.info("Inizializzazione dell'applicazione WebInsights Assistant")
        
        # Creazione e registrazione dell'Orchestration Agent
        self.orchestration_agent = create_orchestration_agent()
        self.register_agent("orchestration", self.orchestration_agent)
        
        # Nelle prossime iterazioni, qui verranno registrati gli altri agenti:
        # - Data Extraction Agent
        # - Data Processing Agent
        # - Insight Generation Agent
        # - Visualization Agent
        # - Recommendation Agent
        
        logger.info("Applicazione WebInsights Assistant inizializzata con successo")
    
    def run(self):
        """Esegue l'applicazione WebInsights Assistant."""
        logger.info("Avvio dell'applicazione WebInsights Assistant")
        # Qui implementeremo la logica di esecuzione dell'applicazione
        # Per ora, è solo un placeholder
        
        logger.info("Applicazione WebInsights Assistant in esecuzione")


def create_app() -> WebInsightsApp:
    """
    Crea e configura un'istanza dell'applicazione WebInsights Assistant.
    
    Returns:
        WebInsightsApp: Istanza configurata dell'applicazione
    """
    app = WebInsightsApp()
    logger.info("Applicazione WebInsights Assistant creata e configurata")
    return app


if __name__ == "__main__":
    # Avvio dell'applicazione
    app = create_app()
    app.run()
    print("WebInsights Assistant avviato con successo")
