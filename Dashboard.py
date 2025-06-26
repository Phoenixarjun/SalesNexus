import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
from datetime import datetime as dt
import os
import numpy as np # Import numpy for dummy data generation

# --- Data Loading and Preparation ---
# Load your data
try:
    # Ensure the directory exists, if not, create it for the dummy data
    if not os.path.exists("artifacts/data_preprocessing"):
        os.makedirs("artifacts/data_preprocessing")
        print("Created directory: artifacts/data_preprocessing") # Debugging print

    train_df = pd.read_csv("artifacts/data_preprocessing/train_merged.csv")
    train_df['date'] = pd.to_datetime(train_df['date'])
    print("Data loaded successfully from train_merged.csv")

except FileNotFoundError:
    print("Files not found. Please ensure the data files are in the correct directory.")
    print("Generating dummy data for demonstration purposes...")
    
    # Function to create dummy DataFrame if actual file is not found
    def create_dummy_data(start_date, end_date, num_stores=50, num_families=10):
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        data = []
        store_types = ['A', 'B', 'C', 'D', 'E']
        families = [f'Family_{i+1}' for i in range(num_families)]
        
        for _ in range(num_stores):
            store_nbr = np.random.randint(1, 51) # Random store numbers
            store_type = np.random.choice(store_types)
            cluster = np.random.randint(1, 18) # Assuming clusters from 1 to 17
            
            for date in dates:
                for family in families:
                    sales = np.random.rand() * 1000 + 50 # Random sales between 50 and 1050
                    onpromotion = np.random.randint(0, 50) # Random items on promotion
                    is_holiday = np.random.choice([0, 1], p=[0.8, 0.2]) # 20% chance of being a holiday
                    
                    data.append([date, store_nbr, family, sales, onpromotion, store_type, cluster, is_holiday])

        df = pd.DataFrame(data, columns=['date', 'store_nbr', 'family', 'sales', 'onpromotion', 'type_x', 'cluster', 'is_holiday'])
        return df

    # Define date range for dummy data
    start_date_dummy = "2016-01-01"
    end_date_dummy = "2017-01-01"
    
    # Generate and assign dummy data
    train_df = create_dummy_data(start_date_dummy, end_date_dummy)
    train_df['date'] = pd.to_datetime(train_df['date']) # Ensure date column is datetime
    
    # Optionally save the dummy data for future runs, so it doesn't regenerate every time
    train_df.to_csv("artifacts/data_preprocessing/train_merged.csv", index=False)
    print("Dummy train_merged.csv created and loaded.")
except Exception as e:
    print(f"An unexpected error occurred during data loading: {e}")
    # In a real application, you might want to log this error and gracefully exit or show an error page.
    exit()

# Prepare data by adding time-based features
def prepare_data(df):
    df['day_of_week'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month_name()
    df['year'] = df['date'].dt.year
    return df

train_df = prepare_data(train_df)

# Define a consistent dark color scheme for the dashboard
colors = {
    'background': '#0f172a',    # Dark blue-gray for the main background
    'text': '#e2e8f0',          # Light text for contrast
    'accent': '#7c3aed',        # Vibrant purple for primary highlights
    'secondary': '#10b981',     # Emerald green for secondary highlights
    'highlight': '#f59e0b',     # Amber for tertiary highlights
    'card': '#1e293b',          # Darker card background
    'border': '#334155'         # Border color for separation
}

# --- Helper Component Functions for consistent styling ---

def metric_card(title, value, color):
    """
    Creates a customizable metric card for displaying key performance indicators.
    """
    return html.Div(className='metric-card', style={
        'background': colors['card'],
        'borderRadius': '10px',
        'padding': '1.5rem',
        'borderLeft': f'4px solid {color}', # Left border for accent
        'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
        'transition': 'transform 0.3s ease', # Smooth hover effect
        'flexGrow': '1' # Allows cards to grow and fill space in a grid
    }, children=[
        html.H3(style={
            'color': colors['text'],
            'opacity': '0.8',
            'margin': '0 0 0.5rem 0',
            'fontSize': '1rem',
            'fontWeight': '600'
        }, children=title),
        html.H2(style={
            'color': color,
            'margin': '0',
            'fontSize': '2rem',
            'fontWeight': '700'
        }, children=value)
    ])

def card_container(title, content, controls=None):
    """
    Creates a container for graphs and controls with a consistent card style.
    """
    return html.Div(className='card', style={
        'background': colors['card'],
        'borderRadius': '10px',
        'overflow': 'hidden', # Ensures content doesn't spill out of rounded corners
        'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
        'display': 'flex',
        'flexDirection': 'column',
        'height': '100%' # Make sure cards fill their grid area
    }, children=[
        html.Div(style={
            'padding': '1.5rem',
            'borderBottom': f'1px solid {colors["border"]}',
            'background': 'linear-gradient(90deg, #0f172a 0%, #1e293b 100%)' # Gradient for header
        }, children=[
            html.H2(style={
                'color': colors['text'],
                'margin': '0',
                'fontSize': '1.25rem',
                'fontWeight': '600'
            }, children=title)
        ]),
        html.Div(style={'padding': '1rem'}, children=controls) if controls else None,
        html.Div(style={
            'padding': '1rem',
            'flex': '1' # Allows the content area to take up remaining space
        }, children=content)
    ])

# --- Dash App Initialization ---
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# --- App Layout with Dark Theme and Responsive Design ---
app.layout = html.Div(style={'backgroundColor': colors['background'], 'color': colors['text'], 'minHeight': '100vh', 'fontFamily': 'Inter, sans-serif'}, children=[
    # Header Section
    html.Div(className='header', style={
        'background': 'linear-gradient(90deg, #0f172a 0%, #1e293b 100%)',
        'padding': '1.5rem 2rem',
        'borderBottom': f'1px solid {colors["border"]}',
        'boxShadow': '0 4px 12px rgba(0,0,0,0.2)',
        'textAlign': 'center' # Center align header text
    }, children=[
        html.H1("SalesNexus Analytics", style={
            'color': colors['text'],
            'margin': '0',
            'fontWeight': '800', # Bolder font for title
            'fontSize': '2.5rem', # Larger font for title
            'background': 'linear-gradient(90deg, #7c3aed, #10b981)', # Gradient text
            '-webkit-background-clip': 'text',
            '-webkit-text-fill-color': 'transparent'
        }),
        html.P("AI-Powered Sales Forecasting Dashboard", style={
            'color': colors['text'],
            'opacity': '0.8',
            'margin': '0.75rem 0 0 0',
            'fontSize': '1.1rem'
        })
    ]),
    
    # Main content container
    html.Div(className='content-wrapper', style={
        'padding': '2rem',
        'maxWidth': '1600px', # Increased max width for more space
        'margin': '0 auto'
    }, children=[
        # Metrics Row - Responsive grid for KPIs
        html.Div(className='metrics-row', style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(280px, 1fr))', # Smaller minmax for better mobile
            'gap': '1.5rem', # Increased gap
            'marginBottom': '2rem'
        }, children=[
            metric_card("Total Sales", f"${train_df['sales'].sum():,.0f}", colors['secondary']),
            metric_card("Avg Daily Sales", f"${train_df['sales'].mean():,.0f}", colors['accent']),
            metric_card("Total Stores", f"{train_df['store_nbr'].nunique()}", colors['highlight'])
        ]),
        
        # Time Series and Category Analysis - Two-column responsive grid
        html.Div(className='grid-row', style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(500px, 1fr))', # Adjusted minmax
            'gap': '1.5rem',
            'marginBottom': '2rem'
        }, children=[
            card_container(
                "Sales Trend Over Time",
                dcc.Graph(id='time-series-plot', config={'displayModeBar': False}), # Hide modebar for cleaner look
                controls=[
                    html.Div(style={'marginBottom': '1rem'}, children=[
                        html.Label("Date Range:", style={'display': 'block', 'marginBottom': '0.5rem', 'color': colors['text']}),
                        dcc.DatePickerRange(
                            id='date-range',
                            min_date_allowed=train_df['date'].min(),
                            max_date_allowed=train_df['date'].max(),
                            start_date=train_df['date'].min(),
                            end_date=train_df['date'].max(),
                            style={
                                'backgroundColor': colors['card'],
                                'color': colors['text'],
                                'borderColor': colors['border'],
                                'borderRadius': '5px'
                            }
                            # Removed calendar_icon_style and clear_icon_style
                        )
                    ]),
                    html.Div(children=[
                        html.Label("Aggregation Level:", style={'display': 'block', 'marginBottom': '0.5rem', 'color': colors['text']}),
                        dcc.Dropdown(
                            id='time-aggregation',
                            options=[
                                {'label': 'Daily', 'value': 'D'},
                                {'label': 'Weekly', 'value': 'W'},
                                {'label': 'Monthly', 'value': 'M'},
                                {'label': 'Quarterly', 'value': 'Q'},
                                {'label': 'Yearly', 'value': 'Y'}
                            ],
                            value='M',
                            clearable=False,
                            style={
                                'backgroundColor': colors['card'],
                                'color': colors['text'],
                                'borderColor': colors['border'],
                                'borderRadius': '5px'
                            },
                            className='dash-dropdown-dark' # Custom class for dropdown styling
                        )
                    ])
                ]
            ),
            card_container(
                "Top Product Categories",
                dcc.Graph(id='category-sales-plot', config={'displayModeBar': False})
            )
        ]),
        
        # Promotion Impact and Cluster Performance - Two-column responsive grid
        html.Div(className='grid-row', style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(400px, 1fr))',
            'gap': '1.5rem',
            'marginBottom': '2rem'
        }, children=[
            card_container(
                "Promotion Impact Analysis",
                dcc.Graph(id='promotion-impact-plot', config={'displayModeBar': False})
            ),
            card_container(
                "Cluster Performance",
                dcc.Graph(id='cluster-performance-plot', config={'displayModeBar': False})
            )
        ]),
        
        # Holiday Impact and Store Type Performance - Two-column responsive grid
        html.Div(className='grid-row', style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(450px, 1fr))', # Adjusted minmax
            'gap': '1.5rem'
        }, children=[
            card_container(
                "Holiday Sales Impact",
                dcc.Graph(id='holiday-impact-plot', config={'displayModeBar': False})
            ),
            card_container(
                "Store Type Performance",
                dcc.Graph(id='store-type-performance', config={'displayModeBar': False}) # Corrected typo here
            )
        ])
    ]),
    
    # Footer Section
    html.Footer(style={
        'background': '#1e293b',
        'padding': '1.5rem',
        'textAlign': 'center',
        'marginTop': '3rem',
        'borderTop': f'1px solid {colors["border"]}',
        'boxShadow': '0 -2px 10px rgba(0,0,0,0.1)'
    }, children=[
        html.P("© 2023 SalesNexus | AI-Powered Sales Forecasting", style={
            'color': colors['text'],
            'margin': '0',
            'opacity': '0.7',
            'fontSize': '0.9rem'
        })
    ])
])

# --- Callbacks for Interactive Plots ---

@callback(
    Output('time-series-plot', 'figure'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('time-aggregation', 'value')]
)
def update_time_series(start_date, end_date, aggregation):
    # Convert date strings to datetime objects for filtering
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # Filter DataFrame based on selected date range
    filtered_df = train_df[(train_df['date'] >= start_date) & (train_df['date'] <= end_date)]
    
    # Resample and sum sales based on selected aggregation level
    time_series = filtered_df.resample(aggregation, on='date')['sales'].sum().reset_index()
    
    # Create line plot using Plotly Express
    fig = px.line(time_series, x='date', y='sales', 
                  title=None, # Title handled by card_container
                  labels={'sales': 'Total Sales', 'date': 'Date'})
    
    # Update layout for dark theme consistency
    fig.update_layout(
        plot_bgcolor=colors['card'],
        paper_bgcolor=colors['card'],
        font_color=colors['text'],
        hovermode='x unified', # Shows hover info across all traces at a given x-value
        xaxis=dict(
            gridcolor=colors['border'],
            linecolor=colors['border'],
            showgrid=True, # Ensure grid lines are visible
            tickfont=dict(color=colors['text'])
        ),
        yaxis=dict(
            gridcolor=colors['border'],
            linecolor=colors['border'],
            showgrid=True,
            tickfont=dict(color=colors['text'])
        ),
        margin=dict(l=20, r=20, t=30, b=20), # Adjust margins for better fit
        # Add tooltips for better user experience on hover
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Inter, sans-serif"
        )
    )
    
    fig.update_traces(
        line=dict(color=colors['accent'], width=3), # Accent color for the line
        hovertemplate='<b>%{x|%b %d, %Y}</b><br>Sales: %{y:,.0f}<extra></extra>' # Custom hover text
    )
    
    return fig

@callback(
    Output('category-sales-plot', 'figure'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_category_sales(start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = train_df[(train_df['date'] >= start_date) & (train_df['date'] <= end_date)]
    
    # Group by product family and get top 10 categories by sales
    category_sales = filtered_df.groupby('family')['sales'].sum().nlargest(10).reset_index()
    
    # Create horizontal bar chart
    fig = px.bar(category_sales, x='sales', y='family', orientation='h',
                 title=None,
                 labels={'sales': 'Total Sales', 'family': 'Product Category'})
    
    fig.update_layout(
        plot_bgcolor=colors['card'],
        paper_bgcolor=colors['card'],
        font_color=colors['text'],
        yaxis={'categoryorder':'total ascending', 'tickfont': dict(color=colors['text'])}, # Sort categories by sales
        xaxis=dict(
            gridcolor=colors['border'],
            linecolor=colors['border'],
            showgrid=True,
            tickfont=dict(color=colors['text'])
        ),
        margin=dict(l=20, r=20, t=30, b=20),
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Inter, sans-serif"
        )
    )
    
    fig.update_traces(
        marker_color=colors['secondary'], # Secondary color for bars
        hovertemplate='<b>%{y}</b><br>Sales: %{x:,.0f}<extra></extra>'
    )
    
    return fig

@callback(
    Output('promotion-impact-plot', 'figure'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_promotion_impact(start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = train_df[(train_df['date'] >= start_date) & (train_df['date'] <= end_date)]
    
    # Create scatter plot with a LOESS trendline to show promotion impact on sales
    fig = px.scatter(filtered_df, x='onpromotion', y='sales', 
                     title=None,
                     labels={'onpromotion': 'Number of Items on Promotion', 'sales': 'Sales'},
                     trendline="lowess") # LOESS regression for non-linear trend
    
    fig.update_layout(
        plot_bgcolor=colors['card'],
        paper_bgcolor=colors['card'],
        font_color=colors['text'],
        xaxis=dict(
            gridcolor=colors['border'],
            linecolor=colors['border'],
            showgrid=True,
            tickfont=dict(color=colors['text'])
        ),
        yaxis=dict(
            gridcolor=colors['border'],
            linecolor=colors['border'],
            showgrid=True,
            tickfont=dict(color=colors['text'])
        ),
        margin=dict(l=20, r=20, t=30, b=20),
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Inter, sans-serif"
        )
    )
    
    fig.update_traces(
        marker=dict(color=colors['highlight'], opacity=0.6), # Highlight color for points
        line=dict(color=colors['accent'], width=3), # Accent color for trendline
        hovertemplate='<b>Promotions: %{x}</b><br>Sales: %{y:,.0f}<extra></extra>'
    )
    
    return fig

@callback(
    Output('cluster-performance-plot', 'figure'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_cluster_performance(start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = train_df[(train_df['date'] >= start_date) & (train_df['date'] <= end_date)]
    
    # Group by cluster and sum sales
    cluster_sales = filtered_df.groupby('cluster')['sales'].sum().reset_index()
    
    fig = px.bar(cluster_sales, x='cluster', y='sales',
                 title=None,
                 labels={'sales': 'Total Sales', 'cluster': 'Cluster'})
    
    fig.update_layout(
        plot_bgcolor=colors['card'],
        paper_bgcolor=colors['card'],
        font_color=colors['text'],
        xaxis={'type': 'category', 'linecolor': colors['border'], 'tickfont': dict(color=colors['text'])},
        yaxis=dict(
            gridcolor=colors['border'],
            linecolor=colors['border'],
            showgrid=True,
            tickfont=dict(color=colors['text'])
        ),
        margin=dict(l=20, r=20, t=30, b=20),
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Inter, sans-serif"
        )
    )
    
    fig.update_traces(
        marker_color=colors['accent'], # Accent color for bars
        hovertemplate='<b>Cluster %{x}</b><br>Sales: %{y:,.0f}<extra></extra>'
    )
    
    return fig

@callback(
    Output('holiday-impact-plot', 'figure'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_holiday_impact(start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = train_df[(train_df['date'] >= start_date) & (train_df['date'] <= end_date)]
    
    # --- Robustness check for 'is_holiday' column ---
    if 'is_holiday' not in filtered_df.columns:
        print("Warning: 'is_holiday' column not found in filtered data. Returning empty figure for Holiday Impact plot.")
        return {} # Return an empty figure dictionary if column is missing
        
    holiday_sales = filtered_df.groupby('is_holiday')['sales'].mean().reset_index()
    
    # Map numerical 'is_holiday' to descriptive strings, handle potential missing values after map
    holiday_sales['is_holiday'] = holiday_sales['is_holiday'].map({0: 'Non-Holiday', 1: 'Holiday'}).fillna('Unknown')
    
    fig = px.bar(holiday_sales, x='is_holiday', y='sales',
                 title=None,
                 labels={'sales': 'Average Sales', 'is_holiday': 'Day Type'})
    
    fig.update_layout(
        plot_bgcolor=colors['card'],
        paper_bgcolor=colors['card'],
        font_color=colors['text'],
        xaxis={'linecolor': colors['border'], 'tickfont': dict(color=colors['text'])},
        yaxis=dict(
            gridcolor=colors['border'],
            linecolor=colors['border'],
            showgrid=True,
            tickfont=dict(color=colors['text'])
        ),
        margin=dict(l=20, r=20, t=30, b=20),
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Inter, sans-serif"
        )
    )
    
    fig.update_traces(
        marker_color=[colors['secondary'], colors['highlight']], # Different colors for categories
        hovertemplate='<b>%{x}</b><br>Avg Sales: %{y:,.0f}<extra></extra>'
    )
    
    return fig

@callback(
    Output('store-type-performance', 'figure'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_store_type_performance(start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = train_df[(train_df['date'] >= start_date) & (train_df['date'] <= end_date)]

    # --- Robustness check for 'type_x' column ---
    if 'type_x' not in filtered_df.columns:
        print("Warning: 'type_x' column not found in filtered data. Returning empty figure for Store Type Performance plot.")
        return {} # Return an empty figure dictionary if column is missing
        
    store_type_sales = filtered_df.groupby('type_x')['sales'].sum().reset_index()
    
    fig = px.pie(store_type_sales, values='sales', names='type_x',
                 title=None,
                 hole=0.4) # Donut chart
    
    fig.update_layout(
        plot_bgcolor=colors['card'],
        paper_bgcolor=colors['card'],
        font_color=colors['text'],
        margin=dict(l=20, r=20, t=30, b=20),
        # Position legend at the bottom center
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2, # Adjust vertical position
            xanchor="center",
            x=0.5, # Center horizontally
            font=dict(color=colors['text'])
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Inter, sans-serif"
        )
    )
    
    fig.update_traces(
        textposition='inside', # Show percentage and label inside slices
        textinfo='percent+label',
        marker=dict(colors=[colors['accent'], colors['secondary'], colors['highlight'], '#6366f1', '#8b5cf6']), # Custom colors for slices
        hovertemplate='<b>%{label}</b><br>Sales: %{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
