import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Cargar los datos

file_id = "1PWTw-akWr59Gu7MoHra5WXMKwllxK9bp"
url = f"https://drive.google.com/uc?export=download&id={file_id}"

df = pd.read_csv(url)

# Inicializar la app
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Histograma de Tiempo de espera en días y Distribución de Especialidades Médicas en cada rango"),
    dcc.Graph(id='histogram', figure=px.histogram(
        df,
        x='DIFERENCIA_DIAS',
        nbins=30,
        title='Distribución de Diferencia de Días',
        labels={'DIFERENCIA_DIAS': 'Diferencia en Días'},
        template='plotly_white'
    )),
    dcc.Graph(id='pie-chart', figure=px.pie(
        names=[], values=[], title="Seleccione una barra en el histograma"
    ))
])

@app.callback(
    Output('pie-chart', 'figure'),
    Input('histogram', 'clickData')
)
def update_pie_chart(clickData):
    if clickData is None:
        return px.pie(names=[], values=[], title="Seleccione una barra en el histograma", height = 500)

    selected_bin = clickData['points'][0]['x']
    bin_start = selected_bin - 0.5
    bin_end = selected_bin + 0.5
    filtered_df = df[(df['DIFERENCIA_DIAS'] >= bin_start) & (df['DIFERENCIA_DIAS'] < bin_end)]
    
    top_especialidades = (
        filtered_df['ESPECIALIDAD']
        .value_counts()
        .nlargest(5)
    )
    
    filtered_df['ESPECIALIDAD_AGRUPADA'] = filtered_df['ESPECIALIDAD'].apply(
        lambda x: x if x in top_especialidades.index else 'Otras'
    )
    
    grouped = filtered_df['ESPECIALIDAD_AGRUPADA'].value_counts().reset_index()
    grouped.columns = ['ESPECIALIDAD', 'CUENTA']
    return px.pie(
        grouped,
        names='ESPECIALIDAD',
        values = "CUENTA",
        title=f"Top 5 Especialidades para un tiempo de espera de {bin_start} a {bin_end} días",
        height=600
     )

if __name__ == '__main__':
      app.run_server(debug=True)
