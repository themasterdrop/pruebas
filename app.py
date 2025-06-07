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

def clasificar_rango(dias):
    if dias < 10:
        return "0-9"
    elif dias < 20:
        return "10-19"
    elif dias < 30:
        return "20-29"
    elif dias < 40:
        return "30-39"
    elif dias < 50:
        return "40-49"
    elif dias < 60:
        return "50-59"
    elif dias < 70:
        return "60-69"
    elif dias < 80:
        return "70-79"
    elif dias < 90:
        return "80-89"    

df['RANGO_DIAS'] = df['DIFERENCIA_DIAS'].apply(clasificar_rango)



app.layout = html.Div([
    html.H1("Histograma de Tiempo de espera en días y Distribución de Especialidades Médicas en cada rango"),
    dcc.Graph(id='histogram', figure=px.histogram(
        df,
        x='RANGO_DIAS',
        category_orders={'RANGO_DIAS': ["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89"]},
        title='Distribución de la Cantidad de Pacientes según su Tiempo de Espera',
        labels={'RANGO_DIAS': 'Rango de Días'},
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

    
    selected_range = clickData['points'][0]['x']
    filtered_df = df[df['RANGO_DIAS'] == selected_range]

    
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
        title=f"Top 5 Especialidades para un tiempo de espera de {selected_range} días",
        height=600
     )

if __name__ == '__main__':
      app.run_server(debug=True)
