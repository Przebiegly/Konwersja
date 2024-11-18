import json

class Json:
    def format(self, data, output_file):
        with open(output_file, mode='w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=4, ensure_ascii=False)
        print(f"Dane wyeksportowane do pliku {output_file} w formacie JSON.")


# https://docs.python.org/3/library/json.html