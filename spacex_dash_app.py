# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data into pandas DataFrame
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    html.Div([
        dcc.Dropdown(id='site-dropdown',
                     options=[
                         {'label': 'All Sites', 'value': 'ALL'},
                         {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                         {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                         {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                         {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                     ],
                     value='ALL',
                     placeholder='Select a Launch Site',
                     searchable=True
                     ),
    ]),
    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P("Payload range (kg):"),
    html.Div([
        dcc.RangeSlider(id='payload-slider',
                        min=0, max=10000, step=1000,
                        value=[min_payload, max_payload],
                        marks={i: str(i) for i in range(0, 10001, 1000)}
                        )
    ]),
    html.Br(),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value')]
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df, 
                     values='class', 
                     names='Launch Site', 
                     title='Success Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, 
                     values='class', 
                     names='Launch Site', 
                     title=f'Success Launches for Site: {selected_site}')
    
    return fig

# TASK 4: Add a callback function to render the success-payload-scatter-chart scatter plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
     Input(component_id="payload-slider", component_property="value")]
)
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    else:
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1]) &
                                (spacex_df['Launch Site'] == selected_site)]
        
    fig = px.scatter(filtered_df, 
                     x='Payload Mass (kg)', 
                     y='class', 
                     color='Booster Version Category',
                     title='Payload Success Scatter Chart',
                     labels={'class': 'Launch Outcome', 'Payload Mass (kg)': 'Payload Mass (kg)'})
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)