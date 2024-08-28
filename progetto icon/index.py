from ontology.air_quality_parser import carica_file
from KB.environmentalKnowledgeBase import EnvironmentalKnowledgeBase 


print("\nSistema di Monitoraggio Ambientale e Controllo della Qualità dell'Aria")
print("______________________________________________")
print("               MONITORAGGIO AMBIENTALE         ")
print("______________________________________________")
print("")

# Menù caricamento dati
scelta = True

while scelta:
    print("Menu:")
    print("1. File pre caricato")
    print("2. Carica file xml")
    print("3. Esci")

    scelta = input("Inserisci il numero dell'opzione desiderata: ")

    if scelta == "1":
        carica_file(0)
    elif scelta == "2":
        carica_file(1)
    elif scelta == "3":
        quit()
    else:
        print("Opzione non valida, per favore riprova.")

# Decidi la sincronizzazione
syncro = input("Vuoi sincronizzare i dati di qualità dell'aria all'interno del sistema? (Y/N) ")
kb = EnvironmentalKnowledgeBase(syncro.upper() == "Y")

# menu principale
while True:
    print("\n\nMenu:")
    print("1. Visualizza le stazioni di monitoraggio")
    print("2. Visualizza i dati di qualità dell'aria")
    print("3. Ricerca delle zone con qualità dell'aria scadente")
    print("4. Esci")

    scelta = input("Inserisci il numero dell'opzione desiderata: ")

    if scelta == "1":
        get_lista_stazioni = kb.lista_stazioni()
        if len(get_lista_stazioni) > 0:
            print(", ".join(get_lista_stazioni))
        else:
            print("Non sono state trovate stazioni di monitoraggio!")
    
    elif scelta == "2":
        get_dati_aria = kb.dati_aria()
        if len(get_dati_aria) > 0:
            for dato in get_dati_aria:
                print(f"Stazione: {dato['stazione']}, PM2.5: {dato['pm25']}, PM10: {dato['pm10']}, NO2: {dato['no2']}, O3: {dato['o3']}")
        else:
            print("Nessun dato di qualità dell'aria è stato trovato!")
    
    elif scelta == "3":
        zona = input("Inserisci il nome della zona per controllare la qualità dell'aria: ")
        risultati = kb.controlla_qualita_aria(zona)
        if len(risultati) > 0:
            print("\nZone con qualità dell'aria scadente: ")
            for risultato in risultati:
                print(f"Zona: {risultato['zona']}, PM2.5: {risultato['pm25']}, PM10: {risultato['pm10']}, NO2: {risultato['no2']}, O3: {risultato['o3']}")
        else:
            print("Nessun problema di qualità dell'aria è stato trovato per la zona specificata!")
    
    elif scelta == "4":
        break  # Esci dal loop
    
    else:
        print("Opzione non valida, per favore riprova.")
