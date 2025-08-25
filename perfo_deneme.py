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
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 🚀 MODERN ENTERPRISE FEATURES
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
                'message': 'Bellek yetersizliği tespit edildi',
                'solution': 'Dosya boyutunu küçültün veya sayfalama kullanın',
                'icon': '🧠'
            }
        elif 'file' in error_str or 'no such file' in error_str:
            return {
                'category': 'File',
                'severity': 'Medium',
                'message': 'Dosya bulunamadı veya okunamadı',
                'solution': 'Dosya yolunu kontrol edin ve dosyanın mevcut olduğundan emin olun',
                'icon': '📁'
            }
        elif 'permission' in error_str or 'access' in error_str:
            return {
                'category': 'Permission',
                'severity': 'Medium',
                'message': 'Dosya erişim izni hatası',
                'solution': 'Dosyanın açık olmadığından emin olun veya yönetici izinleri alın',
                'icon': '🔒'
            }
        elif 'encoding' in error_str or 'decode' in error_str:
            return {
                'category': 'Encoding',
                'severity': 'Low',
                'message': 'Karakter kodlama hatası',
                'solution': 'Dosyayı UTF-8 formatında kaydedin',
                'icon': '🔤'
            }
        else:
            return {
                'category': 'General',
                'severity': 'Medium',
                'message': 'Beklenmeyen hata',
                'solution': 'Dosyayı kontrol edin ve tekrar deneyin',
                'icon': '⚠️'
            }
    
    @staticmethod
    def display_error(error, context=""):
        error_info = SmartErrorHandler.categorize_error(error)
        
        with st.container():
            st.error(f"""
            {error_info['icon']} **{error_info['category']} Hatası** ({error_info['severity']} Öncelik)
            
            **Problem:** {error_info['message']}
            
            **Çözüm:** {error_info['solution']}
            
            {f"**Bağlam:** {context}" if context else ""}
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
            issues.append(f"Yüksek boş veri oranı: %{null_ratio*100:.1f}")
            recommendations.append("Boş hücreleri doldurun veya ilgili satırları kaldırın")
        
        if duplicate_rows > 0:
            issues.append(f"{duplicate_rows} duplicate satır bulundu")
            recommendations.append("Duplicate satırları kaldırın")
        
        if df.shape[1] > 20:
            recommendations.append("Çok sayıda sütun var - gereksiz olanları gizlemeyi düşünün")
        
        if df.shape[0] > 10000:
            recommendations.append("Büyük veri seti - filtreleme ve sayfalama kullanın")
        
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
            title="📊 Veri Türü Dağılımı"
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
            title="🔍 Sütun Bazlı Boş Veri Analizi",
            labels={'x': 'Sütunlar', 'y': 'Boş Hücre Sayısı'}
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
                    title=f"📊 {column} - Dağılım Analizi",
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
                    title=f"📊 {column} - En Sık Değerler (Top 20)",
                    labels={'x': column, 'y': 'Frekans'}
                )
                
                fig.update_layout(xaxis_tickangle=-45)
                
            else:
                # For other data types, create simple value counts
                value_counts = data.value_counts().head(10)
                
                fig = px.pie(
                    values=value_counts.values,
                    names=value_counts.index,
                    title=f"📊 {column} - Değer Dağılımı"
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

# Favori sistemi için session state
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

error_handler = SmartErrorHandler()
data_validator = DataValidator()
smart_visualizer = SmartVisualizer()

# uploads klasöründeki dosyaları listele
import os
uploads_dir = "uploads"
uploads_path = os.path.join(os.getcwd(), uploads_dir)
if not os.path.exists(uploads_path):
    os.makedirs(uploads_path)

st.sidebar.header("Yüklenen Excel Dosyaları")
excel_files = [f for f in os.listdir(uploads_path) if f.endswith(".xlsx")]

# Dosya seçimi için session state
if "selected_file_key" not in st.session_state:
    st.session_state["selected_file_key"] = None

selected_file = st.sidebar.selectbox(
    "Daha önce yüklenen dosyalar",
    options=["Dosya seçin..."] + excel_files,
    key="file_selector"
) if excel_files else None

# Seçilen dosyayı kontrol et
if selected_file and selected_file != "Dosya seçin...":
    st.session_state["selected_file_key"] = selected_file
else:
    selected_file = None

# Dosya silme özelliği
if excel_files:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🗑️ Dosya Yönetimi")
    
    # Her dosya için silme butonu
    files_to_delete = []
    for file in excel_files:
        col1, col2 = st.sidebar.columns([3, 1])
        col1.text(file[:20] + "..." if len(file) > 20 else file)
        if col2.button("🗑️", key=f"delete_{file}", help=f"{file} dosyasını sil"):
            files_to_delete.append(file)
    
    # Silme işlemini gerçekleştir
    for file_to_delete in files_to_delete:
        try:
            file_path = os.path.join(uploads_path, file_to_delete)
            os.remove(file_path)
            st.sidebar.success(f"✅ {file_to_delete} silindi!")
            
            # Eğer silinen dosya seçili dosyaysa, session'ı temizle
            if st.session_state.get("selected_file_key") == file_to_delete:
                st.session_state["selected_file_key"] = None
            
            # Sayfayı yenile
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"❌ Dosya silinemedi: {e}")
    
    # Tüm dosyaları silme butonu
    if len(excel_files) > 1:
        st.sidebar.markdown("---")
        if st.sidebar.button("🗑️ Tüm Dosyaları Sil", help="Tüm Excel dosyalarını sil"):
            try:
                for file in excel_files:
                    file_path = os.path.join(uploads_path, file)
                    os.remove(file_path)
                
                # Session'ı temizle
                st.session_state["selected_file_key"] = None
                st.sidebar.success(f"✅ {len(excel_files)} dosya silindi!")
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"❌ Dosyalar silinemedi: {e}")

# -------------------------
# Sayfa ayarları
# -------------------------
st.set_page_config(
    page_title="Perfo Destek Çözümleri - Talepler Arayüzü",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------
# Yardımcı fonksiyonlar
# -------------------------

def get_voice_input():
    """Sesli arama için mikrofon girişi alır"""
    if not SPEECH_AVAILABLE:
        return "Sesli arama kütüphanesi yüklü değil. 'pip install SpeechRecognition pyaudio' komutunu çalıştırın."
    
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🎤 Konuşun... (3 saniye bekleniyor)")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=3)
        
        text = r.recognize_google(audio, language='tr-TR')
        return text
    except sr.WaitTimeoutError:
        return "Zaman aşımı - tekrar deneyin"
    except sr.UnknownValueError:
        return "Ses anlaşılamadı"
    except sr.RequestError:
        return "Ses tanıma servisi hatası"
    except Exception as e:
        return f"Hata: {str(e)}"

def generate_smart_summary(df):
    """Excel dosyası için basit ve kullanışlı özet oluşturur"""
    
    # En sık tekrar eden kelimeleri bul
    all_text = ""
    text_cols = df.select_dtypes(include=['object']).columns
    for col in text_cols:
        all_text += " " + df[col].astype(str).str.cat(sep=" ")
    
    # Kelimeleri ayıkla ve say
    words = re.findall(r'\b\w{3,}\b', all_text.lower())
    stop_words = {'için', 'olan', 'olan', 'ile', 'bir', 'bu', 've', 'ama', 'fakat', 'nan', 'none'}
    words = [w for w in words if w not in stop_words and not w.isdigit()]
    
    from collections import Counter
    word_counts = Counter(words).most_common(5)
    
    # Basit analiz
    total_rows = len(df)
    total_cols = len(df.columns)
    empty_cells = df.isnull().sum().sum()
    
    # Excel dosyasını akıllı analiz et ve özetle
    excel_analysis = analyze_excel_content(df, word_counts, total_rows, total_cols)
    
    # Akıllı öneriler
    suggestions = []
    if empty_cells > total_rows * 0.1:
        suggestions.append("📝 Çok sayıda boş hücre var - veri temizliği yapılabilir")
    
    if total_rows > 1000:
        suggestions.append("📊 Büyük veri seti - filtreleme kullanmanız önerilir")
    
    if len(text_cols) > 5:
        suggestions.append("🔍 Çok sayıda metin sütunu - arama özelliğini kullanın")
    
    return {
        "toplam_satir": total_rows,
        "toplam_sutun": total_cols,
        "bos_hucre": int(empty_cells),
        "en_sik_kelimeler": word_counts,
        "oneriler": suggestions,
        "akilli_analiz": excel_analysis
    }

def analyze_excel_content(df, top_words, rows, cols):
    """Excel içeriğini analiz edip kısa özet cümleler oluşturur"""
    analysis = []
    
    # Dosya türü analizi
    if any(keyword in ' '.join([word[0] for word in top_words]) for keyword in ['talep', 'ticket', 'request']):
        analysis.append("🎫 Bu bir talep/destek dosyası gibi görünüyor.")
    elif any(keyword in ' '.join([word[0] for word in top_words]) for keyword in ['müşteri', 'customer', 'client']):
        analysis.append("👤 Müşteri bilgileri içeren bir dosya.")
    elif any(keyword in ' '.join([word[0] for word in top_words]) for keyword in ['satış', 'sales', 'revenue', 'gelir']):
        analysis.append("💰 Satış/gelir verileri içeriyor.")
    elif any(keyword in ' '.join([word[0] for word in top_words]) for keyword in ['çalışan', 'employee', 'personel']):
        analysis.append("👥 İnsan kaynakları/personel verisi.")
    else:
        analysis.append("📊 Genel veri tablosu şeklinde düzenlenmiş.")
    
    # Veri yoğunluğu analizi
    if rows < 50:
        analysis.append("📝 Küçük boyutlu, detaylı inceleme için uygun.")
    elif rows < 500:
        analysis.append("📈 Orta boyutlu, analiz için ideal.")
    else:
        analysis.append("🎯 Büyük veri seti, filtreleme önerilir.")
    
    # Sütun çeşitliliği
    numeric_cols = df.select_dtypes(include=['number']).columns
    text_cols = df.select_dtypes(include=['object']).columns
    
    if len(numeric_cols) > len(text_cols):
        analysis.append("🔢 Çoğunlukla sayısal veriler içeriyor.")
    elif len(text_cols) > len(numeric_cols):
        analysis.append("📝 Ağırlıklı olarak metin verileri var.")
    else:
        analysis.append("⚖️ Sayısal ve metin verileri dengeli dağılım.")
    
    # Veri kalitesi
    empty_ratio = df.isnull().sum().sum() / (rows * cols)
    if empty_ratio < 0.05:
        analysis.append("✅ Veri kalitesi yüksek, az boş hücre.")
    elif empty_ratio < 0.20:
        analysis.append("⚠️ Orta düzeyde veri eksikliği var.")
    else:
        analysis.append("🔴 Veri kalitesi düşük, temizlik gerekli.")
    
    return analysis

def smart_voice_assistant(voice_text, df):
    """Akıllı sesli asistan - Excel verilerini analiz ederek doğal dil komutlarını işler"""
    voice_text = voice_text.lower()
    original_df = df.copy()
    
    # Excel sütun isimlerini ve içeriklerini öğren
    column_info = {}
    for col in df.columns:
        col_lower = str(col).lower()
        # Her sütundaki benzersiz değerleri al (ilk 100 satır için performans)
        sample_values = df[col].dropna().astype(str).str.lower().head(100).unique()
        column_info[col_lower] = {
            'original_name': col,
            'sample_values': sample_values
        }
    
    # Sayma komutları
    count_patterns = ['kaç', 'sayı', 'adet', 'tane', 'count']
    is_count_query = any(pattern in voice_text for pattern in count_patterns)
    
    # İçerik arama komutları
    content_patterns = ['içer', 'geç', 'bulunan', 'olan', 'yazan', 'contain']
    is_content_search = any(pattern in voice_text for pattern in content_patterns)
    
    # Sütun seçme komutları
    column_patterns = ['sütun', 'sutun', 'kolon', 'alan', 'field']
    is_column_select = any(pattern in voice_text for pattern in column_patterns)
    
    # Anahtar kelimeleri çıkar
    words = voice_text.split()
    search_terms = [w for w in words if len(w) > 2 and w not in [
        'içer', 'geç', 'bulunan', 'olan', 'yazan', 'sütun', 'sutun', 'kolon',
        'getir', 'göster', 'bul', 'ara', 'kayıt', 'veri', 'sadece', 'olan',
        'kaç', 'tane', 'adet', 'sayı', 'için', 'ile', 'den', 'dan', 'nda', 'nde'
    ]]
    
    # Hangi sütun hedeflendiğini bul
    target_column = None
    target_content = None
    
    for term in search_terms:
        # Sütun ismi eşleşmesi ara
        for col_key, col_data in column_info.items():
            # Sütun isminde geçiyor mu?
            if term in col_key or any(part in term for part in col_key.split()):
                target_column = col_data['original_name']
                break
            
            # Sütun içeriğinde geçiyor mu?
            if any(term in str(val) for val in col_data['sample_values']):
                if not target_column:  # İlk bulunan sütunu al
                    target_column = col_data['original_name']
                target_content = term
                break
    
    # Özel komut analizleri
    result_message = ""
    
    try:
        if is_count_query and target_content:
            # "Kaç tane merhaba yazan veri var" gibi sorular
            if target_column:
                filtered_df = df[df[target_column].astype(str).str.lower().str.contains(target_content, na=False)]
                count = len(filtered_df)
                result_message = f"'{target_content}' kelimesi '{target_column}' sütununda {count} kayıtta bulundu."
                return filtered_df, result_message
            else:
                # Tüm sütunlarda ara
                mask = df.astype(str).apply(lambda x: x.str.lower().str.contains(target_content, na=False)).any(axis=1)
                filtered_df = df[mask]
                count = len(filtered_df)
                result_message = f"'{target_content}' kelimesi toplam {count} kayıtta bulundu."
                return filtered_df, result_message
        
        elif is_content_search and target_content:
            # "Talep açıklaması içerisinde merhaba yazan verileri getir"
            if target_column:
                filtered_df = df[df[target_column].astype(str).str.lower().str.contains(target_content, na=False)]
                result_message = f"'{target_column}' sütununda '{target_content}' içeren {len(filtered_df)} kayıt bulundu."
                return filtered_df, result_message
            else:
                # Genel arama
                mask = df.astype(str).apply(lambda x: x.str.lower().str.contains(target_content, na=False)).any(axis=1)
                filtered_df = df[mask]
                result_message = f"'{target_content}' içeren {len(filtered_df)} kayıt bulundu."
                return filtered_df, result_message
        
        elif is_column_select and target_column:
            # "Sadece talep açıklaması sütununu göster"
            filtered_df = df[[target_column]]
            result_message = f"'{target_column}' sütunu gösteriliyor."
            return filtered_df, result_message
        
        elif target_column and not is_count_query and not is_content_search:
            # Genel sütun bazlı arama
            if target_content:
                filtered_df = df[df[target_column].astype(str).str.lower().str.contains(target_content, na=False)]
                result_message = f"'{target_column}' sütununda '{target_content}' araması: {len(filtered_df)} sonuç."
                return filtered_df, result_message
            else:
                # Sadece sütunu göster
                filtered_df = df[[target_column]]
                result_message = f"'{target_column}' sütunu gösteriliyor."
                return filtered_df, result_message
        
        # Genel arama (hiçbir özel komut yoksa)
        elif search_terms:
            search_term = search_terms[0]
            mask = df.astype(str).apply(lambda x: x.str.lower().str.contains(search_term, na=False)).any(axis=1)
            filtered_df = df[mask]
            result_message = f"'{search_term}' araması: {len(filtered_df)} sonuç bulundu."
            return filtered_df, result_message
    
    except Exception as e:
        result_message = f"Arama hatası: {str(e)}"
        return df, result_message
    
    # Hiçbir şey bulunamazsa
    result_message = "Komut anlaşılamadı. Lütfen daha açık ifade edin."
    return df, result_message

def smart_voice_assistant(voice_text, df):
    """Gelişmiş AI sesli asistan - Excel sütunlarını ve içeriklerini analiz ederek akıllı filtreleme yapar"""
    voice_text = voice_text.lower().strip()
    
    # Debug için orijinal metni logla
    print(f"🎤 Algılanan ses: '{voice_text}'")
    
    # Mevcut sütun isimlerini analiz et
    column_analysis = {}
    for col in df.columns:
        col_clean = str(col).lower()
        # Her sütundaki eşsiz değerleri al (ilk 200 tane - daha fazla veri)
        unique_values = df[col].dropna().astype(str).str.lower().unique()[:200]
        column_analysis[col] = {
            'name_lower': col_clean,
            'original_name': col,
            'sample_values': list(unique_values),
            'value_count': len(df[col].dropna()),
            'dtype': str(df[col].dtype)
        }
    
    # Arama teriminin hangi sütunda bulunduğunu akıllıca tespit et
    def find_best_column_for_content(search_terms, df):
        """Arama terimlerinin hangi sütunlarda bulunduğunu analiz eder"""
        column_scores = {}
        
        for col in df.columns:
            score = 0
            matches = 0
            
            # Her arama terimi için bu sütunda kaç eşleşme var
            for term in search_terms:
                try:
                    col_matches = df[col].astype(str).str.lower().str.contains(term, na=False, case=False, regex=False).sum()
                    if col_matches > 0:
                        score += col_matches
                        matches += 1
                        print(f"   🔎 '{term}' -> '{col}' sütununda {col_matches} eşleşme")
                except:
                    continue
            
            if score > 0:
                column_scores[col] = {
                    'score': score,
                    'term_matches': matches,
                    'avg_score': score / len(search_terms) if len(search_terms) > 0 else 0
                }
        
        # En iyi sütunu seç
        if column_scores:
            # Öncelik: En çok terimi olan, sonra en yüksek skor
            best_col = max(column_scores.items(), 
                          key=lambda x: (x[1]['term_matches'], x[1]['score']))
            
            print(f"🎯 En iyi sütun: '{best_col[0]}' (Skor: {best_col[1]['score']}, Terim: {best_col[1]['term_matches']})")
            return best_col[0], column_scores
        
        return None, {}
    def find_column_by_name(voice_text):
        # Sadece açık sütun belirteçleri varsa sütun ara
        explicit_column_indicators = ['sütun', 'sutun', 'sütunu', 'sutunu', 'alanı', 'alanda']
        
        # Açık sütun belirteci yoksa tüm sütunlarda ara
        if not any(indicator in voice_text for indicator in explicit_column_indicators):
            print(f"🔍 Açık sütun belirteci yok, tüm sütunlarda arama yapılacak")
            return None
        
        # Açık sütun belirteci varsa en uygun sütunu bul
        best_match = None
        best_score = 0
        
        for col_info in column_analysis.values():
            col_original = col_info['original_name'].lower()
            col_words = col_original.split()
            
            # Sesli metindeki kelimeleri temizle
            voice_words = voice_text.replace(':', '').replace(',', '').split()
            voice_words = [w for w in voice_words if len(w) > 2]
            
            # Sütun ismindeki tüm kelimelerin sesli metinde olup olmadığını kontrol et
            matching_words = 0
            total_char_match = 0
            
            for col_word in col_words:
                # Türkçe karakter temizliği
                col_word_clean = col_word.replace('ı', 'i').replace('ğ', 'g').replace('ü', 'u').replace('ş', 's').replace('ö', 'o').replace('ç', 'c')
                
                for voice_word in voice_words:
                    voice_word_clean = voice_word.replace('ı', 'i').replace('ğ', 'g').replace('ü', 'u').replace('ş', 's').replace('ö', 'o').replace('ç', 'c')
                    
                    # Kısmi eşleşme de kabul et
                    if col_word_clean in voice_word_clean or voice_word_clean in col_word_clean:
                        matching_words += 1
                        total_char_match += len(col_word)
                        break
            
            # Eşleşme skorunu hesapla
            if len(col_words) > 0:
                score = (matching_words / len(col_words)) * total_char_match
                
                # Özel kelimeler için bonus puan
                if any(keyword in voice_text for keyword in ['unvan', 'fiili', 'adı', 'adi']):
                    if any(keyword in col_original for keyword in ['unvan', 'fiili', 'ad']):
                        score += 100  # Yüksek bonus
                
                if score > best_score:
                    best_score = score
                    best_match = col_info['original_name']
        
        print(f"🎯 En iyi sütun eşleşmesi: {best_match} (Skor: {best_score})")
        
        # Yeterli skor yoksa tüm sütunlarda ara
        if best_score < 50:
            print(f"🔍 Skor yetersiz ({best_score}), tüm sütunlarda arama yapılacak")
            return None
        
        return best_match
    
    # İçerik kelimelerini ayıkla
    def extract_search_content(voice_text, detected_column=None):
        # Bu kelimeleri atla
        skip_words = {
            'tabloda', 'tablodan', 'kayıt', 'kayıtları', 'kayıtlar', 'veri', 'veriler',
            'getir', 'göster', 'bul', 'ara', 'filtrele', 'içeren', 'olan', 'olanları',
            'yazan', 'yazanları', 'bulunan', 'bulunanları', 'sütun', 'sutun', 'sadece', 
            'için', 'ile', 'den', 'dan', 'nda', 'nde', 'da', 'de', 'adi:', 'adı:', 'olan'
        }
        
        # Eğer sütun tespit edildiyse, o sütunun kelimelerini de atla
        if detected_column:
            column_words = detected_column.lower().split()
            skip_words.update(column_words)
            # Türkçe karakter varyasyonları
            for word in column_words:
                skip_words.add(word.replace('ı', 'i').replace('ğ', 'g').replace('ü', 'u').replace('ş', 's').replace('ö', 'o').replace('ç', 'c'))
        
        words = voice_text.replace(':', '').replace(',', '').split()
        content_words = []
        
        for word in words:
            word_clean = word.lower().strip()
            if len(word_clean) > 2 and word_clean not in skip_words:
                # Özel isimler ve önemli kelimeler
                if any(char.isupper() for char in word) or word_clean in ['genel', 'müdür', 'yardımcısı', 'başkan', 'uzman']:
                    content_words.append(word_clean)
                elif not any(skip in word_clean for skip in skip_words):
                    content_words.append(word_clean)
        
        print(f"📝 Çıkarılan arama kelimeleri: {content_words}")
        return content_words
    
    # Komut türünü belirle ve işle
    result_message = ""
    
    # 0. ÖNCE SAYISAL KARŞILAŞTIRMA KOMUTLARİNI KONTROL ET (en yüksek öncelik)
    comparison_patterns = {
        'küçük': ['küçük', 'kucuk', 'az', 'altında', 'altındaki', 'dan küçük', 'den küçük'],
        'büyük': ['büyük', 'buyuk', 'fazla', 'üstünde', 'üstündeki', 'dan büyük', 'den büyük', 'dan fazla'],
        'eşit': ['eşit', 'esit', 'olan', 'equal']
    }
    
    # Sayı arama
    number_match = re.search(r'(\d+)', voice_text)
    comparison_type = None
    
    if number_match:
        target_number = int(number_match.group(1))
        
        # Karşılaştırma türünü bul
        for comp_type, patterns in comparison_patterns.items():
            if any(pattern in voice_text for pattern in patterns):
                comparison_type = comp_type
                break
        
        if comparison_type:
            # Sütun adını bul
            target_column = find_column_by_name(voice_text)
            
            if not target_column:
                # Sayısal sütunları kontrol et
                numeric_cols = df.select_dtypes(include=['number']).columns
                for col in numeric_cols:
                    col_lower = col.lower()
                    if any(word in col_lower for word in voice_text.split() if len(word) > 2):
                        target_column = col
                        break
                
                # Hala bulunamadıysa ilk sayısal sütunu al
                if not target_column and len(numeric_cols) > 0:
                    target_column = numeric_cols[0]
            
            if target_column:
                try:
                    # Sayısal değerlere dönüştür
                    df_numeric = pd.to_numeric(df[target_column], errors='coerce')
                    
                    if comparison_type == 'küçük':
                        mask = df_numeric < target_number
                        result_message = f"📊 '{target_column}' sütununda {target_number}'dan küçük olan {mask.sum()} kayıt bulundu"
                    elif comparison_type == 'büyük':
                        mask = df_numeric > target_number
                        result_message = f"📊 '{target_column}' sütununda {target_number}'dan büyük olan {mask.sum()} kayıt bulundu"
                    elif comparison_type == 'eşit':
                        mask = df_numeric == target_number
                        result_message = f"📊 '{target_column}' sütununda {target_number}'a eşit olan {mask.sum()} kayıt bulundu"
                    
                    filtered_df = df[mask]
                    print(f"🔢 Sayısal filtreleme: '{target_column}' {comparison_type} {target_number} -> {mask.sum()} sonuç")
                    return filtered_df, result_message
                    
                except Exception as e:
                    print(f"⚠️ Sayısal karşılaştırma hatası: {e}")

    # 1. ÖNCE KAYIT LİMİTLEME KOMUTLARİNI KONTROL ET (en yüksek öncelik)
    if any(word in voice_text for word in ['ilk', 'son']) and any(word in voice_text for word in ['kayıt', 'satır']) and 'sütun' not in voice_text:
        number_match = re.search(r'(\d+)', voice_text)
        if number_match:
            n = int(number_match.group(1))
            
            if 'ilk' in voice_text:
                filtered_df = df.head(n)
                result_message = f"📋 İlk {n} kayıt getiriliyor"
                return filtered_df, result_message
            elif 'son' in voice_text:
                filtered_df = df.tail(n)
                result_message = f"  Son {n} kayıt getiriliyor"
                return filtered_df, result_message
    
    # 1. AKILLI İÇERİK ARAMA ("müfettiş olanları getir", "sadece müfettiş")
    if any(word in voice_text for word in ['getir', 'göster', 'bul', 'ara', 'filtrele', 'olanları', 'yazanları', 'içeren', 'sadece', 'olan']):
        # Önce sütun belirteci var mı kontrol et
        target_column = find_column_by_name(voice_text)
        search_content = extract_search_content(voice_text, target_column)
        
        print(f"🔍 Manuel hedef sütun: {target_column}")
        print(f"🔍 Arama içeriği: {search_content}")
        
        if search_content:
            # Arama terimlerini hazırla
            search_terms = search_content if isinstance(search_content, list) else [search_content]
            
            if target_column:
                # Manuel olarak belirtilmiş sütunda ara
                print(f"🎯 Manuel belirtilen '{target_column}' sütununda arama yapılıyor...")
                search_term = ' '.join(search_terms) if len(search_terms) > 1 else search_terms[0]
                mask = df[target_column].astype(str).str.lower().str.contains(search_term, na=False, case=False, regex=False)
                filtered_df = df[mask]
                matches = mask.sum()
                print(f"   📍 '{search_term}' terimi '{target_column}' sütununda {matches} kayıt buldu")
                result_message = f"🔍 '{target_column}' sütununda '{search_term}' içeren {matches} kayıt bulundu"
                return filtered_df, result_message
            else:
                # Akıllı sütun analizi yap - hangi sütunda bu terimler en çok geçiyor?
                print(f"🧠 Arama terimleri için en uygun sütun analiz ediliyor...")
                best_column, column_scores = find_best_column_for_content(search_terms, df)
                
                if best_column and column_scores[best_column]['score'] >= len(search_terms):
                    # Belirli bir sütunda yoğunlaşmış - o sütunda ara
                    search_term = ' '.join(search_terms) if len(search_terms) > 1 else search_terms[0]
                    mask = df[best_column].astype(str).str.lower().str.contains(search_term, na=False, case=False, regex=False)
                    filtered_df = df[mask]
                    matches = mask.sum()
                    result_message = f"🎯 '{search_term}' için en uygun sütun '{best_column}' - {matches} kayıt bulundu"
                    return filtered_df, result_message
                else:
                    # Hiçbir sütunda yoğunlaşmamış - tüm sütunlarda ara
                    print(f"🔍 Tüm sütunlarda arama yapılıyor ({len(df.columns)} sütun)...")
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
                            print(f"   📍 '{search_term}' terimi '{col}' sütununda {col_matches} kayıt buldu")
                    except Exception as e:
                        print(f"   ⚠️ '{col}' sütununda arama hatası: {e}")
                        continue
                
                if mask.sum() > 0:
                    filtered_df = df[mask]
                    result_message = f"  '{search_term}' içeren {len(filtered_df)} kayıt bulundu"
                    if matching_columns:
                        result_message += f" (Bulunan sütunlar: {', '.join(matching_columns[:3])})"
                    return filtered_df, result_message
                else:
                    result_message = f"❌ '{search_term}' için hiçbir eşleşme bulunamadı"
                    return df, result_message
    
    # 2. İSTATİSTİK KOMUTLARİ
    elif any(word in voice_text for word in ['ortalama', 'average', 'mean']):
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            col = numeric_cols[0]
            avg_val = df[col].mean()
            result_message = f"📊 '{col}' sütununun ortalaması: {avg_val:.2f}"
            return df, result_message
    
    elif any(word in voice_text for word in ['en yüksek', 'maksimum', 'max', 'büyük']):
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            col = numeric_cols[0]
            max_val = df[col].max()
            result_message = f"  '{col}' sütununun en yüksek değeri: {max_val}"
            return df, result_message
    
    elif any(word in voice_text for word in ['toplam kayıt', 'kaç kayıt', 'satır sayısı']):
        result_message = f"📋 Toplam kayıt sayısı: {len(df)}"
        return df, result_message
    
    elif any(word in voice_text for word in ['benzersiz', 'unique', 'farklı']):
        # İlgili sütunu bul
        target_col = find_column_by_name(voice_text)
        
        if target_col:
            unique_count = df[target_col].nunique()
            result_message = f"🔢 '{target_col}' sütununda {unique_count} benzersiz değer var"
            return df, result_message
    
    # 3. SAYMA KOMUTLARİ ("kaç tane", "sayısı", "adet")
    elif any(word in voice_text for word in ['kaç', 'sayı', 'adet', 'toplam']):
        search_content = extract_search_content(voice_text)
        
        if search_content:
            search_term = search_content[0]
            target_column = find_column_by_name(voice_text)
            
            if target_column:
                # Belirli sütunda say
                matching_rows = df[target_column].astype(str).str.lower().str.contains(search_term, na=False, case=False, regex=False)
                count = matching_rows.sum()
                result_message = f"🔢 '{search_term}' kelimesi '{target_column}' sütununda {count} kayıtta bulundu"
            else:
                # Tüm sütunlarda say
                mask = df.astype(str).apply(lambda x: x.str.lower().str.contains(search_term, na=False, case=False)).any(axis=1)
                count = mask.sum()
                result_message = f"  '{search_term}' kelimesi toplam {count} kayıtta bulundu"
            
            return df, result_message
    
    # 4. SÜTUN SEÇİMİ ("sütunu göster", "sadece ... sütun")
    elif any(word in voice_text for word in ['sütun', 'sutun', 'sadece']):
        best_match = None
        best_score = 0
        
        # Özel sütun seçimleri - İlk N sütun
        if 'ilk' in voice_text and 'sütun' in voice_text:
            number_match = re.search(r'(\d+)', voice_text)
            if number_match:
                n = int(number_match.group(1))
                selected_cols = df.columns[:n]
                result_message = f"📋 İlk {n} sütun seçildi"
                return df[selected_cols], result_message
        
        # Akıllı sütun eşleştirme
        target_column = find_column_by_name(voice_text)
        if target_column:
            result_message = f"  '{target_column}' sütunu seçildi"
            return df[[target_column]], result_message
    
    # 5. GENEL ARAMA - basitleştirilmiş
    else:
        search_content = extract_search_content(voice_text)
        if search_content:
            search_term = search_content[0]
            
            # Tüm sütunlarda ara
            mask = pd.Series([False] * len(df))
            matching_columns = []
            
            for col in df.columns:
                col_mask = df[col].astype(str).str.lower().str.contains(search_term, na=False, case=False, regex=False)
                if col_mask.sum() > 0:
                    mask = mask | col_mask
                    matching_columns.append(col)
            
            if mask.sum() > 0:
                filtered_df = df[mask]
                result_message = f"🔎 '{search_term}' için {len(filtered_df)} kayıt bulundu"
                if matching_columns:
                    result_message += f" (Sütunlar: {', '.join(matching_columns[:3])})"
                return filtered_df, result_message
    
    result_message = f"❓ Komut anlaşılamadı: '{voice_text}'. Lütfen daha net konuşun."
    return df, result_message

def process_voice_search(voice_text, df):
    """Sesli arama metnini akıllı asistana yönlendirir"""
    filtered_df, message = smart_voice_assistant(voice_text, df)
    
    # Session state'e mesajı kaydet
    if 'voice_result_message' not in st.session_state:
        st.session_state['voice_result_message'] = ""
    
    st.session_state['voice_result_message'] = message
    return filtered_df

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Başlıkları temizle
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]

    # Olası varyasyonları eşleştir
    aliases = {
        "Talep No": {"Talep No", "Talep_No", "TalepNo", "ID", "No"},
        "Talep Açıklaması": {"Talep Açıklaması", "Talep Aciklamasi", "Aciklama", "Açıklama", "Talep Açıklama"},
        "Yanıt": {"Yanıt", "Yanit", "Cevap", "Sonuç"},
        "Yanıt Açıklaması": {"Yanıt Açıklaması", "Yanit Aciklamasi", "Cevap Açıklaması", "Detay", "Açıklama (Yanıt)"},
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

    # Basit string arama - yazdığınız metni olduğu gibi arar
    mask = pd.Series([False] * len(df), index=df.index)
    
    for c in cols:
        if c in df.columns:
            colvals = df[c].astype(str).fillna("")
            
            if case_sensitive:
                # Büyük/küçük harf duyarlı arama
                if whole_word:
                    # Tam kelime eşleşmesi (regex ile)
                    pattern = r"\b" + re.escape(query) + r"\b"
                    mask = mask | colvals.str.contains(pattern, regex=True, case=True)
                else:
                    # Basit string içerme kontrolü
                    mask = mask | colvals.str.contains(query, case=True, regex=False)
            else:
                # Büyük/küçük harf duyarsız arama
                if whole_word:
                    # Tam kelime eşleşmesi (regex ile)
                    pattern = r"\b" + re.escape(query) + r"\b"
                    mask = mask | colvals.str.contains(pattern, regex=True, case=False)
                else:
                    # Basit string içerme kontrolü (varsayılan)
                    mask = mask | colvals.str.contains(query, case=False, regex=False)
    
    return mask

def highlight_terms(val, terms):
    # Vurgulama devre dışı - sadece orijinal değeri döndür
    return val

def to_excel_bytes(df: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Sonuçlar")
    return output.getvalue()

# -------------------------
# 🚀 MODERN ENTERPRISE HEADER
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
        <span class="feature-badge">🧠 AI Powered</span>
        <span class="feature-badge">⚡ High Performance</span>
        <span class="feature-badge">🔍 Smart Search</span>
        <span class="feature-badge">📊 Advanced Analytics</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------
# Dosya Yükleme ve Validation
# -------------------------

# Eğer streamlit run ile çalıştırılıyorsa dosya yükleme, yoksa doğrudan dosyadan oku

uploaded = st.file_uploader("📁 Excel dosyanızı yükleyin (.xlsx)", type=["xlsx"], key="excel_uploader")
if uploaded is not None:
    # Performance tracking için
    with st.session_state.perf_monitor.track_operation("file_upload"):
        try:
            # Dosyayı uploads klasörüne kaydet
            file_path = os.path.join(uploads_path, uploaded.name)
            with open(file_path, "wb") as f:
                f.write(uploaded.getbuffer())
            st.success(f"✅ Dosya başarıyla yüklendi: {uploaded.name}")
            st.session_state["selected_file_key"] = uploaded.name
        except Exception as e:
            error_handler.display_error(e, "Dosya yükleme sırasında")

# Dosya yükleme mantığı - seçilen dosya veya yeni yüklenen dosya
selected_file_to_load = st.session_state.get("selected_file_key") or selected_file

if selected_file_to_load:
    # Start performance monitoring
    load_operation = st.session_state.perf_monitor.start_operation("file_load")
    
    with st.spinner(f"{selected_file_to_load} dosyası yükleniyor..."):
        try:
            df_raw = pd.read_excel(os.path.join(uploads_path, selected_file_to_load))
            
            # Validate the loaded data
            validation_result = data_validator.validate_excel_file(df_raw)
            
            # Show validation results
            if not validation_result['is_valid']:
                st.warning("⚠️ Veri kalitesi sorunları tespit edildi:")
                for issue in validation_result['issues']:
                    st.write(f"• {issue}")
                
                if validation_result['recommendations']:
                    with st.expander("💡 İyileştirme Önerileri"):
                        for rec in validation_result['recommendations']:
                            st.info(rec)
            
            # Show quality score
            score = validation_result['quality_score']
            score_color = "🟢" if score > 80 else "🟡" if score > 60 else "🔴"
            
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
            error_handler.display_error(e, "Dosya okuma sırasında")
            st.stop()

    # -------------------------
    # MAIN APPLICATION TABS
    # -------------------------
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Veri Analizi", "📈 Akıllı Analitik", "🔍 Keşif & Filtreler", "⭐ Favorilerim", "⚡ Performans"])

    with tab1:
        st.subheader("📊 Veri Görselleştirme ve Temel Analiz")
    
    # Show data summary first
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Toplam Satır", len(df_raw))
    with col2:
        st.metric("Sütun Sayısı", len(df_raw.columns))
    with col3:
        memory_usage = df_raw.memory_usage(deep=True).sum() / 1024**2
        st.metric("Bellek Kullanımı", f"{memory_usage:.1f} MB")
    with col4:
        null_percentage = (df_raw.isnull().sum().sum() / (len(df_raw) * len(df_raw.columns))) * 100
        st.metric("Boş Veri %", f"{null_percentage:.1f}%")

    # Normalized df for processing
    df = normalize_columns(df_raw)

    # -------------------------
    # 🤖 Akıllı Özet
    # -------------------------
    with st.expander("🤖 Akıllı Dosya Özeti", expanded=False):
        summary = generate_smart_summary(df)
        
        # 🤖 AI Analizi
        st.subheader("🧠 AI Analizi")
        for analysis_point in summary['akilli_analiz']:
            st.write(f"• {analysis_point}")
        
        st.markdown("---")
        
        # Kısa özet
        st.write(f"📄 **{summary['toplam_satir']} satır, {summary['toplam_sutun']} sütunlu** bir Excel dosyası analiz edildi.")
        
        if summary['bos_hucre'] > 0:
            st.write(f"⚠️ {summary['bos_hucre']} boş hücre tespit edildi.")
        
        # En sık kelimeler
        if summary['en_sik_kelimeler']:
            st.write("**🔤 En sık kullanılan kelimeler:**")
            for word, count in summary['en_sik_kelimeler']:
                st.write(f"• {word.title()}: {count} kez")
        
        # Öneriler
        if summary['oneriler']:
            st.write("**💡 Akıllı Öneriler:**")
            for suggestion in summary['oneriler']:
                st.info(suggestion)

    required_cols = ["Talep No", "Talep Açıklaması", "Yanıt", "Yanıt Açıklaması"]
    missing = [c for c in required_cols if c not in df.columns]

    with st.expander("📑 Sütun Eşleştirme / Bilgi", expanded=False):
        st.write("Algılanan sütunlar:", list(df.columns))
        if missing:
            st.warning(
                f"Eksik olduğu tespit edilen beklenen sütunlar: {missing}. "
                "Yine de mevcut sütunlarla çalışmaya devam edebilirsiniz."
            )
    
    # Smart pagination for large datasets - TAB 1 DATA DISPLAY
    st.markdown("### 📊 Veri Görüntüleme")
    
    # Apply any sidebar filters first
    filtered_df = df.copy()
    
    if len(filtered_df) > 1000:
        st.info(f"📊 Büyük veri seti tespit edildi ({len(filtered_df):,} satır). Performans için sayfalama aktif.")
        
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1:
            page_size = st.selectbox("📄 Sayfa boyutu", [100, 500, 1000, 2000], index=1, key="tab1_pagesize")
        with col2:
            total_pages = math.ceil(len(filtered_df) / page_size)
            current_page = st.number_input("📍 Sayfa", min_value=1, max_value=total_pages, value=1, key="tab1_page")
        with col3:
            st.metric("📊 Toplam Sayfa", total_pages)
        
        start_idx = (current_page - 1) * page_size
        end_idx = min(start_idx + page_size, len(filtered_df))
        df_display = filtered_df.iloc[start_idx:end_idx]
        
        st.info(f"📄 Gösterilen: {start_idx + 1}-{end_idx} / {len(filtered_df):,} satır (Sayfa {current_page}/{total_pages})")
    else:
        df_display = filtered_df
        st.success(f"✅ Tüm veriler gösteriliyor ({len(df_display):,} satır)")
    
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
    st.markdown("### 📥 Export Seçenekleri")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📥 CSV İndir"):
            with st.session_state.perf_monitor.track_operation("csv_export"):
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    "⬇️ CSV Dosyasını İndir", 
                    csv, 
                    f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", 
                    "text/csv"
                )
    
    with col2:
        if st.button("📥 Excel İndir"):
            with st.session_state.perf_monitor.track_operation("excel_export"):
                excel_buffer = io.BytesIO()
                filtered_df.to_excel(excel_buffer, index=False)
                st.download_button(
                    "⬇️ Excel Dosyasını İndir", 
                    excel_buffer.getvalue(), 
                    f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                )
    
    with col3:
        if st.button("📥 JSON İndir"):
            with st.session_state.perf_monitor.track_operation("json_export"):
                json_str = filtered_df.to_json(indent=2, orient='records')
                st.download_button(
                    "⬇️ JSON Dosyasını İndir", 
                    json_str, 
                    f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 
                    "application/json"
                )
    
    with col4:
        st.metric("📊 Export Hazır", f"{len(filtered_df):,} satır")
    
    # -------------------------
    # 📄 KART GÖRÜNÜMÜ (Orijinal Özellik)
    # -------------------------
    st.markdown("### 📄 Kayıt Kartları Görünümü")
    
    # Toggle between table and card view
    view_col1, view_col2 = st.columns([1, 3])
    with view_col1:
        view_mode = st.selectbox("👁️ Görünüm Modu", ["📊 Tablo", "📄 Kart"], index=1)
    
    if view_mode == "📄 Kart":
        # Pagination for cards
        cards_per_page = st.slider("📄 Sayfa başına kart sayısı", 5, 20, 10)
        total_card_pages = math.ceil(len(df_display) / cards_per_page)
        
        if total_card_pages > 1:
            card_page = st.number_input("📄 Kart Sayfası", min_value=1, max_value=total_card_pages, value=1, key="card_page")
            card_start = (card_page - 1) * cards_per_page
            card_end = min(card_start + cards_per_page, len(df_display))
            cards_to_show = df_display.iloc[card_start:card_end]
            st.info(f"📄 Gösterilen kartlar: {card_start + 1}-{card_end} / {len(df_display)}")
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
                    <h4 style="margin: 0 0 15px 0; color: #333;">Kayıt #{idx + 1}</h4>
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
                    
                    if st.button("⭐" if not is_favorite else "💛", key=f"fav_card_{original_idx}", help="Favorilere ekle/çıkar"):
                        if is_favorite:
                            st.session_state.favorites.remove(record_id)
                            warning_msg = st.warning("💔 Favorilerden çıkarıldı!")
                            time.sleep(1.5)
                            warning_msg.empty()
                        else:
                            st.session_state.favorites.append(record_id)
                            success_msg = st.success("⭐ Favorilere eklendi!")
                            time.sleep(1.5)
                            success_msg.empty()
                        st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Add action buttons for each card
            card_action_cols = st.columns([1, 1, 1, 2])
            with card_action_cols[0]:
                if st.button(f"📋 Kopyala #{idx + 1}", key=f"copy_{idx}"):
                    card_text = f"Kayıt #{idx + 1}:\n" + "\n".join([f"{col}: {val}" for col, val in row.items()])
                    st.info(f"📋 Kayıt #{idx + 1} kopyalandı!")
            
            with card_action_cols[1]:
                if st.button(f"🔍 Detay #{idx + 1}", key=f"detail_{idx}"):
                    st.json(row.to_dict())
            
            with card_action_cols[2]:
                original_idx = df.index[idx]
                record_id = f"record_{original_idx}"
                is_favorite = record_id in st.session_state.favorites
                
                if st.button(f"⭐ Favori #{idx + 1}", key=f"fav_table_{original_idx}"):
                    if is_favorite:
                        # Favorilerden çıkar
                        st.session_state.favorites.remove(record_id)
                        warning_msg = st.warning(f"💔 Kayıt #{idx + 1} favorilerden çıkarıldı!")
                        time.sleep(1.5)
                        warning_msg.empty()
                    else:
                        # Favorilere ekle
                        st.session_state.favorites.append(record_id)
                        success_msg = st.success(f"⭐ Kayıt #{idx + 1} favorilere eklendi!")
                        time.sleep(1.5)
                        success_msg.empty()
                    st.rerun()
            
            # Extra spacing between cards
            st.markdown("<br>", unsafe_allow_html=True)

    with tab2:
        st.subheader("📈 Akıllı Analitik ve İstatistikler")
    
    # Smart statistics
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if numeric_cols:
        st.markdown("### 📊 Sayısal Veriler İçin Akıllı İstatistikler")
        
        # Auto-detect patterns and anomalies
        for col in numeric_cols[:3]:  # Limit to first 3 for performance
            with st.expander(f"📈 {col} - Detaylı Analiz"):
                col1, col2 = st.columns(2)
                
                with col1:
                    # Basic stats
                    stats = df[col].describe()
                    st.write("**Temel İstatistikler:**")
                    for stat, value in stats.items():
                        st.write(f"• {stat.title()}: {value:.2f}")
                
                with col2:
                    # Smart insights
                    st.write("**Akıllı Görüşler:**")
                    
                    # Detect outliers
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    outliers = df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)]
                    
                    if len(outliers) > 0:
                        st.warning(f"⚠️ {len(outliers)} aykırı değer tespit edildi")
                    else:
                        st.success("✅ Aykırı değer tespit edilmedi")
                    
                    # Distribution analysis
                    skewness = df[col].skew()
                    if abs(skewness) < 0.5:
                        st.info("📊 Normal dağılıma yakın")
                    elif skewness > 0.5:
                        st.warning("📈 Sağa çarpık dağılım")
                    else:
                        st.warning("📉 Sola çarpık dağılım")
                
                # Smart visualization
                fig = smart_visualizer.create_smart_chart(df, col)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
    
    # Correlation analysis for multiple numeric columns
    if len(numeric_cols) >= 2:
        st.markdown("### 🔗 Korelasyon Analizi")
        correlation_matrix = df[numeric_cols].corr()
        
        # Create interactive heatmap
        fig_corr = px.imshow(
            correlation_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu_r",
            title="Değişkenler Arası Korelasyon"
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
            st.markdown("#### 🎯 Güçlü Korelasyonlar")
            for col1, col2, corr in strong_correlations:
                correlation_type = "Pozitif" if corr > 0 else "Negatif"
                st.write(f"• **{col1}** ↔ **{col2}**: {correlation_type} ({corr:.3f})")

    with tab3:
        st.subheader("🔍 Gelişmiş Keşif ve Filtreler")
        df = normalize_columns(df_raw)
    
    # Smart search with suggestions
    st.markdown("### 🔍 Akıllı Arama")
    search_col1, search_col2 = st.columns([3, 1])
    
    with search_col1:
        search_term = st.text_input("🔍 Tüm verilerde ara...", placeholder="Aranacak kelime veya değer")
    with search_col2:
        case_sensitive = st.checkbox("Büyük/küçük harf duyarlı")
    
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
            st.success(f"🎯 '{search_term}' için {len(search_results)} sütunda toplam {sum(count for _, count in search_results)} sonuç bulundu:")
            
            for col, count in search_results:
                st.write(f"• **{col}**: {count} eşleşme")
            
            # Show filtered results
            mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=case_sensitive, na=False)).any(axis=1)
            filtered_df = df[mask]
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.warning(f"❌ '{search_term}' için sonuç bulunamadı")
    
    # Advanced filtering
    st.markdown("### ⚙️ Gelişmiş Filtreler")
    
    filter_col1, filter_col2 = st.columns(2)
    
    with filter_col1:
        # Numeric filters
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_columns:
            st.markdown("#### 📊 Sayısal Filtreler")
            selected_numeric = st.selectbox("Sayısal sütun seç", ["Seçiniz..."] + numeric_columns)
            
            if selected_numeric and selected_numeric != "Seçiniz...":
                min_val = float(df[selected_numeric].min())
                max_val = float(df[selected_numeric].max())
                
                range_values = st.slider(
                    f"{selected_numeric} değer aralığı",
                    min_val, max_val, (min_val, max_val)
                )
                
                filtered_by_range = df[
                    (df[selected_numeric] >= range_values[0]) & 
                    (df[selected_numeric] <= range_values[1])
                ]
                
                st.info(f"📊 Filtrelenen satır sayısı: {len(filtered_by_range)}")
    
    with filter_col2:
        # Text filters
        text_columns = df.select_dtypes(include=['object']).columns.tolist()
        if text_columns:
            st.markdown("#### 📝 Metin Filtreleri")
            selected_text_col = st.selectbox("Metin sütunu seç", ["Seçiniz..."] + text_columns)
            
            if selected_text_col and selected_text_col != "Seçiniz...":
                unique_values = df[selected_text_col].dropna().unique()
                if len(unique_values) <= 50:  # Show multiselect for reasonable number of options
                    selected_values = st.multiselect(
                        f"{selected_text_col} değerleri",
                        unique_values
                    )
                    
                    if selected_values:
                        filtered_by_text = df[df[selected_text_col].isin(selected_values)]
                        st.info(f"📝 Filtrelenen satır sayısı: {len(filtered_by_text)}")
                else:
                    st.info(f"⚠️ Çok fazla benzersiz değer ({len(unique_values)}). Arama kutusunu kullanın.")

    with tab4:
        st.subheader("⭐ Favori Kayıtlarım")
        
        if not st.session_state.favorites:
            st.info("💔 Henüz favori kaydınız yok.")
            st.markdown("""
            **Favori nasıl eklenir?**
            1. 📊 Veri Analizi sekmesine gidin
            2. Kart görünümünü seçin
            3. Beğendiğiniz kayıtta ⭐ butonuna tıklayın
            """)
        else:
            # Favori istatistikleri
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Toplam Favori", len(st.session_state.favorites))
            with col2:
                if st.button("🗑️ Tümünü Temizle"):
                    st.session_state.favorites = []
                success_msg = st.success("🗑️ Tüm favoriler temizlendi!")
                time.sleep(2)
                success_msg.empty()
                st.rerun()
        
        st.markdown("---")
        
        # Favori kayıtları göster
        for i, record_id in enumerate(st.session_state.favorites):
            # Record ID'den index'i çıkar
            index = int(record_id.split('_')[1])
            
            # Orijinal veriden kayıt bul
            if index in df.index:
                row = df.loc[index]
                
                # Basit favori kartı
                st.markdown(f"""
                <div style="
                    border: 2px solid #f39c12;
                    border-radius: 8px;
                    padding: 15px;
                    margin: 10px 0;
                    background-color: #fff8e1;
                ">
                    <h4 style="margin: 0 0 15px 0; color: #e67e22;">⭐ Favori Kayıt #{i + 1}</h4>
                """, unsafe_allow_html=True)
                
                # Tüm alanları göster
                for col_name, value in row.items():
                    if pd.isna(value):
                        display_value = "-"
                    else:
                        display_value = str(value)
                    
                    st.markdown(f"**{col_name}:** {display_value}")
                
                # Favoriden çıkar butonu
                if st.button(f"💔 Favoriden Çıkar", key=f"remove_fav_{index}"):
                    st.session_state.favorites.remove(record_id)
                    success_msg = st.success("💔 Favorilerden çıkarıldı!")
                    time.sleep(1.5)
                    success_msg.empty()
                    st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning(f"Kayıt #{index} artık mevcut değil.")

    with tab5:
        st.subheader("⚡ Performans İzleme ve Optimizasyon")
        
        # Performance metrics
    perf_stats = st.session_state.perf_monitor.get_stats()
    
    if perf_stats:
        st.markdown("### 📊 Performans Metrikleri")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Toplam İşlem", 
                perf_stats['total_operations'],
                delta=f"{perf_stats['successful_operations']} başarılı"
            )
        
        with col2:
            avg_time = perf_stats['average_execution_time']
            st.metric("Ortalama Süre", f"{avg_time:.2f}s")
        
        with col3:
            cache_stats = st.session_state.smart_cache.get_stats()
            hit_rate = (cache_stats['hits'] / max(cache_stats['total_requests'], 1)) * 100
            st.metric("Cache Hit Rate", f"{hit_rate:.1f}%")
        
        with col4:
            current_memory = df_raw.memory_usage(deep=True).sum() / 1024**2
            st.metric("Bellek Kullanımı", f"{current_memory:.1f} MB")
        
        # Detailed operation history
        if st.checkbox("🔍 Detaylı İşlem Geçmişi"):
            history = st.session_state.perf_monitor.operation_history
            if history:
                history_df = pd.DataFrame([
                    {
                        'İşlem': op['operation'],
                        'Başlangıç': op['start_time'].strftime('%H:%M:%S'),
                        'Süre (s)': f"{op.get('duration', 0):.3f}",
                        'Durum': '✅ Başarılı' if op.get('success', False) else '❌ Hatalı'
                    } for op in history[-20:]  # Son 20 işlem
                ])
                st.dataframe(history_df, use_container_width=True)
        
        # Performance recommendations
        st.markdown("### 💡 Performans Önerileri")
        
        recommendations = []
        
        if len(df_raw) > 10000:
            recommendations.append("📊 Büyük veri seti tespit edildi. Filtreleme kullanarak performansı artırabilirsiniz.")
        
        if perf_stats['average_execution_time'] > 2.0:
            recommendations.append("⏱️ Ortalama işlem süresi yüksek. Cache kullanımını artırın.")
        
        cache_stats = st.session_state.smart_cache.get_stats()
        hit_rate = (cache_stats['hits'] / max(cache_stats['total_requests'], 1)) * 100
        if hit_rate < 50:
            recommendations.append("💾 Cache hit rate düşük. Benzer sorguları tekrar kullanmaya çalışın.")
        
        current_memory = df_raw.memory_usage(deep=True).sum() / 1024**2
        if current_memory > 100:
            recommendations.append("🧠 Yüksek bellek kullanımı. Daha küçük veri setleri ile çalışmayı deneyin.")
        
        if not recommendations:
            recommendations.append("✅ Performans optimal görünüyor!")
        
        for rec in recommendations:
            st.info(rec)
    
    else:
        st.info("📊 Henüz performans verisi yok. Birkaç işlem yapın ve geri dönün.")
    
    # System info
    with st.expander("🖥️ Sistem Bilgileri"):
        st.json({
            "Python Version": sys.version,
            "Pandas Version": pd.__version__,
            "Streamlit Version": st.__version__,
            "Platform": sys.platform
        })

# -------------------------
# Kenar Çubuğu — Filtreler
# -------------------------
st.sidebar.header("🔎 Filtreler ve Arama")

# 🎤 Voice Search
st.sidebar.subheader("🎤 Sesli Sor")

# Sesli arama yardım mesajı
with st.sidebar.expander("🤖 AI Sesli Asistan Nasıl Kullanılır?", expanded=False):
    st.write("""
    **🤖 AI Sesli Asistan Komutları:**
    
    📊 **İçerik Filtreleme:**
    • "Tabloda adı Ahmet olanları getir"
    • "İsmi Mehmet olan kayıtları göster"
    • "Talep açıklaması içerisinde merhaba yazan verileri getir"
    • "Yanıt sütununda teşekkür geçen kayıtları göster"
    • "Problem kelimesi bulunan satırları göster"
    
    📈 **Akıllı Sayma:**
    • "Adı Ahmet olan kaç kişi var?"
    • "Kaç tane merhaba kelimesi var?"
    • "Talep açıklamasında problem yazan kaç kayıt var?"
    • "Toplam kaç adet ankara yazıyor?"
    
    📋 **Dinamik Sütun Seçimi:**
    • "Sadece talep açıklaması sütununu göster"
    • "Yanıt sütununu getir"
    • "Açıklama sütunlarını getir"
    • "İlk 3 sütunu göster"
    
    📄 **Kayıt Sınırlama:**
    • "İlk 10 kaydı getir"
    • "Son 5 kayıt göster"
    • "İlk 20 satırı göster"
    • "Son 15 kaydı getir"
    
    🔍 **Kapsamlı Arama:**
    • "123 numaralı kayıtları bul"
    • "Ankara yazanları göster"
    • "Admin kelimesini ara"
    • "Email adresi olanları getir"
    
    📅 **Tarih ve Sayı Filtreleri:**
    • "2024 yılındaki kayıtları göster"
    • "100'den büyük değerleri bul"
    • "Bugünkü tarihi içerenler"
    
    🎯 **Gelişmiş Komutlar:**
    • "Boş hücreleri göster"
    • "Tekrar eden kayıtları bul"
    • "En uzun açıklamayı göster"
    • "Kısa yanıtları filtrele"
    • "Büyük harfle yazılanları bul"
    
    🔢 **İstatistik Komutları:**
    • "Ortalama değeri nedir?"
    • "En yüksek değer hangisi?"
    • "Toplam kayıt sayısı kaç?"
    • "Benzersiz değer sayısı?"
    
    **🎯 AI Özellikler:**
    • Sütun isimlerini otomatik tanır
    • Büyük/küçük harf duyarlı değil
    • Türkçe doğal dil işleme
    • Akıllı kelime eşleştirme
    • Sayısal karşılaştırmalar
    • Tarih formatlarını anlıyor
    • "Kaç tane" diyerek sayım yapabilirsiniz
    """)

    # Mevcut sütunları göster
    if 'df' in locals():
        st.write("**📋 Mevcut Sütunlar:**")
        for col in df.columns:
            st.write(f"• {col}")
    

col_voice1, col_voice2 = st.sidebar.columns([3, 1])

with col_voice1:
    if st.button("🎤 Sesli Sor", key="voice_search", help="Mikrofona tıklayıp sorunuzu sorun"):
        voice_result = get_voice_input()
        st.session_state["voice_query"] = voice_result

with col_voice2:
    if st.button("🔄", key="voice_clear", help="Sesli soruyu temizle"):
        st.session_state["voice_query"] = ""

# Sesli arama sonucu göster
if "voice_query" in st.session_state and st.session_state["voice_query"]:
    st.sidebar.info(f"🎤 Sesli Komut: {st.session_state['voice_query']}")
    
    # Sonuç mesajını göster
    if "voice_result_message" in st.session_state and st.session_state["voice_result_message"]:
        if "bulundu" in st.session_state["voice_result_message"] or "gösteriliyor" in st.session_state["voice_result_message"]:
            st.sidebar.success(f"✅ {st.session_state['voice_result_message']}")
        else:
            st.sidebar.warning(f"⚠️ {st.session_state['voice_result_message']}")
    
    if st.session_state["voice_query"] not in ["Zaman aşımı - tekrar deneyin", "Ses anlaşılamadı", "Ses tanıma servisi hatası"]:
        # Sesli aramayı uygula
        df = process_voice_search(st.session_state["voice_query"], df)

st.sidebar.markdown("---")

# 💬 AI Chat Özelliği
st.sidebar.subheader("💬 AI Chat Asistan")

# Chat yardım mesajı
with st.sidebar.expander("💡 Chat Asistan Nasıl Kullanılır?", expanded=False):
    st.write("""
    **💬 AI Chat Komutları:**
    
    🔍 **Doğal Dil ile Arama:**
    • "Tabloda adı Tolga olanları getir"
    • "Şehri İstanbul olan kayıtları bul"
    • "Telefonu 532 ile başlayanları göster"
    • "Email adresi gmail olanları filtrele"
    
    📊 **Akıllı Sorgular:**
    • "Kaç farklı şehir var?"
    • "En uzun açıklama hangisi?"
    • "Boş telefon alanları göster"
    • "İlk 5 kaydı getir"
    
    💡 **İpuçları:**
    • Doğal Türkçe ile yazın
    • Sütun isimlerini tam bilmeniz gerekmez
    • "getir", "göster", "bul" gibi kelimeler kullanın
    """)

# Chat input
col_chat1, col_chat2 = st.sidebar.columns([5, 1])

# Chat temizleme kontrolü
if 'clear_chat' not in st.session_state:
    st.session_state['clear_chat'] = False

with col_chat1:
    # Chat temizlenecekse boş değer kullan
    default_value = "" if st.session_state.get('clear_chat', False) else st.session_state.get("chat_input", "")
    
    # Form kullanarak Enter tuşu ile submit yapalım
    with st.form(key="chat_form", clear_on_submit=True):
        chat_query = st.text_area(
            "💬 Sorunuzu yazın:",
            value=default_value,
            placeholder="Örn: Adı Ahmet olanları getir (Enter ile ara)",
            height=80,
            key="chat_textarea"
        )
        
        # Submit butonu (görünmez)
        submit_button = st.form_submit_button("🔍 Ara", use_container_width=True)
    
    # Form submit edilince chat_query'yi işle
    if submit_button and chat_query and chat_query.strip():
        st.session_state['submitted_chat_query'] = chat_query.strip()

with col_chat2:
    st.write("")  # Boş satır ekle
    if st.button("🗑️", key="chat_clear", help="Chat'i temizle"):
        st.session_state['clear_chat'] = True
        if 'chat_result_message' in st.session_state:
            del st.session_state['chat_result_message']
        if 'chat_history' in st.session_state:
            st.session_state['chat_history'] = []
        if 'submitted_chat_query' in st.session_state:
            del st.session_state['submitted_chat_query']
        st.rerun()

# Clear flag'i sıfırla
if st.session_state.get('clear_chat', False):
    st.session_state['clear_chat'] = False

# Chat sonucu işle
# Form'dan gelen sorgu varsa işle
if 'submitted_chat_query' in st.session_state:
    chat_query = st.session_state['submitted_chat_query']
    del st.session_state['submitted_chat_query']  # Bir kez kullan
else:
    chat_query = None

if chat_query and chat_query.strip():
    st.sidebar.info(f"💬 Chat Komutu: {chat_query}")
    
    # Ana sayfada progress bar göster
    progress_placeholder = st.empty()
    
    with progress_placeholder.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info("🔍 AI Arama yapılıyor...")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Progress bar animasyonu
            for i in range(100):
                progress_bar.progress(i + 1)
                if i < 30:
                    status_text.text("🔍 Sütunlar analiz ediliyor...")
                elif i < 60:
                    status_text.text("🧠 AI komutu işleniyor...")
                elif i < 90:
                    status_text.text("📊 Veriler filtreleniyor...")
                else:
                    status_text.text("✅ Sonuçlar hazırlanıyor...")
                time.sleep(0.02)  # Biraz daha hızlı
    
    # Chat komutunu sesli asistan ile aynı mantıkla işle
    chat_filtered_df, chat_message = smart_voice_assistant(chat_query, df)
    
    # Progress bar'ı temizle
    progress_placeholder.empty()
    
    # Ana sayfada sonuç mesajını göster
    if "bulundu" in chat_message or "gösteriliyor" in chat_message or "seçildi" in chat_message:
        st.success(f"✅ {chat_message}")
        # Chat sonucunu ana dataframe'e uygula
        df = chat_filtered_df
    else:
        st.warning(f"⚠️ {chat_message}")
    
    # Sidebar'da da göster
    st.sidebar.success(f"✅ Arama tamamlandı!")
    
    # Chat geçmişini session state'e kaydet
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    
    # Yeni komutu geçmişe ekle
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

# Chat geçmişini göster
if 'chat_history' in st.session_state and st.session_state['chat_history']:
    with st.sidebar.expander("📜 Son Chat Geçmişi", expanded=False):
        for i, chat in enumerate(reversed(st.session_state['chat_history'])):
            st.write(f"**{chat['timestamp']}** - {chat['query']}")
            if "bulundu" in chat['result']:
                st.success(f"✅ {chat['result']}")
            else:
                st.info(f"ℹ️ {chat['result']}")
            st.write("---")

# Metin arama
options = [c for c in df.columns if df[c].dtype == "object" or str(df[c].dtype).startswith("string")]
search_cols_default = [c for c in required_cols if c in options and c != "Talep No"]
search_cols = st.sidebar.multiselect(
    "Hangi alanlarda aransın?",
    options=options,
    default=search_cols_default or options[:3],
)

query = st.sidebar.text_input("Arama metni", placeholder="Ne yazarsanız o aranır (Örn: genel müdür yardımcısı)")
whole_word = st.sidebar.checkbox("Sadece tam kelime eşleşmesi", value=False)
case_sensitive = st.sidebar.checkbox("Büyük/küçük harf duyarlı", value=False)

# Gelişmiş dinamik filtreler (metin dışı basit filtre)
with st.sidebar.expander("⚙️ Gelişmiş (Opsiyonel)"):
    extra_filters = {}
    for c in df.columns:
        if c in ([talep_no_col] if talep_no_col else []) or c in search_cols:
            continue
        # Çok fazla farklı değer varsa select koymak anlamsız—sınırla
        unique_vals = df[c].dropna().unique()
        if 1 < len(unique_vals) <= 50:
            choice = st.multiselect(f"{c} filtresi", sorted(map(str, unique_vals)))
            if choice:
                extra_filters[c] = set(choice)

# -------------------------
# Filtreleme Mantığı
# -------------------------
mask = pd.Series([True] * len(df), index=df.index)

# Talep No filtresi
if talep_no_col and selected_talep_nos:
    mask = mask & df[talep_no_col].astype(str).isin(selected_talep_nos)

# Metin arama filtresi
if search_cols and query:
    mask = mask & text_search_mask(df, search_cols, query, whole_word, case_sensitive)

# Gelişmiş filtreler
for c, allowed in extra_filters.items():
    mask = mask & df[c].astype(str).isin(allowed)

df_f = df[mask].copy()

# -------------------------
# KPI'lar
# -------------------------
c1, c2, c3 = st.columns(3)
c1.metric("Toplam Kayıt", len(df))
c2.metric("Filtreli Kayıt", len(df_f))
c3.metric("Sütun Sayısı", len(df.columns))

# -------------------------
# Görünüm Ayarları
# -------------------------
view_mode = st.radio(
    "Görünüm",
    options=["Tablo", "Kartlar"],
    horizontal=True,
)

# İndir
excel_bytes = to_excel_bytes(df_f)
st.download_button(
    label="⬇️ Filtreli Sonuçları Excel Olarak İndir",
    data=excel_bytes,
    file_name="perfo_destek_sonuclar.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

# -------------------------
# TABLO GÖRÜNÜMÜ
# -------------------------
if view_mode == "Tablo":
    # Vurgulama için Styler kullan
    terms = [t.strip() for t in query.split() if t.strip()] if query else []

    styled = df_f.copy()
    for c in search_cols:
        if c in styled.columns:
            styled[c] = styled[c].astype(str)
            styled[c] = styled[c].apply(lambda v: highlight_terms(v, terms))

    # Index'i kullanıcı dostu yapalım
    styled.reset_index(drop=True, inplace=True)

    # Güvenli HTML işaretlemeyi aç
    st.dataframe(styled, use_container_width=True, hide_index=True)

# -------------------------
# KART GÖRÜNÜMÜ
# -------------------------
elif view_mode == "📄 Kart":
    if df_f.empty:
        st.info("Gösterilecek kart yok.")
    else:
        # Kartları 2 sütunda göster
        cols = st.columns(2, gap="large")
        for i, (_, row) in enumerate(df_f.iterrows()):
            with cols[i % 2]:
                with st.container(border=True):
                    st.subheader(str(row.get(df_f.columns[0], "—")))
                    for col in df_f.columns:
                        st.markdown(f"**{col}:** {row.get(col, '—') if pd.notna(row.get(col, None)) else '—'}")
                    with st.expander("Tüm Alanlar"):
                        st.json({c: (None if pd.isna(v) else v) for c, v in row.items()})

else:
    st.info("🚀 Başlamak için **.xlsx** dosyanızı yükleyin veya soldan bir dosya seçin.")
