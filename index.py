import dash
from dash import dcc, html
import pandas as pd
from app import *

# Load the CSV data
df = pd.read_csv(r'C:\Users\hvell\Desktop\cesupa\banco_dados\dadostratados.csv', delimiter = ';')

# Print column names to identify the correct column name
print(df.columns)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Preserved Specimen Dashboard"),
    
    # Dropdown for selecting species
    dcc.Dropdown(
        id='species-dropdown',
        options=[{'label': species, 'value': species} for species in df['YourCorrectColumnName']],  # Replace 'YourCorrectColumnName' with the actual column name
        value=df['YourCorrectColumnName'].iloc[0],  # Replace 'YourCorrectColumnName' with the actual column name
        multi=True,
        placeholder="Select species"
    ),
    
    # Scatter plot for coordinates
    dcc.Graph(
        id='scatter-plot',
        figure={
            'data': [
                {'x': df[df['YourCorrectColumnName'] == species]['longitude'], 'y': df[df['YourCorrectColumnName'] == species]['latitude'],
                 'text': df[df['YourCorrectColumnName'] == species]['eventRemarks'], 'mode': 'markers', 'name': species}
                for species in df['YourCorrectColumnName'].unique()  # Replace 'YourCorrectColumnName' with the actual column name
            ],
            'layout': {'title': 'Coordinates of Preserved Specimens'}
        }
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
