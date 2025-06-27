import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
from datetime import datetime as dt
import numpy as np

try:
    train_df = pd.read_csv("data/train_final.csv", low_memory=False)
    train_df['date'] = pd.to_datetime(train_df['date'])
    print("Data loaded successfully from train_final.csv")

except FileNotFoundError:
    print("Files not found. Generating dummy data...")
    
    def create_dummy_data(start_date, end_date, num_stores=50, num_families=10):
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        data = []
        store_types = ['A', 'B', 'C', 'D', 'E']
        families = [f'Family_{i+1}' for i in range(num_families)]
        
        for _ in range(num_stores):
            store_nbr = np.random.randint(1, 51)
            store_type = np.random.choice(store_types)
            cluster = np.random.randint(1, 18)
            
            for date in dates:
                for family in families:
                    sales = np.random.rand() * 1000 + 50
                    onpromotion = np.random.randint(0, 50)
                    transactions = np.random.randint(50, 500)
                    type_y = np.random.choice(['Holiday', 'Regular Day', 'Event'])
                    
                    data.append([date, store_nbr, family, sales, onpromotion, 
                                f"City_{np.random.randint(1, 10)}", f"State_{np.random.randint(1, 5)}", 
                                store_type, cluster, transactions, type_y])

        df = pd.DataFrame(data, columns=['date', 'store_nbr', 'family', 'sales', 'onpromotion', 
                                         'city', 'state', 'type_x', 'cluster', 'transactions', 'type_y'])
        return df

    train_df = create_dummy_data("2016-01-01", "2017-01-01")
    train_df['date'] = pd.to_datetime(train_df['date'])
    print("Dummy data created and loaded.")
except Exception as e:
    print(f"Error loading data: {e}")
    exit()

# Prepare data
def prepare_data(df):
    df['day_of_week'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month_name()
    df['year'] = df['date'].dt.year
    return df

train_df = prepare_data(train_df)

# Color scheme
colors = {
    'background': '#0f172a',
    'text': '#e2e8f0',
    'accent': '#7c3aed',
    'secondary': '#10b981',
    'highlight': '#f59e0b',
    'card': '#1e293b',
    'border': '#334155',
    'input_text': "#000000",
    'input_bg': '#334155'
}

input_style = {
    'backgroundColor': colors['input_bg'],
    'color': colors['input_text'],
    'borderColor': colors['border'],
    'borderRadius': '5px'
}

dropdown_style = {
    **input_style,
    'width': '100%'
}

def metric_card(title, value, color):
    return html.Div(className='metric-card', style={
        'background': colors['card'],
        'borderRadius': '10px',
        'padding': '1.5rem',
        'borderLeft': f'4px solid {color}',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
        'flexGrow': '1'
    }, children=[
        html.H3(title, style={
            'color': colors['text'],
            'opacity': '0.8',
            'margin': '0 0 0.5rem 0',
            'fontSize': '1rem',
            'fontWeight': '600'
        }),
        html.H2(value, style={
            'color': color,
            'margin': '0',
            'fontSize': '2rem',
            'fontWeight': '700'
        })
    ])

def card_container(title, content, controls=None, width="48%"):
    return html.Div(className='card', style={
        'background': colors['card'],
        'borderRadius': '10px',
        'overflow': 'hidden',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
        'display': 'flex',
        'flexDirection': 'column',
        'height': '100%',
        'width': width,
        'flex': '1',
        'minWidth': '400px'
    }, children=[
        html.Div(style={
            'padding': '1.5rem',
            'borderBottom': f'1px solid {colors["border"]}',
            'background': 'linear-gradient(90deg, #0f172a 0%, #1e293b 100%)'
        }, children=[
            html.H2(title, style={
                'color': colors['text'],
                'margin': '0',
                'fontSize': '1.25rem',
                'fontWeight': '600'
            })
        ]),
        html.Div(style={'padding': '1rem'}, children=controls) if controls else None,
        html.Div(style={
            'padding': '1rem',
            'flex': '1'
        }, children=content)
    ])

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# App layout
app.layout = html.Div(
    style={
        'backgroundColor': colors['background'], 
        'color': colors['text'], 
        'minHeight': '100vh', 
        'fontFamily': 'Inter, sans-serif',
        'padding': '0'
    },
    children=[
        # Header
        html.Div(className='header', style={
            'background': 'linear-gradient(90deg, #0f172a 0%, #1e293b 100%)',
            'padding': '1.5rem 2rem',
            'borderBottom': f'1px solid {colors["border"]}',
            'boxShadow': '0 4px 12px rgba(0,0,0,0.2)',
            'textAlign': 'center'
        }, children=[
            html.H1("Sales Analytics Dashboard", style={
                'color': colors['text'],
                'margin': '0',
                'fontWeight': '800',
                'fontSize': '2.5rem',
                'background': 'linear-gradient(90deg, #7c3aed, #10b981)',
                '-webkit-background-clip': 'text',
                '-webkit-text-fill-color': 'transparent'
            }),
            html.P("Comprehensive Sales Analysis Platform", style={
                'color': colors['text'],
                'opacity': '0.8',
                'margin': '0.75rem 0 0 0',
                'fontSize': '1.1rem'
            })
        ]),
        
        # Main content
        html.Div(className='content-wrapper', style={
            'padding': '2rem',
            'maxWidth': '1600px',
            'margin': '0 auto'
        }, children=[
            # Metrics Row
            html.Div(className='metrics-row', style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(auto-fit, minmax(280px, 1fr))',
                'gap': '1.5rem',
                'marginBottom': '2rem'
            }, children=[
                metric_card("Total Sales", f"${train_df['sales'].sum():,.0f}", colors['secondary']),
                metric_card("Avg Daily Sales", f"${train_df['sales'].mean():,.0f}", colors['accent']),
                metric_card("Total Stores", f"{train_df['store_nbr'].nunique()}", colors['highlight'])
            ]),
            
            # Row 1: Sales vs Promotions and Sales by Family
            html.Div(style={
                'display': 'flex',
                'flexWrap': 'wrap',
                'justifyContent': 'space-between',
                'marginBottom': '20px',
                'gap': '15px'
            }, children=[
                card_container(
                    "Sales vs Promotions",
                    dcc.Graph(id='sales-vs-promotion', config={'displayModeBar': False}),
                    controls=[
                        dcc.RangeSlider(
                            id='promotion-range',
                            min=0,
                            max=train_df['onpromotion'].max(),
                            value=[0, train_df['onpromotion'].max()],
                            marks={i: str(i) for i in range(0, train_df['onpromotion'].max()+1, 5)},
                            step=1,
                            tooltip={"placement": "bottom", "always_visible": True}
                        )
                    ]
                ),
                card_container(
                    "Top Product Families",
                    dcc.Graph(id='top-families', config={'displayModeBar': False}),
                    controls=[
                        dcc.RadioItems(
                            id='family-metric',
                            options=[
                                {'label': 'Total Sales', 'value': 'sum'},
                                {'label': 'Average Sales', 'value': 'mean'}
                            ],
                            value='sum',
                            inline=True,
                            style={'color': colors['text']}
                        )
                    ]
                )
            ]),
            
            # Row 2: Sales by City and Sales by State
            html.Div(style={
                'display': 'flex',
                'flexWrap': 'wrap',
                'justifyContent': 'space-between',
                'marginBottom': '20px',
                'gap': '15px'
            }, children=[
                card_container(
                    "Sales by City (Top 10)",
                    dcc.Graph(id='sales-by-city', config={'displayModeBar': False}),
                    controls=[
                        dcc.Slider(
                            id='city-count',
                            min=5,
                            max=20,
                            step=1,
                            value=10,
                            marks={i: str(i) for i in range(5, 21, 5)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        )
                    ]
                ),
                card_container(
                    "Sales by State",
                    dcc.Graph(id='sales-by-state', config={'displayModeBar': False})
                )
            ]),
            
            # Row 3: Store Type and Day Type Analysis
            html.Div(style={
                'display': 'flex',
                'flexWrap': 'wrap',
                'justifyContent': 'space-between',
                'marginBottom': '20px',
                'gap': '15px'
            }, children=[
                card_container(
                    "Sales by Store Type",
                    dcc.Graph(id='store-type-performance', config={'displayModeBar': False}),
                    controls=[
                        dcc.Dropdown(
                            id='store-type-selector',
                            options=[{'label': typ, 'value': typ} for typ in train_df['type_x'].unique()],
                            value=train_df['type_x'].unique()[0],
                            multi=True,
                            style=dropdown_style
                        )
                    ]
                ),
                card_container(
                    "Sales by Day of Week",
                    dcc.Graph(id='sales-by-day', config={'displayModeBar': False})
                )
            ]),
            
            # Row 4: Cluster Performance and Monthly Sales
            html.Div(style={
                'display': 'flex',
                'flexWrap': 'wrap',
                'justifyContent': 'space-between',
                'gap': '15px'
            }, children=[
                card_container(
                    "Cluster Performance",
                    dcc.Graph(id='cluster-performance', config={'displayModeBar': False}),
                    controls=[
                        dcc.RangeSlider(
                            id='cluster-range',
                            min=train_df['cluster'].min(),
                            max=train_df['cluster'].max(),
                            value=[train_df['cluster'].min(), train_df['cluster'].max()],
                            marks={i: str(i) for i in range(train_df['cluster'].min(), train_df['cluster'].max()+1, 2)},
                            step=1,
                            tooltip={"placement": "bottom", "always_visible": True}
                        )
                    ]
                ),
                card_container(
                    "Monthly Sales Trend",
                    dcc.Graph(id='monthly-sales', config={'displayModeBar': False}),
                    controls=[
                        dcc.Dropdown(
                            id='year-selector',
                            options=[{'label': year, 'value': year} for year in sorted(train_df['year'].unique())],
                            value=sorted(train_df['year'].unique())[-1],
                            multi=True,
                            style=dropdown_style
                        )
                    ]
                )
            ])
        ]),
        
        # Footer
        html.Footer(style={
            'background': '#1e293b',
            'padding': '1.5rem',
            'textAlign': 'center',
            'marginTop': '3rem',
            'borderTop': f'1px solid {colors["border"]}',
            'boxShadow': '0 -2px 10px rgba(0,0,0,0.1)'
        }, children=[
            html.P("© 2025 Sales Analytics Dashboard", style={
                'color': colors['text'],
                'margin': '0',
                'opacity': '0.7',
                'fontSize': '0.9rem'
            })
        ])
    ]
)

# Callbacks for interactivity

# Sales vs Promotions
@callback(
    Output('sales-vs-promotion', 'figure'),
    [Input('promotion-range', 'value')]
)
def update_promotion_plot(promotion_range):
    filtered_df = train_df[(train_df['onpromotion'] >= promotion_range[0]) & 
                          (train_df['onpromotion'] <= promotion_range[1])]
    
    # Sample the data to reduce load
    if len(filtered_df) > 10000:
        filtered_df = filtered_df.sample(10000)
    
    fig = px.scatter(
        filtered_df, 
        x='onpromotion', 
        y='sales', 
        color_discrete_sequence=[colors['accent']],
        labels={'onpromotion': 'Number of Items on Promotion', 'sales': 'Sales ($)'}
    )
    
    fig.update_layout(
        plot_bgcolor=colors['card'],
        paper_bgcolor=colors['card'],
        font_color=colors['text'],
        xaxis=dict(gridcolor=colors['border']),
        yaxis=dict(gridcolor=colors['border'])
    )
    
    fig.update_traces(marker=dict(opacity=0.6))
    
    return fig

# Top Families
@callback(
    Output('top-families', 'figure'),
    [Input('family-metric', 'value')]
)
def update_top_families(metric):
    if metric == 'sum':
        family_sales = train_df.groupby('family')['sales'].sum().nlargest(10).reset_index()
        title = "Top 10 Families by Total Sales"
    else:
        family_sales = train_df.groupby('family')['sales'].mean().nlargest(10).reset_index()
        title = "Top 10 Families by Average Sales"
    
    fig = px.bar(
        family_sales, 
        x='sales', 
        y='family', 
        orientation='h',
        color_discrete_sequence=[colors['secondary']],
        labels={'sales': 'Sales ($)', 'family': 'Product Family'},
        title=title
    )
    
    fig.update_layout(
        plot_bgcolor=colors['card'],
        paper_bgcolor=colors['card'],
        font_color=colors['text'],
        yaxis={'categoryorder': 'total ascending'},
        xaxis=dict(gridcolor=colors['border'])
    )
    
    return fig

# Sales by City
@callback(
    Output('sales-by-city', 'figure'),
    [Input('city-count', 'value')]
)
def update_city_plot(count):
    if count is None or 'city' not in train_df.columns or 'sales' not in train_df.columns:
        return px.bar(title="City Sales Data Not Available")

    city_sales = train_df.groupby('city')['sales'].sum().nlargest(count).reset_index()

    fig = px.bar(
        city_sales,
        x='city',
        y='sales',
        color='sales',
        color_continuous_scale='Plasma',
        labels={'sales': 'Total Sales ($)', 'city': 'City'},
        title=f"Top {count} Cities by Sales"
    )

    fig.update_layout(
        plot_bgcolor=colors['card'],
        paper_bgcolor=colors['card'],
        font_color=colors['text'],
        xaxis=dict(gridcolor=colors['border']),
        coloraxis_showscale=False
    )

    return fig


# Sales by State
@callback(
    Output('sales-by-state', 'figure'),
    [Input('promotion-range', 'value')]
)
def update_state_plot(promotion_range):
    filtered_df = train_df[(train_df['onpromotion'] >= promotion_range[0]) & 
                          (train_df['onpromotion'] <= promotion_range[1])]
    
    state_sales = filtered_df.groupby('state')['sales'].sum().reset_index()
    
    fig = px.pie(
        state_sales, 
        values='sales', 
        names='state',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel,
        labels={'sales': 'Total Sales ($)', 'state': 'State'}
    )
    
    fig.update_layout(
        plot_bgcolor=colors['card'],
        paper_bgcolor=colors['card'],
        font_color=colors['text'],
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        )
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label'
    )
    
    return fig

# Store Type Performance
@callback(
    Output('store-type-performance', 'figure'),
    [Input('store-type-selector', 'value')]
)
def update_store_type_performance(selected_types):
    if not isinstance(selected_types, list):
        selected_types = [selected_types]
    
    filtered = train_df[train_df['type_x'].isin(selected_types)]
    store_type_sales = filtered.groupby('type_x')['sales'].sum().reset_index()
    
    fig = px.pie(
        store_type_sales,
        values='sales',
        names='type_x',
        hole=0.4,
        labels={'sales': 'Total Sales ($)', 'type_x': 'Store Type'}
    )
    
    fig.update_layout(
        plot_bgcolor=colors['card'],
        paper_bgcolor=colors['card'],
        font_color=colors['text'],
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        marker=dict(colors=px.colors.qualitative.Pastel)
    )
    
    return fig

# Sales by Day of Week
@callback(
    Output('sales-by-day', 'figure'),
    [Input('promotion-range', 'value')]
)
def update_day_plot(promotion_range):
    filtered_df = train_df[(train_df['onpromotion'] >= promotion_range[0]) & 
                          (train_df['onpromotion'] <= promotion_range[1])]
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_sales = filtered_df.groupby('day_of_week')['sales'].sum().reindex(day_order).reset_index()
    
    fig = px.bar(
        day_sales, 
        x='day_of_week', 
        y='sales',
        color='day_of_week',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        labels={'sales': 'Total Sales ($)', 'day_of_week': 'Day of Week'},
        title="Sales by Day of Week"
    )
    
    fig.update_layout(
        plot_bgcolor=colors['card'],
        paper_bgcolor=colors['card'],
        font_color=colors['text'],
        xaxis=dict(gridcolor=colors['border']),
        showlegend=False
    )
    
    return fig

# Cluster Performance
@callback(
    Output('cluster-performance', 'figure'),
    [Input('cluster-range', 'value')]
)
def update_cluster_performance(cluster_range):
    filtered = train_df[(train_df['cluster'] >= cluster_range[0]) & 
                       (train_df['cluster'] <= cluster_range[1])]
    cluster_sales = filtered.groupby('cluster')['sales'].sum().reset_index()
    
    fig = px.bar(
        cluster_sales,
        x='cluster',
        y='sales',
        color='cluster',
        labels={'sales': 'Total Sales ($)', 'cluster': 'Cluster'},
        title="Sales by Cluster"
    )
    
    fig.update_layout(
        plot_bgcolor=colors['card'],
        paper_bgcolor=colors['card'],
        font_color=colors['text'],
        xaxis=dict(
            gridcolor=colors['border'],
            type='category'
        ),
        coloraxis_showscale=False
    )
    
    return fig

# Monthly Sales Trend
@callback(
    Output('monthly-sales', 'figure'),
    [Input('year-selector', 'value')]
)
def update_monthly_sales(selected_years):
    if not isinstance(selected_years, list):
        selected_years = [selected_years]
    
    filtered = train_df[train_df['year'].isin(selected_years)]
    monthly_sales = filtered.groupby(['year', 'month'])['sales'].sum().reset_index()
    
    # Ensure months are ordered correctly
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                  'July', 'August', 'September', 'October', 'November', 'December']
    monthly_sales['month'] = pd.Categorical(monthly_sales['month'], categories=month_order, ordered=True)
    monthly_sales = monthly_sales.sort_values(['year', 'month'])
    
    fig = px.line(
        monthly_sales,
        x='month',
        y='sales',
        color='year',
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Pastel,
        labels={'sales': 'Total Sales ($)', 'month': 'Month', 'year': 'Year'},
        title="Monthly Sales Trend"
    )
    
    fig.update_layout(
        plot_bgcolor=colors['card'],
        paper_bgcolor=colors['card'],
        font_color=colors['text'],
        xaxis=dict(gridcolor=colors['border'])
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)