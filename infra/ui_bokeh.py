from collections import defaultdict

class UIBokeh:
    def mostrar_grafica(self, dades: dict):
        from bokeh.plotting import figure, show
        from bokeh.models import ColumnDataSource, HoverTool
        

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
                ("Balanç", "@y{0.00}"),
                ("Import", "@import_{0.00}"),
                ("Concepte", "@concepte"),
                ("Banc", "@banc"),
            ],
            formatters={
                "@x": "datetime",
                "@y": "numeral",
                "@import_": "numeral"
            },
            mode="vline"
        )
        p.add_tools(hover)

        p.legend.location = "top_left"
        p.legend.click_policy = "hide"

        show(p)
    
    def mostrar_grafica_categories(self, despeses_dict, estalvi, titol="Distribució d'Ingressos i Despeses", 
                               width=400, height=400):
        """
        Genera un diagrama circular amb les despeses (valors negatius) i ingressos (valor positiu)
        
        Args:
            despeses_dict (dict): Diccionari amb categories com a claus i quantitats negatives com a valors
            ingressos (float): Quantitat positiva d'ingressos
            titol (str): Títol del gràfic
            width (int): Amplada del gràfic
            height (int): Alçada del gràfic
            
        Returns:
            bokeh.plotting.figure: El gràfic de Bokeh
        """
        from bokeh.plotting import figure, show
        from bokeh.models import HoverTool
        from bokeh.transform import cumsum
        import pandas as pd
        import math
        # Preparar les dades
        data = {}
        
        # Convertir despeses a valors positius per al càlcul de percentatges
        despeses_positives = {k: abs(v) for k, v in despeses_dict.items()}
        
        # Afegir ingressos
        data['Estalvi'] = estalvi if estalvi > 0 else 0.0
        
        # Afegir despeses
        data.update(despeses_positives)
        
        # Calcular el total
        total = sum(data.values())
        
        # Crear DataFrame
        categories = list(data.keys())
        quantitats = list(data.values())
        percentatges = [round((q / total) * 100, 2) for q in quantitats]
        
        # Calcular angles per al diagrama circular
        angles = [round((q / total) * 2 * math.pi, 4) for q in quantitats]
        
        df = pd.DataFrame({
            'categoria': categories,
            'quantitat': quantitats,
            'percentatge': percentatges,
            'angle': angles,
            'color': self._generar_colors(len(categories))
        })
        
        # Calcular angles acumulatius
        df['angle_end'] = df['angle'].cumsum()
        df['angle_start'] = df['angle_end'] - df['angle']
        
        # Crear el gràfic
        p = figure(
            height=height, 
            width=width, 
            title=titol,
            toolbar_location=None,
            tools="",
            x_range=(-1.1, 1.1),
            y_range=(-1.1, 1.1)
        )
        
        # Eliminar eixos i graella
        p.axis.visible = False
        p.grid.visible = False
        
        # Crear sectors del diagrama circular
        p.wedge(
            x=0, y=0, 
            radius=1,
            start_angle='angle_start', 
            end_angle='angle_end',
            color='color',
            source=df,
            line_color="white",
            line_width=2
        )
        
        # Afegir hover tool
        hover = HoverTool(
            tooltips=[
                ("Categoria", "@categoria"),
                ("Quantitat", "@quantitat{0.00}€"),
                ("Percentatge", "@percentatge{0.00}%"),
            ]
        )
        p.add_tools(hover)
        show(p)
    
    def _generar_colors(self, num_colors):
        """Genera una llista de colors per al diagrama"""
        colors = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
            '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
            '#c49c94', '#f7b6d3', '#c7c7c7', '#dbdb8d', '#9edae5'
        ]
        
        # Si necessitem més colors, generar colors addicionals
        while len(colors) < num_colors:
            colors.extend(colors[:min(len(colors), num_colors - len(colors))])
            
        return colors[:num_colors]

# Exemple d'ús:
# from bokeh.plotting import figure, show

# ui = UIBokeh()
# despeses = {
#     'Alimentació': -500.50,
#     'Transport': -200.25,
#     'Habitatge': -800.00,
#     'Entreteniment': -150.75
# }
# estalvi = 2000.0

# ui.mostrar_grafica_categories(despeses, ingressos)
# Per mostrar: show(grafica) o curdoc().add_root(grafica)

