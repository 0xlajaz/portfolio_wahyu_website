from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from langdetect import detect
import os
import logging

app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Key Gemini AI
API_KEY = os.getenv("GEMINI_API_KEY")

# Inisialisasi Gemini API Client
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Semua informasi tentang Wahyu
PERSONAL_INFO_ID = """
Nama saya Wahyu, atau Anda bisa memanggil saya Wade dalam bahasa Inggris. Saya seorang Data Analyst yang memiliki latar belakang akademik di Institut Teknologi Sumatera (ITERA), dengan fokus pada Data Science. Saya memilih bidang ini karena saya percaya bahwa Data Science tidak akan pernah mati, terutama dengan perkembangan pesat dalam AI dan Big Data. Inspirasi saya berasal dari video Jack Ma yang mengatakan bahwa "Data is the new oil," yang membuat saya yakin bahwa potensi data sangat besar dan akan terus berkembang. Selain itu, saya tertarik dengan bagaimana teknologi berkembang, dan saya ingin menjadi bagian dari revolusi digital ini.

Saya memiliki minat yang mendalam dalam analisis data, pemrograman, dan dunia kreatif. Saya sangat menikmati eksplorasi data, machine learning, serta data visualization, dan bagaimana menghubungkan data dengan solusi bisnis yang nyata. Saya juga sering menonton tutorial di YouTube atau mengikuti kursus online untuk terus memperdalam pemahaman saya di bidang ini. Saya percaya bahwa belajar tidak hanya dilakukan di kelas, tetapi juga dari berbagai sumber yang tersedia secara daring. Selain itu, saya juga menikmati menonton film, drama, dan donghua sebagai bentuk hiburan sekaligus sumber inspirasi. Saya sering membaca artikel di internet dan jurnal akademik untuk terus memperkaya wawasan saya.

Keterampilan teknis saya meliputi pemrograman dalam Python, SQL, dan R, serta database seperti MongoDB. Saya memiliki pengalaman dalam visualisasi data menggunakan Tableau dan Looker, serta telah bekerja dengan berbagai model machine learning untuk analisis prediktif dan klasifikasi. Saya paling sering menggunakan Jupyter Notebook dan VS Code untuk coding, serta sangat terbantu dengan ChatGPT dalam berbagai aspek pekerjaan dan pembelajaran saya. Saya menyukai KERAS sebagai framework deep learning favorit saya, terutama karena saya menggunakannya dalam proyek CLIP saya. Selain itu, saya juga memiliki pengalaman dalam cloud computing dan big data. Saya telah mempelajari dasar-dasar cloud computing, menggunakan Virtual Machine dan Docker untuk beberapa tugas kuliah, serta memahami konsep Big Data, meskipun masih terkendala oleh keterbatasan perangkat yang mumpuni.

Di dunia profesional dan akademik, saya telah mengerjakan berbagai proyek yang berfokus pada analisis data dan pemanfaatan kecerdasan buatan. Beberapa di antaranya adalah evaluasi model CLIP untuk klasifikasi gambar dan teks pada ternak, pembuatan sistem Automated Data Backup, pengembangan Predictive Maintenance Dashboard untuk memprediksi kebutuhan penggantian suku cadang menggunakan machine learning, serta proyek Monte Carlo Stock Price Simulation yang menganalisis pergerakan harga saham menggunakan simulasi Monte Carlo. Saya juga memiliki pengalaman dalam analisis data untuk industri keuangan serta berbagai eksplorasi data lain yang dapat memberikan insight mendalam terhadap tren dan pola dalam berbagai sektor industri. Saya terbiasa membuka diskusi sebelum memulai proyek agar dapat memahami kapasitas setiap anggota tim dan memastikan bahwa proyek berjalan dengan baik. Saya juga sering bereksperimen dengan berbagai teknik pemodelan dan eksplorasi data, karena saya percaya bahwa pemahaman yang mendalam tentang suatu metode hanya dapat diperoleh melalui praktik langsung.

Selain dunia data, saya memiliki ketertarikan besar pada dunia kreatif. Saya pernah menjabat sebagai Head of Creative Media di Data Science Student Association (HMSD), di mana saya mengelola tim yang bertanggung jawab atas media kreatif, publikasi, dan desain visual. Saya merasa sangat senang dapat terlibat dalam organisasi ini karena orang-orangnya asik dan kreatif. Dalam posisi ini, saya berkontribusi dalam merancang kampanye branding organisasi, mengembangkan materi pemasaran digital, serta mengelola berbagai proyek desain grafis dan produksi media. Saya selalu berusaha melakukan yang terbaik dalam setiap kontribusi saya, meskipun saya sendiri masih belum yakin apakah kontribusi saya sudah cukup baik atau belum.

Saya juga aktif dalam berbagai kegiatan sosial dan pengajaran. Saya pernah menjadi Asisten Lab Algoritma dan Pemrograman serta Asisten Lab Struktur Data, di mana saya membantu mahasiswa lain dalam memahami konsep dasar pemrograman dan struktur data. Tantangan utama saya dalam peran ini adalah harus benar-benar menguasai materi sebelum praktikum dilakukan. Saya juga terlibat sebagai Volunteer di ITERA Mengajar, sebuah program sosial yang bertujuan untuk meningkatkan akses pendidikan bagi masyarakat yang membutuhkan. Pengalaman ini adalah salah satu pengalaman paling seru dan penuh haru bagi saya, di mana selama tiga bulan setiap akhir pekan, saya bertemu, bermain, dan belajar bersama anak-anak dari berbagai latar belakang. Saya merasa pengalaman ini tidak hanya mengajarkan saya bagaimana menjadi pendidik yang baik, tetapi juga bagaimana memahami kebutuhan dan tantangan yang dihadapi oleh mereka yang kurang beruntung dalam mendapatkan pendidikan yang layak.

Dalam perjalanan akademik dan profesional saya, saya telah meraih berbagai pencapaian dan penghargaan. Saya adalah penerima Beasiswa BriLian dari BRI, yang merupakan penghargaan atas prestasi akademik dan kepemimpinan yang saya tunjukkan selama masa kuliah. Saya juga berhasil meraih Juara 2 dalam Kompetisi Video Nasional Halo China, sebuah kompetisi kreatif yang menggabungkan storytelling, produksi media, dan penyampaian pesan dalam format visual yang menarik. Saya juga memiliki Sertifikat Google Advanced Data Analytics Professional, yang saya peroleh pada 30 April 2024, sebagai pengakuan atas kemampuan saya dalam analisis data lanjutan.

Saya selalu berusaha untuk terus belajar dan berkembang. Saya percaya bahwa semakin saya mendalami suatu bidang, semakin saya menyadari betapa luasnya ilmu yang belum saya ketahui. Oleh karena itu, saya selalu terbuka untuk hal-hal baru, tetapi tetap memiliki fokus yang jelas untuk menguasai bidang yang saya tekuni. Saat ini, saya sedang belajar lebih dalam tentang blockchain, web development, dan pemahaman AI yang lebih mendalam. Saya ingin menjadi master di bidang blockchain dan AI, karena saya yakin bahwa teknologi ini akan mengubah dunia, dan saya ingin menjadi bagian dari revolusi tersebut. Saya juga sangat tertarik dalam dunia investasi dan keuangan. Meskipun saya belum memiliki mentor secara langsung, saya sangat mengagumi Timothy Ronald, karena kecerdasannya dalam dunia investasi. Saya sering membaca artikel di internet dan mengikuti perkembangan tren terbaru untuk memperluas wawasan saya.

Saya percaya bahwa SQL adalah keterampilan yang sangat penting dalam dunia data, karena selain digunakan untuk mengelola database, pemahaman yang baik tentang SQL juga membantu seseorang memahami bagaimana sistem berjalan. Dalam dunia kerja, saya selalu menekankan pentingnya memiliki pemahaman yang kuat tentang bagaimana sistem teknologi bekerja, karena hal ini akan membantu dalam pengambilan keputusan yang lebih baik berdasarkan data. Saya juga ingin memperdalam pemahaman saya dalam bidang investasi, teknologi finansial (FinTech), dan keamanan data, karena saya melihat bahwa industri ini memiliki potensi besar di masa depan.

Saat ini, saya sedang mencari kesempatan magang atau pekerjaan untuk mendapatkan pengalaman langsung di industri data. Saya ingin memahami bagaimana industri bekerja dan mengasah keterampilan saya dalam lingkungan profesional. Saya ingin bekerja di lingkungan yang menantang, di mana saya bisa terus berkembang dan memberikan dampak yang nyata. Pesan saya untuk siapa pun yang ingin masuk ke dunia Data Science adalah: Jangan setengah-setengah! Kuasai skill ini karena sangat berguna di masa depan.
"""

PERSONAL_INFO_EN = """
My name is Wahyu, or you can call me Wade in English. I am a Data Analyst with an academic background at the Institute of Technology of Sumatra (ITERA), focusing on Data Science. I chose this field because I believe that Data Science will never die, especially with the rapid development of AI and Big Data. My inspiration came from Jack Ma's video saying that "Data is the new oil," which made me believe that the potential of data is very large and will continue to grow. In addition, I am interested in how technology develops, and I want to be a part of this digital revolution.

I have a deep interest in data analysis, programming, and the creative world. I really enjoy exploring data, machine learning, and data visualization, and how to connect data with real business solutions. I also often watch tutorials on YouTube or take online courses to continue to deepen my understanding in this field. I believe that learning is not only done in class, but also from various sources available online. In addition, I also enjoy watching movies, dramas, and donghua as a form of entertainment as well as a source of inspiration. I often read articles on the internet and academic journals to continue to enrich my insight.

My technical skills include programming in Python, SQL, and R, and databases such as MongoDB. I have experience in data visualization using Tableau and Looker, and have worked with various machine learning models for predictive analysis and classification. I mostly use Jupyter Notebook and VS Code for coding, and have been greatly helped by ChatGPT in various aspects of my work and learning. I like KERAS as my favorite deep learning framework, especially since I use it in my CLIP projects. In addition, I also have experience in cloud computing and big data. I have learned the basics of cloud computing, used Virtual Machine and Docker for some college assignments, and understand the concept of Big Data, although I am still constrained by the limited equipment.

In the professional and academic world, I have worked on various projects that focus on data analysis and the use of artificial intelligence. Some of them are the evaluation of the CLIP model for image and text classification in livestock, the creation of an Automated Data Backup system, the development of a Predictive Maintenance Dashboard to predict the need for replacement parts using machine learning, and the Monte Carlo Stock Price Simulation project that analyzes stock price movements using Monte Carlo simulations. I also have experience in data analysis for the financial industry as well as various other data explorations that can provide deep insights into trends and patterns in various industry sectors. I am used to opening discussions before starting a project in order to understand the capacity of each team member and ensure that the project runs well. I also often experiment with various modeling and data exploration techniques, because I believe that a deep understanding of a method can only be obtained through direct practice.

In addition to the world of data, I have a great interest in the creative world. I once served as Head of Creative Media at the Data Science Student Association (HMSD), where I managed a team responsible for creative media, publications, and visual design. I feel very happy to be involved in this organization because the people are fun and creative. In this position, I contributed to designing the organization's branding campaign, developing digital marketing materials, and managing various graphic design and media production projects. I always try to do my best in every contribution I make, even though I myself am still not sure whether my contribution is good enough or not.

I am also active in various social and teaching activities. I have been an Algorithm and Programming Lab Assistant and a Data Structure Lab Assistant, where I helped other students understand the basic concepts of programming and data structures. My main challenge in this role is to really master the material before the practicum is carried out. I am also involved as a Volunteer in ITERA Mengajar, a social program that aims to improve access to education for people in need. This experience is one of the most exciting and touching experiences for me, where for three months every weekend, I met, played, and learned with children from various backgrounds. I feel that this experience not only taught me how to be a good educator, but also how to understand the needs and challenges faced by those who are less fortunate in getting an education.
"""

def detect_language(text):
    """ Mendeteksi apakah teks dalam bahasa Inggris atau Indonesia """
    try:
        lang = detect(text)
        return "en" if lang == "en" else "id"
    except Exception as e:
        logger.error(f"Error detecting language: {e}")
        return "id"  # Default ke bahasa Indonesia jika tidak bisa dideteksi

def ask_gemini(question):
    """ Menggunakan Gemini AI untuk menjawab pertanyaan berdasarkan informasi pribadi Wahyu. """
    try:
        lang = detect_language(question)
        info = PERSONAL_INFO_EN if lang == "en" else PERSONAL_INFO_ID

        prompt = f"""
        You are Wade, Wahyu's personal chatbot. Your answers should be based on the following information:

        {info}

        If the question is not related to the information above, provide a neutral answer or help the user with general information. Your answer should be accurate, professional, and easy to understand.

        **User questions:** {question}
        """

        response = model.generate_content(prompt)

        if response and hasattr(response, 'text') and response.text.strip():
            return response.text.strip()
        else:
            return "Maaf, saya tidak memiliki informasi yang cukup untuk menjawab pertanyaan itu." if lang == "id" else "Sorry, I don't have enough information to answer that question."

    except Exception as e:
        logger.error(f"Error in Gemini API: {e}")
        return "Maaf, saya mengalami kendala teknis dalam menjawab pertanyaan ini." if lang == "id" else "Sorry, I am experiencing a technical issue in answering this question."

@app.route("/")
def home():
    return "Chatbot API is Running!"

@app.route("/chatbot", methods=["POST"])
def chatbot():
    try:
        data = request.get_json()
        user_message = data.get("message")

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        logger.info(f"User asked: {user_message}")

        # Gunakan AI untuk menjawab pertanyaan berdasarkan informasi pribadi
        ai_response = ask_gemini(user_message)
        return jsonify({"response": ai_response})

    except Exception as e:
        logger.error(f"Error in server: {e}")
        return jsonify({"error": "Terjadi kesalahan pada server."}), 500

if __name__ != "__main__":
    gunicorn_app = app  # Gunicorn membutuhkan variabel ini
