import pandas as pd
import numpy as np

import dash
dash.__version__
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import Covid.models.SIR_model as SIR_model
import plotly.graph_objects as go
from datetime import datetime

import os
print(os.getcwd())
df_input_large=pd.read_csv('data/processed/COVID_final_set.csv',sep=';')



fig = go.Figure()

app = dash.Dash()
app.layout = html.Div([
    html.Div([

    dcc.Markdown('''
    #  COVID-19 DASHBOARD

    The dashboard presents dynamic visualization of the Covid data and SIR model.

    '''),

    dcc.Markdown('''
    ## Multi-Select Country for visualization
    '''),


    dcc.Dropdown(
        id='country_drop_down',
        options=[ {'label': each,'value':each} for each in df_input_large['country'].unique()],
        value=['US', 'Germany','Italy'], # which are pre-selected
        multi=True
    ),

    dcc.Markdown('''
        ## Select Timeline of confirmed COVID-19 cases or the approximated doubling time
        '''),


    dcc.Dropdown(
    id='doubling_time',
    options=[
        {'label': 'Timeline Confirmed ', 'value': 'confirmed'},
        {'label': 'Timeline Confirmed Filtered', 'value': 'confirmed_filtered'},
        {'label': 'Timeline Doubling Rate', 'value': 'confirmed_DR'},
        {'label': 'Timeline Doubling Rate Filtered', 'value': 'confirmed_filtered_DR'},
    ],
    value='confirmed',
    multi=False
    ),

    dcc.Graph(id='main_window_slope')
    ]),
    
    html.Div([

    dcc.Markdown('''
    # SIR model

    '''),

    dcc.Markdown('''
    ## Select Country for visualization
    '''),


    dcc.Dropdown(
        id='country_drop_down2',
        options=[ {'label': each,'value':each} for each in df_input_large['country'].unique()],
        value='Germany', # which are pre-selected
        multi=False
    ),

    dcc.Graph(figure=fig, id='main_window_slope2')
    ])
    
])



@app.callback(
    Output('main_window_slope', 'figure'),
    [Input('country_drop_down', 'value'),
    Input('doubling_time', 'value')])
def update_figure(country_list,show_doubling):


    if 'DR' in show_doubling:
        my_yaxis={'type':"log",
               'title':'Approximated doubling rate over 3 days (larger numbers are better)'
              }
    else:
        my_yaxis={'type':"log",
                  'title':'Confirmed infected people (source johns hopkins csse, log-scale)'
              }


    traces = []
    for each in country_list:

        df_plot=df_input_large[df_input_large['country']==each]

        if show_doubling=='doubling_rate_filtered':
            df_plot=df_plot[['state','country','confirmed','confirmed_filtered','confirmed_DR','confirmed_filtered_DR','date']].groupby(['country','date']).agg(np.mean).reset_index()
        else:
            df_plot=df_plot[['state','country','confirmed','confirmed_filtered','confirmed_DR','confirmed_filtered_DR','date']].groupby(['country','date']).agg(np.sum).reset_index()
       #print(show_doubling)


        traces.append(dict(x=df_plot.date,
                                y=df_plot[show_doubling],
                                mode='markers+lines',
                                opacity=0.9,
                                name=each
                        )
                )

    return {
            'data': traces,
            'layout': dict (
                height=700,

                xaxis={'title':'Timeline',
                        'tickangle':-45,
                        'nticks':20,
                        'tickfont':dict(size=14,color="#7f7f7f"),
                      },

                yaxis=my_yaxis
        )
    }

@app.callback(
    Output('main_window_slope2', 'figure'),
    [Input('country_drop_down2', 'value')])
def update_figure_(country):
    print("country    :",country)
        
    fig = go.Figure()
    if country != None:
        predicted_simulations, data = SIR_model.get_data(country)
        fig.add_trace(go.Scatter(x=[date.strftime("%Y-%m-%d") for date in pd.date_range(datetime.strptime(data["date"][0], "%Y-%m-%d"), periods=len(predicted_simulations)).tolist()],
                            y = predicted_simulations,
                            mode='markers+lines',
                            opacity=0.9,
                            name='predicted'))

        fig.add_bar(x=data['date'],
                            y=data['confirmed'],
                            opacity=0.9,
                            name='actual')
        fig.update_layout(height = 700, xaxis_title="Date", yaxis_title="Population infected")
    return fig

if __name__ == '__main__':

    app.run_server(debug=True)
