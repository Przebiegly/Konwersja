from Csv import CSV
from Json import Json
from Xml import Xml
from Console import Console
from Functions import readcsv, uczestnicy, rozdziel_imie_nazwisko

def main():
    # Wczytaj dane
    file_path = 'plik.csv'
    csv_data = readcsv(file_path)
    uczestnicy_data = uczestnicy(csv_data)

    # Rozdziel imiona i nazwiska
    uczestnicy_z_imieniem_i_nazwiskiem = []
    for row in uczestnicy_data:
        # Zakładając, że pełne imię i nazwisko jest w 1. kolumnie
        imie, nazwisko = rozdziel_imie_nazwisko(row[0])  # Rozdziel imię i nazwisko
        # Jeśli mamy "-" w imieniu lub nazwisku, oznacza to, że osoba została pominięta
        if imie == "-" and nazwisko == "-":
            continue  # Pomijamy taki wiersz

        # Tworzymy nowy wiersz, zastępując pełne imię i nazwisko na dwie kolumny
        updated_row = [imie, nazwisko] + row[1:]  # Dodaj resztę danych po imieniu i nazwisku
        uczestnicy_z_imieniem_i_nazwiskiem.append(updated_row)

    # Nagłówki tabeli
    headers = ["Imię", "Nazwisko", "Pierwsze dołączenie", "Ostatnie wyjście",
               "Czas udziału w spotkaniu", "Adres e-mail", "Identyfikator uczestnika (UPN)", "Rola"]

    # Wybór formatu
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
        exporter.format(uczestnicy_z_imieniem_i_nazwiskiem, headers, output_file)

if __name__ == "__main__":
    main()
