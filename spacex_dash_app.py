# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                        id='site-dropdown',
                                        options=[
                                            {'value': x, 'label': x}
                                                for x in ['CCAFS LC-40','CCAFS SLC-40','KSC LC-39A','VAFB SLC-4E','ALL']],
                                        value='ALL',
                                        placeholder="Select a Launch Site here",
                                        searchable=True
                                ),
                                
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    marks={
                                        0: {'label': '0'},
                                        2500: {'label': '2,500'},
                                        5000: {'label': '5,000'},
                                        7500: {'label': '7,500'},
                                        10000: {'label': '10,000'}
                                    },
                                    value=[min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(
                                    dcc.Graph(
                                        id='success-payload-scatter-chart'
                                    )
                                ),
                            ]
                    )

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"), 
    Input(component_id="site-dropdown", component_property="value"))
def make_pie(site):
    df = spacex_df
    title = f"Successful launches for: {site}"

    if site == "ALL":
        fig = px.pie(df, values='class', names='Launch Site', title=title)
    else:
        df1 = df[df['Launch Site'] == site]
        df2 = df1.groupby(['Launch Site','class']).size().reset_index(name='class count')
        fig = px.pie(df2, values='class count', names='class', title=title)
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')]
)
def make_scatter(site, slider):
    low,high = (slider[0], slider[1])
    mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    df = spacex_df[mask]
    title = f"Correlation between Payload and Success for {site}"

    if site == "ALL":
        fig = px.scatter(df, x="Payload Mass (kg)", y="class", color="Booster Version Category", title=title)
    else:
        df1 = df[df['Launch Site'] == site]
        fig = px.scatter(df1, x="Payload Mass (kg)", y="class", color="Booster Version Category", title=title)
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()

