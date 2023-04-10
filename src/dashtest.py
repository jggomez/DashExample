from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


df_users = pd.read_csv(
    "https://users.csv")

df_users["showadvertising"] = np.where((df_users["showadvertising"] == "No data") | (
    df_users["showadvertising"] == "true"), "true", "false")
df_users["premium"] = np.where((df_users["is premium"] == "true") & (
    df_users["purchasetoken"] != "No data"), True, False)
df_users["trial_activated"] = np.where((df_users["trialactivated"] == "true") & (
    df_users["trialexpired"] == "false") & (df_users["is premium"] == "true"), True, False)
df_users["trial_expired"] = np.where((df_users["trialexpired"] == "true") & (
    df_users["is premium"] == "false"), True, False)

df_users_trial = pd.DataFrame({
    "User_Type": ["Usuarios totales",
                  "Usuarios con trial activo",
                  "Usuarios con trial terminado"],
    "Amount": [df_users.id.count(),
               df_users[df_users["trial_activated"] == True].id.count(),
               df_users[df_users["trial_expired"] == True].id.count()]
})

num_total_users = df_users.id.count()

num_total_premium_users = df_users[(df_users["trialexpired"] == "true") & (
    df_users["is premium"] == "true") & (df_users["premium"] == True)].id.count()

num_total_users_advertising = df_users[df_users["showadvertising"] == "false"].id.count(
)

percentage_users_premium = round(
    ((num_total_premium_users / num_total_users) * 100), 2)

fig_users_trial = px.bar(df_users_trial,
                         x="User_Type",
                         y="Amount",
                         title="Usuarios con trial activo o trial terminado",
                         labels={"Amount": "Cantidad de Usuarios", "User_Type": "Tipo de Usuarios Trial"})

df_user_premium_bar = pd.DataFrame({
    "User_Type": [
        "Usuarios Premium",
        "Usuarios sin publicidad"],
    "Amount": [
        df_users[(df_users["trialexpired"] == "true") & (
            df_users["is premium"] == "true") & (df_users["premium"] == True)].id.count(),
        df_users[df_users["showadvertising"] == "false"].id.count()
    ]
})

fig_user_premium_bar = px.bar(df_user_premium_bar, x="User_Type", y="Amount", title="Tipos de Usuarios", labels={
    "Amount": "Cantidad de Usuarios", "User_Type": "Tipo de Usuarios"})

df_users_level_less_five = df_users[df_users["level"] <= 5]

df_users_level_greater_five_less_10 = df_users[(
    df_users["level"] >= 5) & (df_users["level"] <= 10)]

df_users_level_greater_five_less_20 = df_users[(
    df_users["level"] >= 10) & (df_users["level"] <= 20)]

fig_user_level = make_subplots(2, 2, subplot_titles=["Usuarios con niveles hasta 5", "Usuarios con niveles mayor a 5 y menor que 10",
                                                     "Usuarios con niveles mayor a 10 y menor que 20", "Usuarios con niveles mayores a 20"])


df_users_level_less_five_2 = df_users_level_less_five.groupby(
    ["level"]).count().reset_index()
fig_user_level.add_trace(go.Bar(
    x=df_users_level_less_five_2['level'], y=df_users_level_less_five_2["id"]), row=1, col=1)

df_users_level_greater_five_less_10_2 = df_users_level_greater_five_less_10.groupby(
    ["level"]).count().reset_index()
fig_user_level.add_trace(go.Bar(
    x=df_users_level_greater_five_less_10_2['level'], y=df_users_level_greater_five_less_10_2["id"]), row=1, col=2)

df_users_level_greater_five_less_20_2 = df_users_level_greater_five_less_20.groupby(
    ["level"]).count().reset_index()
fig_user_level.add_trace(go.Bar(
    x=df_users_level_greater_five_less_20_2['level'], y=df_users_level_greater_five_less_20_2["id"]), row=2, col=1)

df_users_level_greater_20 = df_users[df_users["level"] >= 20]
df_users_level_greater_20_2 = df_users_level_greater_20.groupby(
    ["level"]).count().reset_index()
fig_user_level.add_trace(go.Bar(
    x=df_users_level_greater_20_2['level'], y=df_users_level_greater_20_2["id"]), row=2, col=2)


df_users_premium = df_users[df_users["premium"] == True]

code_countries = df_users["country"].unique()

fig_all_user_level_premium = px.scatter(df_users,
                                        x="rank",
                                        y="level",
                                        color="premium",
                                        hover_data=['level'],
                                        title="Usuarios con su nivel y rank y además sin son premium",
                                        labels={
                                            "level": "Nivel del usuario", "rank": "Rank del Usuario"})

fig_user_level_premium = px.scatter(df_users_premium,
                                    x="level",
                                    y="rank",
                                    hover_data=['level'],
                                    title="Usuarios premium con su nivel y rank",
                                    labels={
                                        "level": "Nivel del usuario", "rank": "Rank del Usuario"})

fig_user_level_advertising = px.scatter(df_users,
                                        x="rank",
                                        y="level",
                                        title="Usuarios con su nivel y rank y además si se les muestra advertising",
                                        color="showadvertising",
                                        hover_data=['level'],
                                        labels={
                                            "level": "Nivel del usuario", "rank": "Rank del Usuario"})

fig_user_country_rank = px.scatter(df_users,
                                   x="country",
                                   y="rank",
                                   hover_data=['rank'],
                                   title="Usuarios con su rank por país asociado al leaderboard",
                                   labels={
                                       "country": "País del leaderboard", "rank": "Rank del Usuario"})

fig_users_countries = px.histogram(df_users_premium,
                                   x="country",
                                   title="Usuarios premium por país asociado al leaderboard",
                                   labels={
                                       "country": "País del leaderboard", "count": "Cantidad de Usuarios"})

num_users_card = dbc.Card(
    dbc.CardBody(
        [
            html.Div([
                html.H4("Total Usuarios", className="card-title"),
                html.H5(str(num_total_users), className="card-subtitle"),
            ])
        ]),
    color="primary",
    inverse=True
)

num_users_premium_card = dbc.Card(
    dbc.CardBody(
        [
            html.Div([
                html.H4("Total Usuarios Premium",
                        className="card-title"),
                html.H5(str(num_total_premium_users),
                        className="card-subtitle"),
            ])
        ]),
    color="secondary",
    inverse=True
)

num_users_advertising_card = dbc.Card(
    dbc.CardBody(
        [
            html.Div([
                html.H4("Total Usuarios Sin Publicidad",
                        className="card-title"),
                html.H5(str(num_total_users_advertising),
                        className="card-subtitle"),
            ])
        ]),
    color="info",
    inverse=True
)

percentage_users_premium_card = dbc.Card(
    dbc.CardBody(
        [
            html.Div([
                html.H4("Porcentaje de usuarios premium",
                        className="card-title"),
                html.H5(f"{str(percentage_users_premium)} %",
                        className="card-subtitle"),
            ])
        ]),
    color="success",
    inverse=True
)

user_premium_card = dbc.Card(
    [
        html.Div([
            dcc.Graph(
                id='user_premium_bar',
                figure=fig_user_premium_bar
            )
        ])
    ]
)

user_trial_card = dbc.Card(
    [
        html.Div([
            dcc.Graph(
                id='users_trial',
                figure=fig_users_trial
            )
        ])
    ]
)

user_level_card = dbc.Card(
    [
        html.Div([
            dcc.Graph(
                id='users_level',
                figure=fig_user_level
            )
        ])
    ]
)

all_user_level_premium_card = dbc.Card(
    [
        html.Div([
            dcc.Graph(
                id='all_users_level_premium',
                figure=fig_all_user_level_premium
            )
        ])
    ]
)

user_level_premium_card = dbc.Card(
    [
        html.Div([
            dcc.Graph(
                id='users_level_premium',
                figure=fig_user_level_premium
            )
        ])
    ]
)

user_level_advertising_card = dbc.Card(
    [
        html.Div([
            dcc.Graph(
                id='user_level_advertising',
                figure=fig_user_level_advertising
            )
        ])
    ]
)

user_country_rank_card = dbc.Card(
    [
        html.Div([
            dcc.Graph(
                id='user_country_rank_card',
                figure=fig_user_country_rank
            )
        ])
    ]
)

user_countries_card = dbc.Card(
    [
        html.Div([
            dcc.Graph(
                id='users_countries',
                figure=fig_users_countries
            )
        ])
    ]
)

users_code_countries_card = dbc.Card(
    [
        html.Div([
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Dropdown(
                            options=code_countries,
                            value='MX',
                            id="countries_lead_dropdown",
                        ), width={"size": 6, "offset": 3}),
                ],
                align="center",
            ),
            html.Br(),
            dcc.Graph(
                id='users_code_countries_graph'
            )
        ])
    ]
)


@app.callback(
    Output('users_code_countries_graph', 'figure'),
    Input('countries_lead_dropdown', 'value'))
def update_users_code_countries_graph(code_country):
    df_country = df_users[df_users["country"] == str(code_country)]

    fig = px.scatter(df_country,
                     x="level",
                     y="rank",
                     color="country",
                     title="Usuarios con su rank por país asociado al leaderboard",
                     labels={
                         "country": "País del leaderboard", "rank": "Rank del Usuario", "level": "Nivel del Usuario"})

    return fig


app.layout = dbc.Container(
    [
        html.Br(),
        dbc.Row(
            [
                dbc.Col(html.H1("Visualización Datos Usuarios"),
                        width={"size": 6, "offset": 4}),
            ],
            align="center",
        ),
        html.Hr(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(num_users_card, md=3),
                dbc.Col(num_users_premium_card, md=3),
                dbc.Col(num_users_advertising_card, md=3),
                dbc.Col(percentage_users_premium_card, md=3),
            ],
            align="center",
        ),
        html.Hr(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(user_trial_card),
            ],
            align="center",
        ),
        html.Hr(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(user_premium_card),
            ],
            align="center",
        ),
        html.Hr(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(user_level_card),
            ],
            align="center",
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(all_user_level_premium_card),
            ],
            align="center",
        ),
        html.Hr(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(user_level_premium_card),
            ],
            align="center",
        ),
        html.Hr(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(user_level_advertising_card),
            ],
            align="center",
        ),
        html.Hr(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(user_country_rank_card),
            ],
            align="center",
        ),
        html.Hr(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(user_countries_card),
            ],
            align="center",
        ),
        html.Hr(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(users_code_countries_card),
            ],
            align="center",
        ),
    ],
    fluid=True,
)
