/* Classe sensore
 * 
 * Contiene i seguenti attributi:
 * - id: Identificativo del sensore
 * - tipo: Tipo di sensore (es. NO2, PM2.5, CO2)
 * - posizione: Posizione geografica del sensore (es. latitudine, longitudine)
 * - stato: Stato del sensore (attivo, inattivo)
 */

/* Classe sensore_inquinamento sottoclasse di sensore */
prop(sensore_inquinamento, subClassOf, sensore).

/* Classe sensore_meteo sottoclasse di sensore */
prop(sensore_meteo, subClassOf, sensore).


/* Classe misurazione
 * 
 * Contiene i seguenti attributi:
 * - id: Identificativo della misurazione
 * - inquinante: Tipo di inquinante misurato
 * - valore: Valore della misurazione
 * - data_ora: Data e ora della misurazione
 * - sensore: Sensore che ha effettuato la misurazione
 */

/* Classe misurazione_critica sottoclasse di misurazione */
prop(misurazione_critica, subClassOf, misurazione).

/* Classe misurazione_normale sottoclasse di misurazione */
prop(misurazione_normale, subClassOf, misurazione).


/* Classe condizione_ambientale
 * 
 * Contiene i seguenti attributi:
 * - temperatura: Temperatura dell'aria (in gradi Celsius)
 * - umidita: Percentuale di umidità relativa
 * - velocita_vento: Velocità del vento (in km/h)
 * - direzione_vento: Direzione del vento
 * - pressione: Pressione atmosferica (in hPa)
 * - data_ora: Data e ora della rilevazione
 * - luogo: Luogo della rilevazione
 */

/* Classe condizione_critica sottoclasse di condizione_ambientale */
prop(condizione_critica, subClassOf, condizione_ambientale).

/* Classe condizione_normale sottoclasse di condizione_ambientale */
prop(condizione_normale, subClassOf, condizione_ambientale).

/* Classe allerta
 *
 * Contiene i seguenti attributi:
 * - livello: Livello dell'allerta (basso, medio, alto)
 * - descrizione: Descrizione dell'allerta
 * - data_ora: Data e ora dell'emissione dell'allerta
 */

/* Classe allerta_inquinamento sottoclasse di allerta */
prop(allerta_inquinamento, subClassOf, allerta).

/* Classe allerta_meteo sottoclasse di allerta */
prop(allerta_meteo, subClassOf, allerta).
