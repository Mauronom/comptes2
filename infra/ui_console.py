class UIConsole:
    def mostrar_moviments(self, moviments):
        for m in moviments:
            print(f"{m.data} | {m.concepte} | {m.import_:.2f} €")
