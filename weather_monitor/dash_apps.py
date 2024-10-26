

# dash_apps.py

from dash import dcc, html, Dash
from django.apps import apps
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from django.apps import apps

# Initialize your Dash app
app = DjangoDash('WeatherTrends')

# Function to get data safely
def get_data():
    DailySummary = apps.get_model('weather_monitor', 'DailySummary')  # Safely import model
    # Fetch data from the model
    summaries = DailySummary.objects.all()
    data = {
        'dates': [summary.date for summary in summaries],
        'avg_temps': [summary.avg_temp for summary in summaries],
        'max_temps': [summary.max_temp for summary in summaries],
        'min_temps': [summary.min_temp for summary in summaries],
        'dominant_weathers': [summary.dominant_weather for summary in summaries],
    }
    return data

# Example layout for the Dash app
app.layout = html.Div([
    html.H1("Welcome to the Weather Monitoring System"),
    html.P("Here you can monitor daily weather summaries and alerts."),
    
    html.Div([
        html.H2("Daily Weather Summary"),
        html.Table(id='summary-table'),
        html.Div(id='no-data-message', style={'color': 'red'})
    ]),

    html.Div([
        html.H2("Weather Trends Visualization"),
        dcc.Graph(id='temp-graph'),
        dcc.Dropdown(
            id='city-dropdown',
            options=[{'label': 'All Cities', 'value': 'ALL'}],  # Add more cities dynamically if needed
            value='ALL'
        ),
        dcc.Interval(
            id='interval-component',
            interval=60 * 1000,  # in milliseconds
            n_intervals=0
        )
    ])
])

# Update the table with daily summaries
@app.callback(
    Output('summary-table', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_summary_table(n):
    data = get_data()  # Call the data retrieval function
    if not data['dates']:
        return [html.Tr([html.Td("No data available.")])]  # Show message if no data

    # Create table headers
    headers = [html.Th("Date"), html.Th("City"), html.Th("Average Temperature (°C)"),
               html.Th("Max Temperature (°C)"), html.Th("Min Temperature (°C)"),
               html.Th("Dominant Condition")]

    # Create table rows
    rows = [html.Tr([
        html.Td(data['dates'][i]),
        html.Td("City Name Here"),  # Replace with actual city data
        html.Td(data['avg_temps'][i]),
        html.Td(data['max_temps'][i]),
        html.Td(data['min_temps'][i]),
        html.Td(data['dominant_weathers'][i])
    ]) for i in range(len(data['dates']))]

    return [html.Thead(headers)] + [html.Tbody(rows)]

# Update the graph based on interval and dropdown selection
@app.callback(
    Output('temp-graph', 'figure'),
    [Input('interval-component', 'n_intervals'),
     Input('city-dropdown', 'value')]
)
def update_graph(n, selected_city):
    data = get_data()  # Call the data retrieval function
    
    if selected_city != 'ALL':
        # Filter data based on selected city
        filtered_dates = [date for date, city in zip(data['dates'], data['dominant_weathers']) if city == selected_city]
        filtered_avg_temps = [temp for temp, city in zip(data['avg_temps'], data['dominant_weathers']) if city == selected_city]
    else:
        filtered_dates = data['dates']
        filtered_avg_temps = data['avg_temps']

    figure = {
        'data': [
            {'x': filtered_dates, 'y': filtered_avg_temps, 'type': 'line', 'name': 'Avg Temp'},
        ],
        'layout': {
            'title': 'Average Temperatures Over Time',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Average Temperature (°C)'}
        }
    }
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
