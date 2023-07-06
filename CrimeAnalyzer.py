import requests
import csv
import pandas as pd
import matplotlib.pyplot as plt
import calendar
import folium

class CrimeAnalyzer:
    # Definisco il costruttore
    def __init__(self, url, path, report_path):
        self.url = url
        self.path = path
        self.report_path = report_path
        self.crimes = None
        
    # Definisco i metodi
    
    def download_csv(self):
        response = requests.get(self.url) # Invio richiesta al server
        lines = response.text.strip().split('\n') # Prendo la risposta del server e la sostituisco da stringa a lista
        data = csv.reader(lines) # Creo un oggetto csv che legge la lista
        
        # Apro il file in scrittura
        with open(self.path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def read_data(self):
        self.crimes = pd.read_csv(self.path)

    # Pulisco i dati
    def clean_data(self):
        
        nuove_colonne_diz = {
            'DR_NO': 'ID',
            'Date Rptd': 'Data Segn',
            'DATE OCC': 'Data Avv',
            'TIME OCC': 'Ora Avv',
            'AREA': 'Zona',
            'AREA NAME': 'Nome Zona',
            'Rpt Dist No': 'Distr Num Segn ',
            'Part 1-2': 'Part 1-2',
            'Crm Cd': 'Tipo Crimine Numero',
            'Crm Cd Desc': 'Tipo Crimine Desc',
            'Mocodes': 'Modus Operandi',
            'Vict Age': 'Eta Vittima',
            'Vict Sex': 'Sesso Vittima',
            'Vict Descent': 'Etnia Vittima',
            'Premis Cd': 'Premessa Numero',
            'Premis Desc': 'Premessa Desc',
            'Weapon Used Cd': 'Arma Usata Numero',
            'Weapon Desc': 'Arma Usata Desc',
            'Status': 'Stato',
            'Status Desc': 'Stato Desc',
            'Crm Cd 1': 'Codice Crimine 1',
            'Crm Cd 2': 'Codice Crimine 2',
            'Crm Cd 3': 'Codice Crimine 3',
            'Crm Cd 4': 'Codice Crimine 4',
            'LOCATION': 'Luogo',
            'Cross Street': 'Strada',
            'LAT': 'LAT',
            'LON': 'LON'
        }

        self.crimes = self.crimes.rename(columns=nuove_colonne_diz)
        self.crimes["Etnia Vittima"] = self.crimes["Etnia Vittima"].replace(["H","W","B","O","A","X","K","F","C","J","V","I","Z","P","U","D","G","L","S"],["Ispanico","Caucasico","Di colore","Altro","Asiatico","Sconosciuto","Koreano","Filippino","Cinese","Giapponese","Vietnamita","Nativo Americano","Isolano del Pacifico","Isolano del Pacifico - Samoano","Hawaiano","Cambogiano","Guamaniano","Laotiano","Indo-asiatico"])
        self.crimes = self.crimes[self.crimes['Eta Vittima'] != 0]
        self.crimes['Sesso Vittima'] = self.crimes['Sesso Vittima'].replace(['H', 'X'], 'Other')

    # Stampo le informazioni del Dataframe
    def print_data_info(self):
        print(self.crimes.head())
        print(self.crimes.columns)
        print(self.crimes.shape)
        print(self.crimes.dtypes)

    def analyze_crime_frequency(self):
        print("Drequenza Crimini")
        crime_frequency = self.crimes['Tipo Crimine Desc'].value_counts()
        print(crime_frequency)

    def analyze_temporal_data(self):
        # Trasformiamo la data nel formato %m/%d/%Y %I:%M:%S %p
        self.crimes['Data Segn'] = pd.to_datetime(self.crimes['Data Segn'], format='%m/%d/%Y %I:%M:%S %p')
         
        # Estraiamo il mese e salviamo nella colonna "Mese"
        self.crimes['Mese'] = self.crimes['Data Segn'].dt.month
        
        # Contiamo i valori unici in "Mese" e li ordiniamo
        monthly_crime_count = self.crimes['Mese'].value_counts().sort_index()
        
        # Uso una list comprehension per trasformare i mesi da numeri a string
        month_names = [calendar.month_name[i] for i in range(1, 13)] 
        
        # Assegniamo la lista dei mesi all'indice al posto dei numeri
        monthly_crime_count.index = month_names

        monthly_crime_count.plot(kind='bar', xlabel='Mese', ylabel='Numero di Crimini')
        plt.show()

    def analyze_victim_demographics(self):
        victim_age_distribution = self.crimes['Eta Vittima'].plot.hist(bins=20)
        plt.xlabel('Età')
        plt.ylabel('Frequenza')
        plt.title("Distribuzione dell' età delle vittime")
        plt.show()

        victim_gender_distribution = self.crimes['Sesso Vittima'].value_counts()
        print(victim_gender_distribution)

    def analyze_crime_status(self):
        crime_status_distribution = self.crimes['Stato Desc'].value_counts()
        print(crime_status_distribution)

    def analyze_premise_and_weapon(self):
        premise_distribution = self.crimes['Premessa Desc'].value_counts()
        print(premise_distribution)

        weapon_distribution = self.crimes['Arma Usata Desc'].value_counts()
        print(weapon_distribution)

    def analyze_crime_vs_age(self):
        crime_vs_age = self.crimes.groupby('Tipo Crimine Desc')['Eta Vittima'].mean()
        print(crime_vs_age)

    def analyze_victim_gender_distribution(self):
        sex_counts = self.crimes['Sesso Vittima'].value_counts()

        labels = sex_counts.index
        counts = sex_counts.values

        plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title('Distribuzione del sesso delle vittime')
        plt.show()
        
        
    def plot_crime_map(self):
        
        # Filtriamo le righe con valori mancanti per la latitudine e la longitudine
        locations = self.crimes[['LAT', 'LON']].dropna()

        # Scegliamo un sottoinsieme di 100 righe
        subset = locations.head(100)

        # Creiamo una mappa centrata su Los Angeles
        crime_map = folium.Map(location=[34.0522, -118.2437], zoom_start=13)

        # Aggiungiamo i punti alla mappa
        for _, crime in subset.iterrows():
            lat, lon = crime['LAT'], crime['LON']
            folium.Marker(location=[lat, lon]).add_to(crime_map)

        # Salviamo la mappa come file html
        crime_map.save('data/crime_map.html')
        
        
        
    def plot_ethnicity_histogram(self):
        etnia_count = self.crimes['Etnia Vittima'].value_counts()
        etnia_count.plot(kind='bar', xlabel='Etnia Vittima', ylabel='Numero di Crimini')
        plt.title('Distribuzione delle Etnie delle Vittime')
        plt.show()
  

    def report_file(self):
        
        #impostazione di visualizzazione massima righe
        pd.set_option('display.max_rows', None)
        
        report_data = {
            'Distribuzione Sesso Vittime': self.crimes['Sesso Vittima'].value_counts(),
            'Distribuzione Stato dei crimini': self.crimes['Stato Desc'].value_counts(),
            'Distribuzione delle premesse': self.crimes['Premessa Desc'].value_counts(),
            'Distribuzione Armi Usate': self.crimes['Arma Usata Desc'].value_counts()
        }

        with open(self.report_path, 'w') as file:
            for section, data in report_data.items():
                file.write(f'{section}:\n')
                file.write(f'{data}\n\n')

        print(f"Creato il file di report: {self.report_path}")

    
    # Richiamiamo i metodi per elaborare i dati
    def process_data(self):
        self.download_csv()
        self.read_data()
        self.clean_data()
        self.print_data_info()
        self.analyze_crime_frequency()
        self.analyze_temporal_data()
        self.analyze_victim_demographics()
        self.analyze_crime_status()
        self.analyze_premise_and_weapon()
        self.analyze_crime_vs_age()
        self.analyze_victim_gender_distribution()
        self.plot_ethnicity_histogram()
        self.plot_crime_map()
        self.report_file()


#Istanziamo la classe CrimeAnalyzer e elaboro i dati
url = 'https://data.lacity.org/api/views/2nrs-mtv8/rows.csv?accessType=DOWNLOAD'
path = 'data/crimes.csv'
report_path = 'data/crime_report.txt'
analyzer = CrimeAnalyzer(url, path, report_path)
analyzer.process_data()