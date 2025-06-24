# === Bibliotek för GUI och visualisering ===
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# === Funktion: Beräknar kassaflöden och nuvärde för en obligation ===
def beräkna_obligationspris(kupong, nominellt_belopp, löptid, avkastning):
    """
    Returnerar:
    - En lista över kassaflöden (kuponger + nominellt belopp)
    - Obligationens nuvärde baserat på angiven avkastning
    """
    kassaflöden = [kupong] * (löptid - 1) + [kupong + nominellt_belopp]
    nuvärde = sum(cf / ((1 + avkastning) ** (i + 1)) for i, cf in enumerate(kassaflöden))
    return kassaflöden, nuvärde

# === Funktion: Ritar en tidslinje över kassaflöden ===
def rita_tidslinje(löptid, kassaflöden, avkastning):
    """
    Visualiserar obligationens kassaflöden över tid som en tidslinje
    """
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.set_xlim(-1, löptid + 1)
    ax.set_ylim(-1, 1)
    ax.plot(range(1, löptid + 1), [0] * löptid, 'k-')

    for år in range(1, löptid + 1):
        ax.vlines(x=år, ymin=-0.1, ymax=0.1, color='black')
        ax.text(år, -0.25, f"{år}", ha='center')
        if år <= len(kassaflöden):
            ax.text(år, 0.2, f"{kassaflöden[år - 1]:.0f}", ha='center', color='green', fontsize=10)

    ax.text(0, 0.5, f"YTM = {avkastning * 100:.2f}%", fontsize=10)
    ax.set_title("Tidslinje för obligation")
    ax.axis('off')
    plt.tight_layout()
    return fig

# === Funktion: Körs när användaren klickar på knappen ===
def beräkna_och_visa():
    """
    Hämtar användarinmatning, utför beräkningar och visar resultat + graf
    """
    try:
        löptid = int(inmatning_löptid.get())
        kupongränta = float(inmatning_kupong.get()) / 100
        nominellt_belopp = float(inmatning_nominellt.get())
        avkastning = float(inmatning_ytm.get()) / 100

        kupong = kupongränta * nominellt_belopp
        kassaflöden, pris = beräkna_obligationspris(kupong, nominellt_belopp, löptid, avkastning)
        figur = rita_tidslinje(löptid, kassaflöden, avkastning)

        # Rensar tidigare graf
        for widget in ram_graf.winfo_children():
            widget.destroy()

        # Lägger till ny graf
        canvas = FigureCanvasTkAgg(figur, master=ram_graf)
        canvas.draw()
        canvas.get_tk_widget().pack()

        etikett_resultat.config(text=f"Obligationens värde (nuvärde): {pris:.2f} kr")

    except Exception as fel:
        messagebox.showerror("Fel", str(fel))

# === GUI-uppsättning med Tkinter ===

fönster = tk.Tk()
fönster.title("Obligationskalkylator")

# --- Inmatningsfält ---
tk.Label(fönster, text="Antal år till förfall:").grid(row=0, column=0, sticky="e")
inmatning_löptid = tk.Entry(fönster)
inmatning_löptid.grid(row=0, column=1)

tk.Label(fönster, text="Kupongränta (%):").grid(row=1, column=0, sticky="e")
inmatning_kupong = tk.Entry(fönster)
inmatning_kupong.grid(row=1, column=1)

tk.Label(fönster, text="Nominellt belopp (kr):").grid(row=2, column=0, sticky="e")
inmatning_nominellt = tk.Entry(fönster)
inmatning_nominellt.grid(row=2, column=1)

tk.Label(fönster, text="Avkastning till förfall (YTM %):").grid(row=3, column=0, sticky="e")
inmatning_ytm = tk.Entry(fönster)
inmatning_ytm.grid(row=3, column=1)

# --- Knapp ---
tk.Button(fönster, text="Beräkna och rita tidslinje", command=beräkna_och_visa).grid(row=4, columnspan=2, pady=10)

# --- Resultattext ---
etikett_resultat = tk.Label(fönster, text="", font=("Helvetica", 12))
etikett_resultat.grid(row=5, columnspan=2)

# --- Graf-ruta ---
ram_graf = tk.Frame(fönster)
ram_graf.grid(row=6, columnspan=2)

# --- Kör GUI ---
fönster.mainloop()
