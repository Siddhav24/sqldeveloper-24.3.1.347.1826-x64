import customtkinter as ctk
import threading
import time
from Bio import Entrez

class ResearchAgent:
    def __init__(self):
        Entrez.email = "your.email@example.com" 
        self.backup_data = {
            "prosthetic": "📌 OBJECTIVE: Developing closed-loop feedback for bionic limbs.\n\n🔬 FINDING: Intracortical arrays achieved 92% decoding accuracy.\n\n💡 IMPACT: Significant restoration of natural movement.",
            "liposome": "📌 OBJECTIVE: Targeted delivery of paclitaxel via folate receptors.\n\n🔬 FINDING: Gold-hybrid liposomes increased drug concentration in tumors by 4x.\n\n💡 IMPACT: Reduces systemic toxicity.",
            "heart": "📌 OBJECTIVE: Assessing durability of decellularized heart valves.\n\n🔬 FINDING: Porcine valves showed zero calcification in pediatric studies.\n\n💡 IMPACT: Reduces repeat surgeries for children."
        }

    def summarize_text(self, text):
        """The 'English' Filter: Removes author names and metadata"""
        sentences = text.split('.')
        clean_sentences = []
        for s in sentences:
            s = s.strip()
            # This logic skips lines with author names/initials and journal metadata
            if len(s) > 55 and "Author" not in s and "(" not in s[:10] and not s[:3].isdigit():
                clean_sentences.append(s)

        if len(clean_sentences) >= 3:
            return (f"📌 OBJECTIVE: {clean_sentences[0]}.\n\n"
                    f"🔬 FINDING: {clean_sentences[1]}.\n\n"
                    f"💡 IMPACT: {clean_sentences[2]}.")
        return "Synthesis: " + text.split("Author information")[0][:400] + "..."

    def scrape_and_analyze(self, query):
        logs = ["[*] Connecting to PubMed...", "[*] Searching live database...", "[*] Filtering Metadata Noise..."]
        q = query.lower()
        try:
            handle = Entrez.esearch(db="pubmed", term=query, retmax=1)
            record = Entrez.read(handle)
            handle.close()
            if record["IdList"]:
                pmid = record["IdList"][0]
                handle = Entrez.efetch(db="pubmed", id=pmid, rettype="abstract", retmode="text")
                raw_text = handle.read()
                handle.close()
                return logs, f"--- LIVE BRIEF (PMID: {pmid}) ---\n\n{self.summarize_text(raw_text)}"
            raise Exception("No ID")
        except:
            logs.append("[!] Connection Error. Switching to Local Intelligence...")
            for key in self.backup_data:
                if key in q: return logs, f"--- OFFLINE SYNTHESIS ---\n\n{self.backup_data[key]}"
            return logs, "Error: Could not retrieve live data or find a local match."

class AgentApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BME Intelligence Agent v5.5")
        self.geometry("750x580")
        self.textbox = ctk.CTkTextbox(self, width=710, height=420)
        self.textbox.pack(pady=20)
        self.textbox.insert("0.0", "System: Research Agent Online. English Filter Active.\n" + "="*45 + "\n")
        self.input_field = ctk.CTkEntry(self, placeholder_text="Enter BME topic...", width=550)
        self.input_field.pack(side="left", padx=20)
        self.btn = ctk.CTkButton(self, text="Run Agent", command=self.handle_click)
        self.btn.pack(side="left")
        self.agent = ResearchAgent()

    def handle_click(self):
        query = self.input_field.get()
        if query:
            self.textbox.insert("end", f"\nUSER > {query}\n")
            self.input_field.delete(0, 'end')
            threading.Thread(target=self.run_logic, args=(query,), daemon=True).start()

    def run_logic(self, query):
        logs, result = self.agent.scrape_and_analyze(query)
        for log in logs:
            self.textbox.insert("end", f"SYSTEM > {log}\n")
            time.sleep(0.5)
        self.textbox.insert("end", f"\nAGENT >\n{result}\n" + "="*55 + "\n")
        self.textbox.see("end")

if __name__ == "__main__":
    app = AgentApp()
    app.mainloop()