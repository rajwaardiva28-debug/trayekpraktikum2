import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ==========================================
# 1. INISIALISASI & FUNGSI NAVIGASI
# ==========================================

if "page" not in st.session_state:
    st.session_state.page = "page1"

def go_to_page():
    # Pastikan session state terisi sebelum pindah
    if st.session_state.pilihan == "LKD":
        st.session_state.page = "page2"
    elif st.session_state.pilihan == "LFD":
        st.session_state.page = "page3"

def pilih_modul(modul):
    st.session_state.page = f"modul_{modul}"

# ==========================================
# 2. HALAMAN 1 (HOME / LOGIN)
# ==========================================

if st.session_state.page == "page1":
    st.title("Trayek Praktikum")
    st.write("Selamat Praktikum!")

    input_NIM = st.text_input("Masukkan NIM: ", key="input_nim")
    pilihan_praktikum = ["LKD", "LFD"]

    # Selectbox menyimpan langsung ke st.session_state.pilihan
    st.selectbox(
        "Praktikum yang akan dilakukan:",
        pilihan_praktikum,
        key="pilihan"
    )

    st.button("Enter", on_click=go_to_page)

# ==========================================
# 3. HALAMAN 2 (MENU LKD)
# ==========================================

elif st.session_state.page == "page2":
    st.title("Praktikum LKD")
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
    nim_cari = st.session_state.get("input_nim", "").strip()

    if not nim_cari:
        st.warning("Silakan masukkan NIM di halaman awal.")
    else:
        try:
            # --- BAGIAN PERBAIKAN PEMBACAAN CSV ---
            # 1. Baca CSV
            df = pd.read_csv("Sebaran_LFD_FTI.csv")
            
            # 2. BERSIHKAN NAMA KOLOM (Hapus spasi di depan/belakang nama kolom)
            # Ini mengatasi error jika nama kolom adalah " NAMA" atau "Grup "
            df.columns = df.columns.str.strip()
            
            # 3. Pastikan NIM dibaca sebagai string
            df['NIM'] = df['NIM'].astype(str)
            
            # --- DEBUGGING (Tampilkan jika kolom tidak ditemukan) ---
            if 'NAMA' not in df.columns or 'Grup' not in df.columns:
                st.error("Terjadi kesalahan nama kolom di CSV.")
                st.write("Nama kolom yang terbaca oleh sistem:")
                st.write(df.columns.tolist())
                st.stop() # Hentikan program agar tidak crash

            # 4. Cari Mahasiswa
            student_data = df[df['NIM'] == nim_cari]

            if not student_data.empty:
                # Ambil Data
                nama_mhs = student_data.iloc[0]['NAMA']
                grup_mhs = student_data.iloc[0]['Grup']
                
                st.success(f"Mahasiswa ditemukan: **{nama_mhs}**")
                col_info1, col_info2 = st.columns(2)
                with col_info1: st.write(f"**NIM:** {nim_cari}")
                with col_info2: st.info(f"**Grup:** {grup_mhs}")
                
                st.subheader("Jadwal & Modul Praktikum")

                # Kolom tanggal sesuai file FTI
                date_cols = ["29/09", "13/10", "27/10", "11-Oct"]
                
                cols = st.columns(len(date_cols))
                
                for i, date_col in enumerate(date_cols):
                    with cols[i]:
                        st.markdown(f"**{date_col}**") 
                        
                        # Pastikan nama kolom tanggal juga bersih dari spasi
                        col_name_clean = date_col.strip()

                        if col_name_clean in df.columns:
                            kode_modul = student_data.iloc[0][col_name_clean]
                            
                            if pd.notna(kode_modul):
                                st.write(f"Kode: `{kode_modul}`")
                                try:
                                    # Ambil angka (M01 -> 1)
                                    nomor_modul_int = int(''.join(filter(str.isdigit, str(kode_modul))))
                                    
                                    st.button(
                                        f"Buka {kode_modul}", 
                                        key=f"btn_{col_name_clean}",
                                        on_click=lambda m=nomor_modul_int: pilih_modul(m)
                                    )
                                except ValueError:
                                    st.caption("-") 
                            else:
                                st.caption("Kosong")
                        else:
                            st.caption("Jadwal Tdk Ada")
            else:
                st.error(f"NIM {nim_cari} tidak ditemukan.")
                st.write("Pastikan NIM yang dimasukkan sesuai dengan yang ada di File CSV.")

        except FileNotFoundError:
            st.error("File 'Sebaran_LFD_FTI.csv' tidak ditemukan di folder yang sama.")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

    st.write("---")
    st.button("⬅️ Kembali ke halaman awal", on_click=lambda: st.session_state.update(page="page1"))

# ==========================================
# 5. HALAMAN DETAIL MODUL (KONTEN)
# ==========================================

elif st.session_state.page.startswith("modul_"):
    nomor_modul = st.session_state.page.split("_")[1]

    func_kembali = lambda: st.session_state.update(page="page3")
    label_kembali = "⬅️ Kembali ke Menu LFD"

    # --- KONTEN MODUL 1 ---
    if nomor_modul == "1":
        
        # JIKA PILIHAN LFD (FISIKA)
        if st.session_state.pilihan == "LFD":
            st.title("Modul 01 – Dasar Pengukuran (LFD)")
            st.markdown("### Praktikum Fisika Dasar")
            
            tab1, tab2 = st.tabs(["📄 File Modul", "📝 Tugas Pendahuluan"])
            
            with tab1:
                st.write("**Modul Praktikum**")
                FILE_ID_LFD = "1f8bEu46KVdLVC_pZjucA7H-dtIyj09Us" 
                components.html(
                    f'<iframe src="https://drive.google.com/file/d/{FILE_ID_LFD}/preview" width="100%" height="600"></iframe>',
                    height=600,
                )
            
            with tab2:
                st.write("**Tugas Pendahuluan (TP)**")
                st.info("Kerjakan soal berikut sebelum praktikum dimulai.")
                FILE_ID_TP = "1wSQZtgceUIY-HjzbWspSWlK8KkViBtkG" 
                components.html(
                    f'<iframe src="https://drive.google.com/embeddedfolderview?id={FILE_ID_TP}" width="100%" height="400"></iframe>',
                    height=400,
                )

        # JIKA PILIHAN LKD (KIMIA)
        else:
            st.title(f"Modul 2 ({st.session_state.pilihan})")

    # --- MODUL 2, DST ---
    elif nomor_modul == "2":
        st.title(f"Modul 2 ({st.session_state.pilihan})")
        st.write("Konten belum tersedia.")

    else:
        st.title(f"Modul {nomor_modul}")
        st.write("Konten modul ini belum tersedia.")

    st.write("---")
    st.button(label_kembali, on_click=func_kembali)
