import streamlit as st
import pandas as pd
from datetime import datetime
from typing import List, Any

class UIStreamlitGrafica:
    """UI Streamlit per gestió de moviments bancaris amb arquitectura hexagonal."""
    
    def __init__(self, repositori_moviments):
        self._repositori = repositori_moviments
        self._moviments = []
        self._cas_us_grafica_balance = None
        self._cas_us_grafica_imports = None
        self._cas_us_filtrar_moviments = None
        
    def set_casos_us(self, cas_us_grafica_balance, cas_us_grafica_imports, cas_us_filtrar_moviments):
        """Injecció de dependències dels casos d'ús."""
        self._cas_us_grafica_balance = cas_us_grafica_balance
        self._cas_us_grafica_imports = cas_us_grafica_imports
        self._cas_us_filtrar_moviments = cas_us_filtrar_moviments

    def mostrar_moviments(self, moviments):
        """Mètode perquè el cas d'ús IniciarAplicació li passi els moviments."""
        self._moviments = moviments
        # En Streamlit, les dades es mostren quan es crida run()

    def print(self, info):
        """Equivalent al print anterior, ara usa st.info o st.write."""
        st.info(str(info))

    def _crear_dataframe(self, moviments):
        """Converteix els moviments en DataFrame per Streamlit."""
        if not moviments:
            return pd.DataFrame()
            
        data = []
        for m in moviments:
            data.append({
                'Data': m.data,
                'Concepte': m.concepte,
                'Import (€)': f"{m.import_:.2f}",
                'Import_num': m.import_,  # Per gràfiques
                'Balance': m.balance,
                'Banc': m.banc
            })
        return pd.DataFrame(data)

    def _mostrar_grafica_balance(self, moviments):
        """Genera gràfica de balance."""
        if not moviments:
            return None
            
        df = self._crear_dataframe(moviments)
        fig = px.line(
            df, 
            x='Data', 
            y='Balance',
            title='Evolució del Balance',
            labels={'Balance': 'Balance (€)', 'Data': 'Data'}
        )
        fig.update_traces(line_color='#1f77b4', line_width=3)
        fig.update_layout(
            hovermode='x unified',
            xaxis_title='Data',
            yaxis_title='Balance (€)'
        )
        return fig

    def _mostrar_grafica_imports(self, moviments):
        """Genera gràfica d'imports."""
        if not moviments:
            return None
            
        df = self._crear_dataframe(moviments)
        
        # Separar ingressos i despeses
        df_ingressos = df[df['Import_num'] > 0]
        df_despeses = df[df['Import_num'] < 0]
        
        fig = go.Figure()
        
        if not df_ingressos.empty:
            fig.add_trace(go.Bar(
                x=df_ingressos['Data'],
                y=df_ingressos['Import_num'],
                name='Ingressos',
                marker_color='green',
                text=df_ingressos['Concepte'],
                textposition='auto'
            ))
            
        if not df_despeses.empty:
            fig.add_trace(go.Bar(
                x=df_despeses['Data'],
                y=df_despeses['Import_num'],
                name='Despeses',
                marker_color='red',
                text=df_despeses['Concepte'],
                textposition='auto'
            ))

        fig.update_layout(
            title='Ingressos vs Despeses',
            xaxis_title='Data',
            yaxis_title='Import (€)',
            hovermode='x unified'
        )
        return fig

    def run(self):
        """Mètode principal per executar la UI."""
        st.set_page_config(
            page_title="Gestió Moviments Bancaris",
            page_icon="💰",
            layout="wide"
        )
        
        # Títol principal
        st.title("💰 Gestió de Moviments Bancaris")
        
        # Sidebar per filtres i controls
        with st.sidebar:
            st.header("Filtres i Controls")
            
            # Filtre de text
            filtre_text = st.text_input(
                "Filtrar per concepte:",
                key="filtre_concepte",
                help="Escriu per filtrar els moviments"
            )
            
            # Botó per recarregar dades
            if st.button("🔄 Recarregar dades"):
                st.rerun()
            
            # Filtres addicionals
            st.subheader("Filtres avançats")
            
            if self._moviments:
                df = self._crear_dataframe(self._moviments)
                
                # Filtre per banc
                bancs_unics = df['Banc'].unique().tolist()
                banc_seleccionat = st.selectbox(
                    "Selecciona banc:",
                    ['Tots'] + bancs_unics
                )
                
                # Filtre per rang de dates
                if not df.empty and 'Data' in df.columns:
                    dates = pd.to_datetime(df['Data'])
                    data_min = dates.min().date()
                    data_max = dates.max().date()
                    
                    rang_dates = st.date_input(
                        "Rang de dates:",
                        value=(data_min, data_max),
                        min_value=data_min,
                        max_value=data_max
                    )

        # Aplicar filtres si hi ha casos d'ús definits
        moviments_filtrats = self._moviments.copy()
        
        if filtre_text and self._cas_us_filtrar_moviments:
            # Aquí cridaríem el cas d'ús de filtrar
            # moviments_filtrats = self._cas_us_filtrar_moviments.execute(filtre_text)
            # Per ara, filtre simple:
            moviments_filtrats = [
                m for m in self._moviments 
                if filtre_text.lower() in m.concepte.lower()
            ]

        # Contingut principal
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.header("📊 Taula de Moviments")
            
            if moviments_filtrats:
                df = self._crear_dataframe(moviments_filtrats)
                
                # Mostrar mètriques
                col_met1, col_met2, col_met3 = st.columns(3)
                with col_met1:
                    total_ingressos = sum(m.import_ for m in moviments_filtrats if m.import_ > 0)
                    st.metric("Total Ingressos", f"{total_ingressos:.2f} €")
                    
                with col_met2:
                    total_despeses = sum(m.import_ for m in moviments_filtrats if m.import_ < 0)
                    st.metric("Total Despeses", f"{total_despeses:.2f} €")
                    
                with col_met3:
                    balance_final = total_ingressos + total_despeses
                    st.metric("Balance Net", f"{balance_final:.2f} €", 
                             delta=f"{balance_final:.2f} €")
                
                # Taula interactiva
                st.dataframe(
                    df[['Data', 'Concepte', 'Import (€)', 'Balance', 'Banc']],
                    use_container_width=True,
                    hide_index=True
                )
                
                # Descarregar dades
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Descarregar CSV",
                    data=csv,
                    file_name=f"moviments_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
                
            else:
                st.info("No hi ha moviments per mostrar.")

        with col2:
            st.header("⚙️ Accions")
            
            # Botons per gràfiques
            if st.button("📈 Mostrar gràfica de balance", use_container_width=True):
                if self._cas_us_grafica_balance:
                    self._cas_us_grafica_balance.execute(moviments_filtrats)
                
            if st.button("📊 Mostrar gràfica d'imports", use_container_width=True):
                if self._cas_us_grafica_imports:
                    self._cas_us_grafica_imports.execute(moviments_filtrats)

        # Gràfiques - mostrar les que estan guardades al session_state
        if moviments_filtrats:
            st.header("📈 Gràfiques")
            
            # Mostrar gràfica de balance si existeix
            if hasattr(st.session_state, 'grafica_balance') and st.session_state.grafica_balance:
                st.subheader("Evolució del Balance")
                self._mostrar_grafica_bokeh(st.session_state.grafica_balance)
                
            # Mostrar gràfica d'imports si existeix  
            if hasattr(st.session_state, 'grafica_imports') and st.session_state.grafica_imports:
                st.subheader("Ingressos vs Despeses")
                self._mostrar_grafica_bokeh(st.session_state.grafica_imports)
                
            # Si no hi ha gràfiques, mostrar missatge
            if not (hasattr(st.session_state, 'grafica_balance') or hasattr(st.session_state, 'grafica_imports')):
                st.info("👆 Fes clic als botons de dalt per generar les gràfiques")

# Adaptador per inicialitzar la UI amb Streamlit
class StreamlitUIAdapter:
    """Adaptador per integrar la UI Streamlit amb l'arquitectura hexagonal."""
    
    def __init__(self, repositori_moviments):
        self.ui = UIStreamlitGrafica(repositori_moviments)
        
    def set_casos_us(self, cas_us_grafica_balance, cas_us_grafica_imports, cas_us_filtrar_moviments):
        self.ui.set_casos_us(cas_us_grafica_balance, cas_us_grafica_imports, cas_us_filtrar_moviments)
        
    def mostrar_moviments(self, moviments):
        self.ui.mostrar_moviments(moviments)
        
    def executar(self):
        """Inicia l'aplicació Streamlit."""
        self.ui.run()

# Exemple d'ús (main.py):
"""
if __name__ == "__main__":
    # Configuració de dependències
    repositori = RepositoriMoviments()
    
    # UI
    ui = StreamlitUIAdapter(repositori)
    
    # Casos d'ús - IMPORTANT: passen la UI com a dependència
    cas_us_grafica_balance = MostrarGraficaBalance(ui.ui)  # ← Injectar la UI
    cas_us_grafica_imports = MostrarGraficaImports(ui.ui)   # ← Injectar la UI
    cas_us_filtrar = CasUsFiltrarMoviments()
    
    # Configurar casos d'ús
    ui.set_casos_us(cas_us_grafica_balance, cas_us_grafica_imports, cas_us_filtrar)
    
    # Carregar dades inicials
    moviments = repositori.obtenir_tots()
    ui.mostrar_moviments(moviments)
    
    # Executar aplicació
    ui.executar()
"""