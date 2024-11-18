import csv
import re

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


def przelicz_czas_na_minuty(czas):
    """Przetwarza czas w formacie 'X godz. Y min Z s' lub 'X:Y:Z' na minuty."""
    if match := re.match(r'(\d+)\s*godz\.?\s*(\d+)\s*min\s*(\d+)\s*s', czas):
        godziny, minuty, sekundy = map(int, match.groups())
    elif match := re.match(r'(\d+):(\d+):(\d+)', czas):
        godziny, minuty, sekundy = map(int, match.groups())
    else:
        return 0  # Jeśli format jest niepoprawny

    return godziny * 60 + minuty + sekundy / 60


def sprawdz_obecnosc(czas, first_row=False):
    """Sprawdza, czy czas przekroczył 60 minut, zwraca 'Obecność' lub 'Nieobecność'.
    Jeśli to pierwszy wiersz, zwraca 'Frekwencja'."""

    if first_row:
        return "Frekwencja"  # Zwróć 'Frekwencja' dla pierwszego wiersza

    total_minutes = przelicz_czas_na_minuty(czas)
    return "Obecność" if total_minutes >= 60 else "Nieobecność"


def uczestnicy(data):
    """
    Przetwarza dane uczestników, rozdzielając imię i nazwisko oraz filtrując niepotrzebne wiersze.
    Dodaje również status obecności na podstawie czasu.
    """
    uczestnicy = []
    in_uczestnicy_section = False
    first_row_processed = False  # Flaga dla pierwszego wiersza

    for i, row in enumerate(data):
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
                obecność = sprawdz_obecnosc(row[3], first_row=True)  # Pierwszy wiersz
            else:
                # Standardowe przetwarzanie dla pozostałych wierszy
                imie, nazwisko = rozdziel_imie_nazwisko(row[0])
                obecność = sprawdz_obecnosc(row[3], first_row=False)  # Pozostałe wiersze

            # Ustawienie "-" w miejscach, gdzie brak danych
            imie = imie if imie != "" else "-"
            nazwisko = nazwisko if nazwisko != "" else "-"

            # Uzupełnianie pozostałych danych wiersza
            updated_row = [imie, nazwisko] + [item if item != "" else "-" for item in row[1:]] + [obecność]

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
