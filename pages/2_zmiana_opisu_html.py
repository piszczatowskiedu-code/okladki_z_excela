import streamlit as st
import pandas as pd
import re
from io import BytesIO
from typing import Optional

# ============================================
# KONFIGURACJA STRONY
# ============================================
st.set_page_config(
    page_title="Konwerter opisów na HTML",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #ff7f0e;
        text-align: center;
        margin-bottom: 1rem;
    }
    .preview-box {
        border: 2px solid #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        background-color: #fafafa;
        margin: 1rem 0;
    }
    .html-preview {
        background-color: #f8f9fa;
        border-left: 4px solid #007bff;
        padding: 1rem;
        margin: 1rem 0;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNKCJE KONWERSJI TEKSTU NA HTML
# ============================================

def convert_inline_formatting(text: str) -> str:
    """Konwertuje formatowanie inline (pogrubienie, kursywa)."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    text = re.sub(r'_([^_]+)_', r'<em>\1</em>', text)
    return text


def detect_heading(line: str) -> Optional[tuple[int, str]]:
    """Wykrywa nagłówki w różnych formatach."""
    # Nagłówki Markdown
    match = re.match(r'^(#{1,6})\s+(.+)$', line)
    if match:
        level = len(match.group(1))
        return (level, match.group(2))
    
    # Nagłówki z dwukropkiem
    if line.endswith(':') and len(line) < 60 and not line.startswith('-'):
        return (3, line[:-1])
    
    return None


def text_to_html(text: str, options: dict) -> str:
    """Główna funkcja konwertująca tekst na HTML."""
    if not text or pd.isna(text):
        return ""
    
    text = str(text).strip()
    lines = text.split('\n')
    html_parts = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            i += 1
            continue
        
        # Nagłówki
        if options.get('convert_headings', True):
            heading = detect_heading(line)
            if heading:
                level, heading_text = heading
                if options.get('convert_formatting', True):
                    heading_text = convert_inline_formatting(heading_text)
                html_parts.append(f"<h{level}>{heading_text}</h{level}>")
                i += 1
                continue
        
        # Listy
        if options.get('convert_lists', True):
            # Lista punktowana
            if re.match(r'^[-*•]\s+', line):
                list_items = []
                while i < len(lines) and re.match(r'^[-*•]\s+', lines[i].strip()):
                    item_text = re.sub(r'^[-*•]\s+', '', lines[i].strip())
                    if options.get('convert_formatting', True):
                        item_text = convert_inline_formatting(item_text)
                    list_items.append(f"  <li>{item_text}</li>")
                    i += 1
                html_parts.append("<ul>\n" + "\n".join(list_items) + "\n</ul>")
                continue
            
            # Lista numerowana
            if re.match(r'^\d+[.)]\s+', line):
                list_items = []
                while i < len(lines) and re.match(r'^\d+[.)]\s+', lines[i].strip()):
                    item_text = re.sub(r'^\d+[.)]\s+', '', lines[i].strip())
                    if options.get('convert_formatting', True):
                        item_text = convert_inline_formatting(item_text)
                    list_items.append(f"  <li>{item_text}</li>")
                    i += 1
                html_parts.append("<ol>\n" + "\n".join(list_items) + "\n</ol>")
                continue
        
        # Zwykły paragraf
        paragraph_lines = []
        while i < len(lines) and lines[i].strip():
            current_line = lines[i].strip()
            
            # Sprawdź czy to nie początek listy lub nagłówka
            if options.get('convert_lists', True):
                if re.match(r'^[-*•]\s+', current_line) or re.match(r'^\d+[.)]\s+', current_line):
                    break
            if options.get('convert_headings', True) and detect_heading(current_line):
                break
                
            paragraph_lines.append(current_line)
            i += 1
        
        if paragraph_lines:
            paragraph_text = ' '.join(paragraph_lines)
            if options.get('convert_formatting', True):
                paragraph_text = convert_inline_formatting(paragraph_text)
            if options.get('add_paragraphs', True):
                html_parts.append(f"<p>{paragraph_text}</p>")
            else:
                html_parts.append(paragraph_text)
    
    html = '\n\n'.join(html_parts)
    
    if options.get('wrap_in_div', False):
        html = f'<div class="product-description">\n{html}\n</div>'
    
    return html


# ============================================
# INTERFEJS UŻYTKOWNIKA
# ============================================

# Nagłówek
st.markdown("<div class='main-header'>📝 Konwerter opisów produktów na HTML</div>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar z opcjami
with st.sidebar:
    st.header("⚙️ Opcje konwersji")
    
    options = {
        'add_paragraphs': st.checkbox("Dodaj tagi <p>", value=True, help="Opakuj akapity w tagi <p>"),
        'convert_lists': st.checkbox("Konwertuj listy", value=True, help="Konwertuj listy punktowane i numerowane"),
        'convert_headings': st.checkbox("Konwertuj nagłówki", value=True, help="Wykryj i konwertuj nagłówki"),
        'convert_formatting': st.checkbox("Konwertuj pogrubienie/kursywę", value=True, help="Konwertuj **bold** i *italic*"),
        'wrap_in_div': st.checkbox("Opakuj w <div>", value=False, help="Opakuj całość w div z klasą"),
    }
    
    st.markdown("---")
    st.markdown("### 📋 Instrukcja")
    st.markdown("""
    1. Wgraj plik Excel z opisami
    2. Wybierz kolumny (EAN i opis)
    3. Dostosuj opcje konwersji
    4. Kliknij 'Konwertuj na HTML'
    5. Pobierz wynikowy plik
    """)
    
    st.markdown("---")
    st.markdown("### 🎯 Wspierane formatowanie")
    st.info("""
    - **Nagłówki**: # H1, ## H2, lub tekst z :
    - **Listy**: - punkt lub 1. numeracja
    - **Pogrubienie**: **tekst** lub __tekst__
    - **Kursywa**: *tekst* lub _tekst_
    """)

# Główna część aplikacji
st.header("📤 Wgraj plik Excel")
uploaded_file = st.file_uploader(
    "Wybierz plik Excel (.xlsx, .xls)",
    type=['xlsx', 'xls'],
    help="Plik powinien zawierać kolumnę z opisami produktów"
)

if uploaded_file is not None:
    try:
        # Wczytaj wszystko jako string - zachowuje zera wiodące w EAN
        with st.spinner("Wczytywanie pliku..."):
            df = pd.read_excel(uploaded_file, dtype=str)
        
        st.success(f"✅ Wczytano **{len(df)}** wierszy z pliku **{uploaded_file.name}**")
        
        columns = df.columns.tolist()
        
        # Wybór kolumn
        st.markdown("### 🎯 Wybór kolumn")
        col1, col2 = st.columns(2)
        
        with col1:
            ean_column = st.selectbox(
                "Kolumna z kodami EAN:",
                columns,
                index=columns.index('EAN') if 'EAN' in columns else 0,
                help="Wybierz kolumnę z kodami EAN (SKU)"
            )
        
        with col2:
            # Szukaj kolumny z opisem
            default_desc_index = 1 if len(columns) > 1 else 0
            for i, col in enumerate(columns):
                if 'opis' in col.lower() or 'desc' in col.lower():
                    default_desc_index = i
                    break
                    
            description_column = st.selectbox(
                "Kolumna z opisami produktów:",
                columns,
                index=default_desc_index,
                help="Wybierz kolumnę zawierającą opisy do konwersji"
            )
        
        # Podgląd danych wejściowych
        st.markdown("### 👁️ Podgląd danych wejściowych")
        preview_df = df[[ean_column, description_column]].head(3)
        st.dataframe(preview_df, use_container_width=True)
        
        # Przykład konwersji
        if not df.empty and not pd.isna(df[description_column].iloc[0]):
            with st.expander("🔍 Podgląd konwersji pierwszego opisu"):
                sample_text = str(df[description_column].iloc[0])
                sample_html = text_to_html(sample_text, options)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Tekst oryginalny:**")
                    st.text_area("", sample_text, height=200, disabled=True)
                
                with col2:
                    st.markdown("**HTML wynikowy:**")
                    st.code(sample_html, language='html')
        
        # Przycisk konwersji
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 KONWERTUJ NA HTML", type="primary", use_container_width=True):
                with st.spinner("Konwertuję opisy..."):
                    # Tworzenie DataFrame wynikowego
                    export_df = pd.DataFrame({
                        'sku': df[ean_column].fillna(''),
                        'description-B2B': df[description_column].apply(
                            lambda x: text_to_html(x, options)
                        )
                    })
                    
                    st.session_state['export_df'] = export_df
                    st.success("✅ Konwersja zakończona!")
        
        # Wyświetl wyniki
        if 'export_df' in st.session_state:
            st.markdown("---")
            st.header("📊 Wyniki konwersji")
            
            export_df = st.session_state['export_df']
            
            # Statystyki
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Liczba produktów", len(export_df))
            with col2:
                converted = sum(1 for x in export_df['description-B2B'] if x)
                st.metric("Skonwertowane opisy", converted)
            with col3:
                empty = len(export_df) - converted
                st.metric("Puste opisy", empty)
            
            # Podgląd wyników
            st.markdown("### 📋 Podgląd wyników (pierwsze 10)")
            display_df = export_df.head(10).copy()
            # Skróć długie HTML do podglądu
            display_df['description-B2B'] = display_df['description-B2B'].apply(
                lambda x: x[:200] + '...' if len(x) > 200 else x
            )
            st.dataframe(display_df, use_container_width=True)
            
            # Pobieranie
            st.markdown("---")
            st.markdown("### 💾 Pobierz wynikowy plik")
            
            # Przygotuj plik Excel
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                export_df.to_excel(
                    writer, 
                    index=False, 
                    sheet_name='Produkty_HTML'
                )
                
                workbook = writer.book
                worksheet = writer.sheets['Produkty_HTML']
                
                # Format tekstowy dla SKU (zachowuje zera wiodące)
                text_format = workbook.add_format({'num_format': '@'})
                worksheet.set_column(0, 0, 20, text_format)
                worksheet.set_column(1, 1, 100)
                
                # Dodaj nagłówki z formatowaniem
                header_format = workbook.add_format({
                    'bold': True,
                    'bg_color': '#D7E4BD',
                    'border': 1
                })
                for col_num, value in enumerate(export_df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
            
            output.seek(0)
            
            # Nazwa pliku
            original_name = uploaded_file.name.rsplit('.', 1)[0]
            output_filename = f"{original_name}_HTML.xlsx"
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label="⬇️ POBIERZ EXCEL Z HTML",
                    data=output,
                    file_name=output_filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    type="primary"
                )
            
            st.info(f"📁 Plik **{output_filename}** zawiera **{len(export_df)}** wierszy z przekonwertowanymi opisami HTML.")
            
            # Opcja czyszczenia
            if st.button("🗑️ Wyczyść wyniki", type="secondary"):
                del st.session_state['export_df']
                st.rerun()
                    
    except Exception as e:
        st.error(f"❌ Błąd podczas przetwarzania pliku: {str(e)}")
        st.exception(e)

else:
    # Ekran powitalny
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.info("📤 Wgraj plik Excel z opisami produktów, aby rozpocząć konwersję")
        
        # Przykład
        with st.expander("📝 Przykład formatowania tekstu"):
            st.markdown("""
            **Tekst wejściowy:**
            ```
            # Najlepszy produkt
            
            Cechy produktu:
            - Wysoka jakość
            - **Gwarancja 2 lata**
            - *Darmowa dostawa*
            
            ## Specyfikacja
            1. Wymiary: 10x20cm
            2. Waga: 500g
            ```
            
            **HTML wyjściowy:**
            ```html
            <h1>Najlepszy produkt</h1>
            
            <h3>Cechy produktu</h3>
            <ul>
              <li>Wysoka jakość</li>
              <li><strong>Gwarancja 2 lata</strong></li>
              <li><em>Darmowa dostawa</em></li>
            </ul>
            
            <h2>Specyfikacja</h2>
            <ol>
              <li>Wymiary: 10x20cm</li>
              <li>Waga: 500g</li>
            </ol>
            ```
            """)

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888;'>📝 Moduł konwersji opisów na HTML</div>",
    unsafe_allow_html=True
)