import os
import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

if os.path.exists("./formatted_output.csv"):
    data_path = "./formatted_output.csv"
elif os.path.exists("./formatted_data.csv"):
    data_path = "./formatted_data.csv"
else:
    raise FileNotFoundError("Could not locate 'formatted_output.csv' or 'formatted_data.csv' in the project directory.")

df = pd.read_csv(data_path)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date')

df_daily = df.groupby('date', as_index=False)['sales'].sum()

fig = px.line(
    df_daily,
    x='date',
    y='sales',
    title='Pink Morsel Total Daily Sales Over Time',
    labels={
        'date': 'Date',
        'sales': 'Total Daily Sales ($)'
    }
)

fig.add_vline(
    x='2021-01-15',
    line_width=2,
    line_dash="dash",
    line_color="red",
    annotation_text="Price Increase (Jan 15, 2021)",
    annotation_position="top left"
)

fig.update_layout(
    template='plotly_white',
    title_x=0.5,
    hovermode="x unified"
)

app = Dash(__name__)

app.layout = html.Div(
    style={
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': '#f4f6f9',
        'minHeight': '100vh',
        'padding': '40px 20px'
    },
    children=[
        html.Div(
            style={
                'maxWidth': '1100px',
                'margin': '0 auto',
                'backgroundColor': '#ffffff',
                'padding': '30px',
                'borderRadius': '12px',
                'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.08)'
            },
            children=[
                html.H1(
                    children='Soul Foods - Pink Morsel Sales Visualizer',
                    style={'textAlign': 'center', 'color': '#1f2937', 'marginBottom': '8px'}
                ),
                html.P(
                    children='Evaluating total daily sales performance before and after the January 15, 2021 price increase.',
                    style={'textAlign': 'center', 'color': '#6b7280', 'fontSize': '16px', 'marginBottom': '30px'}
                ),
                dcc.Graph(
                    id='sales-line-chart',
                    figure=fig
                )
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run(debug=True)