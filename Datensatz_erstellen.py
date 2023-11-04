import os
import pandas as pd

xlsx_path = 'Bildervorbearbeitung/Bilder/xlsx'

# Erstellen Sie einen leeren DataFrame, um die kombinierten Daten aufzunehmen
combined_data = pd.DataFrame(columns=['Bildname', 'Porositaet'])

# Verzeichnispfad, in dem Ihre kleinen Excel-Dateien gespeichert sind
xlsx_path = 'Bildervorbearbeitung/Bilder/xlsx'  

# Durchlaufen Sie die Dateien im Verzeichnis
for filename in os.listdir(xlsx_path):
    if filename.endswith('.xlsx'):  # Stellen Sie sicher, dass es sich um Excel-Dateien handelt
        # Vollständigen Pfad zur aktuellen Datei erstellen
        file_path = os.path.join(xlsx_path, filename)
        
        # Laden Sie die Daten aus der aktuellen Datei in einen DataFrame
        data = pd.read_excel(file_path)
        
        # Fügen Sie die Daten zum kombinierten DataFrame hinzu
        combined_data = combined_data.append(data, ignore_index=True)

# Speichern Sie die kombinierten Daten in einer neuen Excel-Datei oder verwenden Sie sie wie gewünscht
combined_data.to_excel('import_data.xlsx', index=False)