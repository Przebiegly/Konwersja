from Csv import CSV
from Json import Json
from Xml import Xml
from Console import Console
from Functions import readcsv, uczestnicy, zamien_kolejnosc_kolumn

def main():
    # Wczytaj dane
    file_path = 'plik.csv'
    csv_data = readcsv(file_path)
    uczestnicy_data = uczestnicy(csv_data)

    # Pytanie o priorytet kolumn
    print("Co chcesz, aby było w pierwszej kolumnie? [Imię/Nazwisko]")
    priorytet = input("Twój wybór: ").strip()

    if priorytet.lower() in ["imię", "nazwisko"]:
        uczestnicy_data = zamien_kolejnosc_kolumn(uczestnicy_data, priorytet)
    else:
        print("Nieprawidłowy wybór. Domyślnie przyjęto 'Imię' jako pierwszą kolumnę.")

    print("Wybierz format wyjściowy: [1] CSV, [2] JSON, [3] XML, [4] Console")
    choice = input("Twój wybór: ")

    exporter = None
    if choice == "1":
        exporter = CSV()
        output_file = 'output.csv'
    elif choice == "2":
        exporter = Json()
        output_file = 'output.json'
    elif choice == "3":
        exporter = Xml()
        output_file = 'output.xml'
    elif choice == "4":
        exporter = Console()
        output_file = None
    else:
        print("Nieprawidłowy wybór.")
        return

    # Eksport danych
    if exporter:
        exporter.format(uczestnicy_data, output_file)

if __name__ == "__main__":
    main()
