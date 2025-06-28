def beräkna_ny_aktiekurs(gammal_utdelning, gammal_pris, ny_utdelning):
    direktavkastning = gammal_utdelning / gammal_pris
    ny_pris = ny_utdelning / direktavkastning
    return ny_pris

# Indata
gammal_utdelning = 1.49
gammal_pris = 37.54
ny_utdelning = 1.79

# Beräkning
ny_pris = beräkna_ny_aktiekurs(gammal_utdelning, gammal_pris, ny_utdelning)

print(f"📈 Den nya aktiekursen bör bli: ${ny_pris:.2f}")
