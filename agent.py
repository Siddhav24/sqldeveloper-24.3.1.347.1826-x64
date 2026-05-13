import tkinter as tk
from tkinter import messagebox, scrolledtext
import webbrowser
from Bio import Entrez
import re
from collections import Counter

# Set your email for PubMed API access
Entrez.email = "student@tcnj.edu"

class BMEAgent:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BME Research Agent v2.1")
        self.root.geometry("700x600")
        self.root.configure(bg="#f4f4f9")

        # Header
        tk.Label(self.root, text="BME RESEARCH AI", font=("Helvetica", 20, "bold"), bg="#f4f4f9", fg="#2c3e50").pack(pady=15)
        
        # Search Box
        tk.Label(self.root, text="Enter Research Topic:", font=("Arial", 10), bg="#f4f4f9").pack()
        self.entry = tk.Entry(self.root, width=55, font=("Arial", 12), bd=2)
        self.entry.pack(pady=10)
        self.entry.insert(0, "Biocompatible Stents")

        # Search Button
        self.btn = tk.Button(self.root, text="GENERATE SUMMARY & LINK", command=self.run_agent, bg="#3498db", fg="white", font=("Arial", 11, "bold"), padx=20, pady=5)
        self.btn.pack(pady=10)

        # Output Area
        self.output = scrolledtext.ScrolledText(self.root, width=80, height=18, font=("Segoe UI", 10), padx=10, pady=10)
        self.output.pack(pady=10, padx=20)

        # Link Button
        self.link_btn = tk.Button(self.root, text="🔗 OPEN FULL PAPER IN BROWSER", command=self.open_link, bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), state="disabled")
        self.link_btn.pack(pady=10)
        self.current_url = ""

    def open_link(self):
        if self.current_url:
            webbrowser.open(self.current_url)

    def run_agent(self):
        query = self.entry.get()
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, f"🔎 Searching Database for: {query}...\n")
        self.root.update()

        try:
            # 1. PubMed API Search
            handle = Entrez.esearch(db="pubmed", term=query, retmax=1)
            record = Entrez.read(handle)
            if not record["IdList"]:
                messagebox.showwarning("No Results", "No articles found.")
                return

            pmid = record["IdList"][0]
            self.current_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

            # 2. Fetch Abstract
            f_handle = Entrez.efetch(db="pubmed", id=pmid, retmode="xml")
            details = Entrez.read(f_handle)
            article = details['PubmedArticle'][0]['MedlineCitation']['Article']
            title = article['ArticleTitle']
            
            abstract_list = article.get('Abstract', {}).get('AbstractText', ["No Abstract Available"])
            abstract = " ".join([str(t) for t in abstract_list])

            # 3. Simple AI Summarization
            sentences = abstract.split('. ')
            words = re.findall(r'\w+', abstract.lower())
            common = [w for w, c in Counter(words).most_common(10) if len(w) > 4]
            summary_sentences = [s for s in sentences if any(k in s.lower() for k in common)]

            # 4. Display Results with Link
            self.output.insert(tk.END, f"\n📌 ARTICLE TITLE:\n{title}\n")
            self.output.insert(tk.END, f"\n🔗 DIRECT LINK:\n{self.current_url}\n")
            self.output.insert(tk.END, f"\n🤖 AI GENERATED SUMMARY:\n{'. '.join(summary_sentences[:3])}.\n")
            
            self.link_btn.config(state="normal")
            
        except Exception as e:
            self.output.insert(tk.END, f"\n⚠️ Connection Error: {str(e)}")

if __name__ == "__main__":
    app = BMEAgent()
    app.root.mainloop()