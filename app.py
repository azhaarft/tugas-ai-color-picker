import streamlit as st
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image

# Setup halaman web
st.set_page_config(page_title="Color Picker K-Means", page_icon="🎨")
st.title("Image Dominant Color Picker")
st.write("Ekstrak 5 warna paling dominan dari gambarmu menggunakan algoritma K-Means Clustering.")

# Fungsi utama untuk ekstrak warna dengan K-Means
def get_dominant_colors(image, k=5):
    # Resize gambar supaya komputasi K-Means lebih ringan dan cepat
    img = image.copy()
    img.thumbnail((200, 200))
    
    # Konversi gambar dari format PIL ke Numpy Array
    img_np = np.array(img)
    
    # Ubah bentuk array dari 3D (tinggi, lebar, RGB) menjadi 2D (jumlah pixel, RGB)
    # Ini wajib karena K-Means minta format data tabular baris x kolom
    pixels = img_np.reshape(-1, 3)
    
    # Inisialisasi dan jalankan algoritma K-Means
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(pixels)
    
    # Centroid yang dihasilkan K-Means adalah warna dominannya
    colors = kmeans.cluster_centers_
    return colors.astype(int)

# Fungsi untuk mengubah nilai RGB jadi kode Hex (biar gampang di-copy)
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % tuple(rgb)

# Widget untuk upload gambar
uploaded_file = st.file_uploader("Pilih gambar dari perangkatmu...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Tampilkan gambar yang diupload
    image = Image.open(uploaded_file)
    st.image(image, caption='Gambar Asli', use_column_width=True)
    
    with st.spinner('Sedang mengekstrak palet warna...'):
        # Panggil fungsi K-Means
        colors = get_dominant_colors(image, k=5)
        
        st.subheader("5 Warna Paling Dominan:")
        
        # Bikin 5 kolom untuk menampilkan warna berjejer
        cols = st.columns(5)
        
        for i, color in enumerate(colors):
            hex_color = rgb_to_hex(color)
            with cols[i]:
                # Render kotak warna pakai sedikit HTML & CSS bawaan Streamlit
                st.markdown(f'''
                    <div style="
                        background-color: {hex_color}; 
                        height: 80px; 
                        border-radius: 10px; 
                        margin-bottom: 10px;
                        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);">
                    </div>
                    <p style="text-align: center; font-family: monospace; font-size: 16px;"><b>{hex_color}</b></p>
                ''', unsafe_allow_html=True)