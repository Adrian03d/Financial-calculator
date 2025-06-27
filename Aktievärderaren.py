# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 15:40:46 2025

@author: Adrian Ghiasi-Tari

Aktievärderingskalkylator för kursen FINA2203

"""

def värdera_aktie():
    earnings = float(input("What are the earnings of the company?: "))
    price_to_earnings = float(input("What are the price to earnings ratio?: "))
    price = price_to_earnings*earnings
    return print(price)

def main():

    värdera_aktie()
    
main()