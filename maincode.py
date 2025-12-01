import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ==========================================
# 1. INISIALISASI & FUNGSI NAVIGASI
# ==========================================

# Inisialisasi variabel permanen agar tidak hilang saat ganti halaman
if "page" not in st.session_state:
    st.session_state.page = "page1"
if "saved_nim" not in st.session_state:
    st.session_state.saved_nim = ""
if "saved_pilihan" not in st.session_state:
    st.session_state.saved_pilihan = "LKD" # Default

def process_login():
    """
    Fungsi ini dipanggil saat tombol Enter ditekan.
    Tugasnya: Menyalin data dari Widget (yang bisa hilang) ke Variabel Permanen.
    """
    # 1. Simpan input widget ke variabel permanen
    st.session_state.saved_nim = st.session_state.widget_nim
    st.session_state.saved_pilihan = st.session_state.widget_pilihan
    
    # 2. Arahkan halaman sesuai pilihan
    if st.session_state.saved_pilihan == "LKD":
        st.session_state.page = "page2"
    elif st.session_state.saved_pilihan == "LFD":
        st.session_state.page = "page3"

def pilih_modul(modul):
    st.session_state.page = f"modul_{modul}"

# ==========================================
# 2. HALAMAN 1 (HOME / LOGIN)
# ==========================================

if st.session_state.page == "page1":
    st.title("Trayek Praktikum")
    st.write("Selamat Praktikum!")

    # Gunakan key 'widget_...' agar tidak bentrok dengan variabel simpanan
    st.text_input("Masukkan NIM: ", key="widget_nim", value=st.session_state.saved_nim)
    
    pilihan_praktikum = ["LKD", "LFD"]
    # Tentukan index default berdasarkan simpanan sebelumnya
    idx_def = 0 if st.session_state.saved_pilihan == "LKD" else 1
    
    st.selectbox(
        "Praktikum yang akan dilakukan:",
        pilihan_praktikum,
        index=idx_def,
        key="widget_pilihan"
    )

    # Panggil fungsi process_login saat diklik
    st.button("Enter", on_click=process_login)

# ==========================================
# 3. HALAMAN 2 (MENU LKD)
# ==========================================

elif st.session_state.page == "page2":
    st.title("Praktikum LKD")
    st.write(f"Login sebagai: {st.session_state.saved_nim}")
    st.write("Silakan pilih modul yang ingin kamu kerjakan:")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: st.button("Modul 1", on_click=lambda: pilih_modul(1))
    with col2: st.button("Modul 2", on_click=lambda: pilih_modul(2))
    with col3: st.button("Modul 3", on_click=lambda: pilih_modul(3))
    with col4: st.button("Modul 4", on_click=lambda: pilih_modul(4))
    with col5: st.button("Modul 5", on_click=lambda: pilih_modul(5))

    st.write("---")
    st.button("⬅️ Kembali ke halaman awal", on_click=lambda: st.session_state.update(page="page1"))

# ==========================================
# 4. HALAMAN 3 (MENU LFD - FTI)
# ==========================================

elif st.session_state.page == "page3":
    st.title("Praktikum LFD (FTI)")
    
    # Ambil NIM dari variabel permanen (saved_nim), BUKAN dari widget
    nim_cari = st.session_state.saved_nim.strip()

    if not nim_cari:
        st.warning("Silakan masukkan NIM di halaman awal.")
    else:
        try:
            # 1. Baca CSV dan bersihkan nama kolom
            df = pd.read_csv("Sebaran_LFD_FTI.csv")
            df.columns = df.columns.str.strip() # Hapus spasi rahasia di header
            df['NIM'] = df['NIM'].astype(str)
            
            # 2. Cari Mahasiswa
            student_data = df[df['NIM'] == nim_cari]

            if not student_data.empty:
                nama_mhs = student_data.iloc[0]['NAMA']
                grup_mhs = student_data.iloc[0]['Grup']
                
                st.success(f"Mahasiswa ditemukan: **{nama_mhs}**")
                col1, col2 = st.columns(2)
                with col1: st.write(f"**NIM:** {nim_cari}")
                with col2: st.info(f"**Grup:** {grup_mhs}")
                
                st.subheader("Jadwal & Modul Praktikum")

                # Kolom tanggal sesuai file FTI
                date_cols = ["29/09", "13/10", "27/10", "11-Oct"]
                
                cols = st.columns(len(date_cols))
                
                for i, date_col in enumerate(date_cols):
                    with cols[i]:
                        st.markdown(f"**{date_col}**") 
                        col_clean = date_col.strip()

                        if col_clean in df.columns:
                            kode_modul = student_data.iloc[0][col_clean]
                            
                            if pd.notna(kode_modul):
                                st.write(f"Kode: `{kode_modul}`")
                                try:
                                    # Ambil angka (M01 -> 1)
                                    nomor_modul_int = int(''.join(filter(str.isdigit, str(kode_modul))))
                                    
                                    st.button(
                                        f"Buka {kode_modul}", 
                                        key=f"btn_{col_clean}",
                                        on_click=lambda m=nomor_modul_int: pilih_modul(m)
                                    )
                                except ValueError:
                                    st.caption("-") 
                            else:
                                st.caption("Kosong")
                        else:
                            st.caption("-")
            else:
                st.error(f"NIM {nim_cari} tidak ditemukan.")
                st.write("Pastikan NIM sesuai dengan file CSV.")

        except FileNotFoundError:
            st.error("File 'Sebaran_LFD_FTI.csv' tidak ditemukan.")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

    st.write("---")
    st.button("⬅️ Kembali ke halaman awal", on_click=lambda: st.session_state.update(page="page1"))

# ==========================================
# 5. HALAMAN DETAIL MODUL (KONTEN)
# ==========================================

elif st.session_state.page.startswith("modul_"):
    nomor_modul = st.session_state.page.split("_")[1]

    # Gunakan saved_pilihan (PERMANEN), bukan key widget
    if st.session_state.saved_pilihan == "LKD":
        func_kembali = lambda: st.session_state.update(page="page2")
        label_kembali = "⬅️ Kembali ke Menu LKD"
    else:
        func_kembali = lambda: st.session_state.update(page="page3")
        label_kembali = "⬅️ Kembali ke Menu LFD"

    # --- KONTEN MODUL 1 ---
    if nomor_modul == "1":
        
        # JIKA LFD
        if st.session_state.saved_pilihan == "LFD":
            st.title("Modul 01 – Dasar Pengukuran (LFD)")
            st.markdown("### Praktikum Fisika Dasar")
            
            tab1, tab2, tab3 = st.tabs(["📄 File Modul", "📝 Tugas Pendahuluan", "Handout Praktikum"])
            
            with tab1:
                st.write("**Modul Praktikum**")
                FILE_ID_LFD = "13kA_JpbASIMrrpECbW3Ijv2DICt2CKBO" 
                components.html(
                    f'<iframe src="https://drive.google.com/file/d/{FILE_ID_LFD}/preview" width="100%" height="600"></iframe>',
                    height=600,
                )
            
            with tab2:
                st.write("**Tugas Pendahuluan (TP)**")
                st.info("Kerjakan soal berikut sebelum praktikum dimulai.")
                FILE_ID_TP = "1iOGIx1C-d9moDGba_KkjZ7v_h370ilWC" 
                components.html(
                    f'<iframe src="https://drive.google.com/file/d/{FILE_ID_TP}/preview" width="100%" height="600"></iframe>',
                    height=600,
                )

            with tab3:
                st.write("**Handout Praktikum**")
                st.info("Print handout berikut sebelum praktikum dimulai.")
                FILE_ID_HP = "177JjjxFBJOiS0EJN6JuwFo_aVy5-kXI8"
                components.html(
                f'<iframe src="https://drive.google.com/file/d/{FILE_ID_HP}/preview" width="100%" height="600"></iframe>',
                height=600,
            )
    

        # JIKA LKD
        else:
            st.title("Modul 1 – Reaksi-reaksi Kimia (LKD)")
            st.subheader("🎯 Modul Praktikum")
            FILE_ID = "1f8bEu46KVdLVC_pZjucA7H-dtIyj09Us"
            components.html(
                f'<iframe src="https://drive.google.com/file/d/{FILE_ID}/preview" width="100%" height="600"></iframe>',
                height=600,
            )
            st.subheader("Jurnal Praktikum")
            FILE_ID1 = "1wSQZtgceUIY-HjzbWspSWlK8KkViBtkG"
            components.html(
                f'<iframe src="https://drive.google.com/embeddedfolderview?id={FILE_ID1}" width="100%" height="100"></iframe>',
                height=100,
            )

    # --- MODUL LAINNYA ---
    elif nomor_modul == "2":
        st.title(f"Modul 2 ({st.session_state.saved_pilihan})")
        st.write("Konten belum tersedia.")

    else:
        st.title(f"Modul {nomor_modul}")
        st.write("Konten modul ini belum tersedia.")

    st.write("---")
    st.button(label_kembali, on_click=func_kembali)
