%% Regole della base di conoscenza

/**
 * Calcola l'indice della qualità dell'aria basato sui parametri ambientali
 *
 * @param Temp: temperatura
 * @param Umidita: umidità
 * @param CO2: livello di CO2
 * @param PM25: livello di PM2.5
 * @param PM10: livello di PM10
 * @param AQI: indice della qualità dell'aria (viene restituito il risultato)
 */
calcola_aqi(Temp, Umidita, CO2, PM25, PM10, AQI) :- 
    AQI is (PM25 + PM10 + CO2) / 3.

/**
 * Verifica se la qualità dell'aria è considerata pericolosa
 *
 * @param AQI: indice della qualità dell'aria
 * @param Allerta: 'true' se la qualità dell'aria è pericolosa, 'false' altrimenti
 */
verifica_allerta_qualita(AQI, Allerta) :- 
    AQI > 100 -> Allerta = true ; Allerta = false.

/**
 * Restituisce la qualità dell'aria di una località specificata
 *
 * @param Localita: località di cui si vuole conoscere la qualità dell'aria
 * @param Qualita: qualità dell'aria della località (viene restituito il risultato)
 */
qualita_aria_localita(Localita, Qualita) :- 
    prop(Localita, temperatura, Temp), 
    prop(Localita, umidita, Umidita), 
    prop(Localita, co2, CO2), 
    prop(Localita, pm25, PM25), 
    prop(Localita, pm10, PM10),
    calcola_aqi(Temp, Umidita, CO2, PM25, PM10, AQI),
    verifica_allerta_qualita(AQI, Allerta),
    (Allerta == true -> Qualita = 'pericolosa' ; Qualita = 'sicura').

/**
 * Restituisce una lista di località con qualità dell'aria pericolosa
 *
 * @param ListaLocalita: lista di località da controllare
 * @param LocalitaPericolose: lista di località con qualità dell'aria pericolosa (viene restituito il risultato)
 */
localita_pericolose([], []).
localita_pericolose([Localita|AltreLocalita], [Localita|LocalitaPericolose]) :- 
    qualita_aria_localita(Localita, Qualita),
    Qualita == 'pericolosa',
    localita_pericolose(AltreLocalita, LocalitaPericolose).
localita_pericolose([_|AltreLocalita], LocalitaPericolose) :- 
    localita_pericolose(AltreLocalita, LocalitaPericolose).

/**
 * Restituisce la latitudine e longitudine di una località specificata
 *
 * @param Localita: località di cui si vogliono conoscere le coordinate
 * @param Latitudine: latitudine della località
 * @param Longitudine: longitudine della località
 */
lat_lon(Localita, Latitudine, Longitudine) :- 
    prop(Localita, latitudine, Latitudine), 
    prop(Localita, longitudine, Longitudine).
