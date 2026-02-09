#!/usr/bin/env python3

import os

# CONFIGURAZIONE
# Nome della cartella contenente i capitoli/lezioni
SUBFILES_DIR = "subfiles"
# Nome del file principale da generare
OUTPUT_FILE = "main.tex"

def main():
    # Verifica che la cartella subfiles esista
    if not os.path.exists(SUBFILES_DIR):
        print(f"Errore: La cartella '{SUBFILES_DIR}' non esiste.")
        return

    # 1. Recupera la lista dei file .tex
    files = [f for f in os.listdir(SUBFILES_DIR) if f.endswith(".tex")]

    # 2. Ordina i file (alfabeticamente)
    files.sort()

    # 3. Costruisce la stringa dei subfiles
    subfiles_latex_code = ""
    for filename in files:
        # Rimuove l'estensione .tex dal nome del file
        # os.path.splitext("file.tex") restituisce ("file", ".tex") -> prendiamo l'indice [0]
        name_without_ext = os.path.splitext(filename)[0]

        # Costruisce il percorso relativo: ./subfiles/NomeFile (senza .tex)
        path = f"{SUBFILES_DIR}/{name_without_ext}"

        subfiles_latex_code += f"\\subfile{{{path}}}\n"

    # 4. Definisce il template richiesto
    template = r"""\documentclass[10pt]{article}

\usepackage{subfiles}
\input{preamble.tex}

\begin{document}

[SUBFILES]

\end{document}
"""

    # 5. Sostituisce il placeholder con il codice generato
    # Se la lista è vuota, mette una stringa vuota o un commento
    replacement = subfiles_latex_code.strip() if subfiles_latex_code else "% Nessun file trovato"
    final_content = template.replace("[SUBFILES]", replacement)

    # 6. Scrive il file main.tex
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(final_content)
        print(f"Successo! Il file '{OUTPUT_FILE}' è stato aggiornato con {len(files)} subfiles (estensioni rimosse).")
    except Exception as e:
        print(f"Errore durante la scrittura del file: {e}")

if __name__ == "__main__":
    main()
