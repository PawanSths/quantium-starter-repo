import os
import pandas as pd
from dash import Dash, html, dcc, Input, Output
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

COLORS = {
    'background': '#f8fafc',
    'card_bg': '#ffffff',
    'text_primary': '#0f172a',
    'text_secondary': '#475569',
    'border': '#e2e8f0',
    'accent_line': '#ef4444',
    'control_bg': '#f1f5f9'
}

app = Dash(__name__)

app.layout = html.Div(
    style={
        'fontFamily': "'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
        'backgroundColor': COLORS['background'],
        'minHeight': '100vh',
        'padding': '40px 20px',
        'color': COLORS['text_primary']
    },
    children=[
        html.Div(
            style={
                'maxWidth': '1100px',
                'margin': '0 auto',
                'backgroundColor': COLORS['card_bg'],
                'padding': '35px',
                'borderRadius': '16px',
                'boxShadow': '0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01)',
                'border': f"1px solid {COLORS['border']}"
            },
            children=[
                html.H1(
                    children='Soul Foods - Pink Morsel Sales Visualizer',
                    style={
                        'textAlign': 'center',
                        'fontWeight': '700',
                        'fontSize': '28px',
                        'marginBottom': '8px',
                        'color': COLORS['text_primary']
                    }
                ),
                html.P(
                    children='Evaluating total daily sales performance before and after the January 15, 2021 price increase.',
                    style={
                        'textAlign': 'center',
                        'color': COLORS['text_secondary'],
                        'fontSize': '15px',
                        'marginBottom': '30px'
                    }
                ),
                html.Div(
                    style={
                        'display': 'flex',
                        'flexDirection': 'column',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'marginBottom': '25px',
                        'padding': '16px',
                        'backgroundColor': COLORS['control_bg'],
                        'borderRadius': '10px'
                    },
                    children=[
                        html.Label(
                            "Filter Sales by Region:",
                            style={
                                'fontWeight': '600',
                                'fontSize': '14px',
                                'marginBottom': '10px',
                                'color': COLORS['text_primary']
                            }
                        ),
                        dcc.RadioItems(
                            id='region-radio',
                            options=[
                                {'label': ' All Regions', 'value': 'all'},
                                {'label': ' North', 'value': 'north'},
                                {'label': ' East', 'value': 'east'},
                                {'label': ' South', 'value': 'south'},
                                {'label': ' West', 'value': 'west'}
                            ],
                            value='all',
                            inline=True,
                            inputStyle={'marginRight': '6px', 'cursor': 'pointer'},
                            labelStyle={
                                'marginRight': '24px',
                                'fontSize': '14px',
                                'fontWeight': '500',
                                'cursor': 'pointer'
                            }
                        )
                    ]
                ),
                dcc.Graph(
                    id='sales-line-chart'
                )
            ]
        )
    ]
)

@app.callback(
    Output('sales-line-chart', 'figure'),
    Input('region-radio', 'value')
)
def update_chart(selected_region):
    if selected_region == 'all':
        filtered_df = df.groupby('date', as_index=False)['sales'].sum()
        chart_title = 'Pink Morsel Total Daily Sales (All Regions)'
    else:
        filtered_df = df[df['region'].str.lower() == selected_region.lower()].groupby('date', as_index=False)['sales'].sum()
        chart_title = f'Pink Morsel Total Daily Sales ({selected_region.capitalize()})'

    fig = px.line(
        filtered_df,
        x='date',
        y='sales',
        title=chart_title,
        labels={
            'date': 'Date',
            'sales': 'Sales Amount ($)'
        }
    )

    fig.add_vline(
        x='2021-01-15',
        line_width=2,
        line_dash="dash",
        line_color=COLORS['accent_line'],
        annotation_text="Price Increase (Jan 15, 2021)",
        annotation_position="top left"
    )

    fig.update_layout(
        template='plotly_white',
        title_x=0.5,
        hovermode="x unified",
        font=dict(family="'Segoe UI', sans-serif"),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)