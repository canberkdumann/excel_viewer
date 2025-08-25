# perfo_destek_app.py
# Streamlit arayüzü: "Perfo Destek Çözümleri.xlsx" gibi dosyalar için
# Kolonlar: Talep No, Talep Açıklaması, Yanıt, Yanıt Açıklaması (ve diğerleri)
# Çalıştırma: streamlit run perfo_destek_app.py


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
import pickle
from datetime import datetime, timedelta
from contextlib import contextmanager
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any, Optional


st.set_page_config(
    page_title="🚀 Enterprise Excel Görüntüleyici",
    page_icon="ğŸ—‚ï¸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ğŸš€ MODERN ENTERPRISE FEATURES
# ===============================

# 1. PERFORMANCE MONITORING SYSTEM
class PerformanceMonitor:
    def __init__(self):
        self.operations = []
        self.operation_history = []
    
    def start_operation(self, operation_name):
        operation = {
            'operation': operation_name,
            'start_time': datetime.now(),
            'timestamp': datetime.now()
        }
        return operation
    
    def end_operation(self, operation, success=True):
        end_time = datetime.now()
        operation['end_time'] = end_time
        operation['duration'] = (end_time - operation['start_time']).total_seconds()
        operation['success'] = success
        
        self.operations.append(operation)
        self.operation_history.append(operation)
        
        # Keep only last 100 operations for memory efficiency
        if len(self.operation_history) > 100:
            self.operation_history = self.operation_history[-100:]
        
        return operation
    
    @contextmanager
    def track_operation(self, operation_name):
        operation = self.start_operation(operation_name)
        try:
            yield operation
            self.end_operation(operation, True)
        except Exception as e:
            self.end_operation(operation, False)
            raise
    
    def get_stats(self):
        """Get performance statistics"""
        if not self.operations:
            return None
        
        total_operations = len(self.operations)
        successful_operations = sum(1 for op in self.operations if op.get('success', False))
        failed_operations = total_operations - successful_operations
        
        durations = [op['duration'] for op in self.operations if 'duration' in op]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        return {
            'total_operations': total_operations,
            'successful_operations': successful_operations,
            'failed_operations': failed_operations,
            'average_execution_time': avg_duration,
            'success_rate': (successful_operations / total_operations * 100) if total_operations > 0 else 0
        }

# 2. SMART CACHE SYSTEM
class SmartCache:
    def __init__(self, max_size=100):
        self.cache = {}
        self.access_times = {}
        self.max_size = max_size
    
    def _generate_key(self, data):
        """Generate unique key for data"""
        if isinstance(data, str):
            return hashlib.md5(data.encode()).hexdigest()
        return hashlib.md5(str(data).encode()).hexdigest()
    
    def get(self, key):
        if key in self.cache:
            self.access_times[key] = time.time()
            self._track_hit()
            return self.cache[key]
        else:
            self._track_miss()
            return None
    
    def set(self, key, value):
        if len(self.cache) >= self.max_size:
            # Remove oldest accessed item
            oldest_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
            del self.cache[oldest_key]
            del self.access_times[oldest_key]
        
        self.cache[key] = value
        self.access_times[key] = time.time()
    
    def clear(self):
        self.cache.clear()
        self.access_times.clear()
    
    def get_stats(self):
        """Get cache statistics"""
        # Initialize counters if not exist
        if not hasattr(self, 'hits'):
            self.hits = 0
        if not hasattr(self, 'misses'):
            self.misses = 0
        if not hasattr(self, 'total_requests'):
            self.total_requests = 0
        
        return {
            'hits': getattr(self, 'hits', 0),
            'misses': getattr(self, 'misses', 0),
            'total_requests': getattr(self, 'total_requests', 0),
            'cache_size': len(self.cache),
            'max_size': self.max_size,
            'hit_rate': (getattr(self, 'hits', 0) / max(getattr(self, 'total_requests', 1), 1)) * 100
        }
    
    def _track_hit(self):
        """Track cache hit"""
        if not hasattr(self, 'hits'):
            self.hits = 0
        if not hasattr(self, 'total_requests'):
            self.total_requests = 0
        self.hits += 1
        self.total_requests += 1
    
    def _track_miss(self):
        """Track cache miss"""
        if not hasattr(self, 'misses'):
            self.misses = 0
        if not hasattr(self, 'total_requests'):
            self.total_requests = 0
        self.misses += 1
        self.total_requests += 1

# 3. ADVANCED ERROR HANDLER
class SmartErrorHandler:
    @staticmethod
    def categorize_error(error):
        error_str = str(error).lower()
        
        if 'memory' in error_str or 'ram' in error_str:
            return {
                'category': 'Memory',
                'severity': 'High',
                'message': 'Bellek yetersizliÄŸi tespit edildi',
                'solution': 'Dosya boyutunu kÃ¼Ã§Ã¼ltÃ¼n veya sayfalama kullanÄ±n',
                'icon': 'ğŸ§ '
            }
        elif 'file' in error_str or 'no such file' in error_str:
            return {
                'category': 'File',
                'severity': 'Medium',
                'message': 'Dosya bulunamadÄ± veya okunamadÄ±',
                'solution': 'Dosya yolunu kontrol edin ve dosyanÄ±n mevcut olduÄŸundan emin olun',
                'icon': 'ğŸ“'
            }
        elif 'permission' in error_str or 'access' in error_str:
            return {
                'category': 'Permission',
                'severity': 'Medium',
                'message': 'Dosya eriÅŸim izni hatasÄ±',
                'solution': 'DosyanÄ±n aÃ§Ä±k olmadÄ±ÄŸÄ±ndan emin olun veya yÃ¶netici izinleri alÄ±n',
                'icon': 'ğŸ”’'
            }
        elif 'encoding' in error_str or 'decode' in error_str:
            return {
                'category': 'Encoding',
                'severity': 'Low',
                'message': 'Karakter kodlama hatasÄ±',
                'solution': 'DosyayÄ± UTF-8 formatÄ±nda kaydedin',
                'icon': 'ğŸ”¤'
            }
        else:
            return {
                'category': 'General',
                'severity': 'Medium',
                'message': 'Beklenmeyen hata',
                'solution': 'DosyayÄ± kontrol edin ve tekrar deneyin',
                'icon': 'âš ï¸'
            }
    
    @staticmethod
    def display_error(error, context=""):
        error_info = SmartErrorHandler.categorize_error(error)
        
        with st.container():
            st.error(f"""
            {error_info['icon']} **{error_info['category']} HatasÄ±** ({error_info['severity']} Ã–ncelik)
            
            **Problem:** {error_info['message']}
            
            **Ã‡Ã¶zÃ¼m:** {error_info['solution']}
            
            {f"**BaÄŸlam:** {context}" if context else ""}
            """)

# 4. DATA VALIDATOR
class DataValidator:
    @staticmethod
    def validate_excel_file(df: pd.DataFrame) -> Dict[str, Any]:
        """Comprehensive data quality analysis"""
        total_cells = df.shape[0] * df.shape[1]
        null_cells = df.isnull().sum().sum()
        duplicate_rows = df.duplicated().sum()
        
        # Calculate quality score
        null_ratio = null_cells / total_cells if total_cells > 0 else 0
        duplicate_ratio = duplicate_rows / len(df) if len(df) > 0 else 0
        
        quality_score = max(0, 100 - (null_ratio * 50) - (duplicate_ratio * 30))
        
        issues = []
        recommendations = []
        
        # Check for issues
        if null_ratio > 0.1:
            issues.append(f"YÃ¼ksek boÅŸ veri oranÄ±: %{null_ratio*100:.1f}")
            recommendations.append("BoÅŸ hÃ¼creleri doldurun veya ilgili satÄ±rlarÄ± kaldÄ±rÄ±n")
        
        if duplicate_rows > 0:
            issues.append(f"{duplicate_rows} duplicate satÄ±r bulundu")
            recommendations.append("Duplicate satÄ±rlarÄ± kaldÄ±rÄ±n")
        
        if df.shape[1] > 20:
            recommendations.append("Ã‡ok sayÄ±da sÃ¼tun var - gereksiz olanlarÄ± gizlemeyi dÃ¼ÅŸÃ¼nÃ¼n")
        
        if df.shape[0] > 10000:
            recommendations.append("BÃ¼yÃ¼k veri seti - filtreleme ve sayfalama kullanÄ±n")
        
        return {
            'is_valid': quality_score > 60,
            'quality_score': quality_score,
            'issues': issues,
            'recommendations': recommendations,
            'stats': {
                'total_rows': df.shape[0],
                'total_columns': df.shape[1],
                'null_cells': null_cells,
                'duplicate_rows': duplicate_rows,
                'null_ratio': null_ratio,
                'duplicate_ratio': duplicate_ratio
            }
        }

# 5. SMART VISUALIZER
class SmartVisualizer:
    @staticmethod
    def create_data_overview_chart(df: pd.DataFrame):
        """Create data type distribution chart"""
        dtype_counts = df.dtypes.value_counts()
        
        fig = px.pie(
            values=dtype_counts.values,
            names=[str(dtype) for dtype in dtype_counts.index],
            title="ğŸ“Š Veri TÃ¼rÃ¼ DaÄŸÄ±lÄ±mÄ±"
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig
    
    @staticmethod
    def create_quality_dashboard(df: pd.DataFrame):
        """Create data quality dashboard"""
        null_counts = df.isnull().sum()
        
        fig = px.bar(
            x=null_counts.index,
            y=null_counts.values,
            title="ğŸ” SÃ¼tun BazlÄ± BoÅŸ Veri Analizi",
            labels={'x': 'SÃ¼tunlar', 'y': 'BoÅŸ HÃ¼cre SayÄ±sÄ±'}
        )
        
        fig.update_layout(xaxis_tickangle=-45)
        return fig
    
    @staticmethod
    def create_smart_chart(df: pd.DataFrame, column: str):
        """Create smart chart based on data type and distribution"""
        try:
            if column not in df.columns:
                return None
            
            data = df[column].dropna()
            if len(data) == 0:
                return None
            
            # Determine chart type based on data
            if pd.api.types.is_numeric_dtype(data):
                # For numeric data, create histogram with distribution info
                fig = px.histogram(
                    data, 
                    x=data,
                    title=f"ğŸ“Š {column} - DaÄŸÄ±lÄ±m Analizi",
                    nbins=min(30, len(data.unique())),
                    marginal="box"  # Add box plot on top
                )
                
                # Add statistical annotations
                mean_val = data.mean()
                median_val = data.median()
                
                fig.add_vline(x=mean_val, line_dash="dash", line_color="red", 
                             annotation_text=f"Ortalama: {mean_val:.2f}")
                fig.add_vline(x=median_val, line_dash="dot", line_color="blue", 
                             annotation_text=f"Medyan: {median_val:.2f}")
                
                fig.update_layout(
                    showlegend=True,
                    xaxis_title=column,
                    yaxis_title="Frekans"
                )
                
            elif pd.api.types.is_categorical_dtype(data) or data.dtype == 'object':
                # For categorical data, create bar chart
                value_counts = data.value_counts().head(20)  # Top 20 values
                
                fig = px.bar(
                    x=value_counts.index,
                    y=value_counts.values,
                    title=f"ğŸ“Š {column} - En SÄ±k DeÄŸerler (Top 20)",
                    labels={'x': column, 'y': 'Frekans'}
                )
                
                fig.update_layout(xaxis_tickangle=-45)
                
            else:
                # For other data types, create simple value counts
                value_counts = data.value_counts().head(10)
                
                fig = px.pie(
                    values=value_counts.values,
                    names=value_counts.index,
                    title=f"ğŸ“Š {column} - DeÄŸer DaÄŸÄ±lÄ±mÄ±"
                )
            
            # Update layout for better appearance
            fig.update_layout(
                height=400,
                showlegend=True,
                font=dict(size=12)
            )
            
            return fig
            
        except Exception as e:
            # Return None if chart creation fails
            return None

# Initialize systems
if 'perf_monitor' not in st.session_state:
    st.session_state.perf_monitor = PerformanceMonitor()

if 'smart_cache' not in st.session_state:
    st.session_state.smart_cache = SmartCache()

# Favori sistemi iÃ§in session state
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

error_handler = SmartErrorHandler()
data_validator = DataValidator()
smart_visualizer = SmartVisualizer()

# uploads klasÃ¶rÃ¼ndeki dosyalarÄ± listele
import os
uploads_dir = "uploads"
uploads_path = os.path.join(os.getcwd(), uploads_dir)
if not os.path.exists(uploads_path):
    os.makedirs(uploads_path)

st.sidebar.header("YÃ¼klenen Excel DosyalarÄ±")
excel_files = [f for f in os.listdir(uploads_path) if f.endswith(".xlsx")]

# Dosya seÃ§imi iÃ§in session state
if "selected_file_key" not in st.session_state:
    st.session_state["selected_file_key"] = None

selected_file = st.sidebar.selectbox(
    "Daha Ã¶nce yÃ¼klenen dosyalar",
    options=["Dosya seÃ§in..."] + excel_files,
    key="file_selector"
) if excel_files else None

# SeÃ§ilen dosyayÄ± kontrol et
if selected_file and selected_file != "Dosya seÃ§in...":
    st.session_state["selected_file_key"] = selected_file
else:
    selected_file = None

# Dosya silme Ã¶zelliÄŸi
if excel_files:
    st.sidebar.markdown("---")
    st.sidebar.subheader("ğŸ—‘ï¸ Dosya YÃ¶netimi")
    
    # Her dosya iÃ§in silme butonu
    files_to_delete = []
    for file in excel_files:
        col1, col2 = st.sidebar.columns([3, 1])
        col1.text(file[:20] + "..." if len(file) > 20 else file)
        if col2.button("ğŸ—‘ï¸", key=f"delete_{file}", help=f"{file} dosyasÄ±nÄ± sil"):
            files_to_delete.append(file)
    
    # Silme iÅŸlemini gerÃ§ekleÅŸtir
    for file_to_delete in files_to_delete:
        try:
            file_path = os.path.join(uploads_path, file_to_delete)
            os.remove(file_path)
            st.sidebar.success(f"âœ… {file_to_delete} silindi!")
            
            # EÄŸer silinen dosya seÃ§ili dosyaysa, session'Ä± temizle
            if st.session_state.get("selected_file_key") == file_to_delete:
                st.session_state["selected_file_key"] = None
            
            # SayfayÄ± yenile
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"âŒ Dosya silinemedi: {e}")
    
    # TÃ¼m dosyalarÄ± silme butonu
    if len(excel_files) > 1:
        st.sidebar.markdown("---")
        if st.sidebar.button("ğŸ—‘ï¸ TÃ¼m DosyalarÄ± Sil", help="TÃ¼m Excel dosyalarÄ±nÄ± sil"):
            try:
                for file in excel_files:
                    file_path = os.path.join(uploads_path, file)
                    os.remove(file_path)
                
                # Session'Ä± temizle
                st.session_state["selected_file_key"] = None
                st.sidebar.success(f"âœ… {len(excel_files)} dosya silindi!")
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"âŒ Dosyalar silinemedi: {e}")

# -------------------------
# Sayfa ayarlarÄ±
# -------------------------
st.set_page_config(
    page_title="Perfo Destek Ã‡Ã¶zÃ¼mleri - Talepler ArayÃ¼zÃ¼",
    page_icon="ğŸ—‚ï¸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------
# YardÄ±mcÄ± fonksiyonlar
# -------------------------

def get_voice_input():
    """Sesli arama iÃ§in mikrofon giriÅŸi alÄ±r"""
    if not SPEECH_AVAILABLE:
        return "Sesli arama kÃ¼tÃ¼phanesi yÃ¼klÃ¼ deÄŸil. 'pip install SpeechRecognition pyaudio' komutunu Ã§alÄ±ÅŸtÄ±rÄ±n."
    
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("ğŸ¤ KonuÅŸun... (3 saniye bekleniyor)")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=3)
        
        text = r.recognize_google(audio, language='tr-TR')
        return text
    except sr.WaitTimeoutError:
        return "Zaman aÅŸÄ±mÄ± - tekrar deneyin"
    except sr.UnknownValueError:
        return "Ses anlaÅŸÄ±lamadÄ±"
    except sr.RequestError:
        return "Ses tanÄ±ma servisi hatasÄ±"
    except Exception as e:
        return f"Hata: {str(e)}"

def generate_smart_summary(df):
    """Excel dosyasÄ± iÃ§in basit ve kullanÄ±ÅŸlÄ± Ã¶zet oluÅŸturur"""
    
    # En sÄ±k tekrar eden kelimeleri bul
    all_text = ""
    text_cols = df.select_dtypes(include=['object']).columns
    for col in text_cols:
        all_text += " " + df[col].astype(str).str.cat(sep=" ")
    
    # Kelimeleri ayÄ±kla ve say
    words = re.findall(r'\b\w{3,}\b', all_text.lower())
    stop_words = {'iÃ§in', 'olan', 'olan', 'ile', 'bir', 'bu', 've', 'ama', 'fakat', 'nan', 'none'}
    words = [w for w in words if w not in stop_words and not w.isdigit()]
    
    from collections import Counter
    word_counts = Counter(words).most_common(5)
    
    # Basit analiz
    total_rows = len(df)
    total_cols = len(df.columns)
    empty_cells = df.isnull().sum().sum()
    
    # Excel dosyasÄ±nÄ± akÄ±llÄ± analiz et ve Ã¶zetle
    excel_analysis = analyze_excel_content(df, word_counts, total_rows, total_cols)
    
    # AkÄ±llÄ± Ã¶neriler
    suggestions = []
    if empty_cells > total_rows * 0.1:
        suggestions.append("ğŸ“ Ã‡ok sayÄ±da boÅŸ hÃ¼cre var - veri temizliÄŸi yapÄ±labilir")
    
    if total_rows > 1000:
        suggestions.append("ğŸ“Š BÃ¼yÃ¼k veri seti - filtreleme kullanmanÄ±z Ã¶nerilir")
    
    if len(text_cols) > 5:
        suggestions.append("ğŸ” Ã‡ok sayÄ±da metin sÃ¼tunu - arama Ã¶zelliÄŸini kullanÄ±n")
    
    return {
        "toplam_satir": total_rows,
        "toplam_sutun": total_cols,
        "bos_hucre": int(empty_cells),
        "en_sik_kelimeler": word_counts,
        "oneriler": suggestions,
        "akilli_analiz": excel_analysis
    }

def analyze_excel_content(df, top_words, rows, cols):
    """Excel iÃ§eriÄŸini analiz edip kÄ±sa Ã¶zet cÃ¼mleler oluÅŸturur"""
    analysis = []
    
    # Dosya tÃ¼rÃ¼ analizi
    if any(keyword in ' '.join([word[0] for word in top_words]) for keyword in ['talep', 'ticket', 'request']):
        analysis.append("ğŸ« Bu bir talep/destek dosyasÄ± gibi gÃ¶rÃ¼nÃ¼yor.")
    elif any(keyword in ' '.join([word[0] for word in top_words]) for keyword in ['mÃ¼ÅŸteri', 'customer', 'client']):
        analysis.append("ğŸ‘¤ MÃ¼ÅŸteri bilgileri iÃ§eren bir dosya.")
    elif any(keyword in ' '.join([word[0] for word in top_words]) for keyword in ['satÄ±ÅŸ', 'sales', 'revenue', 'gelir']):
        analysis.append("ğŸ’° SatÄ±ÅŸ/gelir verileri iÃ§eriyor.")
    elif any(keyword in ' '.join([word[0] for word in top_words]) for keyword in ['Ã§alÄ±ÅŸan', 'employee', 'personel']):
        analysis.append("ğŸ‘¥ Ä°nsan kaynaklarÄ±/personel verisi.")
    else:
        analysis.append("ğŸ“Š Genel veri tablosu ÅŸeklinde dÃ¼zenlenmiÅŸ.")
    
    # Veri yoÄŸunluÄŸu analizi
    if rows < 50:
        analysis.append("ğŸ“ KÃ¼Ã§Ã¼k boyutlu, detaylÄ± inceleme iÃ§in uygun.")
    elif rows < 500:
        analysis.append("ğŸ“ˆ Orta boyutlu, analiz iÃ§in ideal.")
    else:
        analysis.append("ğŸ¯ BÃ¼yÃ¼k veri seti, filtreleme Ã¶nerilir.")
    
    # SÃ¼tun Ã§eÅŸitliliÄŸi
    numeric_cols = df.select_dtypes(include=['number']).columns
    text_cols = df.select_dtypes(include=['object']).columns
    
    if len(numeric_cols) > len(text_cols):
        analysis.append("ğŸ”¢ Ã‡oÄŸunlukla sayÄ±sal veriler iÃ§eriyor.")
    elif len(text_cols) > len(numeric_cols):
        analysis.append("ğŸ“ AÄŸÄ±rlÄ±klÄ± olarak metin verileri var.")
    else:
        analysis.append("âš–ï¸ SayÄ±sal ve metin verileri dengeli daÄŸÄ±lÄ±m.")
    
    # Veri kalitesi
    empty_ratio = df.isnull().sum().sum() / (rows * cols)
    if empty_ratio < 0.05:
        analysis.append("âœ… Veri kalitesi yÃ¼ksek, az boÅŸ hÃ¼cre.")
    elif empty_ratio < 0.20:
        analysis.append("âš ï¸ Orta dÃ¼zeyde veri eksikliÄŸi var.")
    else:
        analysis.append("ğŸ”´ Veri kalitesi dÃ¼ÅŸÃ¼k, temizlik gerekli.")
    
    return analysis

def smart_voice_assistant(voice_text, df):
    """AkÄ±llÄ± sesli asistan - Excel verilerini analiz ederek doÄŸal dil komutlarÄ±nÄ± iÅŸler"""
    voice_text = voice_text.lower()
    original_df = df.copy()
    
    # Excel sÃ¼tun isimlerini ve iÃ§eriklerini Ã¶ÄŸren
    column_info = {}
    for col in df.columns:
        col_lower = str(col).lower()
        # Her sÃ¼tundaki benzersiz deÄŸerleri al (ilk 100 satÄ±r iÃ§in performans)
        sample_values = df[col].dropna().astype(str).str.lower().head(100).unique()
        column_info[col_lower] = {
            'original_name': col,
            'sample_values': sample_values
        }
    
    # Sayma komutlarÄ±
    count_patterns = ['kaÃ§', 'sayÄ±', 'adet', 'tane', 'count']
    is_count_query = any(pattern in voice_text for pattern in count_patterns)
    
    # Ä°Ã§erik arama komutlarÄ±
    content_patterns = ['iÃ§er', 'geÃ§', 'bulunan', 'olan', 'yazan', 'contain']
    is_content_search = any(pattern in voice_text for pattern in content_patterns)
    
    # SÃ¼tun seÃ§me komutlarÄ±
    column_patterns = ['sÃ¼tun', 'sutun', 'kolon', 'alan', 'field']
    is_column_select = any(pattern in voice_text for pattern in column_patterns)
    
    # Anahtar kelimeleri Ã§Ä±kar
    words = voice_text.split()
    search_terms = [w for w in words if len(w) > 2 and w not in [
        'iÃ§er', 'geÃ§', 'bulunan', 'olan', 'yazan', 'sÃ¼tun', 'sutun', 'kolon',
        'getir', 'gÃ¶ster', 'bul', 'ara', 'kayÄ±t', 'veri', 'sadece', 'olan',
        'kaÃ§', 'tane', 'adet', 'sayÄ±', 'iÃ§in', 'ile', 'den', 'dan', 'nda', 'nde'
    ]]
    
    # Hangi sÃ¼tun hedeflendiÄŸini bul
    target_column = None
    target_content = None
    
    for term in search_terms:
        # SÃ¼tun ismi eÅŸleÅŸmesi ara
        for col_key, col_data in column_info.items():
            # SÃ¼tun isminde geÃ§iyor mu?
            if term in col_key or any(part in term for part in col_key.split()):
                target_column = col_data['original_name']
                break
            
            # SÃ¼tun iÃ§eriÄŸinde geÃ§iyor mu?
            if any(term in str(val) for val in col_data['sample_values']):
                if not target_column:  # Ä°lk bulunan sÃ¼tunu al
                    target_column = col_data['original_name']
                target_content = term
                break
    
    # Ã–zel komut analizleri
    result_message = ""
    
    try:
        if is_count_query and target_content:
            # "KaÃ§ tane merhaba yazan veri var" gibi sorular
            if target_column:
                filtered_df = df[df[target_column].astype(str).str.lower().str.contains(target_content, na=False)]
                count = len(filtered_df)
                result_message = f"'{target_content}' kelimesi '{target_column}' sÃ¼tununda {count} kayÄ±tta bulundu."
                return filtered_df, result_message
            else:
                # TÃ¼m sÃ¼tunlarda ara
                mask = df.astype(str).apply(lambda x: x.str.lower().str.contains(target_content, na=False)).any(axis=1)
                filtered_df = df[mask]
                count = len(filtered_df)
                result_message = f"'{target_content}' kelimesi toplam {count} kayÄ±tta bulundu."
                return filtered_df, result_message
        
        elif is_content_search and target_content:
            # "Talep aÃ§Ä±klamasÄ± iÃ§erisinde merhaba yazan verileri getir"
            if target_column:
                filtered_df = df[df[target_column].astype(str).str.lower().str.contains(target_content, na=False)]
                result_message = f"'{target_column}' sÃ¼tununda '{target_content}' iÃ§eren {len(filtered_df)} kayÄ±t bulundu."
                return filtered_df, result_message
            else:
                # Genel arama
                mask = df.astype(str).apply(lambda x: x.str.lower().str.contains(target_content, na=False)).any(axis=1)
                filtered_df = df[mask]
                result_message = f"'{target_content}' iÃ§eren {len(filtered_df)} kayÄ±t bulundu."
                return filtered_df, result_message
        
        elif is_column_select and target_column:
            # "Sadece talep aÃ§Ä±klamasÄ± sÃ¼tununu gÃ¶ster"
            filtered_df = df[[target_column]]
            result_message = f"'{target_column}' sÃ¼tunu gÃ¶steriliyor."
            return filtered_df, result_message
        
        elif target_column and not is_count_query and not is_content_search:
            # Genel sÃ¼tun bazlÄ± arama
            if target_content:
                filtered_df = df[df[target_column].astype(str).str.lower().str.contains(target_content, na=False)]
                result_message = f"'{target_column}' sÃ¼tununda '{target_content}' aramasÄ±: {len(filtered_df)} sonuÃ§."
                return filtered_df, result_message
            else:
                # Sadece sÃ¼tunu gÃ¶ster
                filtered_df = df[[target_column]]
                result_message = f"'{target_column}' sÃ¼tunu gÃ¶steriliyor."
                return filtered_df, result_message
        
        # Genel arama (hiÃ§bir Ã¶zel komut yoksa)
        elif search_terms:
            search_term = search_terms[0]
            mask = df.astype(str).apply(lambda x: x.str.lower().str.contains(search_term, na=False)).any(axis=1)
            filtered_df = df[mask]
            result_message = f"'{search_term}' aramasÄ±: {len(filtered_df)} sonuÃ§ bulundu."
            return filtered_df, result_message
    
    except Exception as e:
        result_message = f"Arama hatasÄ±: {str(e)}"
        return df, result_message
    
    # HiÃ§bir ÅŸey bulunamazsa
    result_message = "Komut anlaÅŸÄ±lamadÄ±. LÃ¼tfen daha aÃ§Ä±k ifade edin."
    return df, result_message

def smart_voice_assistant(voice_text, df):
    """GeliÅŸmiÅŸ AI sesli asistan - Excel sÃ¼tunlarÄ±nÄ± ve iÃ§eriklerini analiz ederek akÄ±llÄ± filtreleme yapar"""
    voice_text = voice_text.lower().strip()
    
    # Debug iÃ§in orijinal metni logla
    print(f"ğŸ¤ AlgÄ±lanan ses: '{voice_text}'")
    
    # Mevcut sÃ¼tun isimlerini analiz et
    column_analysis = {}
    for col in df.columns:
        col_clean = str(col).lower()
        # Her sÃ¼tundaki eÅŸsiz deÄŸerleri al (ilk 200 tane - daha fazla veri)
        unique_values = df[col].dropna().astype(str).str.lower().unique()[:200]
        column_analysis[col] = {
            'name_lower': col_clean,
            'original_name': col,
            'sample_values': list(unique_values),
            'value_count': len(df[col].dropna()),
            'dtype': str(df[col].dtype)
        }
    
    # Arama teriminin hangi sÃ¼tunda bulunduÄŸunu akÄ±llÄ±ca tespit et
    def find_best_column_for_content(search_terms, df):
        """Arama terimlerinin hangi sÃ¼tunlarda bulunduÄŸunu analiz eder"""
        column_scores = {}
        
        for col in df.columns:
            score = 0
            matches = 0
            
            # Her arama terimi iÃ§in bu sÃ¼tunda kaÃ§ eÅŸleÅŸme var
            for term in search_terms:
                try:
                    col_matches = df[col].astype(str).str.lower().str.contains(term, na=False, case=False, regex=False).sum()
                    if col_matches > 0:
                        score += col_matches
                        matches += 1
                        print(f"   ğŸ” '{term}' -> '{col}' sÃ¼tununda {col_matches} eÅŸleÅŸme")
                except:
                    continue
            
            if score > 0:
                column_scores[col] = {
                    'score': score,
                    'term_matches': matches,
                    'avg_score': score / len(search_terms) if len(search_terms) > 0 else 0
                }
        
        # En iyi sÃ¼tunu seÃ§
        if column_scores:
            # Ã–ncelik: En Ã§ok terimi olan, sonra en yÃ¼ksek skor
            best_col = max(column_scores.items(), 
                          key=lambda x: (x[1]['term_matches'], x[1]['score']))
            
            print(f"ğŸ¯ En iyi sÃ¼tun: '{best_col[0]}' (Skor: {best_col[1]['score']}, Terim: {best_col[1]['term_matches']})")
            return best_col[0], column_scores
        
        return None, {}
    def find_column_by_name(voice_text):
        # Sadece aÃ§Ä±k sÃ¼tun belirteÃ§leri varsa sÃ¼tun ara
        explicit_column_indicators = ['sÃ¼tun', 'sutun', 'sÃ¼tunu', 'sutunu', 'alanÄ±', 'alanda']
        
        # AÃ§Ä±k sÃ¼tun belirteci yoksa tÃ¼m sÃ¼tunlarda ara
        if not any(indicator in voice_text for indicator in explicit_column_indicators):
            print(f"ğŸ” AÃ§Ä±k sÃ¼tun belirteci yok, tÃ¼m sÃ¼tunlarda arama yapÄ±lacak")
            return None
        
        # AÃ§Ä±k sÃ¼tun belirteci varsa en uygun sÃ¼tunu bul
        best_match = None
        best_score = 0
        
        for col_info in column_analysis.values():
            col_original = col_info['original_name'].lower()
            col_words = col_original.split()
            
            # Sesli metindeki kelimeleri temizle
            voice_words = voice_text.replace(':', '').replace(',', '').split()
            voice_words = [w for w in voice_words if len(w) > 2]
            
            # SÃ¼tun ismindeki tÃ¼m kelimelerin sesli metinde olup olmadÄ±ÄŸÄ±nÄ± kontrol et
            matching_words = 0
            total_char_match = 0
            
            for col_word in col_words:
                # TÃ¼rkÃ§e karakter temizliÄŸi
                col_word_clean = col_word.replace('Ä±', 'i').replace('ÄŸ', 'g').replace('Ã¼', 'u').replace('ÅŸ', 's').replace('Ã¶', 'o').replace('Ã§', 'c')
                
                for voice_word in voice_words:
                    voice_word_clean = voice_word.replace('Ä±', 'i').replace('ÄŸ', 'g').replace('Ã¼', 'u').replace('ÅŸ', 's').replace('Ã¶', 'o').replace('Ã§', 'c')
                    
                    # KÄ±smi eÅŸleÅŸme de kabul et
                    if col_word_clean in voice_word_clean or voice_word_clean in col_word_clean:
                        matching_words += 1
                        total_char_match += len(col_word)
                        break
            
            # EÅŸleÅŸme skorunu hesapla
            if len(col_words) > 0:
                score = (matching_words / len(col_words)) * total_char_match
                
                # Ã–zel kelimeler iÃ§in bonus puan
                if any(keyword in voice_text for keyword in ['unvan', 'fiili', 'adÄ±', 'adi']):
                    if any(keyword in col_original for keyword in ['unvan', 'fiili', 'ad']):
                        score += 100  # YÃ¼ksek bonus
                
                if score > best_score:
                    best_score = score
                    best_match = col_info['original_name']
        
        print(f"ğŸ¯ En iyi sÃ¼tun eÅŸleÅŸmesi: {best_match} (Skor: {best_score})")
        
        # Yeterli skor yoksa tÃ¼m sÃ¼tunlarda ara
        if best_score < 50:
            print(f"ğŸ” Skor yetersiz ({best_score}), tÃ¼m sÃ¼tunlarda arama yapÄ±lacak")
            return None
        
        return best_match
    
    # Ä°Ã§erik kelimelerini ayÄ±kla
    def extract_search_content(voice_text, detected_column=None):
        # Bu kelimeleri atla
        skip_words = {
            'tabloda', 'tablodan', 'kayÄ±t', 'kayÄ±tlarÄ±', 'kayÄ±tlar', 'veri', 'veriler',
            'getir', 'gÃ¶ster', 'bul', 'ara', 'filtrele', 'iÃ§eren', 'olan', 'olanlarÄ±',
            'yazan', 'yazanlarÄ±', 'bulunan', 'bulunanlarÄ±', 'sÃ¼tun', 'sutun', 'sadece', 
            'iÃ§in', 'ile', 'den', 'dan', 'nda', 'nde', 'da', 'de', 'adi:', 'adÄ±:', 'olan'
        }
        
        # EÄŸer sÃ¼tun tespit edildiyse, o sÃ¼tunun kelimelerini de atla
        if detected_column:
            column_words = detected_column.lower().split()
            skip_words.update(column_words)
            # TÃ¼rkÃ§e karakter varyasyonlarÄ±
            for word in column_words:
                skip_words.add(word.replace('Ä±', 'i').replace('ÄŸ', 'g').replace('Ã¼', 'u').replace('ÅŸ', 's').replace('Ã¶', 'o').replace('Ã§', 'c'))
        
        words = voice_text.replace(':', '').replace(',', '').split()
        content_words = []
        
        for word in words:
            word_clean = word.lower().strip()
            if len(word_clean) > 2 and word_clean not in skip_words:
                # Ã–zel isimler ve Ã¶nemli kelimeler
                if any(char.isupper() for char in word) or word_clean in ['genel', 'mÃ¼dÃ¼r', 'yardÄ±mcÄ±sÄ±', 'baÅŸkan', 'uzman']:
                    content_words.append(word_clean)
                elif not any(skip in word_clean for skip in skip_words):
                    content_words.append(word_clean)
        
        print(f"ğŸ“ Ã‡Ä±karÄ±lan arama kelimeleri: {content_words}")
        return content_words
    
    # Komut tÃ¼rÃ¼nÃ¼ belirle ve iÅŸle
    result_message = ""
    
    # 0. Ã–NCE SAYISAL KARÅILAÅTIRMA KOMUTLARÄ°NI KONTROL ET (en yÃ¼ksek Ã¶ncelik)
    comparison_patterns = {
        'kÃ¼Ã§Ã¼k': ['kÃ¼Ã§Ã¼k', 'kucuk', 'az', 'altÄ±nda', 'altÄ±ndaki', 'dan kÃ¼Ã§Ã¼k', 'den kÃ¼Ã§Ã¼k'],
        'bÃ¼yÃ¼k': ['bÃ¼yÃ¼k', 'buyuk', 'fazla', 'Ã¼stÃ¼nde', 'Ã¼stÃ¼ndeki', 'dan bÃ¼yÃ¼k', 'den bÃ¼yÃ¼k', 'dan fazla'],
        'eÅŸit': ['eÅŸit', 'esit', 'olan', 'equal']
    }
    
    # SayÄ± arama
    number_match = re.search(r'(\d+)', voice_text)
    comparison_type = None
    
    if number_match:
        target_number = int(number_match.group(1))
        
        # KarÅŸÄ±laÅŸtÄ±rma tÃ¼rÃ¼nÃ¼ bul
        for comp_type, patterns in comparison_patterns.items():
            if any(pattern in voice_text for pattern in patterns):
                comparison_type = comp_type
                break
        
        if comparison_type:
            # SÃ¼tun adÄ±nÄ± bul
            target_column = find_column_by_name(voice_text)
            
            if not target_column:
                # SayÄ±sal sÃ¼tunlarÄ± kontrol et
                numeric_cols = df.select_dtypes(include=['number']).columns
                for col in numeric_cols:
                    col_lower = col.lower()
                    if any(word in col_lower for word in voice_text.split() if len(word) > 2):
                        target_column = col
                        break
                
                # Hala bulunamadÄ±ysa ilk sayÄ±sal sÃ¼tunu al
                if not target_column and len(numeric_cols) > 0:
                    target_column = numeric_cols[0]
            
            if target_column:
                try:
                    # SayÄ±sal deÄŸerlere dÃ¶nÃ¼ÅŸtÃ¼r
                    df_numeric = pd.to_numeric(df[target_column], errors='coerce')
                    
                    if comparison_type == 'kÃ¼Ã§Ã¼k':
                        mask = df_numeric < target_number
                        result_message = f"ğŸ“Š '{target_column}' sÃ¼tununda {target_number}'dan kÃ¼Ã§Ã¼k olan {mask.sum()} kayÄ±t bulundu"
                    elif comparison_type == 'bÃ¼yÃ¼k':
                        mask = df_numeric > target_number
                        result_message = f"ğŸ“Š '{target_column}' sÃ¼tununda {target_number}'dan bÃ¼yÃ¼k olan {mask.sum()} kayÄ±t bulundu"
                    elif comparison_type == 'eÅŸit':
                        mask = df_numeric == target_number
                        result_message = f"ğŸ“Š '{target_column}' sÃ¼tununda {target_number}'a eÅŸit olan {mask.sum()} kayÄ±t bulundu"
                    
                    filtered_df = df[mask]
                    print(f"ğŸ”¢ SayÄ±sal filtreleme: '{target_column}' {comparison_type} {target_number} -> {mask.sum()} sonuÃ§")
                    return filtered_df, result_message
                    
                except Exception as e:
                    print(f"âš ï¸ SayÄ±sal karÅŸÄ±laÅŸtÄ±rma hatasÄ±: {e}")

    # 1. Ã–NCE KAYIT LÄ°MÄ°TLEME KOMUTLARÄ°NI KONTROL ET (en yÃ¼ksek Ã¶ncelik)
    if any(word in voice_text for word in ['ilk', 'son']) and any(word in voice_text for word in ['kayÄ±t', 'satÄ±r']) and 'sÃ¼tun' not in voice_text:
        number_match = re.search(r'(\d+)', voice_text)
        if number_match:
            n = int(number_match.group(1))
            
            if 'ilk' in voice_text:
                filtered_df = df.head(n)
                result_message = f"ğŸ“‹ Ä°lk {n} kayÄ±t getiriliyor"
                return filtered_df, result_message
            elif 'son' in voice_text:
                filtered_df = df.tail(n)
                result_message = f"  Son {n} kayÄ±t getiriliyor"
                return filtered_df, result_message
    
    # 1. AKILLI Ä°Ã‡ERÄ°K ARAMA ("mÃ¼fettiÅŸ olanlarÄ± getir", "sadece mÃ¼fettiÅŸ")
    if any(word in voice_text for word in ['getir', 'gÃ¶ster', 'bul', 'ara', 'filtrele', 'olanlarÄ±', 'yazanlarÄ±', 'iÃ§eren', 'sadece', 'olan']):
        # Ã–nce sÃ¼tun belirteci var mÄ± kontrol et
        target_column = find_column_by_name(voice_text)
        search_content = extract_search_content(voice_text, target_column)
        
        print(f"ğŸ” Manuel hedef sÃ¼tun: {target_column}")
        print(f"ğŸ” Arama iÃ§eriÄŸi: {search_content}")
        
        if search_content:
            # Arama terimlerini hazÄ±rla
            search_terms = search_content if isinstance(search_content, list) else [search_content]
            
            if target_column:
                # Manuel olarak belirtilmiÅŸ sÃ¼tunda ara
                print(f"ğŸ¯ Manuel belirtilen '{target_column}' sÃ¼tununda arama yapÄ±lÄ±yor...")
                search_term = ' '.join(search_terms) if len(search_terms) > 1 else search_terms[0]
                mask = df[target_column].astype(str).str.lower().str.contains(search_term, na=False, case=False, regex=False)
                filtered_df = df[mask]
                matches = mask.sum()
                print(f"   ğŸ“ '{search_term}' terimi '{target_column}' sÃ¼tununda {matches} kayÄ±t buldu")
                result_message = f"ğŸ” '{target_column}' sÃ¼tununda '{search_term}' iÃ§eren {matches} kayÄ±t bulundu"
                return filtered_df, result_message
            else:
                # AkÄ±llÄ± sÃ¼tun analizi yap - hangi sÃ¼tunda bu terimler en Ã§ok geÃ§iyor?
                print(f"ğŸ§  Arama terimleri iÃ§in en uygun sÃ¼tun analiz ediliyor...")
                best_column, column_scores = find_best_column_for_content(search_terms, df)
                
                if best_column and column_scores[best_column]['score'] >= len(search_terms):
                    # Belirli bir sÃ¼tunda yoÄŸunlaÅŸmÄ±ÅŸ - o sÃ¼tunda ara
                    search_term = ' '.join(search_terms) if len(search_terms) > 1 else search_terms[0]
                    mask = df[best_column].astype(str).str.lower().str.contains(search_term, na=False, case=False, regex=False)
                    filtered_df = df[mask]
                    matches = mask.sum()
                    result_message = f"ğŸ¯ '{search_term}' iÃ§in en uygun sÃ¼tun '{best_column}' - {matches} kayÄ±t bulundu"
                    return filtered_df, result_message
                else:
                    # HiÃ§bir sÃ¼tunda yoÄŸunlaÅŸmamÄ±ÅŸ - tÃ¼m sÃ¼tunlarda ara
                    print(f"ğŸ” TÃ¼m sÃ¼tunlarda arama yapÄ±lÄ±yor ({len(df.columns)} sÃ¼tun)...")
                    search_term = ' '.join(search_terms) if len(search_terms) > 1 else search_terms[0]
                    mask = pd.Series([False] * len(df))
                    matching_columns = []
                
                for col in df.columns:
                    try:
                        col_mask = df[col].astype(str).str.lower().str.contains(search_term, na=False, case=False, regex=False)
                        col_matches = col_mask.sum()
                        if col_matches > 0:
                            mask = mask | col_mask
                            matching_columns.append(col)
                            print(f"   ğŸ“ '{search_term}' terimi '{col}' sÃ¼tununda {col_matches} kayÄ±t buldu")
                    except Exception as e:
                        print(f"   âš ï¸ '{col}' sÃ¼tununda arama hatasÄ±: {e}")
                        continue
                
                if mask.sum() > 0:
                    filtered_df = df[mask]
                    result_message = f"  '{search_term}' iÃ§eren {len(filtered_df)} kayÄ±t bulundu"
                    if matching_columns:
                        result_message += f" (Bulunan sÃ¼tunlar: {', '.join(matching_columns[:3])})"
                    return filtered_df, result_message
                else:
                    result_message = f"âŒ '{search_term}' iÃ§in hiÃ§bir eÅŸleÅŸme bulunamadÄ±"
                    return df, result_message
    
    # 2. Ä°STATÄ°STÄ°K KOMUTLARÄ°
    elif any(word in voice_text for word in ['ortalama', 'average', 'mean']):
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            col = numeric_cols[0]
            avg_val = df[col].mean()
            result_message = f"ğŸ“Š '{col}' sÃ¼tununun ortalamasÄ±: {avg_val:.2f}"
            return df, result_message
    
    elif any(word in voice_text for word in ['en yÃ¼ksek', 'maksimum', 'max', 'bÃ¼yÃ¼k']):
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            col = numeric_cols[0]
            max_val = df[col].max()
            result_message = f"  '{col}' sÃ¼tununun en yÃ¼ksek deÄŸeri: {max_val}"
            return df, result_message
    
    elif any(word in voice_text for word in ['toplam kayÄ±t', 'kaÃ§ kayÄ±t', 'satÄ±r sayÄ±sÄ±']):
        result_message = f"ğŸ“‹ Toplam kayÄ±t sayÄ±sÄ±: {len(df)}"
        return df, result_message
    
    elif any(word in voice_text for word in ['benzersiz', 'unique', 'farklÄ±']):
        # Ä°lgili sÃ¼tunu bul
        target_col = find_column_by_name(voice_text)
        
        if target_col:
            unique_count = df[target_col].nunique()
            result_message = f"ğŸ”¢ '{target_col}' sÃ¼tununda {unique_count} benzersiz deÄŸer var"
            return df, result_message
    
    # 3. SAYMA KOMUTLARÄ° ("kaÃ§ tane", "sayÄ±sÄ±", "adet")
    elif any(word in voice_text for word in ['kaÃ§', 'sayÄ±', 'adet', 'toplam']):
        search_content = extract_search_content(voice_text)
        
        if search_content:
            search_term = search_content[0]
            target_column = find_column_by_name(voice_text)
            
            if target_column:
                # Belirli sÃ¼tunda say
                matching_rows = df[target_column].astype(str).str.lower().str.contains(search_term, na=False, case=False, regex=False)
                count = matching_rows.sum()
                result_message = f"ğŸ”¢ '{search_term}' kelimesi '{target_column}' sÃ¼tununda {count} kayÄ±tta bulundu"
            else:
                # TÃ¼m sÃ¼tunlarda say
                mask = df.astype(str).apply(lambda x: x.str.lower().str.contains(search_term, na=False, case=False)).any(axis=1)
                count = mask.sum()
                result_message = f"  '{search_term}' kelimesi toplam {count} kayÄ±tta bulundu"
            
            return df, result_message
    
    # 4. SÃœTUN SEÃ‡Ä°MÄ° ("sÃ¼tunu gÃ¶ster", "sadece ... sÃ¼tun")
    elif any(word in voice_text for word in ['sÃ¼tun', 'sutun', 'sadece']):
        best_match = None
        best_score = 0
        
        # Ã–zel sÃ¼tun seÃ§imleri - Ä°lk N sÃ¼tun
        if 'ilk' in voice_text and 'sÃ¼tun' in voice_text:
            number_match = re.search(r'(\d+)', voice_text)
            if number_match:
                n = int(number_match.group(1))
                selected_cols = df.columns[:n]
                result_message = f"ğŸ“‹ Ä°lk {n} sÃ¼tun seÃ§ildi"
                return df[selected_cols], result_message
        
        # AkÄ±llÄ± sÃ¼tun eÅŸleÅŸtirme
        target_column = find_column_by_name(voice_text)
        if target_column:
            result_message = f"  '{target_column}' sÃ¼tunu seÃ§ildi"
            return df[[target_column]], result_message
    
    # 5. GENEL ARAMA - basitleÅŸtirilmiÅŸ
    else:
        search_content = extract_search_content(voice_text)
        if search_content:
            search_term = search_content[0]
            
            # TÃ¼m sÃ¼tunlarda ara
            mask = pd.Series([False] * len(df))
            matching_columns = []
            
            for col in df.columns:
                col_mask = df[col].astype(str).str.lower().str.contains(search_term, na=False, case=False, regex=False)
                if col_mask.sum() > 0:
                    mask = mask | col_mask
                    matching_columns.append(col)
            
            if mask.sum() > 0:
                filtered_df = df[mask]
                result_message = f"ğŸ” '{search_term}' iÃ§in {len(filtered_df)} kayÄ±t bulundu"
                if matching_columns:
                    result_message += f" (SÃ¼tunlar: {', '.join(matching_columns[:3])})"
                return filtered_df, result_message
    
    result_message = f"â“ Komut anlaÅŸÄ±lamadÄ±: '{voice_text}'. LÃ¼tfen daha net konuÅŸun."
    return df, result_message

def process_voice_search(voice_text, df):
    """Sesli arama metnini akÄ±llÄ± asistana yÃ¶nlendirir"""
    filtered_df, message = smart_voice_assistant(voice_text, df)
    
    # Session state'e mesajÄ± kaydet
    if 'voice_result_message' not in st.session_state:
        st.session_state['voice_result_message'] = ""
    
    st.session_state['voice_result_message'] = message
    return filtered_df

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # BaÅŸlÄ±klarÄ± temizle
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]

    # OlasÄ± varyasyonlarÄ± eÅŸleÅŸtir
    aliases = {
        "Talep No": {"Talep No", "Talep_No", "TalepNo", "ID", "No"},
        "Talep AÃ§Ä±klamasÄ±": {"Talep AÃ§Ä±klamasÄ±", "Talep Aciklamasi", "Aciklama", "AÃ§Ä±klama", "Talep AÃ§Ä±klama"},
        "YanÄ±t": {"YanÄ±t", "Yanit", "Cevap", "SonuÃ§"},
        "YanÄ±t AÃ§Ä±klamasÄ±": {"YanÄ±t AÃ§Ä±klamasÄ±", "Yanit Aciklamasi", "Cevap AÃ§Ä±klamasÄ±", "Detay", "AÃ§Ä±klama (YanÄ±t)"},
    }

    colmap = {}
    for target, names in aliases.items():
        for c in df.columns:
            if c in names or c.lower() in {n.lower() for n in names}:
                colmap[c] = target
                break

    df = df.rename(columns=colmap)
    return df

def text_search_mask(df: pd.DataFrame, cols, query: str, whole_word: bool, case_sensitive: bool):
    if not query:
        return pd.Series([True] * len(df), index=df.index)

    # Basit string arama - yazdÄ±ÄŸÄ±nÄ±z metni olduÄŸu gibi arar
    mask = pd.Series([False] * len(df), index=df.index)
    
    for c in cols:
        if c in df.columns:
            colvals = df[c].astype(str).fillna("")
            
            if case_sensitive:
                # BÃ¼yÃ¼k/kÃ¼Ã§Ã¼k harf duyarlÄ± arama
                if whole_word:
                    # Tam kelime eÅŸleÅŸmesi (regex ile)
                    pattern = r"\b" + re.escape(query) + r"\b"
                    mask = mask | colvals.str.contains(pattern, regex=True, case=True)
                else:
                    # Basit string iÃ§erme kontrolÃ¼
                    mask = mask | colvals.str.contains(query, case=True, regex=False)
            else:
                # BÃ¼yÃ¼k/kÃ¼Ã§Ã¼k harf duyarsÄ±z arama
                if whole_word:
                    # Tam kelime eÅŸleÅŸmesi (regex ile)
                    pattern = r"\b" + re.escape(query) + r"\b"
                    mask = mask | colvals.str.contains(pattern, regex=True, case=False)
                else:
                    # Basit string iÃ§erme kontrolÃ¼ (varsayÄ±lan)
                    mask = mask | colvals.str.contains(query, case=False, regex=False)
    
    return mask

def highlight_terms(val, terms):
    # Vurgulama devre dÄ±ÅŸÄ± - sadece orijinal deÄŸeri dÃ¶ndÃ¼r
    return val

def to_excel_bytes(df: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="SonuÃ§lar")
    return output.getvalue()

# -------------------------
# ğŸš€ MODERN ENTERPRISE HEADER
# -------------------------
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    color: white;
    text-align: center;
}
.feature-badge {
    display: inline-block;
    background: rgba(255, 255, 255, 0.2);
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    margin: 0.2rem;
    font-size: 0.8rem;
}
.quality-score {
    font-size: 2rem;
    font-weight: bold;
    margin: 1rem 0;
}
.performance-indicator {
    background: rgba(255, 255, 255, 0.1);
    padding: 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🚀 Enterprise Excel Görüntüleyici</h1>
    <p>AI Destekli • Performance Monitoring • Smart Analytics</p>
    <div>
        <span class="feature-badge">ğŸ§  AI Powered</span>
        <span class="feature-badge">âš¡ High Performance</span>
        <span class="feature-badge">ğŸ” Smart Search</span>
        <span class="feature-badge">ğŸ“Š Advanced Analytics</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------
# Dosya YÃ¼kleme ve Validation
# -------------------------

# EÄŸer streamlit run ile Ã§alÄ±ÅŸtÄ±rÄ±lÄ±yorsa dosya yÃ¼kleme, yoksa doÄŸrudan dosyadan oku

uploaded = st.file_uploader("ğŸ“ Excel dosyanÄ±zÄ± yÃ¼kleyin (.xlsx)", type=["xlsx"], key="excel_uploader")
if uploaded is not None:
    # Performance tracking iÃ§in
    with st.session_state.perf_monitor.track_operation("file_upload"):
        try:
            # DosyayÄ± uploads klasÃ¶rÃ¼ne kaydet
            file_path = os.path.join(uploads_path, uploaded.name)
            with open(file_path, "wb") as f:
                f.write(uploaded.getbuffer())
            st.success(f"âœ… Dosya baÅŸarÄ±yla yÃ¼klendi: {uploaded.name}")
            st.session_state["selected_file_key"] = uploaded.name
        except Exception as e:
            error_handler.display_error(e, "Dosya yÃ¼kleme sÄ±rasÄ±nda")

# Dosya yÃ¼kleme mantÄ±ÄŸÄ± - seÃ§ilen dosya veya yeni yÃ¼klenen dosya
selected_file_to_load = st.session_state.get("selected_file_key") or selected_file

if selected_file_to_load:
    # Start performance monitoring
    load_operation = st.session_state.perf_monitor.start_operation("file_load")
    
    with st.spinner(f"{selected_file_to_load} dosyasÄ± yÃ¼kleniyor..."):
        try:
            df_raw = pd.read_excel(os.path.join(uploads_path, selected_file_to_load))
            
            # Validate the loaded data
            validation_result = data_validator.validate_excel_file(df_raw)
            
            # Show validation results
            if not validation_result['is_valid']:
                st.warning("âš ï¸ Veri kalitesi sorunlarÄ± tespit edildi:")
                for issue in validation_result['issues']:
                    st.write(f"â€¢ {issue}")
                
                if validation_result['recommendations']:
                    with st.expander("ğŸ’¡ Ä°yileÅŸtirme Ã–nerileri"):
                        for rec in validation_result['recommendations']:
                            st.info(rec)
            
            # Show quality score
            score = validation_result['quality_score']
            score_color = "ğŸŸ¢" if score > 80 else "ğŸŸ¡" if score > 60 else "ğŸ”´"
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown(f"""
                <div class="performance-indicator">
                    <h3>{score_color} Veri Kalite Skoru</h3>
                    <div class="quality-score">{score:.1f}/100</div>
                </div>
                """, unsafe_allow_html=True)
            
            # End performance monitoring
            st.session_state.perf_monitor.end_operation(load_operation, True)
            
        except Exception as e:
            st.session_state.perf_monitor.end_operation(load_operation, False)
            error_handler.display_error(e, "Dosya okuma sÄ±rasÄ±nda")
            st.stop()

    # -------------------------
    # MAIN APPLICATION TABS
    # -------------------------
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["ğŸ“Š Veri Analizi", "ğŸ“ˆ AkÄ±llÄ± Analitik", "ğŸ” KeÅŸif & Filtreler", "â­ Favorilerim", "âš¡ Performans"])

    with tab1:
        st.subheader("ğŸ“Š Veri GÃ¶rselleÅŸtirme ve Temel Analiz")
    
    # Show data summary first
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Toplam SatÄ±r", len(df_raw))
    with col2:
        st.metric("SÃ¼tun SayÄ±sÄ±", len(df_raw.columns))
    with col3:
        memory_usage = df_raw.memory_usage(deep=True).sum() / 1024**2
        st.metric("Bellek KullanÄ±mÄ±", f"{memory_usage:.1f} MB")
    with col4:
        null_percentage = (df_raw.isnull().sum().sum() / (len(df_raw) * len(df_raw.columns))) * 100
        st.metric("BoÅŸ Veri %", f"{null_percentage:.1f}%")

    # Normalized df for processing
    df = normalize_columns(df_raw)

    # -------------------------
    # ğŸ¤– AkÄ±llÄ± Ã–zet
    # -------------------------
    with st.expander("ğŸ¤– AkÄ±llÄ± Dosya Ã–zeti", expanded=False):
        summary = generate_smart_summary(df)
        
        # ğŸ¤– AI Analizi
        st.subheader("ğŸ§  AI Analizi")
        for analysis_point in summary['akilli_analiz']:
            st.write(f"â€¢ {analysis_point}")
        
        st.markdown("---")
        
        # KÄ±sa Ã¶zet
        st.write(f"ğŸ“„ **{summary['toplam_satir']} satÄ±r, {summary['toplam_sutun']} sÃ¼tunlu** bir Excel dosyasÄ± analiz edildi.")
        
        if summary['bos_hucre'] > 0:
            st.write(f"âš ï¸ {summary['bos_hucre']} boÅŸ hÃ¼cre tespit edildi.")
        
        # En sÄ±k kelimeler
        if summary['en_sik_kelimeler']:
            st.write("**ğŸ”¤ En sÄ±k kullanÄ±lan kelimeler:**")
            for word, count in summary['en_sik_kelimeler']:
                st.write(f"â€¢ {word.title()}: {count} kez")
        
        # Ã–neriler
        if summary['oneriler']:
            st.write("**ğŸ’¡ AkÄ±llÄ± Ã–neriler:**")
            for suggestion in summary['oneriler']:
                st.info(suggestion)

    required_cols = ["Talep No", "Talep AÃ§Ä±klamasÄ±", "YanÄ±t", "YanÄ±t AÃ§Ä±klamasÄ±"]
    missing = [c for c in required_cols if c not in df.columns]

    with st.expander("ğŸ“‘ SÃ¼tun EÅŸleÅŸtirme / Bilgi", expanded=False):
        st.write("AlgÄ±lanan sÃ¼tunlar:", list(df.columns))
        if missing:
            st.warning(
                f"Eksik olduÄŸu tespit edilen beklenen sÃ¼tunlar: {missing}. "
                "Yine de mevcut sÃ¼tunlarla Ã§alÄ±ÅŸmaya devam edebilirsiniz."
            )
    
    # Smart pagination for large datasets - TAB 1 DATA DISPLAY
    st.markdown("### ğŸ“Š Veri GÃ¶rÃ¼ntÃ¼leme")
    
    # Apply any sidebar filters first
    filtered_df = df.copy()
    
    if len(filtered_df) > 1000:
        st.info(f"ğŸ“Š BÃ¼yÃ¼k veri seti tespit edildi ({len(filtered_df):,} satÄ±r). Performans iÃ§in sayfalama aktif.")
        
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1:
            page_size = st.selectbox("ğŸ“„ Sayfa boyutu", [100, 500, 1000, 2000], index=1, key="tab1_pagesize")
        with col2:
            total_pages = math.ceil(len(filtered_df) / page_size)
            current_page = st.number_input("ğŸ“ Sayfa", min_value=1, max_value=total_pages, value=1, key="tab1_page")
        with col3:
            st.metric("ğŸ“Š Toplam Sayfa", total_pages)
        
        start_idx = (current_page - 1) * page_size
        end_idx = min(start_idx + page_size, len(filtered_df))
        df_display = filtered_df.iloc[start_idx:end_idx]
        
        st.info(f"ğŸ“„ GÃ¶sterilen: {start_idx + 1}-{end_idx} / {len(filtered_df):,} satÄ±r (Sayfa {current_page}/{total_pages})")
    else:
        df_display = filtered_df
        st.success(f"âœ… TÃ¼m veriler gÃ¶steriliyor ({len(df_display):,} satÄ±r)")
    
    # Display the data with smart formatting
    st.dataframe(
        df_display, 
        use_container_width=True, 
        height=400,
        column_config={
            col: st.column_config.TextColumn(
                width="medium" if len(str(df_display[col].iloc[0] if len(df_display) > 0 else "")) < 50 else "large"
            ) for col in df_display.columns
        }
    )
    
    # Export options with performance tracking
    st.markdown("### ğŸ“¥ Export SeÃ§enekleri")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("ğŸ“¥ CSV Ä°ndir"):
            with st.session_state.perf_monitor.track_operation("csv_export"):
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    "â¬‡ï¸ CSV DosyasÄ±nÄ± Ä°ndir", 
                    csv, 
                    f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", 
                    "text/csv"
                )
    
    with col2:
        if st.button("ğŸ“¥ Excel Ä°ndir"):
            with st.session_state.perf_monitor.track_operation("excel_export"):
                excel_buffer = io.BytesIO()
                filtered_df.to_excel(excel_buffer, index=False)
                st.download_button(
                    "â¬‡ï¸ Excel DosyasÄ±nÄ± Ä°ndir", 
                    excel_buffer.getvalue(), 
                    f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                )
    
    with col3:
        if st.button("ğŸ“¥ JSON Ä°ndir"):
            with st.session_state.perf_monitor.track_operation("json_export"):
                json_str = filtered_df.to_json(indent=2, orient='records')
                st.download_button(
                    "â¬‡ï¸ JSON DosyasÄ±nÄ± Ä°ndir", 
                    json_str, 
                    f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 
                    "application/json"
                )
    
    with col4:
        st.metric("ğŸ“Š Export HazÄ±r", f"{len(filtered_df):,} satÄ±r")
    
    # -------------------------
    # ğŸ“„ KART GÃ–RÃœNÃœMÃœ (Orijinal Ã–zellik)
    # -------------------------
    st.markdown("### ğŸ“„ KayÄ±t KartlarÄ± GÃ¶rÃ¼nÃ¼mÃ¼")
    
    # Toggle between table and card view
    view_col1, view_col2 = st.columns([1, 3])
    with view_col1:
        view_mode = st.selectbox("ğŸ‘ï¸ GÃ¶rÃ¼nÃ¼m Modu", ["ğŸ“Š Tablo", "ğŸ“„ Kart"], index=1)
    
    if view_mode == "ğŸ“„ Kart":
        # Pagination for cards
        cards_per_page = st.slider("ğŸ“„ Sayfa baÅŸÄ±na kart sayÄ±sÄ±", 5, 20, 10)
        total_card_pages = math.ceil(len(df_display) / cards_per_page)
        
        if total_card_pages > 1:
            card_page = st.number_input("ğŸ“„ Kart SayfasÄ±", min_value=1, max_value=total_card_pages, value=1, key="card_page")
            card_start = (card_page - 1) * cards_per_page
            card_end = min(card_start + cards_per_page, len(df_display))
            cards_to_show = df_display.iloc[card_start:card_end]
            st.info(f"ğŸ“„ GÃ¶sterilen kartlar: {card_start + 1}-{card_end} / {len(df_display)}")
        else:
            cards_to_show = df_display
        
        # Display cards - Simple and clean
        for idx, row in cards_to_show.iterrows():
            # Create ONE simple card per record
            with st.container():
                st.markdown(f"""
                <div style="
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    padding: 15px;
                    margin: 10px 0;
                    background-color: #ffffff;
                ">
                    <h4 style="margin: 0 0 15px 0; color: #333;">KayÄ±t #{idx + 1}</h4>
                """, unsafe_allow_html=True)
                
                # Show all fields simply
                for col_name, value in row.items():
                    if pd.isna(value):
                        display_value = "-"
                    else:
                        display_value = str(value)
                    
                    st.markdown(f"**{col_name}:** {display_value}")
                
                # Add favorite button with unique key
                col1, col2 = st.columns([1, 10])
                with col1:
                    # Use original index from dataframe for unique key
                    original_idx = df.index[idx]
                    record_id = f"record_{original_idx}"
                    is_favorite = record_id in st.session_state.favorites
                    
                    if st.button("â­" if not is_favorite else "ğŸ’›", key=f"fav_card_{original_idx}", help="Favorilere ekle/Ã§Ä±kar"):
                        if is_favorite:
                            st.session_state.favorites.remove(record_id)
                            warning_msg = st.warning("ğŸ’” Favorilerden Ã§Ä±karÄ±ldÄ±!")
                            time.sleep(1.5)
                            warning_msg.empty()
                        else:
                            st.session_state.favorites.append(record_id)
                            success_msg = st.success("â­ Favorilere eklendi!")
                            time.sleep(1.5)
                            success_msg.empty()
                        st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Add action buttons for each card
            card_action_cols = st.columns([1, 1, 1, 2])
            with card_action_cols[0]:
                if st.button(f"ğŸ“‹ Kopyala #{idx + 1}", key=f"copy_{idx}"):
                    card_text = f"KayÄ±t #{idx + 1}:\n" + "\n".join([f"{col}: {val}" for col, val in row.items()])
                    st.info(f"ğŸ“‹ KayÄ±t #{idx + 1} kopyalandÄ±!")
            
            with card_action_cols[1]:
                if st.button(f"ğŸ” Detay #{idx + 1}", key=f"detail_{idx}"):
                    st.json(row.to_dict())
            
            with card_action_cols[2]:
                original_idx = df.index[idx]
                record_id = f"record_{original_idx}"
                is_favorite = record_id in st.session_state.favorites
                
                if st.button(f"â­ Favori #{idx + 1}", key=f"fav_table_{original_idx}"):
                    if is_favorite:
                        # Favorilerden Ã§Ä±kar
                        st.session_state.favorites.remove(record_id)
                        warning_msg = st.warning(f"ğŸ’” KayÄ±t #{idx + 1} favorilerden Ã§Ä±karÄ±ldÄ±!")
                        time.sleep(1.5)
                        warning_msg.empty()
                    else:
                        # Favorilere ekle
                        st.session_state.favorites.append(record_id)
                        success_msg = st.success(f"â­ KayÄ±t #{idx + 1} favorilere eklendi!")
                        time.sleep(1.5)
                        success_msg.empty()
                    st.rerun()
            
            # Extra spacing between cards
            st.markdown("<br>", unsafe_allow_html=True)

    with tab2:
        st.subheader("ğŸ“ˆ AkÄ±llÄ± Analitik ve Ä°statistikler")
    
    # Smart statistics
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if numeric_cols:
        st.markdown("### ğŸ“Š SayÄ±sal Veriler Ä°Ã§in AkÄ±llÄ± Ä°statistikler")
        
        # Auto-detect patterns and anomalies
        for col in numeric_cols[:3]:  # Limit to first 3 for performance
            with st.expander(f"ğŸ“ˆ {col} - DetaylÄ± Analiz"):
                col1, col2 = st.columns(2)
                
                with col1:
                    # Basic stats
                    stats = df[col].describe()
                    st.write("**Temel Ä°statistikler:**")
                    for stat, value in stats.items():
                        st.write(f"â€¢ {stat.title()}: {value:.2f}")
                
                with col2:
                    # Smart insights
                    st.write("**AkÄ±llÄ± GÃ¶rÃ¼ÅŸler:**")
                    
                    # Detect outliers
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    outliers = df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)]
                    
                    if len(outliers) > 0:
                        st.warning(f"âš ï¸ {len(outliers)} aykÄ±rÄ± deÄŸer tespit edildi")
                    else:
                        st.success("âœ… AykÄ±rÄ± deÄŸer tespit edilmedi")
                    
                    # Distribution analysis
                    skewness = df[col].skew()
                    if abs(skewness) < 0.5:
                        st.info("ğŸ“Š Normal daÄŸÄ±lÄ±ma yakÄ±n")
                    elif skewness > 0.5:
                        st.warning("ğŸ“ˆ SaÄŸa Ã§arpÄ±k daÄŸÄ±lÄ±m")
                    else:
                        st.warning("ğŸ“‰ Sola Ã§arpÄ±k daÄŸÄ±lÄ±m")
                
                # Smart visualization
                fig = smart_visualizer.create_smart_chart(df, col)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
    
    # Correlation analysis for multiple numeric columns
    if len(numeric_cols) >= 2:
        st.markdown("### ğŸ”— Korelasyon Analizi")
        correlation_matrix = df[numeric_cols].corr()
        
        # Create interactive heatmap
        fig_corr = px.imshow(
            correlation_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu_r",
            title="DeÄŸiÅŸkenler ArasÄ± Korelasyon"
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Highlight strong correlations
        strong_correlations = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                corr_val = correlation_matrix.iloc[i, j]
                if abs(corr_val) > 0.7:
                    col1_name = correlation_matrix.columns[i]
                    col2_name = correlation_matrix.columns[j]
                    strong_correlations.append((col1_name, col2_name, corr_val))
        
        if strong_correlations:
            st.markdown("#### ğŸ¯ GÃ¼Ã§lÃ¼ Korelasyonlar")
            for col1, col2, corr in strong_correlations:
                correlation_type = "Pozitif" if corr > 0 else "Negatif"
                st.write(f"â€¢ **{col1}** â†” **{col2}**: {correlation_type} ({corr:.3f})")

    with tab3:
        st.subheader("ğŸ” GeliÅŸmiÅŸ KeÅŸif ve Filtreler")
        df = normalize_columns(df_raw)
    
    # Smart search with suggestions
    st.markdown("### ğŸ” AkÄ±llÄ± Arama")
    search_col1, search_col2 = st.columns([3, 1])
    
    with search_col1:
        search_term = st.text_input("ğŸ” TÃ¼m verilerde ara...", placeholder="Aranacak kelime veya deÄŸer")
    with search_col2:
        case_sensitive = st.checkbox("BÃ¼yÃ¼k/kÃ¼Ã§Ã¼k harf duyarlÄ±")
    
    if search_term:
        # Smart search across all columns
        search_results = []
        for col in df.columns:
            if df[col].dtype == 'object':
                mask = df[col].astype(str).str.contains(search_term, case=case_sensitive, na=False)
            else:
                mask = df[col].astype(str).str.contains(str(search_term), case=case_sensitive, na=False)
            
            matches = df[mask]
            if len(matches) > 0:
                search_results.append((col, len(matches)))
        
        if search_results:
            st.success(f"ğŸ¯ '{search_term}' iÃ§in {len(search_results)} sÃ¼tunda toplam {sum(count for _, count in search_results)} sonuÃ§ bulundu:")
            
            for col, count in search_results:
                st.write(f"â€¢ **{col}**: {count} eÅŸleÅŸme")
            
            # Show filtered results
            mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=case_sensitive, na=False)).any(axis=1)
            filtered_df = df[mask]
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.warning(f"âŒ '{search_term}' iÃ§in sonuÃ§ bulunamadÄ±")
    
    # Advanced filtering
    st.markdown("### âš™ï¸ GeliÅŸmiÅŸ Filtreler")
    
    filter_col1, filter_col2 = st.columns(2)
    
    with filter_col1:
        # Numeric filters
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_columns:
            st.markdown("#### ğŸ“Š SayÄ±sal Filtreler")
            selected_numeric = st.selectbox("SayÄ±sal sÃ¼tun seÃ§", ["SeÃ§iniz..."] + numeric_columns)
            
            if selected_numeric and selected_numeric != "SeÃ§iniz...":
                min_val = float(df[selected_numeric].min())
                max_val = float(df[selected_numeric].max())
                
                range_values = st.slider(
                    f"{selected_numeric} deÄŸer aralÄ±ÄŸÄ±",
                    min_val, max_val, (min_val, max_val)
                )
                
                filtered_by_range = df[
                    (df[selected_numeric] >= range_values[0]) & 
                    (df[selected_numeric] <= range_values[1])
                ]
                
                st.info(f"ğŸ“Š Filtrelenen satÄ±r sayÄ±sÄ±: {len(filtered_by_range)}")
    
    with filter_col2:
        # Text filters
        text_columns = df.select_dtypes(include=['object']).columns.tolist()
        if text_columns:
            st.markdown("#### ğŸ“ Metin Filtreleri")
            selected_text_col = st.selectbox("Metin sÃ¼tunu seÃ§", ["SeÃ§iniz..."] + text_columns)
            
            if selected_text_col and selected_text_col != "SeÃ§iniz...":
                unique_values = df[selected_text_col].dropna().unique()
                if len(unique_values) <= 50:  # Show multiselect for reasonable number of options
                    selected_values = st.multiselect(
                        f"{selected_text_col} deÄŸerleri",
                        unique_values
                    )
                    
                    if selected_values:
                        filtered_by_text = df[df[selected_text_col].isin(selected_values)]
                        st.info(f"ğŸ“ Filtrelenen satÄ±r sayÄ±sÄ±: {len(filtered_by_text)}")
                else:
                    st.info(f"âš ï¸ Ã‡ok fazla benzersiz deÄŸer ({len(unique_values)}). Arama kutusunu kullanÄ±n.")

    with tab4:
        st.subheader("â­ Favori KayÄ±tlarÄ±m")
        
        if not st.session_state.favorites:
            st.info("ğŸ’” HenÃ¼z favori kaydÄ±nÄ±z yok.")
            st.markdown("""
            **Favori nasÄ±l eklenir?**
            1. ğŸ“Š Veri Analizi sekmesine gidin
            2. Kart gÃ¶rÃ¼nÃ¼mÃ¼nÃ¼ seÃ§in
            3. BeÄŸendiÄŸiniz kayÄ±tta â­ butonuna tÄ±klayÄ±n
            """)
        else:
            # Favori istatistikleri
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Toplam Favori", len(st.session_state.favorites))
            with col2:
                if st.button("ğŸ—‘ï¸ TÃ¼mÃ¼nÃ¼ Temizle"):
                    st.session_state.favorites = []
                success_msg = st.success("ğŸ—‘ï¸ TÃ¼m favoriler temizlendi!")
                time.sleep(2)
                success_msg.empty()
                st.rerun()
        
        st.markdown("---")
        
        # Favori kayÄ±tlarÄ± gÃ¶ster
        for i, record_id in enumerate(st.session_state.favorites):
            # Record ID'den index'i Ã§Ä±kar
            index = int(record_id.split('_')[1])
            
            # Orijinal veriden kayÄ±t bul
            if index in df.index:
                row = df.loc[index]
                
                # Basit favori kartÄ±
                st.markdown(f"""
                <div style="
                    border: 2px solid #f39c12;
                    border-radius: 8px;
                    padding: 15px;
                    margin: 10px 0;
                    background-color: #fff8e1;
                ">
                    <h4 style="margin: 0 0 15px 0; color: #e67e22;">â­ Favori KayÄ±t #{i + 1}</h4>
                """, unsafe_allow_html=True)
                
                # TÃ¼m alanlarÄ± gÃ¶ster
                for col_name, value in row.items():
                    if pd.isna(value):
                        display_value = "-"
                    else:
                        display_value = str(value)
                    
                    st.markdown(f"**{col_name}:** {display_value}")
                
                # Favoriden Ã§Ä±kar butonu
                if st.button(f"ğŸ’” Favoriden Ã‡Ä±kar", key=f"remove_fav_{index}"):
                    st.session_state.favorites.remove(record_id)
                    success_msg = st.success("ğŸ’” Favorilerden Ã§Ä±karÄ±ldÄ±!")
                    time.sleep(1.5)
                    success_msg.empty()
                    st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning(f"KayÄ±t #{index} artÄ±k mevcut deÄŸil.")

    with tab5:
        st.subheader("âš¡ Performans Ä°zleme ve Optimizasyon")
        
        # Performance metrics
    perf_stats = st.session_state.perf_monitor.get_stats()
    
    if perf_stats:
        st.markdown("### ğŸ“Š Performans Metrikleri")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Toplam Ä°ÅŸlem", 
                perf_stats['total_operations'],
                delta=f"{perf_stats['successful_operations']} baÅŸarÄ±lÄ±"
            )
        
        with col2:
            avg_time = perf_stats['average_execution_time']
            st.metric("Ortalama SÃ¼re", f"{avg_time:.2f}s")
        
        with col3:
            cache_stats = st.session_state.smart_cache.get_stats()
            hit_rate = (cache_stats['hits'] / max(cache_stats['total_requests'], 1)) * 100
            st.metric("Cache Hit Rate", f"{hit_rate:.1f}%")
        
        with col4:
            current_memory = df_raw.memory_usage(deep=True).sum() / 1024**2
            st.metric("Bellek KullanÄ±mÄ±", f"{current_memory:.1f} MB")
        
        # Detailed operation history
        if st.checkbox("ğŸ” DetaylÄ± Ä°ÅŸlem GeÃ§miÅŸi"):
            history = st.session_state.perf_monitor.operation_history
            if history:
                history_df = pd.DataFrame([
                    {
                        'Ä°ÅŸlem': op['operation'],
                        'BaÅŸlangÄ±Ã§': op['start_time'].strftime('%H:%M:%S'),
                        'SÃ¼re (s)': f"{op.get('duration', 0):.3f}",
                        'Durum': 'âœ… BaÅŸarÄ±lÄ±' if op.get('success', False) else 'âŒ HatalÄ±'
                    } for op in history[-20:]  # Son 20 iÅŸlem
                ])
                st.dataframe(history_df, use_container_width=True)
        
        # Performance recommendations
        st.markdown("### ğŸ’¡ Performans Ã–nerileri")
        
        recommendations = []
        
        if len(df_raw) > 10000:
            recommendations.append("ğŸ“Š BÃ¼yÃ¼k veri seti tespit edildi. Filtreleme kullanarak performansÄ± artÄ±rabilirsiniz.")
        
        if perf_stats['average_execution_time'] > 2.0:
            recommendations.append("â±ï¸ Ortalama iÅŸlem sÃ¼resi yÃ¼ksek. Cache kullanÄ±mÄ±nÄ± artÄ±rÄ±n.")
        
        cache_stats = st.session_state.smart_cache.get_stats()
        hit_rate = (cache_stats['hits'] / max(cache_stats['total_requests'], 1)) * 100
        if hit_rate < 50:
            recommendations.append("ğŸ’¾ Cache hit rate dÃ¼ÅŸÃ¼k. Benzer sorgularÄ± tekrar kullanmaya Ã§alÄ±ÅŸÄ±n.")
        
        current_memory = df_raw.memory_usage(deep=True).sum() / 1024**2
        if current_memory > 100:
            recommendations.append("ğŸ§  YÃ¼ksek bellek kullanÄ±mÄ±. Daha kÃ¼Ã§Ã¼k veri setleri ile Ã§alÄ±ÅŸmayÄ± deneyin.")
        
        if not recommendations:
            recommendations.append("âœ… Performans optimal gÃ¶rÃ¼nÃ¼yor!")
        
        for rec in recommendations:
            st.info(rec)
    
    else:
        st.info("ğŸ“Š HenÃ¼z performans verisi yok. BirkaÃ§ iÅŸlem yapÄ±n ve geri dÃ¶nÃ¼n.")
    
    # System info
    with st.expander("ğŸ–¥ï¸ Sistem Bilgileri"):
        st.json({
            "Python Version": sys.version,
            "Pandas Version": pd.__version__,
            "Streamlit Version": st.__version__,
            "Platform": sys.platform
        })

# -------------------------
# Kenar Ã‡ubuÄŸu â€” Filtreler
# -------------------------
st.sidebar.header("ğŸ” Filtreler ve Arama")

# ğŸ¤ Voice Search
st.sidebar.subheader("ğŸ¤ Sesli Sor")

# Sesli arama yardÄ±m mesajÄ±
with st.sidebar.expander("ğŸ¤– AI Sesli Asistan NasÄ±l KullanÄ±lÄ±r?", expanded=False):
    st.write("""
    **ğŸ¤– AI Sesli Asistan KomutlarÄ±:**
    
    ğŸ“Š **Ä°Ã§erik Filtreleme:**
    â€¢ "Tabloda adÄ± Ahmet olanlarÄ± getir"
    â€¢ "Ä°smi Mehmet olan kayÄ±tlarÄ± gÃ¶ster"
    â€¢ "Talep aÃ§Ä±klamasÄ± iÃ§erisinde merhaba yazan verileri getir"
    â€¢ "YanÄ±t sÃ¼tununda teÅŸekkÃ¼r geÃ§en kayÄ±tlarÄ± gÃ¶ster"
    â€¢ "Problem kelimesi bulunan satÄ±rlarÄ± gÃ¶ster"
    
    ğŸ“ˆ **AkÄ±llÄ± Sayma:**
    â€¢ "AdÄ± Ahmet olan kaÃ§ kiÅŸi var?"
    â€¢ "KaÃ§ tane merhaba kelimesi var?"
    â€¢ "Talep aÃ§Ä±klamasÄ±nda problem yazan kaÃ§ kayÄ±t var?"
    â€¢ "Toplam kaÃ§ adet ankara yazÄ±yor?"
    
    ğŸ“‹ **Dinamik SÃ¼tun SeÃ§imi:**
    â€¢ "Sadece talep aÃ§Ä±klamasÄ± sÃ¼tununu gÃ¶ster"
    â€¢ "YanÄ±t sÃ¼tununu getir"
    â€¢ "AÃ§Ä±klama sÃ¼tunlarÄ±nÄ± getir"
    â€¢ "Ä°lk 3 sÃ¼tunu gÃ¶ster"
    
    ğŸ“„ **KayÄ±t SÄ±nÄ±rlama:**
    â€¢ "Ä°lk 10 kaydÄ± getir"
    â€¢ "Son 5 kayÄ±t gÃ¶ster"
    â€¢ "Ä°lk 20 satÄ±rÄ± gÃ¶ster"
    â€¢ "Son 15 kaydÄ± getir"
    
    ğŸ” **KapsamlÄ± Arama:**
    â€¢ "123 numaralÄ± kayÄ±tlarÄ± bul"
    â€¢ "Ankara yazanlarÄ± gÃ¶ster"
    â€¢ "Admin kelimesini ara"
    â€¢ "Email adresi olanlarÄ± getir"
    
    ğŸ“… **Tarih ve SayÄ± Filtreleri:**
    â€¢ "2024 yÄ±lÄ±ndaki kayÄ±tlarÄ± gÃ¶ster"
    â€¢ "100'den bÃ¼yÃ¼k deÄŸerleri bul"
    â€¢ "BugÃ¼nkÃ¼ tarihi iÃ§erenler"
    
    ğŸ¯ **GeliÅŸmiÅŸ Komutlar:**
    â€¢ "BoÅŸ hÃ¼creleri gÃ¶ster"
    â€¢ "Tekrar eden kayÄ±tlarÄ± bul"
    â€¢ "En uzun aÃ§Ä±klamayÄ± gÃ¶ster"
    â€¢ "KÄ±sa yanÄ±tlarÄ± filtrele"
    â€¢ "BÃ¼yÃ¼k harfle yazÄ±lanlarÄ± bul"
    
    ğŸ”¢ **Ä°statistik KomutlarÄ±:**
    â€¢ "Ortalama deÄŸeri nedir?"
    â€¢ "En yÃ¼ksek deÄŸer hangisi?"
    â€¢ "Toplam kayÄ±t sayÄ±sÄ± kaÃ§?"
    â€¢ "Benzersiz deÄŸer sayÄ±sÄ±?"
    
    **ğŸ¯ AI Ã–zellikler:**
    â€¢ SÃ¼tun isimlerini otomatik tanÄ±r
    â€¢ BÃ¼yÃ¼k/kÃ¼Ã§Ã¼k harf duyarlÄ± deÄŸil
    â€¢ TÃ¼rkÃ§e doÄŸal dil iÅŸleme
    â€¢ AkÄ±llÄ± kelime eÅŸleÅŸtirme
    â€¢ SayÄ±sal karÅŸÄ±laÅŸtÄ±rmalar
    â€¢ Tarih formatlarÄ±nÄ± anlÄ±yor
    â€¢ "KaÃ§ tane" diyerek sayÄ±m yapabilirsiniz
    """)

    # Mevcut sÃ¼tunlarÄ± gÃ¶ster
    if 'df' in locals():
        st.write("**ğŸ“‹ Mevcut SÃ¼tunlar:**")
        for col in df.columns:
            st.write(f"â€¢ {col}")
    

col_voice1, col_voice2 = st.sidebar.columns([3, 1])

with col_voice1:
    if st.button("ğŸ¤ Sesli Sor", key="voice_search", help="Mikrofona tÄ±klayÄ±p sorunuzu sorun"):
        voice_result = get_voice_input()
        st.session_state["voice_query"] = voice_result

with col_voice2:
    if st.button("ğŸ”„", key="voice_clear", help="Sesli soruyu temizle"):
        st.session_state["voice_query"] = ""

# Sesli arama sonucu gÃ¶ster
if "voice_query" in st.session_state and st.session_state["voice_query"]:
    st.sidebar.info(f"ğŸ¤ Sesli Komut: {st.session_state['voice_query']}")
    
    # SonuÃ§ mesajÄ±nÄ± gÃ¶ster
    if "voice_result_message" in st.session_state and st.session_state["voice_result_message"]:
        if "bulundu" in st.session_state["voice_result_message"] or "gÃ¶steriliyor" in st.session_state["voice_result_message"]:
            st.sidebar.success(f"âœ… {st.session_state['voice_result_message']}")
        else:
            st.sidebar.warning(f"âš ï¸ {st.session_state['voice_result_message']}")
    
    if st.session_state["voice_query"] not in ["Zaman aÅŸÄ±mÄ± - tekrar deneyin", "Ses anlaÅŸÄ±lamadÄ±", "Ses tanÄ±ma servisi hatasÄ±"]:
        # Sesli aramayÄ± uygula
        df = process_voice_search(st.session_state["voice_query"], df)

st.sidebar.markdown("---")

# ğŸ’¬ AI Chat Ã–zelliÄŸi
st.sidebar.subheader("ğŸ’¬ AI Chat Asistan")

# Chat yardÄ±m mesajÄ±
with st.sidebar.expander("ğŸ’¡ Chat Asistan NasÄ±l KullanÄ±lÄ±r?", expanded=False):
    st.write("""
    **ğŸ’¬ AI Chat KomutlarÄ±:**
    
    ğŸ” **DoÄŸal Dil ile Arama:**
    â€¢ "Tabloda adÄ± Tolga olanlarÄ± getir"
    â€¢ "Åehri Ä°stanbul olan kayÄ±tlarÄ± bul"
    â€¢ "Telefonu 532 ile baÅŸlayanlarÄ± gÃ¶ster"
    â€¢ "Email adresi gmail olanlarÄ± filtrele"
    
    ğŸ“Š **AkÄ±llÄ± Sorgular:**
    â€¢ "KaÃ§ farklÄ± ÅŸehir var?"
    â€¢ "En uzun aÃ§Ä±klama hangisi?"
    â€¢ "BoÅŸ telefon alanlarÄ± gÃ¶ster"
    â€¢ "Ä°lk 5 kaydÄ± getir"
    
    ğŸ’¡ **Ä°puÃ§larÄ±:**
    â€¢ DoÄŸal TÃ¼rkÃ§e ile yazÄ±n
    â€¢ SÃ¼tun isimlerini tam bilmeniz gerekmez
    â€¢ "getir", "gÃ¶ster", "bul" gibi kelimeler kullanÄ±n
    """)

# Chat input
col_chat1, col_chat2 = st.sidebar.columns([5, 1])

# Chat temizleme kontrolÃ¼
if 'clear_chat' not in st.session_state:
    st.session_state['clear_chat'] = False

with col_chat1:
    # Chat temizlenecekse boÅŸ deÄŸer kullan
    default_value = "" if st.session_state.get('clear_chat', False) else st.session_state.get("chat_input", "")
    
    # Form kullanarak Enter tuÅŸu ile submit yapalÄ±m
    with st.form(key="chat_form", clear_on_submit=True):
        chat_query = st.text_area(
            "ğŸ’¬ Sorunuzu yazÄ±n:",
            value=default_value,
            placeholder="Ã–rn: AdÄ± Ahmet olanlarÄ± getir (Enter ile ara)",
            height=80,
            key="chat_textarea"
        )
        
        # Submit butonu (gÃ¶rÃ¼nmez)
        submit_button = st.form_submit_button("ğŸ” Ara", use_container_width=True)
    
    # Form submit edilince chat_query'yi iÅŸle
    if submit_button and chat_query and chat_query.strip():
        st.session_state['submitted_chat_query'] = chat_query.strip()

with col_chat2:
    st.write("")  # BoÅŸ satÄ±r ekle
    if st.button("ğŸ—‘ï¸", key="chat_clear", help="Chat'i temizle"):
        st.session_state['clear_chat'] = True
        if 'chat_result_message' in st.session_state:
            del st.session_state['chat_result_message']
        if 'chat_history' in st.session_state:
            st.session_state['chat_history'] = []
        if 'submitted_chat_query' in st.session_state:
            del st.session_state['submitted_chat_query']
        st.rerun()

# Clear flag'i sÄ±fÄ±rla
if st.session_state.get('clear_chat', False):
    st.session_state['clear_chat'] = False

# Chat sonucu iÅŸle
# Form'dan gelen sorgu varsa iÅŸle
if 'submitted_chat_query' in st.session_state:
    chat_query = st.session_state['submitted_chat_query']
    del st.session_state['submitted_chat_query']  # Bir kez kullan
else:
    chat_query = None

if chat_query and chat_query.strip():
    st.sidebar.info(f"ğŸ’¬ Chat Komutu: {chat_query}")
    
    # Ana sayfada progress bar gÃ¶ster
    progress_placeholder = st.empty()
    
    with progress_placeholder.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info("ğŸ” AI Arama yapÄ±lÄ±yor...")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Progress bar animasyonu
            for i in range(100):
                progress_bar.progress(i + 1)
                if i < 30:
                    status_text.text("ğŸ” SÃ¼tunlar analiz ediliyor...")
                elif i < 60:
                    status_text.text("ğŸ§  AI komutu iÅŸleniyor...")
                elif i < 90:
                    status_text.text("ğŸ“Š Veriler filtreleniyor...")
                else:
                    status_text.text("âœ… SonuÃ§lar hazÄ±rlanÄ±yor...")
                time.sleep(0.02)  # Biraz daha hÄ±zlÄ±
    
    # Chat komutunu sesli asistan ile aynÄ± mantÄ±kla iÅŸle
    chat_filtered_df, chat_message = smart_voice_assistant(chat_query, df)
    
    # Progress bar'Ä± temizle
    progress_placeholder.empty()
    
    # Ana sayfada sonuÃ§ mesajÄ±nÄ± gÃ¶ster
    if "bulundu" in chat_message or "gÃ¶steriliyor" in chat_message or "seÃ§ildi" in chat_message:
        st.success(f"âœ… {chat_message}")
        # Chat sonucunu ana dataframe'e uygula
        df = chat_filtered_df
    else:
        st.warning(f"âš ï¸ {chat_message}")
    
    # Sidebar'da da gÃ¶ster
    st.sidebar.success(f"âœ… Arama tamamlandÄ±!")
    
    # Chat geÃ§miÅŸini session state'e kaydet
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    
    # Yeni komutu geÃ§miÅŸe ekle
    st.session_state['chat_history'].append({
        'query': chat_query,
        'result': chat_message,
        'timestamp': pd.Timestamp.now().strftime("%H:%M")
    })
    
    # Son 5 komutu tut
    if len(st.session_state['chat_history']) > 5:
        st.session_state['chat_history'] = st.session_state['chat_history'][-5:]
    
    # Session state'e kaydet
    st.session_state['chat_result_message'] = chat_message

# Chat geÃ§miÅŸini gÃ¶ster
if 'chat_history' in st.session_state and st.session_state['chat_history']:
    with st.sidebar.expander("ğŸ“œ Son Chat GeÃ§miÅŸi", expanded=False):
        for i, chat in enumerate(reversed(st.session_state['chat_history'])):
            st.write(f"**{chat['timestamp']}** - {chat['query']}")
            if "bulundu" in chat['result']:
                st.success(f"âœ… {chat['result']}")
            else:
                st.info(f"â„¹ï¸ {chat['result']}")
            st.write("---")

else:
    st.info(" Başlamak için **.xlsx** dosyanızı yükleyin veya soldan bir dosya seçin.")
