import streamlit as st
import json
import os
import time
import streamlit.components.v1 as components

# 1. Konfigurasi Halaman Dasar
st.set_page_config(
    page_title="Portal Ujian Minimalis",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="auto"
)

# 2. Inisialisasi State Management
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'exam_data' not in st.session_state:
    st.session_state.exam_data = []
if 'end_time' not in st.session_state:
    st.session_state.end_time = None
if 'exam_title' not in st.session_state:
    st.session_state.exam_title = ""

# 3. CSS Kustom 
st.markdown("""
    <style>
    /* --- TOMBOL UTAMA --- */
    div.stButton > button:first-child { 
        background-color: #00BFFF; 
        color: white; 
        width: 100%; 
        border: 1px solid transparent; 
        border-radius: 6px; 
        font-weight: bold; 
        padding: 10px 10px;
    }
    div.stButton > button:first-child:hover { 
        background-color: #1E90FF; 
        color: white; 
    }

    /* --- TOMBOL NAVIGASI SIDEBAR --- */
    .nav-btn > button:first-child { background-color: #F8F9FA; color: #333; border: 1px solid #DDD; }
    
    /* --- GAYA PILIHAN JAWABAN (RADIO BUTTON) KOTAK --- */
    /* Target Container Radio */
    [data-testid="stRadio"] > div {
        flex-direction: column !important;
        gap: 15px !important; /* Jarak antar kotak jawaban */
    }

    /* Target Kotak Label Jawaban */
    [data-testid="stRadio"] div[role="radiogroup"] label {
        background-color: #ffffff !important;
        padding: 15px 20px !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 10px !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03) !important;
        cursor: pointer !important;
    }

    /* Efek Hover (Saat mouse diarahkan) */
    [data-testid="stRadio"] label:hover {
        border-color: #00BFFF !important;
        background-color: #f4faff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 10px rgba(0,191,255,0.1) !important;
        color: #00BFFF !important;
    }

    /* Target Teks di dalam pilihan */
    [data-testid="stRadio"] label p {
        font-size: 16px !important;
        font-weight: 500 !important;
        margin: 0 !important;
        color: #333 !important;
    }

    /* --- STICKY HEADER --- */
    .sticky-header { 
        position: sticky; 
        top: 0; 
        background: rgba(255,255,255,0.95); 
        z-index: 999; 
        padding: 15px 0; 
        border-bottom: 1px solid #EEE; 
        margin-bottom: 20px; 
        display: flex; 
        justify-content: space-between; 
        align-items: center;
        backdrop-filter: blur(5px);
    }

    /* --- HASIL JAWABAN --- */
    .correct-ans { color: #28a745; font-weight: bold; background: #e6ffec; padding: 2px 5px; border-radius: 4px; }
    .wrong-ans { color: #dc3545; font-weight: bold; background: #ffe6e6; padding: 2px 5px; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

# Fungsi untuk memuat soal dari JSON
def load_exam(file_name, title, duration_minutes):
    filepath = os.path.join("data", file_name)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            st.session_state.exam_data = json.load(f)
        
        # Atur state untuk memulai ujian
        st.session_state.exam_title = title
        st.session_state.end_time = time.time() + (duration_minutes * 60)
        st.session_state.page = 'exam'
        st.session_state.current_q = 0
        st.session_state.answers = {}
        st.session_state.doubts = set()
        st.rerun()
    except FileNotFoundError:
        st.error(f"File soal {file_name} tidak ditemukan di folder data.")

# ==========================================
# HALAMAN LANDING PAGE
# ==========================================
def show_landing_page():
    st.markdown("#### 🎓 Uji Coba Tes CPNS")
    st.divider()
    st.title("Selamat Datang.")
    st.markdown("Silakan pilih modul ujian yang tersedia di bawah ini.")
    st.write("") 

    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.markdown("<div style='padding-top: 10px;font-weight: bold;'>TWK NASIONALISME 1</div>", unsafe_allow_html=True)
            st.markdown("<small><br>⏱️ 30 Menit<br>📝 30 Soal<br></small>", unsafe_allow_html=True)
            st.write("")
            if st.button("Mulai Ujian", key="twk_1"):
                load_exam("twk_1.json", "Tes Wawasan Kebangsaan - Nasionalisme 1", 30)
    with col2:
        with st.container(border=True):
            st.markdown("<div style='padding-top: 10px;font-weight: bold;'>TWK NASIONALISME 2</div>", unsafe_allow_html=True)
            st.markdown("<small><br>⏱️ 30 Menit<br>📝 30 Soal<br></small>", unsafe_allow_html=True)
            st.write("")
            if st.button("Mulai Ujian", key="twk_2"):
                load_exam("twk_2.json", "Tes Wawasan Kebangsaan - Nasionalisme 2", 30)

# ==========================================
# HALAMAN UJIAN
# ==========================================
def show_exam_page():
    questions = st.session_state.exam_data
    total_q = len(questions)
    
    if total_q == 0:
        st.error("Data ujian kosong.")
        return

    # --- CSS KHUSUS HALAMAN UJIAN ---
    st.markdown(f"""
        <style>
        /* 1. RESET STYLE TOMBOL SIDEBAR */
        [data-testid="stSidebar"] div.stButton > button {{
            width: 100%;
            border-radius: 4px;       
            height: 30px;             
            padding: 0px;
            font-size: 13px;          
            line-height: 30px;
            margin: 0px;              
            transition: all 0.2s ease-in-out;
            border: 1px solid transparent; 
        }}
        
        /* 2. MENGATUR JARAK ANTAR KOLOM (HORIZONTAL) */
        /* Memaksa gap antar kolom menjadi sangat kecil (2px) */
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {{
            gap: 6px !important;
        }}

        /* Mengatur padding di dalam kolom agar tidak memakan tempat */
        [data-testid="stSidebar"] [data-testid="column"] {{
            padding: 0 !important;
            min-width: 0 !important;
            flex: 1 1 auto !important;
        }}

        /* 3. MENGATUR JARAK ANTAR BARIS (VERTIKAL) */
        /* Mengurangi jarak vertikal antar elemen button */
        [data-testid="stSidebar"] .stElementContainer {{
            margin-bottom: 3px !important; /* Jarak antar baris atas-bawah */
        }}

        /* 4. LOGIKA WARNA STATUS */
        [data-testid="stSidebar"] button[kind="secondary"] {{
            background-color: #f8f9fa !important;
            color: #31333F !important;
            border: 1px solid #dce0e6 !important;
        }}
        [data-testid="stSidebar"] button[kind="secondary"]:hover {{
            background-color: #e2e6ea !important;
            border-color: #adb5bd !important;
            color: #000000 !important;
        }}
        [data-testid="stSidebar"] button[kind="primary"] {{
            background-color: #00BFFF !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }}
        [data-testid="stSidebar"] button[kind="primary"]:hover {{
            background-color: #009ACD !important; 
            color: white !important;
        }}
        </style>
    """, unsafe_allow_html=True)

    # --- PANEL NAVIGASI SOAL ---
    st.sidebar.markdown("### 📋 Navigasi Soal")
    st.sidebar.caption("🟦 : Sudah | ⬜ : Belum")
    
    grid_cols = st.sidebar.columns(5)
    for i in range(total_q):
        is_answered = str(i) in st.session_state.answers
        
        btn_type = "primary" if is_answered else "secondary"
        label = f"{i+1}"
        
        # Masukkan tombol ke kolom yang sesuai secara berurutan
        with grid_cols[i % 5]:
            if st.button(label, key=f"nav_{i}", type=btn_type, use_container_width=True):
                st.session_state.current_q = i
                st.rerun()

    curr_num = st.session_state.current_q + 1
    components.html(
        f"""
        <script>
            // Tunggu sebentar agar elemen sidebar termuat sempurna
            setTimeout(function() {{
                const buttons = window.parent.document.querySelectorAll('[data-testid="stSidebar"] button');
                const currentNum = "{curr_num}";

                buttons.forEach(btn => {{
                    // 1. RESET: Hapus style custom dari SEMUA tombol sidebar
                    // Ini penting agar tombol yang TIDAK aktif kembali ke warna aslinya (Biru/Abu)
                    btn.style.removeProperty('border');
                    btn.style.removeProperty('background-color');
                    btn.style.removeProperty('color');
                    btn.style.removeProperty('font-weight');
                    btn.style.removeProperty('transform');
                    btn.style.removeProperty('box-shadow');

                    // 2. CEK & HIGHLIGHT: Warnai HANYA tombol yang sesuai nomor sekarang
                    if (btn.innerText.trim() === currentNum) {{
                        btn.style.setProperty('border', '2px solid #00BFFF', 'important');
                        btn.style.setProperty('background-color', '#f5f5ff', 'important');
                        btn.style.setProperty('color', '#00BFFF', 'important');
                        btn.style.setProperty('font-weight', 'bold', 'important');
                        btn.style.setProperty('transform', 'scale(1.1)', 'important');
                        btn.style.setProperty('box-shadow', '0px 2px 5px rgba(0,0,0,0.2)', 'important');
                    }}
                }});
            }}, 100); // Delay 100ms untuk memastikan sinkronisasi
        </script>
        """,
        height=0
    )

    st.sidebar.divider()
    if st.sidebar.button("Kumpulkan Ujian", key="sidebar_finish", type="primary", use_container_width=True):
        st.session_state.page = 'result'
        st.rerun()

    # --- BAGIAN ATAS (STICKY HEADER & TIMER) ---
    time_left = int(st.session_state.end_time - time.time())
    
    st.markdown(f"""
        <div class="sticky-header">
            <div style="font-weight: bold; font-size: 18px; color: #0B192C;">Ujian: {st.session_state.exam_title}</div>
            <div id="timer_display" style="font-size: 20px; font-weight: bold; color: #F2613F;">⏱️ Menghitung...</div>
        </div>
    """, unsafe_allow_html=True)
    
    components.html(f"""
        <script>
            var timeLeft = {time_left};
            var timerDisplay = window.parent.document.getElementById("timer_display");
            if (timerDisplay) {{
                var timerId = setInterval(function() {{
                    if (timeLeft <= 0) {{
                        clearInterval(timerId);
                        timerDisplay.innerHTML = "WAKTU HABIS";
                        window.parent.location.reload();
                    }} else {{
                        var m = Math.floor(timeLeft / 60);
                        var s = timeLeft % 60;
                        m = m < 10 ? "0" + m : m;
                        s = s < 10 ? "0" + s : s;
                        timerDisplay.innerHTML = "⏱️ " + m + ":" + s;
                        timeLeft--;
                    }}
                }}, 1000);
            }}
        </script>
    """, height=0)

    if time_left <= 0:
        st.warning("Waktu Anda telah habis! Ujian otomatis dikumpulkan.")
        st.session_state.page = 'result'
        time.sleep(2)
        st.rerun()

    # --- AREA KONTEN UTAMA ---
    curr = st.session_state.current_q
    q_data = questions[curr]

    st.markdown(f"**Soal {curr + 1} dari {total_q}** ")
    st.markdown(f"#### {q_data['q']}")
    st.write("")

    current_answer = st.session_state.answers.get(str(curr))
    index_val = q_data['opts'].index(current_answer) if current_answer in q_data['opts'] else None

    selected = st.radio(
        "Pilih jawaban:", 
        options=q_data['opts'], 
        index=index_val, 
        key=f"radio_{curr}", 
        label_visibility="collapsed" # Menyembunyikan label "Pilih jawaban" agar bersih
    )
    
    if selected:
        st.session_state.answers[str(curr)] = selected

    st.write("")
    st.write("")

    # --- NAVIGASI BAWAH ---
    st.divider()
    col_prev, col_next = st.columns([1, 1])

    with col_prev:
        if curr > 0:
            if st.button("**Sebelumnya** ", use_container_width=True): 
                st.session_state.current_q -= 1
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    with col_next:
        if curr < total_q - 1:
            if st.button("**Selanjutnya** ", use_container_width=True):
                st.session_state.current_q += 1
                st.rerun()
        else:
            if st.button("Kumpulkan Ujian", use_container_width=True, type="primary"): 
                st.session_state.page = 'result'
                st.rerun()

# ==========================================
# HALAMAN HASIL
# ==========================================
def show_result_page():
    questions = st.session_state.exam_data
    answers = st.session_state.answers
    
    correct_count = 0
    total_q = len(questions)

    for i, q_data in enumerate(questions):
        user_ans = answers.get(str(i))
        if user_ans == q_data['answer']:
            correct_count += 1
            
    score = (correct_count / total_q) * 100 if total_q > 0 else 0

    components.html(
        """
        <script>
            window.location.hash = "#top";
        </script>
        """,
        height=0
    )
    st.title("📊 Hasil Ujian")
    st.markdown(f"### Skor Anda: **{score:.2f}**")
    st.caption(f"Benar: {correct_count} | Salah/Kosong: {total_q - correct_count} | Total Soal: {total_q}")
    st.divider()

    st.markdown("### Pembahasan Soal")
    
    for i, q_data in enumerate(questions):
        user_ans = answers.get(str(i), "Tidak dijawab")
        correct_ans = q_data['answer']
        is_correct = user_ans == correct_ans

        with st.expander(f"Soal {i+1} - {'✅ Benar' if is_correct else '❌ Salah'}"):
            st.markdown(f"**Pertanyaan:** {q_data['q']}")
            
            if is_correct:
                st.markdown(f"Jawaban Anda: <span class='correct-ans'>{user_ans}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"Jawaban Anda: <span class='wrong-ans'>{user_ans}</span>", unsafe_allow_html=True)
                st.markdown(f"Jawaban Benar: <span class='correct-ans'>{correct_ans}</span>", unsafe_allow_html=True)
            
            st.info(f"**Penjelasan:**\n{q_data.get('explanation', 'Tidak ada penjelasan tersedia.')}")
            

    st.write("")
    if st.button("Kembali ke Beranda"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ==========================================
# ROUTING HALAMAN
# ==========================================
if st.session_state.page == 'landing':
    show_landing_page()
elif st.session_state.page == 'exam':
    show_exam_page()
elif st.session_state.page == 'result':
    show_result_page()