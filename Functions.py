import csv
import re


def readcsv(file_path, encoding='utf-16', delimiter='\t'): # Funkcja otwiera plik CSV, odczytuje jego zawartość i zapisuje do listy.

    data = []
    try:
        with open(file_path, encoding=encoding) as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"File {file_path} not found")
    return data


def rozdziel_imie_nazwisko(full_name):  # Rozdziela pełne imię i nazwisko na dwie kolumny.

    full_name = full_name.replace(" (Niezweryfikowany)", "").strip()

    if " i " in full_name: # Obsługuje przypadek, gdy imię i nazwisko są połączone za pomocą 'i'
        parts = full_name.split(" i ")
        imie = parts[0].strip() if len(parts) > 0 else "-"
        nazwisko = parts[1].strip() if len(parts) > 1 else "-"
    else:
        # Jeśli nie ma 'i', traktujemy pierwszy element jako imię, a drugi jako nazwisko
        parts = full_name.split()
        imie = parts[0] if len(parts) > 0 else "-"
        nazwisko = parts[1] if len(parts) > 1 else "-"

    return imie, nazwisko


def przelicz_czas_na_minuty(czas):      # przelicza czas
    if match := re.match(r'(\d+)\s*godz\.?\s*(\d+)\s*min\s*(\d+)\s*s', czas):
        godziny, minuty, sekundy = map(int, match.groups())  # Konwertuje godziny, minuty i sekundy na liczby
    else:
        return 0  # Jeśli format jest niepoprawny, zwróć 0

    return godziny * 60 + minuty + sekundy / 60 # Przelicza czas na minuty


def sprawdz_obecnosc(czas, first_row=False): # Sprawdza, czy czas przekroczył 60 minut, zwraca 'Obecność' lub 'Nieobecność'

    if first_row:
        return "Frekwencja"  # Dla pierwszego zwraca Frekwencja (naglowek kolumny)

    total_minutes = przelicz_czas_na_minuty(czas)     # Przelicza czas na minuty kozysta wlasnie z funcki przelicz_czas_na_minuty
    return "Obecność" if total_minutes >= 60 else "Nieobecność"


def uczestnicy(data): #Przetwarza dane uczestników
    uczestnicy = []
    in_uczestnicy_section = False  # aby mie tylko sekcje Uczestnicy
    first_row_processed = False   # aby pierszwy wiersz dodstal inna nazwe

    for i, row in enumerate(data):  # Iteracja po wszystkich wierszach danych
        if len(row) > 0 and row[0].startswith('2. Uczestnicy'):
            in_uczestnicy_section = True
            continue

        if in_uczestnicy_section:  # Przetwarzamy tylko wiersze w sekcji uczestników
            if len(row) == 0 or not any(row):  # Zatrzymuje sie, jeśli napotkamy pusty wiersz ( by nie bralo wiecej z csv)
                break

            # Przetwarzanie imienia i nazwiska
            imie, nazwisko = rozdziel_imie_nazwisko(row[0])  # Wywołujemy funkcję ktora jest powyżej

            # Przetwarzanie obecności
            if not first_row_processed:
                first_row_processed = True  # aby pierszwy wiersz dodstal inna nazwe
                obecność = sprawdz_obecnosc(row[3], first_row=True)  # Pierwszy wiersz dostaje specjalną wartość 'Frekwencja'
            else:
                obecność = sprawdz_obecnosc(row[3], first_row=False)  # Pozostałe wiersze maja obecnosc

            # Uzupełniamy dane w wierszu, a w ostatniej kolumnie dodajemy status obecności
            updated_row = [imie, nazwisko] + [item if item != "" else "-" for item in row[1:]] + [obecność]

            uczestnicy.append(updated_row)

    return uczestnicy

def zamien_kolejnosc_kolumn(data, priorytet):  #Zamienia kolejność kolumn na podstawie priorytetu użytkownika ('Imię' lub 'Nazwisko').

    if priorytet.lower() == "nazwisko":
        for row in data:
            row[0], row[1] = row[1], row[0] # Zamieniamy kolejność kolumn: imię <-> nazwisko
    return data
