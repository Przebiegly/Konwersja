import csv

def readcsv(file_path, encoding='utf-16', delimiter='\t'):
    """
    Wczytuje dane z pliku CSV.
    """
    data = []
    try:
        with open(file_path, encoding=encoding) as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"File {file_path} not found")
    return data


def rozdziel_imie_nazwisko(full_name):
    """
    Rozdziela pełne imię i nazwisko na dwie kolumny.
    """
    full_name = full_name.replace(" (Niezweryfikowany)", "").strip()
    parts = full_name.split()
    imie = parts[0] if len(parts) > 0 else "-"
    nazwisko = parts[1] if len(parts) > 1 else "-"
    return imie, nazwisko


def uczestnicy(data):
    """
    Przetwarza dane uczestników, rozdzielając imię i nazwisko oraz filtrując niepotrzebne wiersze.
    """
    uczestnicy = []
    in_uczestnicy_section = False
    first_row_processed = False  # Flaga dla pierwszego wiersza

    for row in data:
        if len(row) > 0 and row[0].startswith('2. Uczestnicy'):
            in_uczestnicy_section = True
            continue

        if in_uczestnicy_section:
            if len(row) == 0 or not any(row):
                break

            # Przetwarzanie pierwszego wiersza z "i" w imieniu i nazwisku
            if not first_row_processed:
                full_name = row[0].replace(" (Niezweryfikowany)", "").strip()
                if " i " in full_name:
                    parts = full_name.split(" i ")
                    imie = parts[0].strip() if len(parts) > 0 else "-"
                    nazwisko = parts[1].strip() if len(parts) > 1 else "-"
                else:
                    imie, nazwisko = rozdziel_imie_nazwisko(row[0])
                first_row_processed = True
            else:
                # Standardowe przetwarzanie dla pozostałych wierszy
                imie, nazwisko = rozdziel_imie_nazwisko(row[0])

            # Ustawienie "-" w miejscach, gdzie brak danych
            imie = imie if imie != "" else "-"
            nazwisko = nazwisko if nazwisko != "" else "-"

            # Uzupełnianie pozostałych danych wiersza
            updated_row = [imie, nazwisko] + [item if item != "" else "-" for item in row[1:]]

            # Dodanie przetworzonego wiersza do listy uczestników
            uczestnicy.append(updated_row)

    return uczestnicy


def zamien_kolejnosc_kolumn(data, priorytet):
    """
    Zamienia kolejność kolumn na podstawie priorytetu użytkownika ('Imię' lub 'Nazwisko').
    """
    if priorytet.lower() == "nazwisko":
        for row in data:
            if len(row) > 1:
                row[0], row[1] = row[1], row[0]
    return data
