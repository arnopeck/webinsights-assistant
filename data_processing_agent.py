"""
WebInsights Assistant - Data Processing Agent

Questo modulo implementa il Data Processing Agent, responsabile dell'elaborazione
dei dati grezzi estratti da Google Analytics per renderli più comprensibili.
"""

import logging
from typing import Dict, List, Any, Optional
from google.adk.orchestration import Agent, AgentContext
from google.adk.orchestration.agent import AgentResponse

# Configurazione del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("DataProcessingAgent")

class DataProcessingAgent(Agent):
    """
    Data Processing Agent è responsabile dell'elaborazione dei dati grezzi
    estratti da Google Analytics.
    
    Questo agente:
    1. Pulisce i dati grezzi
    2. Calcola metriche derivate e KPI significativi
    3. Identifica tendenze e anomalie
    4. Prepara i dati per l'analisi successiva
    """
    
    def __init__(self):
        """Inizializza il Data Processing Agent."""
        super().__init__()
        logger.info("Data Processing Agent inizializzato")
        
    def process(self, context: AgentContext) -> AgentResponse:
        """
        Elabora i dati grezzi estratti da Google Analytics.
        
        Args:
            context: Contesto dell'agente contenente i dati da elaborare
            
        Returns:
            AgentResponse: Risposta contenente i dati elaborati
        """
        raw_data = context.get_request()
        logger.info(f"Elaborazione dei dati grezzi: {type(raw_data)}")
        
        # Verifica che i dati siano nel formato atteso
        if not isinstance(raw_data, dict):
            return AgentResponse(
                response="Errore: i dati forniti non sono nel formato atteso",
                data={"error": "Invalid data format"}
            )
        
        # Elabora i dati
        processed_data = self._process_data(raw_data)
        
        return AgentResponse(
            response="Dati elaborati con successo",
            data=processed_data
        )
    
    def _process_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Elabora i dati grezzi per renderli più comprensibili.
        
        Args:
            raw_data: Dati grezzi estratti da Google Analytics
            
        Returns:
            Dict: Dati elaborati con metriche derivate e insight
        """
        processed_data = {
            "report_info": {
                "title": raw_data.get("report_name", "Analisi del sito web"),
                "periodo": f"Dal {raw_data.get('start_date')} al {raw_data.get('end_date')}"
            },
            "metriche_principali": {},
            "tendenze": {},
            "confronti": {},
            "anomalie": []
        }
        
        # Estrai e semplifica le metriche principali
        if "metrics" in raw_data:
            metrics = raw_data["metrics"]
            processed_data["metriche_principali"] = {
                "visitatori_totali": metrics.get("visitors", {}).get("total", 0),
                "visualizzazioni_pagina_totali": metrics.get("pageviews", {}).get("total", 0),
                "pagine_per_sessione": metrics.get("pages_per_session", 0)
            }
            
            # Calcola tendenze (crescita/decrescita)
            if "visitors" in metrics and "daily" in metrics["visitors"]:
                daily_visitors = list(metrics["visitors"]["daily"].values())
                if len(daily_visitors) >= 2:
                    first_half = daily_visitors[:len(daily_visitors)//2]
                    second_half = daily_visitors[len(daily_visitors)//2:]
                    avg_first = sum(first_half) / len(first_half)
                    avg_second = sum(second_half) / len(second_half)
                    
                    if avg_first > 0:
                        growth_rate = ((avg_second - avg_first) / avg_first) * 100
                        trend_direction = "crescita" if growth_rate > 0 else "decrescita"
                        processed_data["tendenze"]["visitatori"] = {
                            "direzione": trend_direction,
                            "percentuale": round(abs(growth_rate), 2)
                        }
        
        # Semplifica le fonti di traffico
        if "traffic_sources" in raw_data:
            sources = raw_data["traffic_sources"]
            total_traffic = sum(sources.values())
            
            processed_data["fonti_traffico"] = {
                source: {
                    "valore": value,
                    "percentuale": round((value / total_traffic) * 100, 2) if total_traffic > 0 else 0
                }
                for source, value in sources.items()
            }
            
            # Identifica la fonte principale
            if sources:
                main_source = max(sources.items(), key=lambda x: x[1])
                processed_data["fonti_traffico"]["principale"] = {
                    "nome": main_source[0],
                    "percentuale": round((main_source[1] / total_traffic) * 100, 2) if total_traffic > 0 else 0
                }
        
        # Semplifica i dispositivi
        if "devices" in raw_data:
            devices = raw_data["devices"]
            total_devices = sum(devices.values())
            
            processed_data["dispositivi"] = {
                device: {
                    "valore": value,
                    "percentuale": round((value / total_devices) * 100, 2) if total_devices > 0 else 0
                }
                for device, value in devices.items()
            }
        
        # Semplifica le pagine più visitate
        if "top_pages" in raw_data:
            processed_data["pagine_principali"] = [
                {
                    "nome": self._simplify_page_path(page["path"]),
                    "percorso": page["path"],
                    "visualizzazioni": page["pageviews"],
                    "tempo_medio": page["avg_time"]
                }
                for page in raw_data["top_pages"]
            ]
        
        # Identifica possibili anomalie (esempio: picchi o cali improvvisi)
        if "metrics" in raw_data and "visitors" in raw_data["metrics"] and "daily" in raw_data["metrics"]["visitors"]:
            daily_data = raw_data["metrics"]["visitors"]["daily"]
            values = list(daily_data.values())
            dates = list(daily_data.keys())
            
            if len(values) >= 3:
                avg = sum(values) / len(values)
                std_dev = (sum((x - avg) ** 2 for x in values) / len(values)) ** 0.5
                
                for i, value in enumerate(values):
                    if abs(value - avg) > 2 * std_dev:  # Oltre 2 deviazioni standard
                        anomaly_type = "picco" if value > avg else "calo"
                        processed_data["anomalie"].append({
                            "tipo": anomaly_type,
                            "data": dates[i],
                            "valore": value,
                            "differenza_percentuale": round(abs((value - avg) / avg) * 100, 2)
                        })
        
        return processed_data
    
    def _simplify_page_path(self, path: str) -> str:
        """
        Semplifica il percorso della pagina per renderlo più leggibile.
        
        Args:
            path: Percorso URL della pagina
            
        Returns:
            str: Nome semplificato della pagina
        """
        if path == "/":
            return "Home Page"
        
        # Rimuovi slash iniziale e finale
        clean_path = path.strip("/")
        
        # Sostituisci trattini e underscore con spazi
        clean_path = clean_path.replace("-", " ").replace("_", " ")
        
        # Capitalizza ogni parola
        clean_path = " ".join(word.capitalize() for word in clean_path.split())
        
        return clean_path


# Funzione di utilità per creare un'istanza del Data Processing Agent
def create_data_processing_agent() -> DataProcessingAgent:
    """
    Crea e configura un'istanza del Data Processing Agent.
    
    Returns:
        DataProcessingAgent: Istanza configurata del Data Processing Agent
    """
    agent = DataProcessingAgent()
    logger.info("Data Processing Agent creato e configurato")
    return agent


if __name__ == "__main__":
    # Test di base del Data Processing Agent
    agent = create_data_processing_agent()
    print("Data Processing Agent inizializzato con successo")
