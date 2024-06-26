import pandas as pd

# Einlesen der CSV-Dateien
umsatzdaten = pd.read_csv('/workspaces/UmsatzWetterBackereiKiel/0_DataPreparation/umsatzdaten_gekuerzt.csv')
fremdenverkehr_var2 = pd.read_csv('/workspaces/UmsatzWetterBackereiKiel/0_DataPreparation/Ordnungsamt Kiel/CSV/Fremdenverkehr_Variante_2.csv')

## Bearbeiten der Datei Fremdenverkehr Variante 2  

# Anzeigen der ersten Zeilen
print("Erste Zeilen der Daten:")
print(fremdenverkehr_var2.head())

# 1. Entfernen der letzten Spalte
fremdenverkehr_var2 = fremdenverkehr_var2.drop(columns=['durchschnittl_aufenthaltsdauer_Tage', 'gaeste_ankuenfte'])

# 2. Erstellen der täglichen Daten
fremdenverkehr_var2['Zeitraum_von'] = pd.to_datetime(fremdenverkehr_var2['Zeitraum_von'])
fremdenverkehr_var2['Zeitraum_bis'] = pd.to_datetime(fremdenverkehr_var2['Zeitraum_bis'])

# 3. Erzeugen des täglichen Datumsbereichs
all_data = []
for _, row in fremdenverkehr_var2.iterrows():
    start_date = row['Zeitraum_von']
    end_date = row['Zeitraum_bis']
    num_days = (end_date - start_date).days + 1
    
    for single_date in pd.date_range(start_date, end_date):
        all_data.append({
            'Datum': single_date,
            'uebernachtungen': row['uebernachtungen'] / num_days
        })

# 4. Erstellen eines neuen DataFrame mit den täglichen Daten
fremdenverkehr_var2_daily = pd.DataFrame(all_data)

# 5. Anzeigen der ersten Zeilen des neuen DataFrames zur Überprüfung
print("Erste Zeilen der transformierten Daten:")
print(fremdenverkehr_var2_daily.head())

# 6. Löschen aller Zeilen ab Datum '2019-08-01' [da außerhalb des Zeitraums]
datum_zum_loeschen = '2019-08-01'
fremdenverkehr_var2_daily = fremdenverkehr_var2_daily[fremdenverkehr_var2_daily['Datum'] < datum_zum_loeschen]
datum_zum_loeschen_2 = '2013-04-29'
fremdenverkehr_var2_daily = fremdenverkehr_var2_daily[fremdenverkehr_var2_daily['Datum'] > datum_zum_loeschen_2]
print(fremdenverkehr_var2_daily.head())

# 7. Speichern des aktualisierten DataFrame als CSV-Datei im entsprechenden Ordner
pfad_zur_ausgabedatei = '/workspaces/UmsatzWetterBackereiKiel/0_DataPreparation/Ordnungsamt Kiel/CSV/Fremdenverkehr_Var2_daily.csv'
fremdenverkehr_var2_daily.to_csv(pfad_zur_ausgabedatei, index=False)


## Ermitteln des Einflusses der Ankuenfte auf den Umsatz