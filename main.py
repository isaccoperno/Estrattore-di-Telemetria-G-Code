import re
import math

def calcola_distanza_estrusore(filepath):
    # Pattern RegEx per trovare G0 o G1
    pattern_g = re.compile(r'^G[01]\b')
    
    # Pattern per estrarre i valori numerici di X, Y e Z
    pattern_x = re.compile(r'X(-?\d+\.?\d*)')
    pattern_y = re.compile(r'Y(-?\d+\.?\d*)')
    pattern_z = re.compile(r'Z(-?\d+\.?\d*)')

    distanza_totale = 0.0
    
    # Inizializziamo le coordinate dell'estrusore all'origine
    curr_x, curr_y, curr_z = 0.0, 0.0, 0.0

    with open(filepath, 'r') as file:
        for linea in file:
            # Bambu Studio inserisce molti commenti: ignoriamo tutto dopo il ';'
            linea_pulita = linea.split(';')[0].strip()

            if pattern_g.match(linea_pulita):
                # Cerchiamo le coordinate nella riga
                match_x = pattern_x.search(linea_pulita)
                match_y = pattern_y.search(linea_pulita)
                match_z = pattern_z.search(linea_pulita)

                # Se la coordinata è presente, la aggiorniamo. Altrimenti teniamo la vecchia.
                new_x = float(match_x.group(1)) if match_x else curr_x
                new_y = float(match_y.group(1)) if match_y else curr_y
                new_z = float(match_z.group(1)) if match_z else curr_z

                # Calcoliamo la distanza percorsa in questo singolo movimento
                distanza = math.sqrt((new_x - curr_x)**2 + (new_y - curr_y)**2 + (new_z - curr_z)**2)
                distanza_totale += distanza

                # Aggiorniamo la posizione corrente per il prossimo ciclo
                curr_x, curr_y, curr_z = new_x, new_y, new_z

    return distanza_totale

nome_file_gcode = input("Inserisci il nome del gcode da analizzare (escluso il .gcode finale): ")

filepath = f"file_gcode/{nome_file_gcode}.gcode"
distanza = calcola_distanza_estrusore(filepath)
print(f"Distanza totale percorsa dall'estrusore: {distanza / 1000:.2f} metri")