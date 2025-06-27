# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 15:40:46 2025

@author: Adrian Ghiasi-Tari

Aktievärderingskalkylator för kursen FINA2203

"""

import yfinance as yf

def värdera_aktie(ticker):
    aktie = yf.Ticker(ticker)

    try:
        earnings = aktie.info["trailingEps"]  # Vinst per aktie (EPS)
        pe_ratio = aktie.info["trailingPE"]   # P/E-tal

        if earnings is None or pe_ratio is None:
            print("Data saknas för EPS eller P/E-tal.")
            return

        price = earnings * pe_ratio
        print(f"\n📊 Aktieanalys för {ticker}:")
        print(f"Vinst per aktie (EPS): {earnings}")
        print(f"P/E-tal: {pe_ratio}")
        print(f"Beräknat pris (EPS × P/E): {price:.2f}")

    except Exception as e:
        print(f"Något gick fel: {e}")

def main():
    ticker = input("Ange aktiens ticker (t.ex. AAPL, MSFT): ").strip().upper()
    värdera_aktie(ticker)

main()
