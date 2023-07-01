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
        self.crimes = self.crimes[self.crimes['Vict Age'] != 0]
        self.crimes['Vict Sex'] = self.crimes['Vict Sex'].replace(['H', 'X'], 'Other')

    # Stampo le informazioni del Dataframe
    def print_data_info(self):
        print(self.crimes.head())
        print(self.crimes.columns)
        print(self.crimes.shape)
        print(self.crimes.dtypes)

    def analyze_crime_frequency(self):
        print("Crime Frequency")
        crime_frequency = self.crimes['Crm Cd Desc'].value_counts()
        print(crime_frequency)

    def analyze_temporal_data(self):
        self.crimes['Date Rptd'] = pd.to_datetime(self.crimes['Date Rptd'], format='%m/%d/%Y %I:%M:%S %p')
        self.crimes['Month'] = self.crimes['Date Rptd'].dt.month
        monthly_crime_count = self.crimes['Month'].value_counts().sort_index()
        
        # Uso una list comprehension per trasformare i mesi da numeri a string
        month_names = [calendar.month_name[i] for i in range(1, 13)] 
        monthly_crime_count.index = month_names

        monthly_crime_count.plot(kind='bar', xlabel='Month', ylabel='Number of Crimes')
        plt.show()

    def analyze_victim_demographics(self):
        victim_age_distribution = self.crimes['Vict Age'].plot.hist(bins=20)
        plt.xlabel('Age')
        plt.ylabel('Frequency')
        plt.title('Distribution of Victim Ages')
        plt.show()

        victim_gender_distribution = self.crimes['Vict Sex'].value_counts()
        print(victim_gender_distribution)

    def analyze_crime_status(self):
        crime_status_distribution = self.crimes['Status Desc'].value_counts()
        print(crime_status_distribution)

    def analyze_premise_and_weapon(self):
        premise_distribution = self.crimes['Premis Desc'].value_counts()
        print(premise_distribution)

        weapon_distribution = self.crimes['Weapon Desc'].value_counts()
        print(weapon_distribution)

    def analyze_crime_vs_age(self):
        crime_vs_age = self.crimes.groupby('Crm Cd Desc')['Vict Age'].mean()
        print(crime_vs_age)

    def analyze_victim_gender_distribution(self):
        sex_counts = self.crimes['Vict Sex'].value_counts()

        labels = sex_counts.index
        counts = sex_counts.values

        plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title('Distribution of Crime Victims by Gender')
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

    def report_file(self):
        
        #impostazione di visualizzazione massima righe
        pd.set_option('display.max_rows', None)
        
        report_data = {
            'Victim Gender Distribution': self.crimes['Vict Sex'].value_counts(),
            'Crime Status Distribution': self.crimes['Status Desc'].value_counts(),
            'Premise Distribution': self.crimes['Premis Desc'].value_counts(),
            'Weapon Distribution': self.crimes['Weapon Desc'].value_counts()
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
        self.plot_crime_map()
        self.report_file()


#Istanziamo la classe CrimeAnalyzer e elaboro i dati
url = 'https://data.lacity.org/api/views/2nrs-mtv8/rows.csv?accessType=DOWNLOAD'
path = 'data/crimes.csv'
report_path = 'data/crime_report.txt'
analyzer = CrimeAnalyzer(url, path, report_path)
analyzer.process_data()