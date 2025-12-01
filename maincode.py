import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ==========================================
# 1. INISIALISASI & FUNGSI NAVIGASI
# ==========================================

if "page" not in st.session_state:
    st.session_state.page = "page1"

def go_to_page():
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

    pilihan_terpilih = st.selectbox(
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

    # Tombol Modul LKD
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
            # Baca File CSV
            df = pd.read_csv("Sebaran_LFD_FTI.csv")
            df['NIM'] = df['NIM'].astype(str) # Pastikan NIM string
            
            # Cari Mahasiswa
            student_data = df[df['NIM'] == nim_cari]

            if not student_data.empty:
                # Ambil Data
                nama_mhs = student_data.iloc[0]['NAMA']
                grup_mhs = student_data.iloc[0]['Grup']
                
                # Tampilkan Info Mahasiswa
                st.success(f"Mahasiswa ditemukan: **{nama_mhs}**")
                col_info1, col_info2 = st.columns(2)
                with col_info1: st.write(f"**NIM:** {nim_cari}")
                with col_info2: st.info(f"**Grup:** {grup_mhs}")
                
                st.subheader("Jadwal & Modul Praktikum")

                # Kolom tanggal yang akan dicek (15/09 diabaikan sesuai request)
                date_cols = ["29/09", "13/10", "27/10", "11-Oct"]
                
                cols = st.columns(len(date_cols))
                
                for i, date_col in enumerate(date_cols):
                    with cols[i]:
                        st.markdown(f"**{date_col}**") # Header Tanggal
                        
                        if date_col in student_data.columns:
                            kode_modul = student_data.iloc[0][date_col]
                            
                            if pd.notna(kode_modul):
                                st.write(f"Kode: `{kode_modul}`")
                                try:
                                    # Ambil angka (M01 -> 1)
                                    nomor_modul_int = int(''.join(filter(str.isdigit, str(kode_modul))))
                                    
                                    # TOMBOL KHUSUS
                                    st.button(
                                        f"Buka {kode_modul}", 
                                        key=f"btn_{date_col}",
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
                st.write("Cek kembali file CSV atau input NIM Anda.")

        except FileNotFoundError:
            st.error("File 'Sebaran_LFD_FTI.csv' belum diupload.")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

    st.write("---")
    st.button("⬅️ Kembali ke halaman awal", on_click=lambda: st.session_state.update(page="page1"))

# ==========================================
# 5. HALAMAN DETAIL MODUL (KONTEN)
# ==========================================

elif st.session_state.page.startswith("modul_"):
    nomor_modul = st.session_state.page.split("_")[1]

    # Logika Tombol Kembali (Beda tujuan LKD vs LFD)
    if st.session_state.pilihan == "LKD":
        func_kembali = lambda: st.session_state.update(page="page2")
        label_kembali = "⬅️ Kembali ke Menu LKD"
    else:
        func_kembali = lambda: st.session_state.update(page="page3")
        label_kembali = "⬅️ Kembali ke Menu LFD"

    # --- KONTEN MODUL 1 ---
    if nomor_modul == "1":
        
        # JIKA PILIHAN LFD (FISIKA)
        if st.session_state.pilihan == "LFD":
            st.title("Modul 01 – Dasar Pengukuran (LFD)")
            st.markdown("### Praktikum Fisika Dasar")
            
            # Gunakan Tab untuk memisahkan Modul dan TP
            tab1, tab2 = st.tabs(["📄 File Modul", "📝 Tugas Pendahuluan"])
            
            with tab1:
                st.write("**Modul Praktikum**")
                # ID FILE MODUL FISIKA (Ganti jika ada file khusus fisika)
                FILE_ID_LFD = "1f8bEu46KVdLVC_pZjucA7H-dtIyj09Us" 
                components.html(
                    f'<iframe src="https://drive.google.com/file/d/{FILE_ID_LFD}/preview" width="100%" height="600"></iframe>',
                    height=600,
                )
            
            with tab2:
                st.write("**Tugas Pendahuluan (TP)**")
                st.info("Kerjakan soal berikut sebelum praktikum dimulai.")
                # ID FILE TP FISIKA (Ganti dengan ID file TP Anda)
                FILE_ID_TP = "1wSQZtgceUIY-HjzbWspSWlK8KkViBtkG" 
                components.html(
                    f'<iframe src="https://drive.google.com/embeddedfolderview?id={FILE_ID_TP}" width="100%" height="400"></iframe>',
                    height=400,
                )

        # JIKA PILIHAN LKD (KIMIA - KODE LAMA)
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
            
            st.subheader("📘 Video Praktikum")
            # Contoh link video
            st.write("Video Praktikum LKD Modul 1...")

    # --- KONTEN MODUL 2 ---
    elif nomor_modul == "2":
        st.title(f"Modul 2 ({st.session_state.pilihan})")
        if st.session_state.pilihan == "LKD":
            # Konten LKD Modul 2
            st.write("Konten LKD Modul 2...")
            # Masukkan iframe LKD Modul 2 disini
        else:
            # Konten LFD Modul 2
            st.write("Konten LFD Modul 2...")

    # --- TEMPLATE MODUL LAIN ---
    else:
        st.title(f"Modul {nomor_modul}")
        st.write("Konten modul ini belum tersedia.")

    st.write("---")
    st.button(label_kembali, on_click=func_kembali)
