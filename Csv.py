import Csv

class CSV:
    def format(self, data, headers, output_file):
        with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = Csv.writer(csvfile)
            writer.writerow(headers)
            writer.writerows(data)
        print(f"Data exported to {output_file} in CSV format.")
