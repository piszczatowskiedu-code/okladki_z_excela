import streamlit as st

# CSS dla lepszego wyglądu
st.markdown("""
<style>
    .tool-card {
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #f0f2f6;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        height: 100%;
    }
    .tool-card:hover {
        border-color: #1f77b4;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .stButton > button {
        width: 100%;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Pierwszy rząd - 2 kolumny
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='tool-card'>
    <h3>📥 Pobieranie Okładek</h3>
    <p>Automatyczne pobieranie obrazów okładek produktów na podstawie linków z pliku Excel.</p>
    <ul>
        <li>✅ Wsparcie dla wielu formatów obrazów</li>
        <li>✅ Konwersja WebP na PNG</li>
        <li>✅ Filtrowanie po kodach EAN</li>
        <li>✅ Eksport do ZIP</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Otwórz narzędzie pobierania", key="btn_covers", type="primary"):
        st.switch_page("pages/1_pobieranie_okladek.py")

with col2:
    st.markdown("""
    <div class='tool-card'>
    <h3>📝 Konwerter HTML</h3>
    <p>Konwersja opisów produktów z formatu tekstowego na HTML z zachowaniem formatowania.</p>
    <ul>
        <li>✅ Automatyczne wykrywanie nagłówków</li>
        <li>✅ Konwersja list punktowanych</li>
        <li>✅ Formatowanie tekstu (bold, italic)</li>
        <li>✅ Eksport do Excel</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Otwórz konwerter HTML", key="btn_html", type="primary"):
        st.switch_page("pages/2_zmiana_opisu_html.py")

# Drugi rząd
st.markdown("---")
col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class='tool-card'>
    <h3>🖼️ Konwerter WebP</h3>
    <p>Konwersja obrazów WebP i innych formatów graficznych z obsługą przetwarzania wsadowego.</p>
    <ul>
        <li>✅ Konwersja między formatami (WebP, PNG, JPG)</li>
        <li>✅ Przetwarzanie wielu plików jednocześnie</li>
        <li>✅ Regulacja jakości JPEG</li>
        <li>✅ Automatyczne pakowanie do ZIP</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Otwórz konwerter obrazów", key="btn_webp", type="primary"):
        st.switch_page("pages/3_konwerter_webp.py")

# Informacje dodatkowe
st.markdown("---")
with st.expander("ℹ️ Informacje o aplikacji"):
    st.markdown("""
    ### Dostępne narzędzia:
    
    #### 📥 Pobieranie okładek:
    - Automatyczne pobieranie obrazów z URL
    - Konwersja formatów (WebP → PNG)
    - Filtrowanie po kodach EAN
    - Pomijanie plików PDF
    - Raport z błędami i statystykami
    
    #### 📝 Konwerter HTML:
    - Konwersja markdown na HTML
    - Obsługa list i nagłówków
    - Formatowanie tekstu (bold, italic)
    - Zachowanie struktury dokumentu
    
    #### 🖼️ Konwerter WebP:
    - Konwersja między popularnymi formatami obrazów
    - Wsadowe przetwarzanie wielu plików
    - Regulowana jakość kompresji
    - Inteligentne pakowanie do ZIP
    """)

# Stopka
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888;'>Made with ❤️ using Streamlit</div>",
    unsafe_allow_html=True
)