import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()

df = pd.read_parquet('service_reports.parquet')
columns_df = df.columns[1:-1] 
c = []

for i in columns_df:
    c.append({'label': i, 'value': i})

c.append({'label': 'Density of HHA Providers', 'value': 'Density of HHA Providers'})


df_ = pd.read_parquet('HHProviders.parquet')
limits = [(0,1),(2,50),(51,500)]
colors = ["rgb(0,116,217)","rgb(255,65,54)","rgb(133,20,75)"]
cities = []
scale = 10

df__ = pd.read_parquet('hhc_providers_general.parquet')

c.append({'label': 'General View of Percent of Providers', 'value': 'General View of Percent of Providers'})

for i in range(len(limits)):
    lim = limits[i]
    df_sub = df_[df_['Provider Name'].between(lim[0], lim[1])]
    city = dict(
        type = 'scattergeo',
        locationmode = 'USA-states',
        lon = df_sub['lng'],
        lat = df_sub['lat'],
        text = df_sub['text'],
        marker = dict(
            size = df_sub['Provider Name']*scale,
            color = colors[i],
            line = dict(width=0.5, color='rgb(40,40,40)'),
            sizemode = 'area'
        ),
        name = '{0} - {1}'.format(lim[0],lim[1]) )
    cities.append(city)



app.layout = html.Div([



        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=c,
                value= columns_df[0]
            ),
        ],
        style={'width': '40%', 'display': 'inline-block', 'horizontal-align': 'center'}),
   

    dcc.Graph(
        id='opinion-graph',
        style={
            'height': "100vh",
            'width': '100%'
        },
    )
])



@app.callback(
    dash.dependencies.Output('opinion-graph', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value')])
def update_graph(xaxis_column_name):

    if "Offers" in xaxis_column_name:
        word = "Providers"
    else:
        word = "Patients"

    if(xaxis_column_name == 'Density of HHA Providers'):

        return {

            'data': cities,
                
            'layout': dict(
                    title = 'Home Health Providers',
                    showlegend = True,
                    geo = dict(
                        scope='usa',
                        projection=dict( type='albers usa' ),
                        showland = True,
                        landcolor = 'rgb(217, 217, 217)',
                        subunitwidth=1,
                        countrywidth=1,
                        subunitcolor="rgb(255, 255, 255)",
                        countrycolor="rgb(255, 255, 255)"
                    ),
                )
            }

    if(xaxis_column_name == 'General View of Percent of Providers'):

        return     { 

                'data' : [go.Pie(labels=df__['Name'],values=df__['Percent of HHC providers'])],


                'layout' : dict( title = 'Percent of Home Health Providers' ) }


    else:

        return {
                'data': [ dict(
            type='choropleth',
        
           colorscale=[[0.0, 'rgb(165,0,38)'], [0.1, 'rgb(215,48,39)'], [0.2, 'rgb(244,109,67)'],
            [0.3, 'rgb(253,174,97)'], [0.4, 'rgb(254,224,144)'], [0.5, 'rgb(224,243,248)'],
            [0.6, 'rgb(171,217,233)'],[0.7, 'rgb(116,173,209)'], [0.8, 'rgb(69,117,180)'],
            [1.0, 'rgb(49,54,149)']],
          

            autocolorscale = False,

            locations = df['State'],
        
            z = df[xaxis_column_name],
        
            locationmode = 'USA-states',
            text = df['Name'],
            marker = dict(
                line = dict (
                    color = 'rgb(255,255,255)',
                    width = 2
                ) ),
            colorbar = dict(
                title = "%")
            ) ],

                'layout': dict(
                title = f"% {word} who {xaxis_column_name}",
                geo = dict(
                scope='usa',
                projection=dict( type='albers usa' ),
                showlakes = True,
                lakecolor = 'rgb(255, 255, 255)'),
                 )
            }





if __name__ == '__main__':
    app.run_server()