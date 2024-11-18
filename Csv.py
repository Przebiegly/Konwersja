import csv

class CSV:
    def format(self, data, output_file):
        with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
        print(f"Dane wyeksportowane do pliku {output_file} w formacie CSV.")


# https://docs.python.org/3/library/csv.html