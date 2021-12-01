import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
# import plotly.graph_objects as go
from plotly import graph_objs as go
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn import linear_model, tree, neighbors
import pandas as pd
from sklearn.linear_model import LinearRegression
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
server = app.server

# ---------- Import and clean data (importing csv into pandas)

dfr = pd.read_csv('coffeequality.csv')

# ---------- Import and clean data (Linear coefficient)
df = dfr.drop(columns=['species', 'country','harvest_year'])
df = df.sort_values(['total_cup_points'],ascending=[True])
df = df.iloc[1:]
X = df.drop(columns=['total_cup_points'])
y = df['total_cup_points']
model1 = LinearRegression()
model1.fit(X, y)

# ------------------------------------------------------------------------------
# Linear coefficient fig1
colors = ['Strong' if c > 1 else 'Weak' for c in model1.coef_]
fig1 = px.bar(
    x = X.columns, y=model1.coef_, color=colors,
    color_discrete_sequence=['#A2B45F', '#4B7EA4'],
    labels=dict(x='Features', y='Linear coefficient'),
    title='Weight of each feature for predicting total cup points',
    range_y = (0.994, 1.0031),)
fig1.update_layout(
    font_color="#e9e9e9",
    paper_bgcolor="#323232",
    plot_bgcolor="#323232",
    title_font_color="#e9e9e9",
    legend_title_font_color="#e9e9e9",
    title_font_size= 22
)

# ---------- Import and clean data (Prediction_error)
train_idx, test_idx = train_test_split(df.index, test_size=.25, random_state=0)
df['split'] = 'train'
df.loc[test_idx, 'split'] = 'test'

X_train = df.loc[train_idx, ['aroma', 'cupper_points','sweetness','clean_cup','uniformity','balance','body','acidity','aftertaste','flavor']]
y_train = df.loc[train_idx, 'total_cup_points']

model2 = LinearRegression()
model2.fit(X_train, y_train)
df['prediction'] = model2.predict(X)

# ------------------------------------------------------------------------------
# Prediction_error fig2
fig2 = px.scatter(
    df, x='total_cup_points', y='prediction',
    marginal_x='histogram', marginal_y='histogram',
    color='split', trendline='ols',
    title='Prediction error analysis',
    range_y = (70, 90),
    range_x = (75, 90),
)
fig2.update_layout(
    font_color="#e9e9e9",
    paper_bgcolor="#323232",
    plot_bgcolor="#323232",
    title_font_color="#e9e9e9",
    legend_title_font_color="#e9e9e9",
    title_font_size= 22
)
fig2.update_traces(histnorm='probability', selector={'type':'histogram'})
fig2.add_shape(
    type="line", line=dict(dash='dash'),
    x0=y.min(), y0=y.min(),
    x1=y.max(), y1=y.max()
)

# ---------- Import and clean data (Residual)
df['residual'] = df['prediction'] - df['total_cup_points']

# ------------------------------------------------------------------------------
# Residual fig3
fig3 = px.scatter(
    df, x='prediction', y='residual',
    marginal_y='violin',
    color='split', trendline='ols',
    title='Residual plots',
    range_y = (-0.03, 0.03),
    range_x = (65, 95),
)
fig3.update_layout(
    font_color="#e9e9e9",
    paper_bgcolor="#323232",
    plot_bgcolor="#323232",
    title_font_color="#e9e9e9",
    legend_title_font_color="#e9e9e9",
    title_font_size= 22
)

# ------------------------------------------------------------------------------
# slider list for the layout
slider_list = []
features = ['aroma', 'cupper_points','sweetness','clean_cup','uniformity','balance','body','acidity','aftertaste','flavor']
for f in features:
    slider_list.append(

        html.Div([
            
            html.Div(id=f'{f}-container', style={'margin-left': 20}),
            dcc.Slider(
                id=f'{f}-slider',min=0,max=10,step=0.1,value=5,
                marks={
                0: {'label': '0', 'style': {'color': '#77b0b1'}},
                10: {'label': '10', 'style': {'color': '#f50'}}},
                included=True)
        ], style={'textAlign':'center'}),
        
        # html.Div([
            
        #     html.Div(id=f'{f}-container', style={'margin-left': 20}),
        #     dcc.Slider(
        #         id=f'{f}-slider',min=0,max=10,step=0.1,value=5,
        #         marks={
        #         0: {'label': '0', 'style': {'color': '#77b0b1'}},
        #         10: {'label': '10', 'style': {'color': '#f50'}}},
        #         included=True)
        # ], style={'textAlign':'center'}),
        
    )
# ------------------------------------------------------------------------------
# predict card for the layout
predict_cart = dbc.Card(
    [
        dbc.CardImg(src="https://previews.123rf.com/images/giffaleens/giffaleens1801/giffaleens180100012/93894844-color-chalk-coffee-of-proportions-set-.jpg", top=True),
        dbc.CardBody(
            [
                html.H4("Predicted Total Cup Point", className="card-title"),
                html.P(
                    "Based on all the ten coffee features selected on the left"
                    ", here is our predicted Total Cup Point:",
                    className="card-text",
                ),
                dbc.Button(html.Div(id='predicted-output', style={'margin-left': 15}),block=True,color="info",size="lg",)
                # dbc.Button(html.Div(id='predicted-output', style={'margin-left': 15}),style={"align": "middle"}, size="lg", className="mr-1",color="info",)
            ]
        ),
    ],
    style={"width": "26rem", "height":"37.5rem"},
)

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(html.H1("Machine Learning Coffee Rating ", style={'text-align': 'center'}),width=12)
    ]),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(slider_list, xs=4, sm=4, md=4, lg=2, xl=2),
        dbc.Col(predict_cart, xs=6, sm=6, md=6, lg=3, xl=3),
        dbc.Col(dcc.Graph(id='radar_chart', figure={},
                          config={'displayModeBar': False}), xs=6, sm=6, md=6, lg=5, xl=5)
    ],justify="center",),
    html.Br(),

    dbc.Row([
        dbc.Col(dcc.Graph(id='coefficients', figure= fig1,
                          config={'displayModeBar':False}), xs=8, sm=8, md=8, lg=6, xl=6),
    ],justify="center",),
    html.Br(),
    dbc.Row([
        dbc.Col(dcc.Graph(id='prediction_error', figure= fig2,
                          config={'displayModeBar':False}), xs=8, sm=8, md=8, lg=5, xl=5),
        dbc.Col(dcc.Graph(id='residual', figure= fig3,
                          config={'displayModeBar':False}), xs=8, sm=8, md=8, lg=5, xl=5),
    ],justify="center",),


    

])

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [dash.dependencies.Output('aroma-container', 'children'),dash.dependencies.Output('cupper_points-container', 'children'),
    dash.dependencies.Output('sweetness-container', 'children'),dash.dependencies.Output('clean_cup-container', 'children'),
    dash.dependencies.Output('uniformity-container', 'children'),dash.dependencies.Output('balance-container', 'children'),
    dash.dependencies.Output('body-container', 'children'),dash.dependencies.Output('acidity-container', 'children'),
    dash.dependencies.Output('aftertaste-container', 'children'),dash.dependencies.Output('flavor-container', 'children'),
    Output('predicted-output', 'children'),Output('radar_chart','figure')],
    [dash.dependencies.Input('aroma-slider', 'value'),dash.dependencies.Input('cupper_points-slider', 'value'),
    dash.dependencies.Input('sweetness-slider', 'value'),dash.dependencies.Input('clean_cup-slider', 'value'),
    dash.dependencies.Input('uniformity-slider', 'value'),dash.dependencies.Input('balance-slider', 'value'),
    dash.dependencies.Input('body-slider', 'value'),dash.dependencies.Input('acidity-slider', 'value'),
    dash.dependencies.Input('aftertaste-slider', 'value'),dash.dependencies.Input('flavor-slider', 'value')
    ])

def update_output(aroma, cupper_points,sweetness,clean_cup,uniformity,balance,body,acidity,aftertaste,flavor):
    aroma1 = 'Aroma: {}'.format(aroma),
    cupper_points1 = 'Cupper points: {}'.format(cupper_points),
    sweetness1 = 'Sweetness: {}'.format(sweetness),
    clean_cup1 = 'Clean Cup: {}'.format(clean_cup),
    uniformity1 = 'Uniformity: {}'.format(uniformity),
    balance1 = 'Balance: {}'.format(balance),
    body1 = 'Body: {}'.format(body),
    acidity1 = 'Acidity: {}'.format(acidity),
    aftertaste1 = 'Aftertaste: {}'.format(aftertaste),
    flavor1 = 'Flavor: {}'.format(flavor),
    X_input = [aroma, cupper_points,sweetness,clean_cup,uniformity,balance,body,acidity,aftertaste,flavor],
    predict = round(model1.predict(X_input)[0],2),

    # ------------------------------------------------------------------------------
    # Prepare data for radar chart
    dff = df.copy()
    dff = dff.sort_values(['total_cup_points'],ascending=[False])
    dff = dff.drop(columns=['total_cup_points'])
    topCoffee = dff.iloc[0].tolist()
    featuresTop = ['aroma', 'cupper_points','sweetness','clean_cup','uniformity','balance','body','acidity','aftertaste','flavor']

    # Radar chart
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
      r=topCoffee,
      theta=featuresTop,
      fill='toself',
      name='Top Coffee',
    ))

    fig.add_trace(go.Scatterpolar(
      r=[aroma, cupper_points,sweetness,clean_cup,uniformity,balance,body,acidity,aftertaste,flavor],
      theta=featuresTop,
      fill='toself',
      name='Predicted Coffee'
    ))

    fig.update_layout(
    polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 10],
      
    )),
    margin=dict(l=40, r=20, t=100, b=40),
    showlegend=True,
    title='Predicted Coffee VS. Top Rating Coffee',
    title_font_color="#e9e9e9",
    autosize=False,
    width=770,
    height=600,
    font_color="#e9e9e9",
    paper_bgcolor="#323232",
    polar_bgcolor="#323232",
    title_font_size= 22
    )
    


    return aroma1,cupper_points1,sweetness1,clean_cup1,uniformity1,balance1,body1,acidity1,aftertaste1,flavor1,predict,fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)