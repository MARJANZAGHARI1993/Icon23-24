import copy
from math import atan2, cos, radians, sin, sqrt
import random
import time
import pickle
import numpy as np
from pyswip import Prolog
from KB.path_finding.A_star import SearchProblemHiddenGraph
from KB.markovChain.markov_chain import syncro, getprobverde

class EnvironmentalKnowledgeBase:
    def __init__(self, syncro):
        '''
        Metodo init
        ---------------
        Inizializza il motore di prolog e gli algoritmi di machine learning

        ----------------
        Dati di input
        --------------
        syncro: booleano che indica se sincronizzare i controlli ambientali
        '''
        self.prolog = Prolog()
        self.prolog.consult("KB/prolog/knowledge_base.pl", catcherrors=False)

        # Carica il modello di previsione della qualità dell'aria
        with open('supervised_learning/models/air_quality_model.sav', 'rb') as pickle_file:
            self.air_quality_model = pickle.load(pickle_file)

        with open('supervised_learning/models/scaler_air_quality.sav', 'rb') as pickle_file:
            self.scaler = pickle.load(pickle_file)

        # Previsione della qualità dell'aria per le diverse aree
        self.dic = { 
            "zona_urbana": self.predizione_qualita_aria(1),
            "zona suburbana": self.predizione_qualita_aria(2),
            "zona rurale": self.predizione_qualita_aria(3)
        }

        # Ottieni tutte le stazioni di monitoraggio
        stazioni_monitoraggio = []
        query_stazione = "prop(Stazione, monitoraggio, 1)"
        for atom in self.prolog.query(query_stazione):
            stazioni_monitoraggio.append(atom["Stazione"])

        self.dict_stazioni = {}
        for stazione in stazioni_monitoraggio:
            self.setup_stazione_monitoraggio(stazione)

        if syncro:
            # Inizializzazione e ottimizzazione della configurazione
            stazioni_sincronizzate = self.sincronizzazione_stazioni()
            self.modifica_monitoraggio(stazioni_sincronizzate)

    def modifica_monitoraggio(self, assegnazione):
        '''
        Metodo modifica_monitoraggio
        -------------------
        Modifica la configurazione di monitoraggio per una stazione

        Dati di input
        --------------
        assegnazione: dizionario contenente come chiave la stazione A
                      e come valore la stazione B sincronizzata con A
                      in modo che A dipende da B (A è slave di B).
                      Se il valore di A è A stesso significa che non
                      è sincronizzato con nessun altro stazione.
        '''
        for slave, master in assegnazione.items():
            slave = slave.name
            if slave != master:
                nuova_configurazione_slave = self.sincronizza_stazioni(master, slave)
                self.rimuovi_stazione_monitoraggio(slave)
                self.assegna_stazione_monitoraggio(slave, nuova_configurazione_slave)

    def valutazione_efficacia(self, stazioni_sincronizzate):
        '''
        Metodo valutazione_efficacia
        -------------------
        Dati di input
        --------------
        stazioni_sincronizzate: dizionario contenente come chiave la stazione A
                                e come valore la stazione B sincronizzata con A
                                in modo che A dipende da B (A è slave di B).
                                Se il valore di A è A stesso significa che non
                                è sincronizzato con nessun altro stazione.
        Dati di output
        --------------
        efficacia: efficacia totale
        '''
        efficacia = 0

        configurazioni_aggiornate = copy.deepcopy(self.dict_stazioni)

        # aggiorna le configurazioni di monitoraggio
        for slave, master in stazioni_sincronizzate.items():
            if isinstance(slave, str) == False:
                slave = slave.name

            if master != slave:
                nuova_configurazione_slave = self.sincronizza_stazioni(master, slave)
                configurazioni_aggiornate[slave] = nuova_configurazione_slave

        count_zone = 0
        # calcola l'efficacia
        for master, vicini in self.stazione_vicini.items():
            for vicino in vicini:
                zone_comuni = self.stazione_zone_comuni(master, vicino)

                zona = ""
                if len(zone_comuni) > 0:
                    zona = zone_comuni[0]

                    distanza_stazioni, velocita = self.distanza_nodi_secondi(master, vicino, 0, False)
                    configurazione_vicino = configurazioni_aggiornate[vicino][zona]
                    configurazione_master = configurazioni_aggiornate[master][zona]
                    prob_qualita = getprobverde(configurazione_vicino, configurazione_master, distanza_stazioni)
                    efficacia += prob_qualita
                    count_zone += 1

        if count_zone > 0:
            return efficacia / count_zone
        else:
            return 0

    def sincronizzazione_stazioni(self):
        '''
        Metodo sincronizzazione_stazioni
        -------------------
        Inizializza e restituisce la sincronizzazione delle stazioni.

        Dati di output
        --------------
        stazioni_sincronizzate: dizionario contenente come chiave la stazione A
                                e come valore la stazione B sincronizzata con A
                                in modo che A dipende da B (A è slave di B).
        '''
        stazioni_sincronizzate = {}
        self.stazione_vicini = self.init_vicini_stazioni()

        for stazione, vicini in self.stazione_vicini.items():
            for vicino in vicini:
                stazioni_sincronizzate[stazione] = vicino

        return stazioni_sincronizzate

    def init_vicini_stazioni(self):
        '''
        Metodo init_vicini_stazioni
        -------------------
        Inizializza la relazione tra stazioni e i loro vicini.

        Dati di output
        --------------
        stazione_vicini: dizionario contenente stazioni e i loro vicini
        '''
        self.stazione_vicini = {}

        stazioni = []
        query = "prop(Stazione, type, stazione)"
        for atom in self.prolog.query(query):
            stazioni.append(atom["Stazione"])

        for stazione in stazioni:
            monitoraggio = 0
            query = "prop("+stazione+", monitoraggio, Monitoraggio)"
            for atom in self.prolog.query(query):
                monitoraggio = atom["Monitoraggio"]

            if monitoraggio == 1:
                vicini = self.vicini_stazione(stazione)

                lista_vicini = []
                for vicino in vicini:
                    monitoraggio = 0
                    query = "prop("+vicino+", monitoraggio, Monitoraggio)"
                    for atom in self.prolog.query(query):
                        monitoraggio = atom["Monitoraggio"]

                    if monitoraggio == 1:
                        lista_vicini.append(vicino)
                self.stazione_vicini[stazione] = lista_vicini
        return self.stazione_vicini

    def sincronizza_stazioni(self, stazione_1, stazione_2):
        '''
        Metodo sincronizza_stazioni
        -------------------
        Dati di input
        --------------
        stazione_1: prima stazione da sincronizzare
        stazione_2: seconda stazione da sincronizzare

        Dati di output
        --------------
        new_configurazione2: nuova configurazione della seconda stazione
        '''
        new_configurazione2 = {}
        zone_comuni = self.stazione_zone_comuni(stazione_1, stazione_2)

        if len(zone_comuni) == 0:
            return

        zona_comune = zone_comuni[0]

        new_configurazione2 = {}
        query_stazione = f"prop({stazione_2}, zone, Zone)"
        lista_zone = list(self.prolog.query(query_stazione))
        for atom in lista_zone:
            zone = atom["Zone"]
            get_zone = [zona.value for zona in zone]
        for zona in get_zone:
            if zona != zona_comune:
                new_configurazione2[zona] = self.get_configurazione_stazione(stazione_2, zona)

        configurazione_1 = self.get_configurazione_stazione(stazione_1, zona_comune)
        configurazione_2 = self.get_configurazione_stazione(stazione_2, zona_comune)

        if len(configurazione_1) == 0 or len(configurazione_2) == 0:
            return

        distanza_stazioni, velocita = self.distanza_nodi_secondi(stazione_1, stazione_2, 0, False)

        configurazione_sincr, new_configurazione2 = syncro(configurazione_1, configurazione_2, new_configurazione2, distanza_stazioni, velocita)
        new_configurazione2[zona_comune] = configurazione_sincr    

        self.aggiorna_configurazione_monitoraggio(stazione_2, new_configurazione2)
        return new_configurazione2

    def distanza_nodi_secondi(self, nodo1, nodo2, min_distanza, calcola):
        '''
        Metodo distanza_nodi_secondi
        -------------------
        Dati di input
        --------------
        nodo1: primo nodo
        nodo2: secondo nodo
        min_distanza: distanza minima
        calcola: se calcolare la distanza

        Dati di output
        --------------
        distanza: distanza tra i due nodi
        velocita: velocità media
        '''
        if calcola:
            query = f"prop({nodo1}, {nodo2}, Distanza)"
            for atom in self.prolog.query(query):
                distanza = atom["Distanza"]

            query = f"prop({nodo1}, {nodo2}, Velocita)"
            for atom in self.prolog.query(query):
                velocita = atom["Velocita"]

            return distanza, velocita
        else:
            distanza = random.randint(1, 100)
            velocita = random.randint(1, 10)
            return distanza, velocita

    def stazione_zone_comuni(self, stazione1, stazione2):
        '''
        Metodo stazione_zone_comuni
        -------------------
        Dati di input
        --------------
        stazione1: prima stazione
        stazione2: seconda stazione

        Dati di output
        --------------
        zone_comuni: zone comuni tra le due stazioni
        '''
        zone_comuni = []
        query = f"prop({stazione1}, zone, Zona)"
        for atom in self.prolog.query(query):
            zone_comuni.append(atom["Zona"])

        query = f"prop({stazione2}, zone, Zona)"
        for atom in self.prolog.query(query):
            if atom["Zona"] in zone_comuni:
                zone_comuni.append(atom["Zona"])
        return zone_comuni

    def get_configurazione_stazione(self, stazione, zona):
        '''
        Metodo get_configurazione_stazione
        -------------------
        Dati di input
        --------------
        stazione: stazione da cui ottenere la configurazione
        zona: zona da considerare

        Dati di output
        --------------
        configurazione: configurazione della stazione per la zona specificata
        '''
        configurazione = {}
        query = f"prop({stazione}, {zona}, Caratteristica, Valore)"
        for atom in self.prolog.query(query):
            configurazione[atom["Caratteristica"]] = atom["Valore"]
        return configurazione

    def predizione_qualita_aria(self, zona):
        '''
        Metodo predizione_qualita_aria
        -------------------
        Dati di input
        --------------
        zona: zona da valutare (1 = zona urbana, 2 = zona suburbana, 3 = zona rurale)

        Dati di output
        --------------
        qualita: predizione della qualità dell'aria
        '''
        if zona == 1:
            features = [0.8, 0.6, 0.4]  # esempio di feature per la zona urbana
        elif zona == 2:
            features = [0.6, 0.4, 0.2]  # esempio di feature per la zona suburbana
        elif zona == 3:
            features = [0.4, 0.2, 0.1]  # esempio di feature per la zona rurale
        else:
            features = [0.0, 0.0, 0.0]

        features_scaled = self.scaler.transform([features])
        qualita = self.air_quality_model.predict(features_scaled)[0]
        return qualita

    def setup_stazione_monitoraggio(self, stazione):
        '''
        Metodo setup_stazione_monitoraggio
        -------------------
        Dati di input
        --------------
        stazione: stazione di monitoraggio da configurare
        '''
        configurazione_stazione = {}
        query = f"prop({stazione}, zone, Zona)"
        for atom in self.prolog.query(query):
            zona = atom["Zona"]
            configurazione_zona = {}
            query_zona = f"prop({stazione}, {zona}, Caratteristica, Valore)"
            for sub_atom in self.prolog.query(query_zona):
                caratteristica = sub_atom["Caratteristica"]
                valore = sub_atom["Valore"]
                configurazione_zona[caratteristica] = valore
            configurazione_stazione[zona] = configurazione_zona
        self.dict_stazioni[stazione] = configurazione_stazione

    def aggiorna_dati_ambientali(self, stazione, dati_ambientali):
        '''
        Metodo aggiorna_dati_ambientali
        -------------------
        Dati di input
        --------------
        stazione: stazione di monitoraggio da aggiornare
        dati_ambientali: dizionario contenente i nuovi dati ambientali
        '''
        if stazione not in self.dict_stazioni:
            print(f"Stazione {stazione} non trovata nella KB.")
            return

        # Aggiorna i dati ambientali nel dizionario della KB
        self.dict_stazioni[stazione].update(dati_ambientali)

        # Aggiorna i dati nel file Prolog (se necessario)
        for key, value in dati_ambientali.items():
            query = f"assertz(prop({stazione}, {key}, {value}))"
            self.prolog.query(query)
        print(f"Dati ambientali per {stazione} aggiornati.")

    def aggiorna_configurazione_monitoraggio(self, stazione, configurazione):
        '''
        Metodo aggiorna_configurazione_monitoraggio
        -------------------
        Dati di input
        --------------
        stazione: stazione di monitoraggio da aggiornare
        configurazione: nuova configurazione della stazione
        '''
        if stazione not in self.dict_stazioni:
            print(f"Stazione {stazione} non trovata nella KB.")
            return

        self.dict_stazioni[stazione] = configurazione

        # Aggiorna la configurazione nel file Prolog
        for zona, config in configurazione.items():
            query = f"assertz(prop({stazione}, zona, {zona}))"
            self.prolog.query(query)
            for key, value in config.items():
                query = f"assertz(prop({stazione}, {zona}, {key}, {value}))"
                self.prolog.query(query)
        print(f"Configurazione di monitoraggio per {stazione} aggiornata.")

    def rimuovi_stazione_monitoraggio(self, stazione):
        '''
        Metodo rimuovi_stazione_monitoraggio
        -------------------
        Dati di input
        --------------
        stazione: stazione di monitoraggio da rimuovere
        '''
        if stazione in self.dict_stazioni:
            del self.dict_stazioni[stazione]

            # Rimuovi la stazione anche dal file Prolog
            query = f"retractall(prop({stazione}, _, _))"
            self.prolog.query(query)
            print(f"Stazione {stazione} rimossa dalla KB.")
        else:
            print(f"Stazione {stazione} non trovata nella KB.")

    def assegna_stazione_monitoraggio(self, stazione, configurazione):
        '''
        Metodo assegna_stazione_monitoraggio
        -------------------
        Dati di input
        --------------
        stazione: stazione di monitoraggio da assegnare
        configurazione: configurazione della stazione
        '''
        self.dict_stazioni[stazione] = configurazione

        # Assegna la nuova stazione anche al file Prolog
        for zona, config in configurazione.items():
            query = f"assertz(prop({stazione}, zona, {zona}))"
            self.prolog.query(query)
            for key, value in config.items():
                query = f"assertz(prop({stazione}, {zona}, {key}, {value}))"
                self.prolog.query(query)
        print(f"Stazione {stazione} assegnata alla KB.")
