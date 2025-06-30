import tkinter as tk
from tkinter import messagebox
from decimal import Decimal, ROUND_HALF_UP
import datetime

class Bokforing:
    def __init__(self):
        self.transaktioner = []
        self.konton = {}

    def lagg_till_konto(self, kontonamn, saldo=Decimal('0.00')):
        if kontonamn not in self.konton:
            self.konton[kontonamn] = saldo
        else:
            raise ValueError(f"Konto '{kontonamn}' finns redan.")

    def lagg_till_transaktion(self, datum, beskrivning, konto, belopp):
        if konto not in self.konton:
            raise ValueError(f"Konto '{konto}' finns inte.")
        if not isinstance(belopp, (int, float, Decimal, str)):
            raise TypeError("Belopp måste vara ett tal.")

        belopp = Decimal(belopp).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.konton[konto] += belopp
        self.transaktioner.append((datum, beskrivning, konto, belopp))

    def hamta_saldo(self, konto):
        return self.konton.get(konto, Decimal('0.00'))

    def hamta_transaktioner(self):
        return self.transaktioner


class BokforingGUI:
    def __init__(self, root, bokforing):
        self.bokforing = bokforing
        self.root = root
        self.root.title("Bokföringssystem (Utbildning)")

        # --- Kontoformulär
        tk.Label(root, text="Konto:").grid(row=0, column=0)
        self.konto_entry = tk.Entry(root)
        self.konto_entry.grid(row=0, column=1)
        tk.Button(root, text="Lägg till konto", command=self.lagg_till_konto_gui).grid(row=0, column=2)

        # --- Transaktionsformulär
        tk.Label(root, text="Datum (YYYY-MM-DD):").grid(row=1, column=0)
        self.datum_entry = tk.Entry(root)
        self.datum_entry.grid(row=1, column=1)
        self.datum_entry.insert(0, str(datetime.date.today()))

        tk.Label(root, text="Beskrivning:").grid(row=2, column=0)
        self.beskrivning_entry = tk.Entry(root)
        self.beskrivning_entry.grid(row=2, column=1)

        tk.Label(root, text="Konto:").grid(row=3, column=0)
        self.trans_konto_entry = tk.Entry(root)
        self.trans_konto_entry.grid(row=3, column=1)

        tk.Label(root, text="Belopp:").grid(row=4, column=0)
        self.belopp_entry = tk.Entry(root)
        self.belopp_entry.grid(row=4, column=1)

        tk.Button(root, text="Lägg till transaktion", command=self.lagg_till_transaktion_gui).grid(row=5, column=1)

        # --- Visning
        self.transaktionslogg = tk.Text(root, height=10, width=60)
        self.transaktionslogg.grid(row=6, column=0, columnspan=3)
        self.uppdatera_logg()

    def lagg_till_konto_gui(self):
        namn = self.konto_entry.get()
        try:
            self.bokforing.lagg_till_konto(namn)
            messagebox.showinfo("Konto tillagt", f"Konto '{namn}' tillagt.")
        except Exception as e:
            messagebox.showerror("Fel", str(e))
        self.uppdatera_logg()

    def lagg_till_transaktion_gui(self):
        datum = self.datum_entry.get()
        beskrivning = self.beskrivning_entry.get()
        konto = self.trans_konto_entry.get()
        belopp = self.belopp_entry.get()
        try:
            self.bokforing.lagg_till_transaktion(datum, beskrivning, konto, belopp)
        except Exception as e:
            messagebox.showerror("Fel", str(e))
        self.uppdatera_logg()

    def uppdatera_logg(self):
        self.transaktionslogg.delete(1.0, tk.END)
        self.transaktionslogg.insert(tk.END, "Transaktioner:\n")
        for t in self.bokforing.hamta_transaktioner():
            self.transaktionslogg.insert(tk.END, f"{t[0]} | {t[1]} | {t[2]} | {t[3]} kr\n")
        self.transaktionslogg.insert(tk.END, "\nSaldon:\n")
        for k, v in self.bokforing.konton.items():
            self.transaktionslogg.insert(tk.END, f"{k}: {v} kr\n")


if __name__ == "__main__":
    bokforing = Bokforing()
    root = tk.Tk()
    app = BokforingGUI(root, bokforing)
    root.mainloop()
