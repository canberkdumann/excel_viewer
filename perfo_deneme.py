import streamlit as st
import pandas as pd
import numpy as np
import re
import sys
import io
import math
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import time
import hashlib
from datetime import datetime
from contextlib import contextmanager
import os
from PIL import Image
import base64

# Set page configuration
st.set_page_config(
    page_title="Enterprise Excel Viewer",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Performance Monitoring System
class PerformanceMonitor:
    def __init__(self):
        self.operations = []
        self.operation_history = []

    def start_operation(self, operation_name):
        operation = {
            'operation': operation_name,
            'start_time': datetime.now(),
        }
        return operation

    def end_operation(self, operation, success=True):
        end_time = datetime.now()
        operation['end_time'] = end_time
        operation['duration'] = (end_time - operation['start_time']).total_seconds()
        operation['success'] = success

        self.operations.append(operation)
        self.operation_history.append(operation)

        if len(self.operation_history) > 100:
            self.operation_history = self.operation_history[-100:]

        return operation

    @contextmanager
    def track_operation(self, operation_name):
        operation = self.start_operation(operation_name)
        try:
            yield operation
            self.end_operation(operation, True)
        except Exception:
            self.end_operation(operation, False)
            raise

    def get_stats(self):
        if not self.operations:
            return None

        total_operations = len(self.operations)
        successful_operations = sum(1 for op in self.operations if op['success'])
        failed_operations = total_operations - successful_operations
        average_execution_time = sum(op['duration'] for op in self.operations) / total_operations
        success_rate = (successful_operations / total_operations) * 100

        return {
            'total_operations': total_operations,
            'successful_operations': successful_operations,
            'failed_operations': failed_operations,
            'average_execution_time': average_execution_time,
            'success_rate': success_rate,
        }

# Smart Cache System
class SmartCache:
    def __init__(self, max_size=100):
        self.cache = {}
        self.access_times = {}
        self.max_size = max_size

    def get(self, key):
        if key in self.cache:
            self.access_times[key] = time.time()
            return self.cache[key]
        return None

    def set(self, key, value):
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.access_times, key=self.access_times.get)
            del self.cache[oldest_key]
            del self.access_times[oldest_key]

        self.cache[key] = value
        self.access_times[key] = time.time()

# Smart Error Handler
class SmartErrorHandler:
    @staticmethod
    def categorize_error(error):
        error_str = str(error).lower()
        if 'memory' in error_str:
            return {
                'category': 'Memory',
                'message': 'Memory issue detected.',
                'solution': 'Reduce file size or use pagination.',
            }
        elif 'file' in error_str:
            return {
                'category': 'File',
                'message': 'File not found or unreadable.',
                'solution': 'Check file path and ensure the file exists.',
            }
        elif 'permission' in error_str:
            return {
                'category': 'Permission',
                'message': 'Permission denied.',
                'solution': 'Check file permissions or run as administrator.',
            }
        elif 'encoding' in error_str:
            return {
                'category': 'Encoding',
                'message': 'Character encoding issue.',
                'solution': 'Ensure the file is saved in UTF-8 format.',
            }
        else:
            return {
                'category': 'General',
                'message': 'Unexpected error occurred.',
                'solution': 'Check the file and try again.',
            }

    @staticmethod
    def display_error(error):
        error_info = SmartErrorHandler.categorize_error(error)
        st.error(f"**{error_info['category']} Error**: {error_info['message']}\nSolution: {error_info['solution']}")

# Data Validator
class DataValidator:
    @staticmethod
    def validate_excel_file(df):
        total_cells = df.size
        null_cells = df.isnull().sum().sum()
        duplicate_rows = df.duplicated().sum()

        quality_score = max(0, 100 - (null_cells / total_cells * 50) - (duplicate_rows / len(df) * 30))

        return {
            'is_valid': quality_score > 60,
            'quality_score': quality_score,
            'null_cells': null_cells,
            'duplicate_rows': duplicate_rows,
        }

# Smart Visualizer
class SmartVisualizer:
    @staticmethod
    def create_data_overview_chart(df):
        dtype_counts = df.dtypes.value_counts()
        fig = px.pie(
            values=dtype_counts.values,
            names=dtype_counts.index.astype(str),
            title="Data Type Distribution",
        )
        return fig

# Initialize systems
if 'perf_monitor' not in st.session_state:
    st.session_state.perf_monitor = PerformanceMonitor()

if 'smart_cache' not in st.session_state:
    st.session_state.smart_cache = SmartCache()

# Ensure session state persists across page reloads
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

if 'selected_file' not in st.session_state:
    st.session_state.selected_file = None

# Directory to store uploaded files
uploads_dir = "uploads"
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

# List previously uploaded files
uploaded_files = [f for f in os.listdir(uploads_dir) if f.endswith(".xlsx")]


tab1, tab2, tab3, tab4 = st.tabs(["Data Analysis", "Smart Analytics", "Performance", "Favorites"])

# Add export functionality
def download_link(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)
    
    b64 = base64.b64encode(object_to_download.encode()).decode()  # Encode to base64
    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

# Extend Data Validation and Recommendations
with tab1:
    st.markdown(
        """
        <style>
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
        }
        .card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            background-color: var(--background-color, #f9f9f9);
            color: var(--text-color, #333);
        }
        .card h4 {
            margin: 0 0 10px 0;
            color: var(--text-color, #333);
        }
        .card ul {
            padding-left: 20px;
            color: var(--text-color, #333);
        }
        </style>
        <div class="main-header">
            <h1>🚀 Enterprise Excel Viewer</h1>
            <p>Analyze your data with advanced insights and modern UI</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # File upload
    uploaded_file = st.file_uploader(
        "Upload your Excel file", 
        type=["xlsx"], 
        key="file_uploader_tab1"
    )

    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file
        try:
            df = pd.read_excel(uploaded_file)

            # Display uploaded file name
            st.write(f"### Uploaded: {uploaded_file.name}")

            # Add search functionality
            st.write("### Search and Filter Records")
            search_keyword = st.text_input("Enter a keyword to search:")

            if search_keyword:
                filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_keyword, case=False).any(), axis=1)]
            else:
                filtered_df = df

            # Display filtered card view
            st.write("### Card View")
            if not filtered_df.empty:
                for idx, row in filtered_df.iterrows():
                    with st.container():
                        st.markdown(
                            f"""
                            <div class='card'>
                                <h4>Record #{idx + 1}</h4>
                                <ul>
                                    {''.join([f'<li><strong>{col}:</strong> {row[col]}</li>' for col in filtered_df.columns])}
                                </ul>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"⭐ Add to Favorites (Record #{idx + 1})", key=f"add_fav_{uploaded_file.name}_{idx}"):
                                st.session_state.favorites.append(row.to_dict())
                                st.success(f"Record #{idx + 1} added to favorites!")
                        with col2:
                            if st.button(f"❌ Remove from Favorites (Record #{idx + 1})", key=f"remove_fav_{uploaded_file.name}_{idx}"):
                                if row.to_dict() in st.session_state.favorites:
                                    st.session_state.favorites.remove(row.to_dict())
                                    st.warning(f"Record #{idx + 1} removed from favorites!")
            else:
                st.warning("No records match your search. Please try a different keyword.")

            # Add export buttons
            if not filtered_df.empty:
                st.write("### Export Data")
                col1, col2, col3 = st.columns(3)

                with col1:
                    csv_link = download_link(filtered_df, "filtered_data.csv", "📥 Export as CSV")
                    st.markdown(csv_link, unsafe_allow_html=True)

                with col2:
                    json_link = download_link(filtered_df.to_json(orient="records"), "filtered_data.json", "📥 Export as JSON")
                    st.markdown(json_link, unsafe_allow_html=True)

        except Exception as e:
            error_handler = SmartErrorHandler()
            error_handler.display_error(e)

    # File deletion
    if uploaded_files:
        st.sidebar.markdown("---")
        st.sidebar.subheader("🗑️ File Management")

        files_to_delete = []
        for file in uploaded_files:
            col1, col2 = st.sidebar.columns([3, 1])
            col1.text(file[:20] + "..." if len(file) > 20 else file)
            if col2.button("🗑️", key=f"delete_{file}", help=f"Delete {file}"):
                files_to_delete.append(file)

        for file_to_delete in files_to_delete:
            try:
                file_path = os.path.join(uploads_dir, file_to_delete)
                os.remove(file_path)
                st.sidebar.success(f"✅ {file_to_delete} deleted!")
                st.experimental_rerun()
            except Exception as e:
                st.sidebar.error(f"❌ Could not delete {file_to_delete}: {e}")

  
with tab2:
    st.header("🤖 Smart Analytics")
    st.write("Advanced insights and recommendations.")

    if 'df' in locals() and isinstance(df, pd.DataFrame):
        # Total number of records
        total_records = len(df)
        st.metric(label="Total Records", value=total_records)

        # Most frequent words in the dataset
        all_text = ' '.join(df.astype(str).apply(lambda x: ' '.join(x), axis=1))
        word_counts = pd.Series(all_text.split()).value_counts()
        top_words = word_counts.head(5)

        st.write("### Top 5 Most Frequent Words")
        for word, count in top_words.items():
            st.write(f"{word}: {count} occurrences")

        # Additional statistics can be added here
    else:
        st.info("No data available. Please upload an Excel file to see analytics.")

# Add performance metrics to the Performance tab
with tab3:
    st.header("⚡ Performance")
    st.write("Monitor and optimize application performance.")

    perf_stats = st.session_state.perf_monitor.get_stats()
    if perf_stats:
        st.write("### Performance Metrics")
        st.metric("Total Operations", perf_stats['total_operations'])
        st.metric("Successful Operations", perf_stats['successful_operations'])
        st.metric("Failed Operations", perf_stats['failed_operations'])
        st.metric("Average Execution Time", f"{perf_stats['average_execution_time']:.2f} seconds")
        st.metric("Success Rate", f"{perf_stats['success_rate']:.1f}%")

        st.write("### Operation History")
        history = st.session_state.perf_monitor.operation_history
        if history:
            history_df = pd.DataFrame(history)
            st.dataframe(history_df.tail(10), use_container_width=True)
    else:
        st.info("No performance data available yet. Perform some operations to see metrics.")

# Correctly set query parameters using st.query_params
with tab4:
    st.header("⭐ Favorites")
    if st.session_state.favorites:
        favorites_df = pd.DataFrame(st.session_state.favorites)

        # Display favorites in table view
        st.write("### Favorite Records (Table View)")
        st.dataframe(favorites_df)

        # Display favorites in card view
        st.write("### Favorite Records (Card View)")
        for idx, row in favorites_df.iterrows():
            with st.container():
                st.markdown(
                    f"""
                    <div class='card'>
                        <h4>Favorite Record #{idx + 1}</h4>
                        <ul>
                            {''.join([f'<li><strong>{col}:</strong> {row[col]}</li>' for col in favorites_df.columns])}
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                if st.button(f"❌ Remove from Favorites (Record #{idx + 1})", key=f"remove_fav_tab4_{idx}"):
                    st.session_state.favorites.remove(row.to_dict())
                    st.warning(f"Record #{idx + 1} removed from favorites!")
                    # Workaround to refresh the UI dynamically
                    st.session_state["refresh_trigger"] = not st.session_state.get("refresh_trigger", False)
    else:
        st.info("No favorite records yet. Add some from the Data Analysis tab!")

# Add a feedback panel under File Management in the sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("💬 Feedback")
st.sidebar.write("We value your feedback! Please share your questions, suggestions or comments.")

# Feedback button to send an email
if st.sidebar.button("Send Feedback via Email"):
    feedback_email = "mailto:CemilCanberk.DUMAN@vakifbank.com.tr?subject=Feedback%20on%20Excel%20Viewer&body=Please%20share%20your%20feedback%20here."
    st.sidebar.markdown(f"[Click here to send feedback](<{feedback_email}>)", unsafe_allow_html=True)

# Add custom CSS for the toolbar
st.markdown(
    """
    <style>
    .st-emotion-cache-14vh5up {
        display: flex;
        -webkit-box-align: center;
        align-items: center;
        height: 100%;
        width: 100%;
        padding: 0px;
        pointer-events: auto;
        position: relative;
        z-index: 999990;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add additional custom CSS for the toolbar
st.markdown(
    """
    <style>
    .st-emotion-cache-1ffuo7c {
        position: absolute;
        top: 0px;
        left: -15px;
        right: 0px;
        display: flex;
        -webkit-box-align: center;
        align-items: center;
        height: 3.75rem;
        min-height: 3.75rem;
        width: 100%;
        background: rgb(255, 255, 255);
        outline: none;
        z-index: 999990;
        pointer-events: auto;
        font-size: 0.875rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add additional custom CSS for the toolbar
st.markdown(
    """
    <style>
    .st-emotion-cache-gquqoo {
        position: absolute;
        top: 0px;
        left: -15px;
        right: 0px;
        display: flex;
        -webkit-box-align: center;
        align-items: center;
        height: 3.75rem;
        min-height: 3.75rem;
        width: 100%;
        background: rgb(14, 17, 23);
        outline: none;
        z-index: 999990;
        pointer-events: auto;
        font-size: 0.875rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add additional custom CSS for the terminal button
st.markdown(
    """
    <style>
    ._terminalButton_rix23_138 {
        position: fixed;
        right: 10px;
        bottom: 0;
        font-size: .875rem;
        line-height: 1.25rem;
        padding: .75rem 1.5rem;
        --tw-text-opacity: 1;
        color: rgb(255 255 255 / var(--tw-text-opacity));
        --tw-bg-opacity: 1;
        background-color: rgb(14 17 23 / var(--tw-bg-opacity));
        display: flex;
        align-items: center;
        border-radius: .5rem .25rem .25rem;
        border-bottom-left-radius: 0;
        border-top-right-radius: 0;
        border-bottom-right-radius: 0;
        -webkit-user-select: none;
        user-select: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)


