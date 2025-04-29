import streamlit as st
import pyrebase
from datetime import datetime

# ----------------- KONFIGURASI FIREBASE -----------------
firebase_config = {
    "apiKey": "AIzaSyBzQWJl7_DV7vhLc4lxqgWQeTmYu0e1b3g",
    "authDomain": "studygram-31834.firebaseapp.com",
    "databaseURL": "https://studygram-31834-default-rtdb.firebaseio.com",
    "projectId": "studygram-31834",
    "storageBucket": "studygram-31834.appspot.com",
    "messagingSenderId": "1010209551377",
    "appId": "1:1010209551377:web:e100fc3a20d6ee2f5cadb0",
    "measurementId": "G-P7PJBZ2HGV"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

# ----------------- FUNGSI AUTENTIKASI -----------------
def signup_user(email, password, username):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        db.child("users").child(user['localId']).set({
            "email": email,
            "username": username,
            "join_date": datetime.now().isoformat()
        })
        return True, "✅ Signup berhasil! Silakan login."
    except Exception as e:
        error_message = str(e)
        if "EMAIL_EXISTS" in error_message:
            return False, "❌ Email sudah terdaftar."
        elif "WEAK_PASSWORD" in error_message:
            return False, "❌ Password terlalu lemah (minimal 6 karakter)."
        return False, f"❌ Error: {error_message}"

def login_user(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        # Dapatkan data user langsung menggunakan UID
        user_info = db.child("users").child(user['localId']).get().val()
        
        if user_info:
            return True, {
                "user": user,
                "user_id": user['localId'],
                "username": user_info.get("username", email.split('@')[0]),
                "email": email
            }
        return False, "❌ Data pengguna tidak ditemukan."
    except Exception as e:
        error_message = str(e)
        if "INVALID_PASSWORD" in error_message:
            return False, "❌ Password salah."
        elif "EMAIL_NOT_FOUND" in error_message:
            return False, "❌ Email tidak terdaftar."
        return False, f"❌ Error: {error_message}"

def logout_user():
    st.session_state.clear()
    st.rerun()

# ----------------- FUNGSI POSTING -----------------
def tambah_post(username, post_text, mata_pelajaran):
    timestamp = datetime.now().isoformat()
    data = {
        "username": username,
        "post": post_text,
        "mata_pelajaran": mata_pelajaran,
        "likes": 0,
        "timestamp": timestamp,
        "replies": {}
    }
    try:
        db.child("posts").push(data)
        return True, "✅ Post berhasil dikirim!"
    except Exception as e:
        return False, f"❌ Gagal mengirim post: {str(e)}"

def tambah_balasan(post_id, username, balasan_text):
    timestamp = datetime.now().isoformat()
    data = {
        "username": username,
        "balasan": balasan_text,
        "timestamp": timestamp
    }
    try:
        db.child("posts").child(post_id).child("replies").push(data)
        return True, "✅ Balasan berhasil dikirim!"
    except Exception as e:
        return False, f"❌ Gagal mengirim balasan: {str(e)}"

# ----------------- FUNGSI ALAT BANTU -----------------
def tampilkan_alat_bantu(mata_pelajaran):
    st.subheader("🔧 Alat Bantu")
    if mata_pelajaran == "Matematika":
        st.markdown("""
        ### 📐 Rumus Matematika
        - **Luas Persegi**: `s × s`
        - **Luas Segitiga**: `½ × alas × tinggi`
        - **Luas Lingkaran**: `π × r²`
        - **Keliling Lingkaran**: `2 × π × r`
        - **Pythagoras**: `a² + b² = c²`
        """)
        st.markdown("""
        ### 🧮 Kalkulator Online
        - [Kalkulator Sederhana](https://www.calculator.net/)
        - [Kalkulator Ilmiah](https://www.desmos.com/scientific)
        """)

    elif mata_pelajaran == "Fisika":
        st.markdown("""
        ### ⚙️ Rumus Fisika
        - **Hukum Newton II**: `F = m × a`
        - **Energi Kinetik**: `Ek = ½ × m × v²`
        - **Energi Potensial**: `Ep = m × g × h`
        - **Kecepatan**: `v = s / t`
        """)
        st.markdown("""
        ### 🧮 Kalkulator Fisika
        - [Kalkulator Fisika](https://www.omnicalculator.com/physics)
        """)

    elif mata_pelajaran == "Kimia":
        st.markdown("""
        ### 🧪 Tabel Periodik
        - [Klik di sini untuk melihat tabel periodik interaktif](https://ptable.com/)
        """)
        st.markdown("""
        ### 🔬 Alat Bantu Kimia
        - [Kalkulator Kimia](https://www.webqc.org/balance.php)
        """)

    elif mata_pelajaran == "Biologi":
        st.markdown("""
        ### 🌱 Anatomi Tubuh Manusia
        - **Sistem Pernapasan**: Hidung → Tenggorokan → Paru-paru
        - **Sistem Pencernaan**: Mulut → Kerongkongan → Lambung → Usus
        """)
        st.markdown("""
        ### 🔬 Referensi Biologi
        - [Khan Academy - Biologi](https://www.khanacademy.org/science/biology)
        """)

    elif mata_pelajaran in ["Bahasa Inggris", "Bahasa Indonesia"]:
        st.markdown("""
        ### 📖 Kamus
        - [Kamus Bahasa Inggris](https://translate.google.com/)
        - [Kamus Besar Bahasa Indonesia (KBBI)](https://kbbi.kemdikbud.go.id/)
        """)
        st.markdown("""
        ### 🌐 Translate
        - [Google Translate](https://translate.google.com/)
        - [DeepL Translator](https://www.deepl.com/translator)
        """)

    elif mata_pelajaran == "Sejarah":
        st.markdown("""
        ### 📜 Kronologi Sejarah
        - **Perang Dunia I**: 1914 - 1918
        - **Proklamasi Kemerdekaan Indonesia**: 17 Agustus 1945
        - **Revolusi Industri**: Abad ke-18
        """)
        st.markdown("""
        ### 📚 Referensi Sejarah
        - [Wikipedia - Sejarah Dunia](https://en.wikipedia.org/wiki/History)
        """)

    elif mata_pelajaran == "Geografi":
        st.markdown("""
        ### 🗺️ Peta Dunia
        - [Google Maps](https://maps.google.com/)
        - [Peta Interaktif](https://www.nationalgeographic.org/maps/)
        """)
        st.markdown("""
        ### 🌍 Alat Bantu Geografi
        - [Kalkulator Koordinat](https://www.gps-coordinates.net/)
        """)

    elif mata_pelajaran == "Ekonomi":
        st.markdown("""
        ### 💰 Rumus Ekonomi
        - **Pendapatan Nasional**: `Y = C + I + G + (X - M)`
        - **Elastisitas Permintaan**: `Ed = (%ΔQ) / (%ΔP)`
        """)
        st.markdown("""
        ### 📊 Alat Bantu Ekonomi
        - [Kalkulator Keuangan](https://www.calculator.net/financial-calculator.html)
        """)

    elif mata_pelajaran == "Informatika":
        st.markdown("""
        ### 💻 Alat Bantu Pemrograman
        - [Python Documentation](https://docs.python.org/3/)
        - [W3Schools](https://www.w3schools.com/)
        - [GeeksforGeeks](https://www.geeksforgeeks.org/)
        """)
        st.markdown("""
        ### 🛠️ Tools Online
        - [Replit - Online IDE](https://replit.com/)
        - [JSON Formatter](https://jsonformatter.org/)
        """)

# ----------------- SETUP LAYOUT -----------------
st.set_page_config(page_title="Talk And Learn", page_icon="📚", layout="wide")

# ----------------- SESSION INIT -----------------
if "user" not in st.session_state:
    st.session_state.user = None
    st.session_state.page = "login"

# ----------------- AUTO REDIRECT -----------------
if st.session_state.user and st.session_state.page == "login":
    st.session_state.page = "diskusi"
    st.rerun()

# ----------------- LOGIN/SIGNUP PAGE -----------------
if st.session_state.page == "login":
    st.title("📚 Talk And Learn")
    st.subheader("Platform Kolaborasi Belajar Digital untuk Pelajar Indonesia")

    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            submit_login = st.form_submit_button("Login")
            
            if submit_login:
                with st.spinner("Sedang memproses login..."):
                    success, result = login_user(email, password)
                    if success:
                        st.session_state.update(result)
                        st.session_state.page = "diskusi"
                        st.success("Login berhasil!")
                        st.rerun()
                    else:
                        st.error(result)

    with tab2:
        with st.form("signup_form"):
            email = st.text_input("Email", key="signup_email")
            username = st.text_input("Username", key="signup_username")
            password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Konfirmasi Password", type="password", key="signup_confirm_password")
            submit_signup = st.form_submit_button("Signup")
            
            if submit_signup:
                if password == confirm_password:
                    with st.spinner("Mendaftarkan akun..."):
                        success, message = signup_user(email, password, username)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                else:
                    st.error("Password tidak cocok!")

# ----------------- DISKUSI PAGE -----------------
elif st.session_state.page == "diskusi":
    st.sidebar.title(f"👋 Halo, {st.session_state['username']}!")
    
    # Pilihan mata pelajaran
    mata_pelajaran = st.sidebar.selectbox(
        "Pilih Mata Pelajaran:",
        ["Matematika", "Fisika", "Kimia", "Biologi", "Bahasa Inggris",
         "Bahasa Indonesia", "Sejarah", "Geografi", "Ekonomi", "Informatika"],
        key="mata_pelajaran_select"
    )
    
    if st.sidebar.button("🚪 Logout"):
        logout_user()

    st.title(f"📚 Diskusi {mata_pelajaran}")
    
    # Tampilkan alat bantu
    tampilkan_alat_bantu(mata_pelajaran)
    
    # Form posting baru
    with st.expander("✏️ Buat Posting Baru", expanded=True):
        with st.form("new_post_form"):
            post_text = st.text_area("Apa yang ingin Anda tanyakan atau bagikan?", height=150)
            submit_post = st.form_submit_button("Posting")
            
            if submit_post and post_text.strip():
                with st.spinner("Mengunggah posting..."):
                    success, message = tambah_post(st.session_state['username'], post_text, mata_pelajaran)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
            elif submit_post:
                st.warning("Isi posting tidak boleh kosong!")

    # ----------------- CUSTOM CSS -----------------
    st.markdown("""
    <style>
    /* Gaya untuk diskusi publik */
    .post-container {
        background-color: #2c2f33; /* Warna latar belakang gelap */
        color: #ffffff; /* Warna teks putih */
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .post-container h4 {
        color: #4CAF50; /* Warna hijau untuk nama pengguna */
        margin: 0;
    }
    .post-container small {
        color: #b0b3b8; /* Warna abu-abu terang untuk timestamp */
    }
    .post-container p {
        margin: 10px 0;
        color: #ffffff; /* Warna teks putih */
    }
    .reply-container {
        background-color: #23272a; /* Warna latar belakang lebih gelap untuk balasan */
        color: #ffffff; /* Warna teks putih */
        padding: 10px;
        border-left: 3px solid #4CAF50; /* Garis hijau di sebelah kiri */
        margin-bottom: 10px;
        border-radius: 5px;
    }
    .reply-container strong {
        color: #4CAF50; /* Warna hijau untuk nama pengguna */
    }
    .reply-container small {
        color: #b0b3b8; /* Warna abu-abu terang untuk timestamp */
    }
    </style>
    """, unsafe_allow_html=True)

    # ----------------- MENAMPILKAN POSTINGAN -----------------
    try:
        posts = db.child("posts").order_by_child("mata_pelajaran").equal_to(mata_pelajaran).get().val()
        
        if not posts:
            st.info("Belum ada diskusi di mata pelajaran ini. Jadilah yang pertama memulai!")
        else:
            for post_id, post_data in sorted(posts.items(), key=lambda x: x[1]['timestamp'], reverse=True):
                with st.container():
                    # Menampilkan postingan
                    st.markdown(f"""
                    <div class="post-container">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h4>👤 {post_data['username']}</h4>
                            <small>🕒 {datetime.fromisoformat(post_data['timestamp']).strftime('%d %b %Y %H:%M')}</small>
                        </div>
                        <p>{post_data['post']}</p>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span>❤️ {post_data.get('likes', 0)} Likes</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Tombol untuk memberi "like"
                    if st.button(f"👍 Like", key=f"like_{post_id}"):
                        try:
                            current_likes = post_data.get("likes", 0)
                            db.child("posts").child(post_id).update({"likes": current_likes + 1})
                            # Memicu pembaruan halaman dengan mengubah nilai session state
                            st.session_state.page = "diskusi"
                        except Exception as e:
                            st.error(f"Gagal memberikan like: {str(e)}")
                    
                    # Menampilkan balasan
                    replies = post_data.get("replies", {})
                    if replies:
                        with st.expander(f"💬 Balasan ({len(replies)})"):
                            for reply_id, reply_data in replies.items():
                                st.markdown(f"""
                                <div class="reply-container">
                                    <strong>{reply_data['username']}</strong>
                                    <p>{reply_data['balasan']}</p>
                                    <small>{datetime.fromisoformat(reply_data['timestamp']).strftime('%d %b %Y %H:%M')}</small>
                                </div>
                                """, unsafe_allow_html=True)
                    
                    # Form untuk menambahkan balasan
                    with st.expander("Tulis Balasan"):
                        with st.form(f"reply_form_{post_id}"):
                            reply_text = st.text_area("Balasan Anda", key=f"reply_text_{post_id}")
                            submit_reply = st.form_submit_button("Kirim Balasan")
                            if submit_reply:
                                if reply_text.strip():
                                    success, message = tambah_balasan(post_id, st.session_state['username'], reply_text)
                                    if success:
                                        st.success(message)
                                        # Memicu pembaruan halaman dengan mengubah nilai session state
                                        st.session_state.page = "diskusi"
                                    else:
                                        st.error(message)
                                else:
                                    st.warning("Balasan tidak boleh kosong!")
    except Exception as e:
        st.error(f"Gagal memuat diskusi: {str(e)}")