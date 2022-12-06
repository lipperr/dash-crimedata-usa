from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

from data import choose_dataset, crimes, racePop

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                options=['All_states', 'blackPop', 'whitePop', 'asianPop', 'hispanicPop', 'population', 'murders',
                         'rapes',
                         'robberies', 'assaults', 'burglaries', 'larcenies', 'autoTheft', 'arsons',
                         'ViolentCrimesPerPop', 'nonViolPerPop', 'medIncome', 'perCapInc', 'NumUnderPov'],
                value='All_states', id='x_axis_query')],
            style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(options=['race', 'crime'], value='race', id='opt')
        ],

            style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    ],
        style={'padding': '10px 5px'}
    ),

    html.Div([
        html.Div([
            dcc.Dropdown(options=['blackPop', 'whitePop', 'asianPop', 'hispanicPop', 'population', 'murders', 'rapes',
                                  'robberies', 'assaults', 'burglaries', 'larcenies', 'autoTheft', 'arsons',
                                  'ViolentCrimesPerPop', 'nonViolPerPop', 'medIncome', 'perCapInc', 'NumUnderPov'],
                         value='larcenies', id='y_axis_query')],
            style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                options=['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
                         'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI',
                         'MN', 'MO', 'MS', 'NC', 'ND', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH',
                         'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT',
                         'WA', 'WI', 'WV', 'WY'],
                value='MO',
                id='state'
            )],

            style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    ],
        style={'padding': '10px 5px'}
    ),

    html.Div([
        dcc.Graph(
            id='all_states_graph'
        )
    ], style={'width': '55%', 'display': 'inline-block', 'padding': '0 20'}),

    html.Div([
        dcc.Graph(
            id='one_state_graph'
        )
    ], style={'width': '45%', 'display': 'inline-block', 'padding': '0 20'}),

    dcc.RadioItems(['All', 'towns', 'cities', 'boroughs', 'villages'], value='All', id='typeC', inline=True)
])


@app.callback(
    Output('all_states_graph', 'figure'),
    Input('x_axis_query', 'value'),
    Input('y_axis_query', 'value'),
    Input('typeC', 'value'))
def update_graph(x_axis_query, y_axis_query, typeC):
    data = choose_dataset[typeC]
    if x_axis_query == 'All_states':
        fig = px.bar(data, x='state', y=y_axis_query)
        fig.update_traces(marker_color='orange')
    else:
        fig = px.scatter(data, x=x_axis_query, y=y_axis_query, color='state')
    return fig


@app.callback(
    Output('one_state_graph', 'figure'),
    Input('state', 'value'),
    Input('opt', 'value'),
    Input('typeC', 'value'))
def update_graph(state, opt, typeC):
    data = choose_dataset[typeC]
    data = data.groupby('state')
    if state not in data.groups:
        fig = px.pie()
        return fig
    data = data.get_group(state)
    qlist = []
    if opt == 'race':
        for r in racePop:
            qlist.append(int(data[r]))
        dfSt = pd.DataFrame({'race': racePop, 'quantity': qlist})
        fig = px.bar(dfSt, x='race', y='quantity')
        fig.update_traces(marker_color='red')

    else:  # y_query = 'crime'
        for c in crimes:
            qlist.append(int(data[c]))
        dfSt = pd.DataFrame({'crime': crimes, 'quantity': qlist})
        fig = px.bar(dfSt, x='crime', y='quantity')
        fig.update_traces(marker_color='purple')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)  # запускаем сервер
