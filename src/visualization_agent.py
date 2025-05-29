"""
WebInsights Assistant - Visualization Agent

Questo modulo implementa il Visualization Agent, responsabile della creazione
di visualizzazioni intuitive dei dati e degli insight generati.
"""

import logging
from typing import Dict, List, Any, Optional
import json
from google.adk.orchestration import Agent, AgentContext
from google.adk.orchestration.agent import AgentResponse

# Configurazione del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("VisualizationAgent")

class VisualizationAgent(Agent):
    """
    Visualization Agent è responsabile della creazione di visualizzazioni intuitive
    dei dati e degli insight generati.
    
    Questo agente:
    1. Crea grafici e dashboard interattive
    2. Genera report visivi comprensibili
    3. Adatta le visualizzazioni per diversi tipi di utenti
    4. Rende le informazioni facilmente comprensibili anche per utenti non tecnici
    """
    
    def __init__(self):
        """Inizializza il Visualization Agent."""
        super().__init__()
        logger.info("Visualization Agent inizializzato")
        
    def process(self, context: AgentContext) -> AgentResponse:
        """
        Crea visualizzazioni dai dati e dagli insight.
        
        Args:
            context: Contesto dell'agente contenente i dati e gli insight
            
        Returns:
            AgentResponse: Risposta contenente le visualizzazioni generate
        """
        input_data = context.get_request()
        logger.info(f"Creazione di visualizzazioni dai dati: {type(input_data)}")
        
        # Verifica che i dati siano nel formato atteso
        if not isinstance(input_data, dict):
            return AgentResponse(
                response="Errore: i dati forniti non sono nel formato atteso",
                data={"error": "Invalid data format"}
            )
        
        # Genera visualizzazioni
        visualizations = self._create_visualizations(input_data)
        
        return AgentResponse(
            response="Visualizzazioni create con successo",
            data=visualizations
        )
    
    def _create_visualizations(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea visualizzazioni dai dati e dagli insight.
        
        Args:
            input_data: Dati elaborati e insight generati
            
        Returns:
            Dict: Configurazioni per le visualizzazioni
        """
        # Estrai dati rilevanti
        processed_data = input_data.get("processed_data", {})
        insights = input_data.get("insights", {})
        
        # Inizializza il dizionario delle visualizzazioni
        visualizations = {
            "dashboard": {
                "title": "Dashboard Web Analytics",
                "description": "Panoramica delle performance del sito web",
                "charts": []
            },
            "report": {
                "sections": []
            }
        }
        
        # Aggiungi sezione di riepilogo al report
        if insights and "sommario" in insights:
            visualizations["report"]["sections"].append({
                "type": "summary",
                "title": "Riepilogo",
                "content": insights.get("sommario", "")
            })
        
        # Crea grafico per le metriche principali
        if processed_data and "metriche_principali" in processed_data:
            metriche = processed_data["metriche_principali"]
            
            # Grafico a barre per le metriche principali
            visualizations["dashboard"]["charts"].append({
                "type": "bar",
                "id": "main_metrics",
                "title": "Metriche Principali",
                "data": {
                    "labels": ["Visitatori", "Visualizzazioni Pagina"],
                    "datasets": [{
                        "label": "Valori",
                        "data": [
                            metriche.get("visitatori_totali", 0),
                            metriche.get("visualizzazioni_pagina_totali", 0)
                        ],
                        "backgroundColor": ["#4285F4", "#34A853"]
                    }]
                },
                "options": {
                    "responsive": True,
                    "maintainAspectRatio": False,
                    "scales": {
                        "y": {
                            "beginAtZero": True
                        }
                    }
                }
            })
            
            # Aggiungi sezione al report
            visualizations["report"]["sections"].append({
                "type": "metrics",
                "title": "Metriche Principali",
                "metrics": [
                    {
                        "name": "Visitatori Totali",
                        "value": metriche.get("visitatori_totali", 0),
                        "icon": "users"
                    },
                    {
                        "name": "Visualizzazioni Pagina",
                        "value": metriche.get("visualizzazioni_pagina_totali", 0),
                        "icon": "eye"
                    },
                    {
                        "name": "Pagine per Sessione",
                        "value": metriche.get("pagine_per_sessione", 0),
                        "icon": "file"
                    }
                ]
            })
        
        # Crea grafico per le tendenze dei visitatori
        if processed_data and "metrics" in processed_data.get("raw_data", {}):
            raw_metrics = processed_data.get("raw_data", {}).get("metrics", {})
            if "visitors" in raw_metrics and "daily" in raw_metrics["visitors"]:
                daily_visitors = raw_metrics["visitors"]["daily"]
                
                # Ordina i dati per data
                sorted_data = sorted(daily_visitors.items())
                dates = [item[0] for item in sorted_data]
                values = [item[1] for item in sorted_data]
                
                # Grafico a linee per le tendenze dei visitatori
                visualizations["dashboard"]["charts"].append({
                    "type": "line",
                    "id": "visitors_trend",
                    "title": "Tendenza Visitatori",
                    "data": {
                        "labels": dates,
                        "datasets": [{
                            "label": "Visitatori",
                            "data": values,
                            "borderColor": "#4285F4",
                            "backgroundColor": "rgba(66, 133, 244, 0.2)",
                            "tension": 0.1
                        }]
                    },
                    "options": {
                        "responsive": True,
                        "maintainAspectRatio": False,
                        "scales": {
                            "y": {
                                "beginAtZero": True
                            }
                        }
                    }
                })
        
        # Crea grafico per le fonti di traffico
        if processed_data and "fonti_traffico" in processed_data:
            fonti = processed_data["fonti_traffico"]
            # Rimuovi la chiave 'principale' per il grafico
            fonti_copy = {k: v for k, v in fonti.items() if k != "principale"}
            
            if fonti_copy:
                labels = [k.replace('_', ' ').capitalize() for k in fonti_copy.keys()]
                values = [v.get("percentuale", 0) for v in fonti_copy.values()]
                
                # Grafico a torta per le fonti di traffico
                visualizations["dashboard"]["charts"].append({
                    "type": "pie",
                    "id": "traffic_sources",
                    "title": "Fonti di Traffico",
                    "data": {
                        "labels": labels,
                        "datasets": [{
                            "data": values,
                            "backgroundColor": [
                                "#4285F4", "#34A853", "#FBBC05", "#EA4335", "#5F6368"
                            ]
                        }]
                    },
                    "options": {
                        "responsive": True,
                        "maintainAspectRatio": False
                    }
                })
                
                # Aggiungi sezione al report
                visualizations["report"]["sections"].append({
                    "type": "chart",
                    "title": "Fonti di Traffico",
                    "chartId": "traffic_sources"
                })
        
        # Crea grafico per i dispositivi
        if processed_data and "dispositivi" in processed_data:
            dispositivi = processed_data["dispositivi"]
            
            if dispositivi:
                labels = [k.capitalize() for k in dispositivi.keys()]
                values = [v.get("percentuale", 0) for v in dispositivi.values()]
                
                # Grafico a ciambella per i dispositivi
                visualizations["dashboard"]["charts"].append({
                    "type": "doughnut",
                    "id": "devices",
                    "title": "Dispositivi",
                    "data": {
                        "labels": labels,
                        "datasets": [{
                            "data": values,
                            "backgroundColor": ["#4285F4", "#34A853", "#FBBC05"]
                        }]
                    },
                    "options": {
                        "responsive": True,
                        "maintainAspectRatio": False
                    }
                })
                
                # Aggiungi sezione al report
                visualizations["report"]["sections"].append({
                    "type": "chart",
                    "title": "Dispositivi",
                    "chartId": "devices"
                })
        
        # Crea grafico per le pagine principali
        if processed_data and "pagine_principali" in processed_data:
            pagine = processed_data["pagine_principali"]
            
            if pagine:
                labels = [page.get("nome", "") for page in pagine]
                values = [page.get("visualizzazioni", 0) for page in pagine]
                
                # Grafico a barre orizzontali per le pagine principali
                visualizations["dashboard"]["charts"].append({
                    "type": "horizontalBar",
                    "id": "top_pages",
                    "title": "Pagine Più Visitate",
                    "data": {
                        "labels": labels,
                        "datasets": [{
                            "label": "Visualizzazioni",
                            "data": values,
                            "backgroundColor": "#4285F4"
                        }]
                    },
                    "options": {
                        "responsive": True,
                        "maintainAspectRatio": False,
                        "indexAxis": "y"
                    }
                })
                
                # Aggiungi sezione al report
                visualizations["report"]["sections"].append({
                    "type": "table",
                    "title": "Pagine Più Visitate",
                    "columns": ["Pagina", "Visualizzazioni", "Tempo Medio"],
                    "data": [
                        [
                            page.get("nome", ""),
                            page.get("visualizzazioni", 0),
                            page.get("tempo_medio", "00:00:00")
                        ]
                        for page in pagine
                    ]
                })
        
        # Aggiungi sezione di insight al report
        if insights and "punti_chiave" in insights:
            punti_chiave = insights["punti_chiave"]
            
            if punti_chiave:
                visualizations["report"]["sections"].append({
                    "type": "insights",
                    "title": "Punti Chiave",
                    "items": punti_chiave
                })
        
        # Aggiungi sezione di opportunità al report
        if insights and "opportunita" in insights:
            opportunita = insights["opportunita"]
            
            if opportunita:
                visualizations["report"]["sections"].append({
                    "type": "opportunities",
                    "title": "Opportunità",
                    "items": opportunita
                })
        
        # Aggiungi sezione di consigli pratici al report
        if insights and "consigli_pratici" in insights:
            consigli = insights["consigli_pratici"]
            
            if consigli:
                visualizations["report"]["sections"].append({
                    "type": "recommendations",
                    "title": "Consigli Pratici",
                    "items": consigli
                })
        
        return visualizations


# Funzione di utilità per creare un'istanza del Visualization Agent
def create_visualization_agent() -> VisualizationAgent:
    """
    Crea e configura un'istanza del Visualization Agent.
    
    Returns:
        VisualizationAgent: Istanza configurata del Visualization Agent
    """
    agent = VisualizationAgent()
    logger.info("Visualization Agent creato e configurato")
    return agent


if __name__ == "__main__":
    # Test di base del Visualization Agent
    agent = create_visualization_agent()
    print("Visualization Agent inizializzato con successo")
