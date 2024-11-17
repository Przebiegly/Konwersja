from tabulate import tabulate

class Console:
    def format(self, data, headers, output_file=None):
        print(tabulate(data, headers=headers, tablefmt="grid"))
