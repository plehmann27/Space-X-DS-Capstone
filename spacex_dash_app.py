# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
print(spacex_df.columns)
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown',searchable = True, 
                                placeholder = 'Select a Launch Site', value='ALL',
                                 options = [{'label':'All Sites', 'value':'ALL'},
                                 {'label': spacex_df['Launch Site'].unique()[0], 
                                 'value' : spacex_df['Launch Site'].unique()[0] },
                                 {'label': spacex_df['Launch Site'].unique()[1], 
                                 'value' : spacex_df['Launch Site'].unique()[1]},
                                 {'label': spacex_df['Launch Site'].unique()[2], 
                                 'value' : spacex_df['Launch Site'].unique()[2]},
                                 {'label': spacex_df['Launch Site'].unique()[3], 
                                 'value' : spacex_df['Launch Site'].unique()[3]}
                                 
                                 ]),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider', min = 0, max = 10000, step = 1000 , value =[min_payload, max_payload], marks = {0:'0', 10000:'10000',5000:'5000', 2500:'2500',7500:'7500'}),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                                Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[['Launch Site','class']].groupby('Launch Site').count()
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
            names = filtered_df.index,
            title='Number of Successful Launches')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        NoOfSuccesses = filtered_df['class'].sum()
        NoOfFails = len(filtered_df) - NoOfSuccesses
        fig = px.pie(filtered_df, values = [NoOfSuccesses,NoOfFails], names = ['Success', 'Failure'], title = 'Comparison Successful/Failed Launches')
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
            [Input(component_id = 'site-dropdown', component_property = 'value'), Input(component_id = 'payload-slider', component_property = 'value')])
def get_scatter_plot(entered_site, entered_payload):
    if entered_site == 'ALL':
        fig = px.scatter(spacex_df, x = 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category')
        return fig
    else:
        nextfiltered = spacex_df[spacex_df['Launch Site'] == entered_site]
        nextfiltered = nextfiltered[nextfiltered['Payload Mass (kg)'] <= entered_payload[1]]
        nextfiltered = nextfiltered[nextfiltered['Payload Mass (kg)'] >= entered_payload[0]]
        fig = px.scatter(nextfiltered, x= 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category')
        return fig
# Run the app
if __name__ == '__main__':
    app.run_server(port = 8090)
