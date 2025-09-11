from collections import defaultdict
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool

class UIBokeh:
    def mostrar_grafica(self, dades: dict):
        punts = dades["punts"]
        etiqueta_x = dades["etiqueta_x"]
        etiqueta_y = dades["etiqueta_y"]

        if not punts:
            print("No hi ha dades per mostrar")
            return

        # Agrupar punts per banc
        per_banc = defaultdict(list)
        for dt, balance, banc, concepte, import_ in punts:
            # Convertim Decimal -> float
            per_banc[banc].append((dt, float(balance), concepte, float(import_)))

        # Crear la figura
        p = figure(
            x_axis_type="datetime",
            width=1800,
            height=900,
            title="Evolució per banc",
            tools="pan,wheel_zoom,box_zoom,reset,save"
        )
        p.xaxis.axis_label = etiqueta_x
        p.yaxis.axis_label = etiqueta_y

        colors = ["blue", "red", "green", "orange", "purple", "brown"]
        for i, (banc, punts_banc) in enumerate(per_banc.items()):
            punts_banc.sort(key=lambda p: p[0])
            x = [p[0] for p in punts_banc]
            y = [p[1] for p in punts_banc]
            conceptes = [p[2] for p in punts_banc]
            import_s = [p[3] for p in punts_banc]

            source = ColumnDataSource(data={"x": x, "y": y, "banc": [banc]*len(x), "concepte": conceptes, "import_": import_s})

            p.line("x", "y", source=source, line_width=2, color=colors[i % len(colors)], legend_label=banc)
            p.circle("x", "y", source=source, size=6, color=colors[i % len(colors)], legend_label=banc)

        hover = HoverTool(
            tooltips=[
                ("Data", "@x{%F %H:%M}"),
                ("Balanç", "@y"),
                ("Import", "@import_"),
                ("Concepte", "@concepte"),
                ("Banc", "@banc"),
            ],
            formatters={"@x": "datetime"},
            mode="vline"
        )
        p.add_tools(hover)

        p.legend.location = "top_left"
        p.legend.click_policy = "hide"

        show(p)
