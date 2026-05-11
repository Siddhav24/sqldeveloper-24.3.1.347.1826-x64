🧬 BME PubMed Research Agent
A streamlined research assistant for Biomedical Engineers that transforms live PubMed data into clear Objectives, Findings, and Impacts.

🚀 Quick Start
1. Install Dependencies
Run the following command to install all required libraries:
pip install -r requirements.txt

If you are on a restricted or managed device:  
Use this instead:
pip install -r requirements.txt --break-system-packages

3. Launch the Agent
Start the interface with:
python agent.py

🕹️ How to Use
Launch: Run the command above to open the BME Research Agent window.

Search: Enter a biomedical keyword (e.g., stent, biocompatibility, metal) and click Search.

Analyze: The agent queries the live PubMed API, removes metadata noise, and generates a structured Live Research Brief.

Export: A file named Research_Brief_Export.txt is automatically created or updated with your results.

🛠️ Requirements
This project uses:

customtkinter — Modern GUI framework

biopython — PubMed API access

pandas & numpy — Data handling and processing

Developed for Biomedical Research Synthesis — 2026
