import tkinter as tk
from tkinter import messagebox, ttk
from decimal import Decimal, ROUND_HALF_UP
import datetime


class Bokforing:
    """En klass för att hantera bokföring med konton och transaktioner."""

    def __init__(self):
        """Initialiserar bokföringen med tomma transaktioner och konton."""
        self.transaktioner = []
        self.konton = {}
        self.valuta = "kr"  # Standardvaluta

    def lagg_till_konto(self, kontonamn, saldo=Decimal('0.00')):
        """
        Lägger till ett nytt konto med ett initialt saldo.
        Om kontot redan finns kastas ett fel.
        """
        if kontonamn not in self.konton:
            self.konton[kontonamn] = saldo
        else:
            raise ValueError(f"Konto '{kontonamn}' finns redan.")

    def lagg_till_transaktion(self, datum, beskrivning, konto, belopp):
        """
        Lägger till en transaktion till bokföringen.
        Validerar datumformat och kontonamn.
        """
        if not isinstance(datum, str):
            raise ValueError("Datum måste vara en sträng i formatet 'YYYY-MM-DD'.")

        try:
            datum = datetime.datetime.strptime(datum, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Datum måste vara i formatet 'YYYY-MM-DD'.")

        if konto not in self.konton:
            raise ValueError(f"Konto '{konto}' finns inte.")

        belopp = Decimal(belopp).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.konton[konto] += belopp
        self.transaktioner.append((datum, beskrivning, konto, belopp))

    def hamta_transaktioner(self):
        """
        Returnerar alla transaktioner som en lista av tuples.
        Varje tuple innehåller datum, beskrivning, konto och belopp.
        """
        return self.transaktioner or []

    def hamta_saldo(self, konto):
        """
        Returnerar saldot för ett specifikt konto.
        Om kontot inte finns kastas ett fel.
        """
        if konto not in self.konton:
            raise ValueError(f"Konto '{konto}' finns inte.")

        return self.konton.get(konto, Decimal('0.00'))

    def berakna_resultatrakning(self):
        """
        Beräknar intäkter, kostnader och resultat utifrån kontonummer.
        Intäkter: konton som börjar med '3'
        Kostnader: konton som börjar med '5', '6', eller '7'
        """
        intakter = Decimal('0.00')
        kostnader = Decimal('0.00')

        for konto, saldo in self.konton.items():
            if konto.startswith('3'):
                intakter += saldo
            elif konto.startswith(('5', '6', '7')):
                kostnader += saldo

        resultat = intakter - kostnader
        return intakter, kostnader, resultat

    def berakna_balansrakning(self):
        """
        Beräknar tillgångar, skulder och eget kapital.
        Tillgångar: konton som börjar med '1'
        Skulder: konton som börjar med '2'
        """
        tillgangar = Decimal('0.00')
        skulder = Decimal('0.00')

        for konto, saldo in self.konton.items():
            if konto.startswith('1'):
                tillgangar += saldo
            elif konto.startswith('2'):
                skulder += saldo

        eget_kapital = tillgangar - skulder
        return tillgangar, skulder, eget_kapital


class BokforingGUI:
    """Grafiskt användargränssnitt för bokföringssystemet."""

    def __init__(self, root, bokforing):
        """Initialiserar GUI och layout för användarinteraktion."""
        self.bokforing = bokforing
        self.root = root
        self.root.title("Bokföringssystem (Utbildning)")

        # Valutaväljare
        tk.Label(root, text="Valuta:").grid(row=0, column=0)
        self.valuta_var = tk.StringVar(value="kr")
        self.valuta_menu = ttk.Combobox(
            root, textvariable=self.valuta_var, values=["kr", "$", "€", "£"], width=5
        )
        self.valuta_menu.grid(row=0, column=1)
        self.valuta_menu.bind("<<ComboboxSelected>>", self.byta_valuta)

        # Kontoformulär
        tk.Label(root, text="Konto:").grid(row=1, column=0)
        self.konto_entry = tk.Entry(root)
        self.konto_entry.grid(row=1, column=1)
        tk.Button(root, text="Lägg till konto", command=self.lagg_till_konto_gui).grid(row=1, column=2)

        # Transaktionsformulär
        tk.Label(root, text="Datum (YYYY-MM-DD):").grid(row=2, column=0)
        self.datum_entry = tk.Entry(root)
        self.datum_entry.grid(row=2, column=1)
        self.datum_entry.insert(0, str(datetime.date.today()))

        tk.Label(root, text="Beskrivning:").grid(row=3, column=0)
        self.beskrivning_entry = tk.Entry(root)
        self.beskrivning_entry.grid(row=3, column=1)

        tk.Label(root, text="Konto:").grid(row=4, column=0)
        self.trans_konto_entry = tk.Entry(root)
        self.trans_konto_entry.grid(row=4, column=1)

        tk.Label(root, text="Belopp:").grid(row=5, column=0)
        self.belopp_entry = tk.Entry(root)
        self.belopp_entry.grid(row=5, column=1)

        tk.Button(root, text="Lägg till transaktion", command=self.lagg_till_transaktion_gui).grid(row=6, column=1)

        # Transaktionslogg
        self.transaktionslogg = tk.Text(root, height=15, width=70)
        self.transaktionslogg.grid(row=7, column=0, columnspan=3)
        self.uppdatera_logg()

        # Rapportknappar
        tk.Button(root, text="Visa Resultaträkning", command=self.visa_resultatrakning).grid(row=8, column=0)
        tk.Button(root, text="Visa Balansräkning", command=self.visa_balansrakning).grid(row=8, column=1)

    def byta_valuta(self, event):
        """Uppdaterar aktuell valuta enligt användarens val."""
        self.bokforing.valuta = self.valuta_var.get()
        self.uppdatera_logg()

    def lagg_till_konto_gui(self):
        """Hanterar inmatning av nytt konto via GUI."""
        namn = self.konto_entry.get()
        try:
            self.bokforing.lagg_till_konto(namn)
            messagebox.showinfo("Konto tillagt", f"Konto '{namn}' tillagt.")
        except Exception as e:
            messagebox.showerror("Fel", str(e))
        self.uppdatera_logg()

    def lagg_till_transaktion_gui(self):
        """Hanterar inmatning av ny transaktion via GUI."""
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
        """Uppdaterar visningen av transaktioner och kontosaldon i GUI."""
        val = self.bokforing.valuta
        self.transaktionslogg.delete(1.0, tk.END)
        self.transaktionslogg.insert(tk.END, "Transaktioner:\n")

        for t in self.bokforing.hamta_transaktioner():
            self.transaktionslogg.insert(tk.END, f"{t[0]} | {t[1]} | {t[2]} | {t[3]} {val}\n")

        self.transaktionslogg.insert(tk.END, "\nSaldon:\n")
        for k, v in self.bokforing.konton.items():
            self.transaktionslogg.insert(tk.END, f"{k}: {v} {val}\n")

    def visa_resultatrakning(self):
        """Visar ett popupfönster med resultaträkningen."""
        intakter, kostnader, resultat = self.bokforing.berakna_resultatrakning()
        val = self.bokforing.valuta

        messagebox.showinfo(
            "Resultaträkning",
            f"Intäkter: {intakter} {val}\nKostnader: {kostnader} {val}\nResultat: {resultat} {val}"
        )

    def visa_balansrakning(self):
        """Visar ett popupfönster med balansräkningen."""
        tillgangar, skulder, eget_kapital = self.bokforing.berakna_balansrakning()
        val = self.bokforing.valuta

        messagebox.showinfo(
            "Balansräkning",
            f"Tillgångar: {tillgangar} {val}\nSkulder: {skulder} {val}\nEget kapital: {eget_kapital} {val}"
        )


# Programstart
if __name__ == "__main__":
    bokforing = Bokforing()
    root = tk.Tk()
    app = BokforingGUI(root, bokforing)
    root.mainloop()
