import streamlit as st
import pandas as pd

# Inisialisasi halaman
if "page" not in st.session_state:
    st.session_state.page = "page1"

def go_to_page():
    if st.session_state.pilihan == "LKD":
        st.session_state.page = "page2"
    elif st.session_state.pilihan == "LFD":
        st.session_state.page = "page3"

def pilih_modul(modul):
    st.session_state.page = f"modul_{modul}"

# --- HALAMAN 1 (HOME) ---
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
    
# --- HALAMAN 2 (MENU LKD) ---
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

# --- HALAMAN 3 (MENU LFD - KHUSUS FTI) ---
elif st.session_state.page == "page3":
    st.title("Praktikum LFD (FTI)")
    nim_cari = st.session_state.get("input_nim", "").strip()

    if not nim_cari:
        st.warning("Silakan masukkan NIM di halaman awal.")
    else:
        try:
            # 1. BACA FILE KHUSUS FTI
            # Tidak pakai skiprows karena header ada di baris pertama
            df = pd.read_csv("Sebaran_LFD_FTI.csv")
            
            # Pastikan kolom NIM dibaca sebagai string agar cocok
            df['NIM'] = df['NIM'].astype(str)
            
            # 2. CARI DATA MAHASISWA
            student_data = df[df['NIM'] == nim_cari]

            if not student_data.empty:
                nama_mhs = student_data.iloc[0]['NAMA']
                st.success(f"Mahasiswa ditemukan: **{nama_mhs}** (NIM: {nim_cari})")
                
                st.subheader("Jadwal & Modul Praktikum Anda")
                
                # Daftar kolom tanggal SESUAI FILE FTI
                date_cols = ["15/09", "29/09", "13/10", "27/10", "11-Oct"]
                
                cols = st.columns(len(date_cols))
                
                for i, date_col in enumerate(date_cols):
                    with cols[i]:
                        st.write(f"📅 **{date_col}**")
                        
                        if date_col in student_data.columns:
                            kode_modul = student_data.iloc[0][date_col]
                            
                            # Cek jika sel tidak kosong (NaN)
                            if pd.notna(kode_modul):
                                st.info(f"Kode: {kode_modul}")
                                
                                try:
                                    # Ambil angka dari string (contoh: "M01" -> 1)
                                    nomor_modul_int = int(''.join(filter(str.isdigit, str(kode_modul))))
                                    
                                    # Tombol untuk masuk ke modul tersebut
                                    st.button(
                                        f"Buka {kode_modul}", 
                                        key=f"btn_{date_col}",
                                        on_click=lambda m=nomor_modul_int: pilih_modul(m)
                                    )
                                except ValueError:
                                    # Jika isinya bukan kode modul (misal huruf 'P' atau 'E')
                                    st.caption("-") 
                            else:
                                st.write("-")
                        else:
                            st.caption("Jadwal Tdk Ada")
            else:
                st.error(f"NIM {nim_cari} tidak ditemukan dalam data FTI.")
                st.write("Pastikan NIM benar atau hubungi asisten.")

        except FileNotFoundError:
            st.error("File 'Sebaran_LFD_FTI.csv' tidak ditemukan. Harap unggah file tersebut.")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

    st.write("---")
    st.button("⬅️ Kembali ke halaman awal", on_click=lambda: st.session_state.update(page="page1"))


# --- HALAMAN MODUL ---
elif st.session_state.page.startswith("modul_"):
    nomor_modul = st.session_state.page.split("_")[1]

    if st.session_state.pilihan == "LKD":
        kembali_func = lambda: st.session_state.update(page="page2")
        label_kembali = "⬅️ Kembali ke Menu LKD"
    else:
        kembali_func = lambda: st.session_state.update(page="page3")
        label_kembali = "⬅️ Kembali ke Menu LFD"

    if nomor_modul == "1":
        st.title("Modul 1")
        st.write("Selamat datang di Modul 1!")
        
        st.subheader("🎯 Modul Praktikum")
        FILE_ID = "1f8bEu46KVdLVC_pZjucA7H-dtIyj09Us"
        st.components.v1.html(
            f'<iframe src="https://drive.google.com/file/d/{FILE_ID}/preview" width="100%" height="600"></iframe>',
            height=600,
        )
        st.subheader("Jurnal Praktikum")
        FILE_ID1 = "1wSQZtgceUIY-HjzbWspSWlK8KkViBtkG"
        st.components.v1.html(
            f'<iframe src="https://drive.google.com/embeddedfolderview?id={FILE_ID1}" width="100%" height="100"></iframe>',
            height=100,
        )

    elif nomor_modul == "2":
        st.title("Modul 2")
        st.write("Konten Modul 2...")
    
    # ... Lanjutkan untuk modul lainnya ...
    
    else:
        st.title(f"Modul {nomor_modul}")
        st.write("Konten belum tersedia.")

    st.write("---")
    st.button(label_kembali, on_click=kembali_func)
