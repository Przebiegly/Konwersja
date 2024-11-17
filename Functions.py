import csv

def readcsv(file_path):
    data = []
    try:
        with open(file_path, encoding='utf-16') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"File {file_path} not found")
    return data


def uczestnicy(data):
    uczestnicy = []
    in_uczestnicy_section = False

    for row in data:
        if len(row) > 0 and row[0].startswith('2. Uczestnicy'):
            in_uczestnicy_section = True
            continue

        if in_uczestnicy_section:
            if len(row) == 0 or not any(row):  # Stop if an empty row or all cells are empty
                break
            uczestnicy.append(row)

    return uczestnicy




def rozdziel_imie_nazwisko(full_name):
    """
    Rozdziela pełne imię i nazwisko na dwie kolumny.
    Jeśli nazwisko jest nieobecne, wstawia '-' jako nazwisko.
    Jeśli w imieniu lub nazwisku występuje 'Niezweryfikowany', ignoruje tę część.
    """
    # Usuń frazę '(Niezweryfikowany)' z pełnego imienia i nazwiska
    full_name = full_name.replace(" (Niezweryfikowany)", "")

    # Rozdzielamy pełne imię i nazwisko na części
    parts = full_name.split()
    imie = parts[0] if len(parts) > 0 else "-"
    nazwisko = parts[1] if len(parts) > 1 else "-"

    return imie, nazwisko

