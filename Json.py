import json

class Json:
    def format(self, data, headers, output_file):
        json_data = [dict(zip(headers, row)) for row in data]
        with open(output_file, mode='w', encoding='utf-8') as jsonfile:
            json.dump(json_data, jsonfile, indent=4, ensure_ascii=False)
        print(f"Data exported to {output_file} in JSON format.")
