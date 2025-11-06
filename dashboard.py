import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Energy Dashboard + Forecast", layout="wide")

# Helpers / Load Data
@st.cache_data
def load_data(path="cleaned_consumption_dataset.csv"):
    df = pd.read_csv(path)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Date'] = df['Timestamp'].dt.date
    df['Hour'] = df['Timestamp'].dt.hour
    df['Weekday'] = df['Timestamp'].dt.day_name()
    return df

@st.cache_data
def load_forecast_data(path="forecast_next_7_days.csv"):
    """Loads the pre-computed forecast data."""
    forecast_df = pd.read_csv(path)
    forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])
    return forecast_df

df = load_data()
forecast_df = load_forecast_data() # Load forecast data

# global list of consumers (used in both tabs)
all_consumers = sorted(df['Consumer'].unique())

# Top-level tabs: Dashboard (EDA) and Forecast
tab1, tab2 = st.tabs(["Dashboard (EDA)", "Forecast (Prophet)"])

# TAB 1 - Dashboard (EDA)
with tab1:
    st.title("⚡ Energy Consumption Dashboard")

    # Per-tab consumer filter (placed inside the EDA tab)
    eda_consumers = st.multiselect(
        "Select Consumers (for EDA)",
        options=all_consumers,
        default=all_consumers,
        key="eda_consumers"
    )

    if not eda_consumers:
        st.warning("No consumers selected — showing all.")
        df_filtered = df.copy()
    else:
        df_filtered = df[df['Consumer'].isin(eda_consumers)]

    # Define a color palette for consumers
    color_palette = px.colors.qualitative.Set2  # or try Set3 / Bold / Dark24

    # Consumption Trends (daily)
    daily = df_filtered.groupby(['Date', 'Consumer'])['Consumption'].sum().reset_index()
    fig1 = px.line(
        daily,
        x='Date',
        y='Consumption',
        color='Consumer',
        title='Daily Consumption Trends',
        color_discrete_sequence=color_palette
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Comparative Analysis (average)
    avg_consumption = df_filtered.groupby('Consumer')['Consumption'].mean().reset_index()
    fig2 = px.bar(
        avg_consumption,
        x='Consumer',
        y='Consumption',
        title='Average Consumption by Consumer',
        color='Consumer',
        color_discrete_sequence=color_palette
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Peak Demand (hourly average)
    hourly_avg = df_filtered.groupby(['Hour', 'Consumer'])['Consumption'].mean().reset_index()
    fig3 = px.bar(
        hourly_avg,
        x='Hour',
        y='Consumption',
        color='Consumer',
        title='Average Hourly Consumption',
        barmode='group',
        color_discrete_sequence=color_palette
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Usage Distribution (boxplot by consumer)
    fig4 = px.box(
        df_filtered,
        x='Consumer',
        y='Consumption',
        color='Consumer',
        title='Consumption Distribution by Consumer',
        color_discrete_sequence=color_palette
    )
    st.plotly_chart(fig4, use_container_width=True)

    # Extra Insights - Weekday average
    weekday_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    weekday_avg = (
        df_filtered.groupby(['Weekday', 'Consumer'])['Consumption']
                .mean()
                .reindex(weekday_order, level=0)
                .reset_index()
    )
    fig5 = px.bar(
        weekday_avg,
        x='Weekday',
        y='Consumption',
        color='Consumer',
        title='Average Consumption by Weekday',
        barmode='group',
        color_discrete_sequence=color_palette
    )
    st.plotly_chart(fig5, use_container_width=True)

# TAB 2 - Forecast (Prophet)
with tab2:
    st.title("Energy Consumption Forecast (Prophet)")

    st.markdown("### View Forecast for a Specific Consumer")
    st.markdown(
        "This data represents a 7-day forecast loaded from `forecast_next_7_days.csv`. "
        "Select a consumer below to visualize their predicted consumption."
    )

    # Get list of consumers from the forecast file, or use all_consumers if they match
    forecast_consumers_list = sorted(forecast_df['Consumer'].unique())

    # Filter for forecast tab
    forecast_consumer = st.selectbox(
        "Select Consumer (for Forecast)",
        options=forecast_consumers_list, 
        key="forecast_consumer"
    )

    if forecast_consumer:
        st.subheader(f"Forecast Plot for: {forecast_consumer}")
        
        # Filter data for the selected consumer
        consumer_forecast_df = forecast_df[forecast_df['Consumer'] == forecast_consumer].copy()

        if consumer_forecast_df.empty:
            st.warning(f"No forecast data found for {forecast_consumer} in 'forecast_next_7_days.csv'.")
        else:
            # Create the forecast plot using Plotly GO
            fig_forecast = go.Figure()

            # Add the confidence interval (upper and lower bounds)
            fig_forecast.add_trace(go.Scatter(
                x=consumer_forecast_df['ds'],
                y=consumer_forecast_df['yhat_upper'],
                mode='lines',
                line=dict(width=0),
                fillcolor='rgba(68, 68, 68, 0.2)',
                fill='tonexty', # Fill to the 'yhat_lower' trace
                name='Confidence Interval'
            ))

            fig_forecast.add_trace(go.Scatter(
                x=consumer_forecast_df['ds'],
                y=consumer_forecast_df['yhat_lower'],
                mode='lines',
                line=dict(width=0),
                fillcolor='rgba(68, 68, 68, 0.2)',
                name='Lower Bound',
                showlegend=False # Hide legend for this trace
            ))

            # Add the forecast line (yhat)
            fig_forecast.add_trace(go.Scatter(
                x=consumer_forecast_df['ds'],
                y=consumer_forecast_df['yhat'],
                mode='lines',
                line=dict(color='royalblue', width=3),
                name='Forecast (yhat)'
            ))

            fig_forecast.update_layout(
                title=f"7-Day Consumption Forecast for {forecast_consumer}",
                xaxis_title="Date",
                yaxis_title="Predicted Consumption",
                hovermode="x unified",
                legend_title_text="Components"
            )

            st.plotly_chart(fig_forecast, use_container_width=True)

            #  To display the raw forecast data
            with st.expander("View Raw Forecast Data"):
                st.dataframe(
                    consumer_forecast_df[['ds', 'yhat', 'yhat_lower', 'yhat_upper', 'trend']]
                    .style.format({"yhat": "{:.2f}", "yhat_lower": "{:.2f}", "yhat_upper": "{:.2f}", "trend": "{:.2f}"})
                )

    else:
        st.info("Select a consumer from the dropdown to see their 7-day forecast.")