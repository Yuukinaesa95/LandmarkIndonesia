import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import folium
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static
from tensorflow.keras.models import load_model

# Load model
model = load_model('model.h5')

st.set_page_config(page_title="Klasifikasi Landmark", page_icon=":🏛️:")

# Define the class names
nama_class = ['Candi Borobudur', 'Gedung Sate', 'Istana Maimun', 'Jembatan Ampera', 'Monumen Nasional']

# Define the locations of each class
class_locations = {
    'Candi Borobudur': {'nama': 'Candi Borobudur', 'Latitude': -7.60788, 'Longitude': 110.20367, 'kota, provinsi' : 'Magelang, Jawa Tengah',
                        'deskripsi': 'Candi Borobudur adalah candi Buddha Mahayana dari abad ke-9 yang terletak di Jawa Tengah, Indonesia. Candi besar ini merupakan salah satu monumen Buddha terbesar di dunia dan telah menjadi tujuan wisata yang populer. Candi ini memiliki 2.672 panel relief dan 504 patung Buddha, dengan kubah utama di tengah-tengah platform teratas yang dikelilingi oleh 72 patung Buddha yang duduk di dalam stupa berlubang. Tempat ini dinyatakan sebagai Situs Warisan Dunia UNESCO pada tahun 1991.'},
	'Gedung Sate': {'nama': 'Gedung Sate', 'Latitude': -6.90249, 'Longitude': 107.61872, 'kota, provinsi' : 'Bandung, Jawa Barat',
                    'deskripsi': 'Gedung Sate adalah sebuah gedung pemerintahan yang terletak di Bandung, Jawa Barat, Indonesia. Gedung ini dibangun pada tahun 1920 dan berfungsi sebagai kantor pusat pemerintahan Hindia Belanda. Gedung ini memiliki gaya arsitektur yang unik yang memadukan unsur Belanda dan tradisional Sunda. Gedung ini dinamai sesuai dengan tusuk sate yang dijual oleh para pedagang di sekitarnya. Saat ini, gedung ini digunakan sebagai kantor Gubernur Jawa Barat dan menjadi landmark serta objek wisata yang populer.'},
	'Istana Maimun': {'nama': 'Istana Maimun', 'Latitude': 3.5752, 'Longitude': 98.6837, 'kota, provinsi' : 'Medan, Sumatra Utara',
                      'deskripsi': 'Istana Maimun adalah istana Kesultanan Deli yang terletak di Medan, Sumatera Utara, Indonesia. Istana ini dibangun pada tahun 1888 dan menampilkan perpaduan unik antara gaya arsitektur Melayu, Islam, dan Eropa. Istana ini terbuka untuk umum dan pengunjung dapat menjelajahi berbagai ruangan dan galeri yang menampilkan sejarah dan budaya kesultanan. Istana ini juga menyimpan koleksi kebesaran kerajaan, termasuk singgasana, mahkota, dan kereta kencana.'},
    'Jembatan Ampera': {'nama': 'Jembatan Ampera', 'Latitude': -2.99178, 'Longitude': 104.76354, 'kota, provinsi' : 'Palembang, Sumatra Selatan',
                        'deskripsi': 'Jembatan Ampera adalah sebuah jembatan penghubung vertikal yang terletak di Palembang, Sumatera Selatan, Indonesia. Jembatan ini membentang di atas Sungai Musi dan dibangun pada tahun 1965. Jembatan ini telah menjadi simbol kota dan merupakan penghubung transportasi yang penting antara bagian utara dan selatan Palembang. Jembatan ini juga merupakan tempat yang populer bagi wisatawan untuk menikmati pemandangan Sungai Musi dan cakrawala kota.'},
	'Monumen Nasional': {'nama': 'Monumen Nasional', 'Latitude': -6.1754, 'Longitude': 106.8272, 'kota, provinsi' : 'Jakarta, DKI Jakarta',
                         'deskripsi': 'Monumen Nasional adalah sebuah monumen yang terletak di tengah-tengah Lapangan Merdeka, Jakarta Pusat, Indonesia. Monumen ini dibangun pada tahun 1961 untuk memperingati perjuangan kemerdekaan Indonesia. Monumen ini berdiri di ketinggian 132 meter dan di atasnya terdapat api yang dilapisi kertas emas. Pengunjung dapat menggunakan lift untuk mencapai puncak monumen dan menikmati panorama kota Jakarta. Monumen ini dikelilingi oleh taman dan berbagai museum yang memamerkan sejarah dan budaya Indonesia.'},
}

    # Function to preprocess the image
def preprocess_image(image):
    img = image.resize((224, 224))
    img = np.array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# Define the prediction function
def predict(image):
    try:
        # Preprocess the image
        img = preprocess_image(image)
        # Predict the class probabilities
        probabilities = model.predict(img)[0]
        # Get the predicted class index
        predicted_class_idx = np.argmax(probabilities)
        # Get the predicted class name
        predicted_class = nama_class[predicted_class_idx]
        # Get the probability of the predicted class
        predicted_prob = probabilities[predicted_class_idx]
        # Convert the probability to a percentage
        predicted_prob_pct = round(predicted_prob * 100, 2)
        # Convert the probabilities to percentages
        probabilities_pct = [round(prob * 100, 2) for prob in probabilities]
        # Return the predicted class name and probabilities
        return (predicted_class, predicted_prob_pct, probabilities_pct)
    except:
        # Return None if the image cannot be processed
        return None

def tentang_aplikasi():
    st.markdown("<h1 style='text-align: center'>Tentang Aplikasi 🔥</h1>", unsafe_allow_html=True)
    st.write("")
    st.write("**Aplikasi ini dibuat dengan tujuan untuk memajukan pariwisata Indonesia.**")
    st.write("Sehingga wisatawan dapat mengetahui landmark apa saja yang ada di Indonesia.✨")
    st.write('''Landmark ini tidak hanya menjadi daya tarik wisata bagi wisatawan lokal maupun mancanegara,
      tetapi juga menjadi simbol identitas dari suatu kota atau wilayah.
      Oleh karena itu, penting untuk melestarikan dan menjaga keberadaan dari landmark ini sebagai bagian dari warisan budaya Indonesia. 💌''')

def cara_penggunaan():
    st.markdown("<h1 style='text-align: center'>Selamat datang di web aplikasi klasifikasi landmark 👋</h1>", unsafe_allow_html=True)
    st.write("")
    st.write("**Cara penggunaan**: ")
    # Define the custom CSS class for the instructions
    st.markdown(
        """
        <style>
        .rounded-instructions {
            border-radius: 10px;
            box-shadow: 3px 3px 5px #999;
            padding: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Display the instructions with the custom CSS class
    st.markdown(
        """
        <div class="rounded-instructions">
        <p>1. Pilih menu yang berada pada sidebar sebelah kiri untuk berpindah ke <i><b>Aplikasi Utama</i></b> 👈</p>
        <p>2. Unggah gambar landmark dengan cara klik browse file.</p>
        <p>3. Aplikasi ini akan mulai memprediksi landmark yang telah di unggah.</p>
        <p>4. Aplikasi akan menampilkan probabilitas dari landmark yang diprediksi.</p>
        <p>5. Aplikasi akan menampilkan lokasi landmark yang telah diprediksi.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.success('''
    Jika sudah membaca cara penggunaan. \n
    Silahkan pilih menu untuk berpindah ke **Aplikasi Utama** ✅
    ''')

# Define the mapping demo function
def aplikasi_utama():

    # Set up the Streamlit app
    array_color = '#00FFAB'
    # Add a map to the app
    geolocator = Nominatim(user_agent="Landmark", timeout=10)
    location = geolocator.geocode("Indonesia") # Initial location
    m = folium.Map(location=[location.latitude, location.longitude], zoom_start=5)

    st.markdown("<h1 style='text-align: center'>Klasifikasi Landmark 📌</h1>", unsafe_allow_html=True)
    st.write("")
    st.write("**Unggah gambar dan aplikasi akan mengklasifikasikannya ke dalam salah satu landmark berikut** 👇")
    st.write(f'<span style="color:{array_color}">{nama_class}</span>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Read the image
        image = Image.open(uploaded_file)
        # Show the image
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        # Make a prediction
        prediction = predict(image)
        if prediction is not None:
            predicted_class, predicted_prob, probabilities = prediction
            # Show the predicted class and probability
            st.write("Prediksi landmark:", predicted_class)
            st.write("Probabilitas:", predicted_prob, "%")
            # Show the probabilities for each class
            for class_name, prob in zip(nama_class, probabilities):
                st.write(class_name, ":", prob, "%")
            # Get the location of the predicted class
            class_location = class_locations[predicted_class]
            # Add a marker to the map
            folium.Marker(
                location=[class_location['Latitude'], class_location['Longitude']],
                popup=class_location['nama'],
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
            # Zoom to the location
            m.fit_bounds([[class_location['Latitude'], class_location['Longitude']]])
            # Show the class location

            st.write("Informasi lebih lanjut:", class_location)
            st.markdown("<h3 style='text-align: center'>Peta lokasi landmark 📍</h1>", unsafe_allow_html=True)

            # Update the map
            folium_static(m, width=700, height=500)

page_names_to_funcs = {
    "Cara Penggunaan": cara_penggunaan,
    "Aplikasi Utama": aplikasi_utama,
    "Tentang Aplikasi": tentang_aplikasi
}

demo_name = st.sidebar.selectbox("Menu", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()

hide_st_style = """
            <style>

            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
