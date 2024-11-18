from tabulate import tabulate

class Console:
    def format(self, data, output_file=None):
        print(tabulate(data, tablefmt="grid"))
