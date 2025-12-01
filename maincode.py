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
    st.write("Selamat datang di praktikum LKD!")

    st.subheader("🎯 Modul Praktikum")
    FILE_ID = "1f8bEu46KVdLVC_pZjucA7H-dtIyj09Us"

    st.components.v1.html(
        f"""
        <iframe src="https://drive.google.com/file/d/{FILE_ID}/preview"
            width="100%" height="600"></iframe>
        """,
            height=600,
        )

    st.subheader("Jurnal Praktikum")
    FILE_ID2 = "114LSosxqP_GIZ8KGI1nZpno_0L1e23BR"
        
    st.components.v1.html(
        f"""
        <iframe src="https://drive.google.com/embeddedfolderview?id={FILE_ID2}"
            width="100%" height="200"></iframe>
        """,
            height=200,
        )

    st.subheader("Video Praktikum")
    FILE_ID3 = "1qQ4ROgoR1X3yalDSmubNbIP3OSDJLTT4"
        
    st.components.v1.html(
        f"""
        <iframe src="https://drive.google.com/embeddedfolderview?id={FILE_ID3}"
            width="100%" height="200"></iframe>
        """,
            height=200,
        )
    
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
            # 1. BACA FILE (Header di baris pertama, jadi tidak perlu skiprows)
            df = pd.read_csv("Sebaran_LFD_FTI.csv")
            
            # Pastikan kolom NIM dibaca sebagai string
            df['NIM'] = df['NIM'].astype(str)
            
            # 2. CARI DATA MAHASISWA
            student_data = df[df['NIM'] == nim_cari]

            if not student_data.empty:
                # Ambil Data Diri
                nama_mhs = student_data.iloc[0]['NAMA']
                grup_mhs = student_data.iloc[0]['Grup']  # Mengambil data kolom Grup
                
                st.success(f"Mahasiswa ditemukan: **{nama_mhs}**")
                st.write(f"**NIM:** {nim_cari}")
                st.info(f"**Grup:** {grup_mhs}") # Menampilkan Grup
                
                st.subheader("Jadwal & Modul Praktikum")
                st.write("Berikut adalah jadwal praktikum Anda:")

                # Daftar kolom tanggal modul (15/09 SUDAH DIHAPUS dari daftar ini)
                # Sesuaikan nama kolom persis dengan di CSV (termasuk '11-Oct')
                date_cols = ["29/09", "13/10", "27/10", "11-Oct"]
                
                cols = st.columns(len(date_cols))
                
                for i, date_col in enumerate(date_cols):
                    with cols[i]:
                        # Tampilkan Tanggal sebagai Header Kecil
                        st.markdown(f"##### {date_col}")
                        
                        if date_col in student_data.columns:
                            kode_modul = student_data.iloc[0][date_col]
                            
                            # Cek validitas kode modul
                            if pd.notna(kode_modul):
                                st.write(f"Kode: **{kode_modul}**")
                                
                                try:
                                    # Ambil angka dari string (contoh: "M01" -> 1)
                                    nomor_modul_int = int(''.join(filter(str.isdigit, str(kode_modul))))
                                    
                                    # Tombol Buka Modul
                                    st.button(
                                        f"Buka {kode_modul}", 
                                        key=f"btn_{date_col}",
                                        on_click=lambda m=nomor_modul_int: pilih_modul(m)
                                    )
                                except ValueError:
                                    # Jika isinya bukan format modul (misal kosong atau text lain)
                                    st.caption("-") 
                            else:
                                st.caption("Libur / Kosong")
                        else:
                            st.caption("Jadwal Tdk Ada")
            else:
                st.error(f"NIM {nim_cari} tidak ditemukan dalam data.")
                st.write("Pastikan file CSV benar dan NIM sesuai.")

        except FileNotFoundError:
            st.error("File 'Sebaran_LFD_FTI.csv' tidak ditemukan. Harap unggah file tersebut.")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

    st.write("---")
    st.button("⬅️ Kembali ke halaman awal", on_click=lambda: st.session_state.update(page="page1"))


# --- HALAMAN MODUL ---
elif st.session_state.page.startswith("modul_"):
    nomor_modul = st.session_state.page.split("_")[1]

    # Tentukan tombol kembali arahnya ke mana
    if st.session_state.pilihan == "LKD":
        kembali_func = lambda: st.session_state.update(page="page2")
        label_kembali = "⬅️ Kembali ke Menu LKD"
    else:
        kembali_func = lambda: st.session_state.update(page="page3")
        label_kembali = "⬅️ Kembali ke Menu LFD"

    # Konten Modul
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
        
    elif nomor_modul == "3":
        st.title("Modul 3")
        st.write("Konten Modul 3...")

    elif nomor_modul == "4":
        st.title("Modul 4")
        st.write("Konten Modul 4...")

    elif nomor_modul == "5":
        st.title("Modul 5")
        st.write("Konten Modul 5...")
        
    elif nomor_modul == "11": # Contoh jika ada M11
        st.title("Modul 11")
        st.write("Konten Modul 11...")
        
    elif nomor_modul == "12": # Contoh jika ada M12
        st.title("Modul 12")
        st.write("Konten Modul 12...")
    
    else:
        st.title(f"Modul {nomor_modul}")
        st.write("Modul ini belum tersedia kontennya.")

    st.write("---")
    st.button(label_kembali, on_click=kembali_func)
