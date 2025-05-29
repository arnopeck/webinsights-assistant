"""
WebInsights Assistant - Main Application

Questo script avvia l'applicazione WebInsights Assistant e fornisce
un'interfaccia di comando per interagire con il sistema.
"""

import argparse
import logging
import os
from datetime import datetime, timedelta

from .webinsights_integration import create_webinsights_assistant

# Configurazione del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("WebInsightsApp")

def main():
    """Funzione principale per l'avvio dell'applicazione WebInsights Assistant."""
    # Configura il parser degli argomenti
    parser = argparse.ArgumentParser(description="WebInsights Assistant - Analisi semplificata dei dati web")
    parser.add_argument("--property-id", type=str, default="GA4_PROPERTY_ID", help="ID della proprietà Google Analytics")
    parser.add_argument("--start-date", type=str, help="Data di inizio nel formato YYYY-MM-DD (default: 7 giorni fa)")
    parser.add_argument("--end-date", type=str, help="Data di fine nel formato YYYY-MM-DD (default: oggi)")
    parser.add_argument("--credentials", type=str, help="Percorso del file di credenziali per Google Analytics")
    parser.add_argument("--output-format", type=str, choices=["html", "json"], default="html", help="Formato di output del report")
    
    # Analizza gli argomenti
    args = parser.parse_args()

    # Richiedi interattivamente il property ID se non fornito
    if not args.property_id or args.property_id == "GA4_PROPERTY_ID":
        args.property_id = input("Inserisci il tuo Google Analytics Property ID (GA4): ").strip()
        if not args.property_id:
            logger.error("Property ID obbligatorio. Uscita.")
            return

    # Imposta date predefinite se non specificate
    if not args.start_date:
        args.start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    if not args.end_date:
        args.end_date = datetime.now().strftime("%Y-%m-%d")

    # Crea e configura l'assistente
    logger.info("Avvio di WebInsights Assistant")
    assistant = create_webinsights_assistant(args.credentials)

    # Autentica con Google Analytics
    if assistant.authenticate_google_analytics():
        logger.info("Autenticazione con Google Analytics completata con successo")
    else:
        logger.error("Errore durante l'autenticazione con Google Analytics")
        return

    # Analizza i dati
    logger.info(f"Analisi dei dati per la proprietà {args.property_id} dal {args.start_date} al {args.end_date}")
    results = assistant.analyze_website_data(args.property_id, args.start_date, args.end_date)

    # Genera il report
    logger.info(f"Generazione del report in formato {args.output_format}")
    report_path = assistant.generate_collaborative_report(results, args.output_format)

    logger.info(f"Report generato con successo: {report_path}")
    print(f"\nReport generato con successo: {report_path}")
    print(f"Apri il file nel tuo browser per visualizzare il report completo.")

if __name__ == "__main__":
    main()
