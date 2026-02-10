#!/usr/bin/env python3

import os
import re

# ================= CONFIGURAZIONE =================
# Nome della cartella contenente i capitoli/lezioni
SUBFILES_DIR = "subfiles"
# Nome del file principale da generare
OUTPUT_FILE = "main.tex"

# Lista di pattern (Regex) da ELIMINARE dai subfiles
# Il simbolo '^' indica l'inizio della riga, '.*' indica qualsiasi carattere
PATTERNS_TO_REMOVE = [
    r"^\s*\\usepackage.*\{biblatex\}.*$",  # Rimuove biblatex (con o senza opzioni)
    r"^\s*\\(title|date|author)\{.*\}.*$"  # Rimuove \title{}, \date{}, \author{}
]
# ==================================================

def clean_file_content(filepath):
    """
    Legge un file, rimuove le righe indesiderate tramite regex e lo salva.
    Restituisce True se il file è stato modificato.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Applica tutte le regex di pulizia
        for pattern in PATTERNS_TO_REMOVE:
            # re.MULTILINE permette a ^ di matchare l'inizio di ogni riga
            # flags=re.DOTALL serve per hypersetup se è su più righe (ma attenzione ai greedy match)
            content = re.sub(pattern, "", content, flags=re.MULTILINE)

        # Rimuove eventuali righe vuote multiple lasciate dalla cancellazione (opzionale)
        # content = re.sub(r'\n\s*\n', '\n\n', content)

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False

    except Exception as e:
        print(f"Errore durante la pulizia di {filepath}: {e}")
        return False

def main():
    # Verifica che la cartella subfiles esista
    if not os.path.exists(SUBFILES_DIR):
        print(f"Errore: La cartella '{SUBFILES_DIR}' non esiste.")
        return

    # 1. Recupera la lista dei file .tex
    files = [f for f in os.listdir(SUBFILES_DIR) if f.endswith(".tex")]

    # 2. Ordina i file (alfabeticamente)
    files.sort()

    # Contatore per i file puliti
    cleaned_count = 0

    # 3. Costruisce la stringa dei subfiles E pulisce i file
    subfiles_latex_code = ""

    print(f"Processando {len(files)} file in '{SUBFILES_DIR}'...")

    for filename in files:
        # --- FASE DI PULIZIA ---
        full_path = os.path.join(SUBFILES_DIR, filename)
        if clean_file_content(full_path):
            cleaned_count += 1
            # Opzionale: stampa quale file è stato pulito
            # print(f"  -> Pulito: {filename}")

        # --- FASE DI GENERAZIONE MAIN ---
        # Rimuove l'estensione .tex dal nome del file
        name_without_ext = os.path.splitext(filename)[0]

        # Costruisce il percorso relativo per il main.tex
        # Nota: usiamo f-string con / forzato per compatibilità LaTeX
        path = f"{SUBFILES_DIR}/{name_without_ext}"

        subfiles_latex_code += f"\\subfile{{{path}}}\n"

    if cleaned_count > 0:
        print(f"Note: Rimossi comandi indesiderati da {cleaned_count} file.")

    # 4. Definisce il template richiesto
    template = r"""\documentclass[10pt]{article}

\usepackage{subfiles}
\input{preamble.tex}

\begin{document}

[SUBFILES]

\end{document}
"""

    # 5. Sostituisce il placeholder con il codice generato
    replacement = subfiles_latex_code.strip() if subfiles_latex_code else "% Nessun file trovato"
    final_content = template.replace("[SUBFILES]", replacement)

    # 6. Scrive il file main.tex
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(final_content)
        print(f"Successo! '{OUTPUT_FILE}' generato con {len(files)} subfiles.")
    except Exception as e:
        print(f"Errore durante la scrittura di {OUTPUT_FILE}: {e}")

if __name__ == "__main__":
    main()
