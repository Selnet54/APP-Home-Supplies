import streamlit as st
import os

# --- KONFIGURACIJA ---
st.set_page_config(page_title="Zalihe", layout="wide")

# --- TVOJ REČNIK (Skraćena verzija radi koda) ---
if 'jezik_kljuc' not in st.session_state: st.session_state.jezik_kljuc = "srpski"

# --- CSS KOJI FORSIRA DESKTOP IZGLED ---
st.markdown("""
    <style>
    /* Poništavamo Streamlit ograničenja */
    .block-container {
        padding-top: 10px !important;
        max-width: 1000px !important;
        min-width: 800px !important; /* Ovo sprečava sužavanje */
        margin: auto;
    }

    /* Forsiramo da kontejner sa jezicima i hederom uvek ide horizontalno */
    .flex-header {
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        align-items: center;
        width: 100%;
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    /* Stil za dugmad u jezicima (Grid 3x3 koji se ne raspada) */
    .language-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        width: 100%;
        text-align: center;
    }

    .lang-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        cursor: pointer;
    }

    /* Povećavamo font da se vidi na mobilnom */
    .stButton > button {
        font-size: 14px !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNKCIJA ZA HEDER (Bez st.columns) ---
def prikazi_heder():
    # Koristimo HTML za heder da bismo bili sigurni da je u jednom redu
    st.markdown(f"""
        <div class="flex-header">
            <div style="font-weight:bold;">Home</div>
            <div style="font-weight:bold; margin-left: 20px;">Kategorija</div>
            <div style="font-weight:bold;">Zalihe</div>
            <div style="font-weight:bold;">Spisak</div>
            <div style="font-weight:bold; color:red;">Izlaz</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Prikaz izabranog jezika ispod hedera
    if 'izabrani_jezik_kod' in st.session_state:
        kod = st.session_state.izabrani_jezik_kod
        naziv = st.session_state.izabrani_jezik_naziv
        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                <img src="https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/{kod.lower() if kod != 'Srpski' else 'rs'}.svg" width="30">
                <span style="font-weight:bold;">{naziv}</span>
            </div>
            <hr>
        """, unsafe_allow_html=True)

# --- LOGIKA ---
prikazi_heder()

if 'korak' not in st.session_state: st.session_state.korak = "jezik"

if st.session_state.korak == "jezik":
    st.write("### Izaberite jezik / Choose Language")
    
    # Ručni grid za jezike
    jezici = [
        ("rs", "Srpski"), ("gb", "English"), ("de", "Deutsch"),
        ("ru", "Русский"), ("ua", "Українська"), ("hu", "Magyar"),
        ("es", "Español"), ("pt", "Português"), ("cn", "中文")
    ]
    
    # Koristimo kolone ali im fiksiramo širinu kroz CSS gore
    cols = st.columns(3)
    for i, (kod, ime) in enumerate(jezici):
        with cols[i % 3]:
            # Prikaz zastave preko URL-a za test (sigurnije na GitHub-u)
            flag_url = f"https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/{kod}.svg"
            st.image(flag_url, width=60)
            if st.button(ime, key=kod):
                st.session_state.izabrani_jezik_kod = kod
                st.session_state.izabrani_jezik_naziv = ime
                st.session_state.korak = "kategorije"
                st.rerun()

elif st.session_state.korak == "kategorije":
    if st.button("← Nazad"):
        st.session_state.korak = "jezik"
        st.rerun()
    st.success(f"Izabrali ste: {st.session_state.izabrani_jezik_naziv}")
