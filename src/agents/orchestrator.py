from ..utils.logger import logger
from .data_agent import fetch_data
from .analysis_agent import generate_report
from .mail_agent import send_report

def run_pipeline():
    """Execute the complete automated reporting pipeline.

    This function orchestrates the entire reporting process by:
    1. Fetching data using the data agent
    2. Generating analysis report using the analysis agent
    3. Sending the report via email using the mail agent

    The pipeline uses three main components:
    - Data Agent: Retrieves data from the configured API
    - Analysis Agent: Processes data and generates report using LLM
    - Mail Agent: Distributes the report to configured recipients

    Raises:
        Any exceptions from the component agents are not caught here
        and will propagate up to the caller.
    """
    logger.info("=== Agentic pipeline started ===")
    #Gün verisi al.
    
    # data = fetch_data()
    data={
    "Dönen_Varlıklar": 12500000,
    "Kısa_Vadeli_Borçlar": 7200000,
    "Net_Dönem_Karı": 1850000,
    "Net_Satışlar": 15600000,
    "Ortalama_Ticari_Alacaklar": 3900000,
    "Toplam_Borçlar": 9600000,
    "Toplam_Varlıklar": 18400000,
    "Stok": 2800000
    }
    report = generate_report(data)
    send_report(report)
    logger.info("=== Agentic pipeline finished ===")
