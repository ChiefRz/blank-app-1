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
if 'doubts' not in st.session_state:
    st.session_state.doubts = set()
if 'exam_data' not in st.session_state:
    st.session_state.exam_data = []
if 'end_time' not in st.session_state:
    st.session_state.end_time = None
if 'exam_title' not in st.session_state:
    st.session_state.exam_title = ""
if 'scroll_to_top' not in st.session_state:
    st.session_state.scroll_to_top = False

# 3. CSS Kustom 
st.markdown("""
    <style>
    div.stButton > button:first-child { background-color: #00BFFF; color: white; width: 100%; border: none; border-radius: 6px; font-weight: bold; }
    div.stButton > button:first-child:hover { background-color: #1E90FF; color: white; }
    .nav-btn > button:first-child { background-color: #F8F9FA; color: #333; border: 1px solid #DDD; }
    .nav-btn > button:first-child:hover { background-color: #E2E6EA; color: black; }
    div.row-widget.stRadio > div { flex-direction: column; gap: 10px; }
    div.row-widget.stRadio > div > label { border: 1px solid #E2E6EA; padding: 15px 20px; border-radius: 8px; background-color: #FFFFFF; cursor: pointer; transition: all 0.2s ease-in-out; }
    div.row-widget.stRadio > div > label:hover { border-color: #00BFFF; background-color: #F0F8FF; }
    .sticky-header { position: sticky; top: 0; background: white; z-index: 999; padding: 15px 0; border-bottom: 1px solid #EEE; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;}
    .correct-ans { color: #28a745; font-weight: bold; }
    .wrong-ans { color: #dc3545; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

if st.session_state.scroll_to_top:
    scroll_js = """
    <script>
        const parentDoc = window.parent.document;
        // Mencari semua kemungkinan container scroll di Streamlit dan memaksanya ke posisi 0
        const containers = parentDoc.querySelectorAll('.main, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"]');
        containers.forEach(container => {
            container.scrollTop = 0;
        });
        parentDoc.documentElement.scrollTop = 0;
        parentDoc.body.scrollTop = 0;
    </script>
    """
    components.html(scroll_js, height=0)
    st.session_state.scroll_to_top = False

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
    st.markdown("Silakan pilih modul ujian yang tersedia di bawah ini. Pastikan koneksi internet Anda stabil sebelum memulai.")
    st.write("") 

    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.markdown("<div style='padding-top: 10px;font-weight: bold;'>TWK 1</div>", unsafe_allow_html=True)
            st.markdown("<small><br>⏱️ 30 Menit<br>📝 30 Soal<br></small>", unsafe_allow_html=True)
            st.write("")
            if st.button("Mulai Ujian", key="twk_1"):
                st.session_state.scroll_to_top = True 
                # Panggil fungsi load_exam (nama file, judul, durasi dalam menit)
                load_exam("twk_1.json", "Tes Wawasan Kebangsaan 1", 30)
    with col2:
        with st.container(border=True):
            st.markdown("<div style='padding-top: 10px;font-weight: bold;'>TWK 2</div>", unsafe_allow_html=True)
            st.markdown("<small><br>⏱️ 30 Menit<br>📝 30 Soal<br></small>", unsafe_allow_html=True)
            st.write("")
            if st.button("Mulai Ujian", key="twk_2"):
                st.session_state.scroll_to_top = True 
                # Panggil fungsi load_exam (nama file, judul, durasi dalam menit)
                load_exam("twk_2.json", "Tes Wawasan Kebangsaan 2", 30)

# ==========================================
# HALAMAN UJIAN
# ==========================================
def show_exam_page():
    questions = st.session_state.exam_data
    total_q = len(questions)
    
    # Keamanan jika data kosong
    if total_q == 0:
        st.error("Data ujian kosong.")
        return

    # --- PANEL NAVIGASI SOAL (SIDEBAR) ---
    st.sidebar.markdown("### 📋 Navigasi Soal")
    st.sidebar.markdown("<small>⬜ Belum | 🟦 Sudah</small>", unsafe_allow_html=True)
    st.sidebar.write("")
    
    cols = st.sidebar.columns(5)
    for i in range(total_q):
        # Menyederhanakan logika: hanya mengecek apakah sudah dijawab atau belum
        status = "🟦" if str(i) in st.session_state.answers else "⬜"
        
        with cols[i % 5]:
            if st.button(f"{i+1}\n{status}", key=f"nav_{i}"):
                st.session_state.current_q = i
                st.session_state.scroll_to_top = True 
                st.rerun()

    # --- BAGIAN ATAS (STICKY HEADER & TIMER) ---
    # Menggunakan JavaScript untuk visual timer yang berjalan mundur
    time_left = int(st.session_state.end_time - time.time())
    
    # 1. Tampilkan UI Header (Tetap gunakan st.markdown untuk layout)
    st.markdown(f"""
        <div class="sticky-header">
            <div style="font-weight: bold; font-size: 18px; color: #0B192C;">Ujian: {st.session_state.exam_title}</div>
            <div id="timer_display" style="font-size: 20px; font-weight: bold; color: #F2613F;">⏱️ Menghitung...</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 2. Jalankan Skrip Timer menggunakan st.components.v1.html
    # Height disetel 0 agar iframe tidak memakan tempat (tersembunyi)
    components.html(f"""
        <script>
            var timeLeft = {time_left};
            // Gunakan window.parent.document untuk menargetkan elemen di luar iframe komponen
            var timerDisplay = window.parent.document.getElementById("timer_display");
            
            if (timerDisplay) {{
                var timerId = setInterval(function() {{
                    if (timeLeft <= 0) {{
                        clearInterval(timerId);
                        timerDisplay.innerHTML = "WAKTU HABIS";
                        
                        // Opsional: Paksa refresh otomatis saat waktu habis
                        // agar Python backend segera memproses pengumpulan ujian
                        window.parent.location.reload();
                    }} else {{
                        var m = Math.floor(timeLeft / 60);
                        var s = timeLeft % 60;
                        
                        // Tambahkan angka 0 di depan jika waktu di bawah 10 (misal: 09:05)
                        m = m < 10 ? "0" + m : m;
                        s = s < 10 ? "0" + s : s;
                        
                        timerDisplay.innerHTML = "⏱️ " + m + ":" + s;
                        timeLeft--;
                    }}
                }}, 1000);
            }}
        </script>
    """, height=0)

    # 3. Cek jika waktu habis dari sisi Python
    if time_left <= 0:
        st.warning("Waktu Anda telah habis! Ujian otomatis dikumpulkan.")
        st.session_state.page = 'result'
        time.sleep(2)
        st.rerun()

    # --- AREA KONTEN UTAMA ---
    curr = st.session_state.current_q
    q_data = questions[curr]

    st.caption(f"Soal {curr + 1} dari {total_q}")
    st.markdown(f"#### {q_data['q']}")
    st.write("")

    current_answer = st.session_state.answers.get(str(curr))
    index_val = q_data['opts'].index(current_answer) if current_answer in q_data['opts'] else None

    selected = st.radio("Pilih jawaban:", options=q_data['opts'], index=index_val, key=f"radio_{curr}", label_visibility="collapsed")
    
    if selected:
        st.session_state.answers[str(curr)] = selected

    st.write("")
    st.write("")

    # --- NAVIGASI BAWAH (FOOTER KONTROL) ---
    st.divider()
    col_prev, col_next = st.columns([1, 1])

    with col_prev:
        if curr > 0:
            if st.button("⬅️ Sebelumnya", use_container_width=True):
                st.session_state.scroll_to_top = True 
                st.session_state.current_q -= 1
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    with col_next:
        if curr < total_q - 1:
            if st.button("Selanjutnya ➡️", use_container_width=True):
                st.session_state.scroll_to_top = True 
                st.session_state.current_q += 1
                st.rerun()
        else:
            if st.button("Kumpulkan Ujian", use_container_width=True, type="primary"):
                st.session_state.scroll_to_top = True 
                st.session_state.page = 'result'
                st.rerun()

# ==========================================
# HALAMAN HASIL & PEMBAHASAN
# ==========================================
def show_result_page():
    questions = st.session_state.exam_data
    answers = st.session_state.answers
    
    correct_count = 0
    total_q = len(questions)

    # Kalkulasi Nilai
    for i, q_data in enumerate(questions):
        user_ans = answers.get(str(i))
        if user_ans == q_data['answer']:
            correct_count += 1
            
    score = (correct_count / total_q) * 100 if total_q > 0 else 0

    st.title("📊 Hasil Ujian")
    st.markdown(f"### Skor Anda: **{score:.2f}**")
    st.caption(f"Benar: {correct_count} | Salah/Kosong: {total_q - correct_count} | Total Soal: {total_q}")
    st.divider()

    st.markdown("### Pembahasan Soal")
    
    for i, q_data in enumerate(questions):
        user_ans = answers.get(str(i), "Tidak dijawab")
        correct_ans = q_data['answer']
        is_correct = user_ans == correct_ans

        # Desain blok pembahasan
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
        st.session_state.scroll_to_top = True 
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