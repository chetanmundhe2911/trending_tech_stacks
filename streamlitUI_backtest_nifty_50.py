import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="OHLCV Viewer",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📈 OHLCV Dataset Viewer for NIFTY 50")

# Sidebar for file upload
with st.sidebar:
    st.header("Upload Your OHLCV Data")
    uploaded_file = st.file_uploader(r"C:\Users\cheta\OneDrive\Chetan\Destiny\archive\processed_nifty_50_data.xlsx", type=["xlsx", "xls"])

    # Optional: Adjust the timeframe if needed
    timeframe = st.selectbox(
        "Select Timeframe",
        ("5T", "1T", "15T", "30T", "60T"),  # Pandas offset aliases
        index=0,
        help="Choose the resampling timeframe (e.g., 5T for 5 minutes)."
    )

if uploaded_file is not None:
    try:
        # Read the uploaded Excel file
        df = pd.read_excel(uploaded_file)

        # Standardize column names to lowercase and strip whitespace
        df.columns = df.columns.str.strip().str.lower()

        # Check for necessary columns
        required_columns = {'date', 'time', 'open', 'high', 'low', 'close', 'volume'}
        if not required_columns.issubset(df.columns):
            st.error(f"The uploaded Excel file must contain the following columns: {required_columns}")
            st.stop()

        # Combine 'date' and 'time' into a single 'Datetime' column
        df['Datetime'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['time'].astype(str), format='%d-%m-%Y %H:%M')

        # Set 'Datetime' as the index
        df.set_index('Datetime', inplace=True)

        # Drop original 'date' and 'time' columns as they are no longer needed
        df.drop(['date', 'time'], axis=1, inplace=True)

        # Ensure numerical columns are of correct dtype
        numerical_cols = ['open', 'high', 'low', 'close', 'volume']
        df[numerical_cols] = df[numerical_cols].apply(pd.to_numeric, errors='coerce')

        # Optional: Resample the data to the selected timeframe
        df = df.resample(timeframe).agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }).dropna()

        # Calculate Simple Moving Averages (optional)
        df['SMA_20'] = df['close'].rolling(window=20).mean()
        df['SMA_50'] = df['close'].rolling(window=50).mean()

        st.sidebar.success("File uploaded and processed successfully!")

        # Display the raw data
        with st.expander("Show Raw Data"):
            st.dataframe(df)

        # Create the candlestick chart
        fig = go.Figure()

        # Candlestick
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name="Candlesticks"
            )
        )

        # SMA Indicators
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['sma_20'],
                mode='lines',
                line=dict(color='blue', width=1),
                name='SMA 20'
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['sma_50'],
                mode='lines',
                line=dict(color='orange', width=1),
                name='SMA 50'
            )
        )

        # Volume Bars
        fig.add_trace(
            go.Bar(
                x=df.index,
                y=df['volume'],
                marker_color='blue',
                name='Volume',
                opacity=0.3,
                yaxis='y2'
            )
        )

        # Update layout for dual y-axes
        fig.update_layout(
            title="NIFTY 50 Candlestick Chart with Volume and SMA",
            xaxis_title="Datetime",
            yaxis_title="Price",
            yaxis=dict(
                side='left'
            ),
            yaxis2=dict(
                title="Volume",
                overlaying='y',
                side='right',
                showgrid=False,
                zeroline=False
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            template='plotly_dark',
            xaxis_rangeslider_visible=False,
            hovermode="x unified",
            height=800
        )

        # Display the chart
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Awaiting Excel file to be uploaded.")
