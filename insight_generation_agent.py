"""
WebInsights Assistant - Insight Generation Agent

Questo modulo implementa l'Insight Generation Agent, responsabile dell'analisi
dei dati elaborati per generare insight significativi e comprensibili.
"""

import logging
from typing import Dict, List, Any, Optional
from google.adk.orchestration import Agent, AgentContext
from google.adk.orchestration.agent import AgentResponse

# Configurazione del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("InsightGenerationAgent")

class InsightGenerationAgent(Agent):
    """
    Insight Generation Agent è responsabile dell'analisi dei dati elaborati
    per generare insight significativi e comprensibili.
    
    Questo agente:
    1. Analizza i dati elaborati per identificare pattern e correlazioni
    2. Genera insight significativi in linguaggio naturale
    3. Identifica opportunità di miglioramento
    4. Traduce concetti tecnici in informazioni comprensibili
    """
    
    def __init__(self):
        """Inizializza l'Insight Generation Agent."""
        super().__init__()
        logger.info("Insight Generation Agent inizializzato")
        
    def process(self, context: AgentContext) -> AgentResponse:
        """
        Analizza i dati elaborati e genera insight significativi.
        
        Args:
            context: Contesto dell'agente contenente i dati elaborati
            
        Returns:
            AgentResponse: Risposta contenente gli insight generati
        """
        processed_data = context.get_request()
        logger.info(f"Generazione di insight dai dati elaborati: {type(processed_data)}")
        
        # Verifica che i dati siano nel formato atteso
        if not isinstance(processed_data, dict):
            return AgentResponse(
                response="Errore: i dati forniti non sono nel formato atteso",
                data={"error": "Invalid data format"}
            )
        
        # Genera insight
        insights = self._generate_insights(processed_data)
        
        return AgentResponse(
            response="Insight generati con successo",
            data=insights
        )
    
    def _generate_insights(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Genera insight significativi dai dati elaborati.
        
        Args:
            processed_data: Dati elaborati dal Data Processing Agent
            
        Returns:
            Dict: Insight generati in formato strutturato e in linguaggio naturale
        """
        insights = {
            "sommario": "",
            "punti_chiave": [],
            "opportunita": [],
            "consigli_pratici": []
        }
        
        # Estrai informazioni rilevanti dai dati elaborati
        metriche = processed_data.get("metriche_principali", {})
        tendenze = processed_data.get("tendenze", {})
        fonti_traffico = processed_data.get("fonti_traffico", {})
        dispositivi = processed_data.get("dispositivi", {})
        pagine = processed_data.get("pagine_principali", [])
        anomalie = processed_data.get("anomalie", [])
        
        # Genera sommario generale
        visitatori = metriche.get("visitatori_totali", 0)
        pageviews = metriche.get("visualizzazioni_pagina_totali", 0)
        pages_per_session = metriche.get("pagine_per_sessione", 0)
        
        insights["sommario"] = (
            f"Nel periodo analizzato, il sito ha ricevuto {visitatori} visitatori "
            f"che hanno visualizzato {pageviews} pagine, con una media di {pages_per_session} "
            f"pagine per sessione. "
        )
        
        # Aggiungi informazioni sulle tendenze
        if "visitatori" in tendenze:
            trend = tendenze["visitatori"]
            insights["sommario"] += (
                f"Il traffico è in {trend.get('direzione', '')} del {trend.get('percentuale', 0)}% "
                f"rispetto al periodo precedente. "
            )
        
        # Aggiungi informazione sulla fonte principale di traffico
        if "principale" in fonti_traffico:
            fonte_principale = fonti_traffico["principale"]
            insights["sommario"] += (
                f"La principale fonte di traffico è {fonte_principale.get('nome', '').replace('_', ' ').capitalize()} "
                f"({fonte_principale.get('percentuale', 0)}% del totale)."
            )
        
        # Genera punti chiave
        insights["punti_chiave"] = []
        
        # Punto chiave sulle fonti di traffico
        if fonti_traffico:
            # Rimuovi la chiave 'principale' per l'analisi delle fonti
            fonti_copy = {k: v for k, v in fonti_traffico.items() if k != "principale"}
            if fonti_copy:
                sorted_sources = sorted(
                    [(k, v.get("percentuale", 0)) for k, v in fonti_copy.items()],
                    key=lambda x: x[1],
                    reverse=True
                )
                
                sources_text = ", ".join(
                    f"{source.replace('_', ' ').capitalize()} ({percentage}%)"
                    for source, percentage in sorted_sources
                )
                
                insights["punti_chiave"].append(
                    f"Le principali fonti di traffico sono: {sources_text}."
                )
        
        # Punto chiave sui dispositivi
        if dispositivi:
            sorted_devices = sorted(
                [(k, v.get("percentuale", 0)) for k, v in dispositivi.items()],
                key=lambda x: x[1],
                reverse=True
            )
            
            devices_text = ", ".join(
                f"{device.capitalize()} ({percentage}%)"
                for device, percentage in sorted_devices
            )
            
            insights["punti_chiave"].append(
                f"I visitatori accedono al sito principalmente da: {devices_text}."
            )
        
        # Punto chiave sulle pagine più visitate
        if pagine:
            top_pages = pagine[:3]  # Prendi le prime 3 pagine
            pages_text = ", ".join(
                f"{page.get('nome', '')} ({page.get('visualizzazioni', 0)} visualizzazioni)"
                for page in top_pages
            )
            
            insights["punti_chiave"].append(
                f"Le pagine più visitate sono: {pages_text}."
            )
        
        # Punto chiave sulle anomalie
        if anomalie:
            anomalies_text = ", ".join(
                f"{anomaly.get('tipo', '')} del {anomaly.get('differenza_percentuale', 0)}% "
                f"il {anomaly.get('data', '')}"
                for anomaly in anomalie
            )
            
            insights["punti_chiave"].append(
                f"Sono state rilevate le seguenti anomalie: {anomalies_text}."
            )
        
        # Genera opportunità
        insights["opportunita"] = []
        
        # Opportunità basate sulle fonti di traffico
        if fonti_traffico:
            # Identifica fonti con bassa percentuale che potrebbero essere migliorate
            low_sources = [
                (k.replace('_', ' ').capitalize(), v.get("percentuale", 0))
                for k, v in fonti_traffico.items()
                if k != "principale" and v.get("percentuale", 0) < 15
            ]
            
            for source, percentage in low_sources:
                insights["opportunita"].append(
                    f"Potenziale di crescita dal canale {source} (attualmente solo {percentage}% del traffico)."
                )
        
        # Opportunità basate sui dispositivi
        if dispositivi and "mobile" in dispositivi:
            mobile_percentage = dispositivi["mobile"].get("percentuale", 0)
            if mobile_percentage < 30:
                insights["opportunita"].append(
                    f"Migliorare l'esperienza mobile potrebbe aumentare il traffico (attualmente solo {mobile_percentage}% da dispositivi mobili)."
                )
            elif mobile_percentage > 50:
                insights["opportunita"].append(
                    f"Con {mobile_percentage}% di traffico da mobile, ottimizzare ulteriormente l'esperienza su questi dispositivi potrebbe migliorare le conversioni."
                )
        
        # Genera consigli pratici
        insights["consigli_pratici"] = []
        
        # Consigli basati sulle metriche
        if pages_per_session < 2:
            insights["consigli_pratici"].append(
                "Migliorare i collegamenti interni tra le pagine per aumentare il numero di pagine visitate per sessione."
            )
        
        # Consigli basati sulle fonti di traffico
        if fonti_traffico and "organic" in fonti_traffico:
            organic_percentage = fonti_traffico["organic"].get("percentuale", 0)
            if organic_percentage < 20:
                insights["consigli_pratici"].append(
                    "Migliorare la SEO del sito per aumentare il traffico organico dai motori di ricerca."
                )
        
        if fonti_traffico and "social" in fonti_traffico:
            social_percentage = fonti_traffico["social"].get("percentuale", 0)
            if social_percentage < 10:
                insights["consigli_pratici"].append(
                    "Aumentare la presenza sui social media per incrementare il traffico da queste piattaforme."
                )
        
        # Consigli basati sulle pagine
        if pagine:
            # Trova la pagina con il tempo medio più basso
            lowest_time_page = min(pagine, key=lambda x: self._time_to_seconds(x.get("tempo_medio", "00:00:00")))
            if lowest_time_page:
                insights["consigli_pratici"].append(
                    f"Migliorare il contenuto della pagina '{lowest_time_page.get('nome', '')}' per aumentare il tempo di permanenza."
                )
        
        return insights
    
    def _time_to_seconds(self, time_str: str) -> int:
        """
        Converte una stringa di tempo nel formato HH:MM:SS in secondi.
        
        Args:
            time_str: Stringa di tempo nel formato HH:MM:SS
            
        Returns:
            int: Tempo convertito in secondi
        """
        try:
            parts = time_str.split(":")
            if len(parts) == 3:
                hours, minutes, seconds = map(int, parts)
                return hours * 3600 + minutes * 60 + seconds
            elif len(parts) == 2:
                minutes, seconds = map(int, parts)
                return minutes * 60 + seconds
            else:
                return int(parts[0])
        except (ValueError, IndexError):
            return 0


# Funzione di utilità per creare un'istanza dell'Insight Generation Agent
def create_insight_generation_agent() -> InsightGenerationAgent:
    """
    Crea e configura un'istanza dell'Insight Generation Agent.
    
    Returns:
        InsightGenerationAgent: Istanza configurata dell'Insight Generation Agent
    """
    agent = InsightGenerationAgent()
    logger.info("Insight Generation Agent creato e configurato")
    return agent


if __name__ == "__main__":
    # Test di base dell'Insight Generation Agent
    agent = create_insight_generation_agent()
    print("Insight Generation Agent inizializzato con successo")
