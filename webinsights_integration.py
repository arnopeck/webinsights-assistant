"""
WebInsights Assistant - Main Application Integration

Questo modulo integra tutti gli agenti e le componenti del sistema WebInsights Assistant
per fornire un'esperienza completa e collaborativa.
"""

import logging
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

from google.adk.orchestration import AgentApp
from src.orchestration_agent import create_orchestration_agent
from src.data_extraction_agent import create_data_extraction_agent
from src.data_processing_agent import create_data_processing_agent
from src.insight_generation_agent import create_insight_generation_agent
from src.visualization_agent import create_visualization_agent
from src.google_analytics_integration import create_google_analytics_integration

# Configurazione del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("WebInsightsIntegration")

class WebInsightsAssistant:
    """
    Classe principale che integra tutti gli agenti e le componenti del sistema
    WebInsights Assistant.
    
    Questa classe:
    1. Inizializza e configura tutti gli agenti
    2. Gestisce il flusso di lavoro tra gli agenti
    3. Fornisce un'interfaccia unificata per l'interazione con il sistema
    4. Coordina l'estrazione, l'elaborazione e la visualizzazione dei dati
    """
    
    def __init__(self, ga_credentials_path: Optional[str] = None):
        """
        Inizializza il WebInsights Assistant.
        
        Args:
            ga_credentials_path: Percorso del file di credenziali per Google Analytics
        """
        logger.info("Inizializzazione di WebInsights Assistant")
        
        # Inizializza l'integrazione con Google Analytics
        self.ga_integration = create_google_analytics_integration(ga_credentials_path)
        
        # Inizializza l'applicazione ADK
        self.app = AgentApp()
        
        # Inizializza gli agenti
        self.orchestration_agent = create_orchestration_agent()
        self.data_extraction_agent = create_data_extraction_agent()
        self.data_processing_agent = create_data_processing_agent()
        self.insight_generation_agent = create_insight_generation_agent()
        self.visualization_agent = create_visualization_agent()
        
        # Registra gli agenti nell'applicazione
        self.app.register_agent("orchestration", self.orchestration_agent)
        self.app.register_agent("data_extraction", self.data_extraction_agent)
        self.app.register_agent("data_processing", self.data_processing_agent)
        self.app.register_agent("insight_generation", self.insight_generation_agent)
        self.app.register_agent("visualization", self.visualization_agent)
        
        # Registra gli agenti nell'Orchestration Agent
        self.orchestration_agent.register_agent("data_extraction", self.data_extraction_agent)
        self.orchestration_agent.register_agent("data_processing", self.data_processing_agent)
        self.orchestration_agent.register_agent("insight_generation", self.insight_generation_agent)
        self.orchestration_agent.register_agent("visualization", self.visualization_agent)
        
        logger.info("WebInsights Assistant inizializzato con successo")
        
    def authenticate_google_analytics(self) -> bool:
        """
        Autentica con Google Analytics.
        
        Returns:
            bool: True se l'autenticazione ha avuto successo, False altrimenti
        """
        return self.ga_integration.authenticate()
        
    def analyze_website_data(self, property_id: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Analizza i dati del sito web per il periodo specificato.
        
        Args:
            property_id: ID della proprietà Google Analytics
            start_date: Data di inizio nel formato YYYY-MM-DD (default: 7 giorni fa)
            end_date: Data di fine nel formato YYYY-MM-DD (default: oggi)
            
        Returns:
            Dict: Risultati dell'analisi
        """
        logger.info(f"Avvio analisi per la proprietà {property_id}")
        
        # Imposta date predefinite se non specificate
        if not start_date:
            start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
            
        # Estrai dati da Google Analytics
        traffic_data = self.ga_integration.get_website_traffic(property_id, start_date, end_date)
        traffic_sources = self.ga_integration.get_traffic_sources(property_id, start_date, end_date)
        top_pages = self.ga_integration.get_top_pages(property_id, start_date, end_date)
        devices = self.ga_integration.get_device_breakdown(property_id, start_date, end_date)
        
        # Combina i dati in un unico oggetto
        raw_data = {
            "report_name": traffic_data["report_name"],
            "start_date": start_date,
            "end_date": end_date,
            "metrics": traffic_data["metrics"],
            "traffic_sources": traffic_sources,
            "top_pages": top_pages,
            "devices": devices
        }
        
        # Esegui il flusso di lavoro completo
        return self._execute_workflow(raw_data)
        
    def _execute_workflow(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Esegue il flusso di lavoro completo attraverso tutti gli agenti.
        
        Args:
            raw_data: Dati grezzi estratti da Google Analytics
            
        Returns:
            Dict: Risultati completi dell'analisi
        """
        logger.info("Esecuzione del flusso di lavoro completo")
        
        # Fase 1: Elaborazione dei dati
        processed_data = self.data_processing_agent.process(AgentContext(raw_data)).data
        processed_data["raw_data"] = raw_data  # Mantieni i dati grezzi per riferimento
        
        # Fase 2: Generazione di insight
        insights = self.insight_generation_agent.process(AgentContext(processed_data)).data
        
        # Fase 3: Creazione di visualizzazioni
        visualization_input = {
            "processed_data": processed_data,
            "insights": insights
        }
        visualizations = self.visualization_agent.process(AgentContext(visualization_input)).data
        
        # Combina tutti i risultati
        results = {
            "raw_data": raw_data,
            "processed_data": processed_data,
            "insights": insights,
            "visualizations": visualizations
        }
        
        logger.info("Flusso di lavoro completato con successo")
        return results
        
    def generate_collaborative_report(self, analysis_results: Dict[str, Any], output_format: str = "html") -> str:
        """
        Genera un report collaborativo dai risultati dell'analisi.
        
        Args:
            analysis_results: Risultati dell'analisi
            output_format: Formato di output del report (html, pdf, json)
            
        Returns:
            str: Percorso del file di report generato
        """
        logger.info(f"Generazione report in formato {output_format}")
        
        # Estrai le visualizzazioni e gli insight
        visualizations = analysis_results.get("visualizations", {})
        insights = analysis_results.get("insights", {})
        
        # Genera il report in base al formato richiesto
        if output_format == "html":
            return self._generate_html_report(visualizations, insights)
        elif output_format == "json":
            return self._generate_json_report(analysis_results)
        else:
            logger.warning(f"Formato {output_format} non supportato, generazione report HTML")
            return self._generate_html_report(visualizations, insights)
            
    def _generate_html_report(self, visualizations: Dict[str, Any], insights: Dict[str, Any]) -> str:
        """
        Genera un report HTML dai risultati dell'analisi.
        
        Args:
            visualizations: Configurazioni delle visualizzazioni
            insights: Insight generati
            
        Returns:
            str: Percorso del file HTML generato
        """
        # In una implementazione reale, qui genereremmo un file HTML completo
        # Per ora, creiamo un file di esempio
        
        report_path = os.path.join(os.getcwd(), "webinsights_report.html")
        
        # Contenuto di esempio del report
        report_content = f"""
        <!DOCTYPE html>
        <html lang="it">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>WebInsights Assistant - Report</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; color: #333; }}
                .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4285F4; color: white; padding: 20px; text-align: center; }}
                .summary {{ background-color: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 5px; }}
                .metrics {{ display: flex; justify-content: space-between; margin: 20px 0; }}
                .metric-card {{ background-color: white; padding: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); flex: 1; margin: 0 10px; text-align: center; }}
                .chart-container {{ background-color: white; padding: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin: 20px 0; }}
                .insights {{ background-color: #e8f0fe; padding: 20px; border-radius: 5px; margin: 20px 0; }}
                .opportunities {{ background-color: #fef8e8; padding: 20px; border-radius: 5px; margin: 20px 0; }}
                .recommendations {{ background-color: #e6f4ea; padding: 20px; border-radius: 5px; margin: 20px 0; }}
                h1, h2, h3 {{ color: #4285F4; }}
                ul {{ padding-left: 20px; }}
                li {{ margin-bottom: 10px; }}
                .footer {{ text-align: center; margin-top: 40px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>WebInsights Assistant</h1>
                <p>Report generato il {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
            </div>
            
            <div class="container">
                <div class="summary">
                    <h2>Riepilogo</h2>
                    <p>{insights.get("sommario", "Nessun riepilogo disponibile.")}</p>
                </div>
                
                <div class="metrics">
                    <div class="metric-card">
                        <h3>Visitatori</h3>
                        <p class="metric-value">1,234</p>
                    </div>
                    <div class="metric-card">
                        <h3>Visualizzazioni Pagina</h3>
                        <p class="metric-value">5,678</p>
                    </div>
                    <div class="metric-card">
                        <h3>Pagine per Sessione</h3>
                        <p class="metric-value">4.6</p>
                    </div>
                </div>
                
                <div class="chart-container">
                    <h2>Tendenza Visitatori</h2>
                    <canvas id="visitors-chart"></canvas>
                </div>
                
                <div class="chart-container">
                    <h2>Fonti di Traffico</h2>
                    <canvas id="sources-chart"></canvas>
                </div>
                
                <div class="chart-container">
                    <h2>Dispositivi</h2>
                    <canvas id="devices-chart"></canvas>
                </div>
                
                <div class="insights">
                    <h2>Punti Chiave</h2>
                    <ul>
                        {"".join([f"<li>{item}</li>" for item in insights.get("punti_chiave", [])])}
                    </ul>
                </div>
                
                <div class="opportunities">
                    <h2>Opportunità</h2>
                    <ul>
                        {"".join([f"<li>{item}</li>" for item in insights.get("opportunita", [])])}
                    </ul>
                </div>
                
                <div class="recommendations">
                    <h2>Consigli Pratici</h2>
                    <ul>
                        {"".join([f"<li>{item}</li>" for item in insights.get("consigli_pratici", [])])}
                    </ul>
                </div>
                
                <div class="footer">
                    <p>Generato da WebInsights Assistant - Un progetto per l'ADK Hackathon di Google Cloud</p>
                </div>
            </div>
            
            <script>
                // Codice JavaScript per inizializzare i grafici
                // In una implementazione reale, qui utilizzeremmo i dati effettivi
                
                // Grafico tendenza visitatori
                const visitorsCtx = document.getElementById('visitors-chart').getContext('2d');
                new Chart(visitorsCtx, {{
                    type: 'line',
                    data: {{
                        labels: ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom'],
                        datasets: [{{
                            label: 'Visitatori',
                            data: [120, 150, 180, 190, 210, 160, 140],
                            borderColor: '#4285F4',
                            backgroundColor: 'rgba(66, 133, 244, 0.2)',
                            tension: 0.1
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        scales: {{
                            y: {{
                                beginAtZero: true
                            }}
                        }}
                    }}
                }});
                
                // Grafico fonti di traffico
                const sourcesCtx = document.getElementById('sources-chart').getContext('2d');
                new Chart(sourcesCtx, {{
                    type: 'pie',
                    data: {{
                        labels: ['Diretto', 'Organico', 'Referral', 'Social', 'Email'],
                        datasets: [{{
                            data: [35, 25, 20, 15, 5],
                            backgroundColor: ['#4285F4', '#34A853', '#FBBC05', '#EA4335', '#5F6368']
                        }}]
                    }},
                    options: {{
                        responsive: true
                    }}
                }});
                
                // Grafico dispositivi
                const devicesCtx = document.getElementById('devices-chart').getContext('2d');
                new Chart(devicesCtx, {{
                    type: 'doughnut',
                    data: {{
                        labels: ['Desktop', 'Mobile', 'Tablet'],
                        datasets: [{{
                            data: [55, 35, 10],
                            backgroundColor: ['#4285F4', '#34A853', '#FBBC05']
                        }}]
                    }},
                    options: {{
                        responsive: true
                    }}
                }});
            </script>
        </body>
        </html>
        """
        
        # Scrivi il report su file
        with open(report_path, "w") as f:
            f.write(report_content)
            
        logger.info(f"Report HTML generato: {report_path}")
        return report_path
        
    def _generate_json_report(self, analysis_results: Dict[str, Any]) -> str:
  
(Content truncated due to size limit. Use line ranges to read in chunks)