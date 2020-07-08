# Logistic Routing Problem

<img src="https://picjumbo.com/wp-content/uploads/white-tir-truck-in-motion-driving-on-highway_free_stock_photos_picjumbo_DSC04205-1080x720.jpg" class="img-responsive" width="50%" height="50%"><img src="https://upload.wikimedia.org/wikipedia/commons/1/1a/Luftaufnahmen_Nordseekueste_2013_05_by-RaBoe_tele_46.jpg" class="img-responsive" width="50%" height="50%">

## Author
Taufiq Husada Daryanto<br>
13518058

## Tujuan Tugas
1. Review materi pathfinding pada mata kuliah Strategi Algoritma.
2. Mengenal multiple-agent TSP.
3. Melakukan visualisasi data.

## Deskripsi Masalah
Welcome to **Oldenburg** ! Kota kecil cantik ini merupakan sebuah kota kecil di barat lau kota Bremen , Jerman , dengan penduduk kurang lebih 168 ribu jiwa [2018]. Kota kecil ini cocok menjadi lahan uji coba untuk melakukan pemodelan sederhana pembuatan rute pengantaran logistik.<br>
Setiap beberapa jam sekali, sebuah perusahaan logistik akan mengirimkan beberapa kurirnya untuk mengantar barang dari kantor pusat mereka ke beberapa titik tujuan yang tersebar di penjuru kota Oldenburg. Anda diminta untuk mencari rute untuk seluruh kurir sehingga jarak yang ditempuh oleh semua kurir paling kecil, sehingga perusahaan logistik dapat menghemat biaya bensin.

## Multiple-Agent TSP
Masalah pengantaran barang untuk satu kendaraan dengan fungsi objektif jarak minimal dapat dimodelkan oleh Travelling Salesman Problem. Akan tetapi, perusahaan logistik biasanya memiliki lebih dari satu kendaraan yang berangkat bersamaan, sehingga TSP kurang cocok digunakan. Generalisasi TSP untuk beberapa agen adalah **multiple-agent TSP (mTSP)**, dan model masalah ini akan kita gunakan. Pada mTSP, akan terdapat *m* tur yang akan dibangun. Syarat dari semua tur mirip dengan TSP, yaitu bahwa seluruh tur akan kembali ke simpul awal (mewakili kantor pusat) dan setiap tujuan hanya akan dilewati oleh satu tur.

## How to run
1. Install library tambahan
- MIP `pip install mip`
2. Open terminal
3. Go to src directory
4. Type `python code.py`
5. Ikuti alur programnya
- masukkan pilihan kota (pilihan angkanya)
- masukkan simpul kantor pusat
- masukkan jumlah simpul tujuan
- masukkan node-node tujuan (pisahkan dengan spasi)
- masukkan jumlah kurir

## Pendekatan solusi
1. Pembuatan subgraph (milestone 1)
- pencarian jarak terpendek antar masing masing node
Menggunakan djikstra dari setiap node untuk mencari jarak terpendek. Ketika proses djikstra, dilakukan juga pencatatan path nya
2. Penyelesaian mTSP (milestone 2)
- membagi rata node nya sesuai jumlah kurirnya: 
Pertama tama adalah melakukan proses TSP untuk keseluruhan simpul dan mencatat urutan path nya. Dari hasil tersebut kemudian bagi node nya sama rata untuk tiap kurir berdasarkan urutan pathnya. misal hasil TSP keseluruhannya 0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 0 dan ada 3 kurir maka dibaginya [kurir 1 : 1, 2], [kurir 2 : 3, 4], [kurir 1: 5, 6]. Metode greedy ini didasari oleh alasan bahwa node-node yang berurutan di TSP "secara umum" berdekatan dibandingkan node yang lain
- melakukan single TSP untuk tiap kurir dengan node-node yang sudah di assign di proses sebelumnya:
Melakukan proses TSP dengan menggunakan library MIP, berdasarkan persamaan matematika dari TSP
3. Visualisasi map
- Visualisasi dengan matplotlib:
mengeplot garis tiap edge yang menghubungkan kedua node. Pertama, plot seluruh edge di map dulu. Kemudian, plot path masing masing TSP dengan warna warna tertentu

## Referensi
[1] Dataset : https://www.cs.utah.edu/~lifeifei/SpatialDataset.htm<br>
[2] Pengenalan dan formulasi mTSP : https://neos-guide.org/content/multiple-traveling-salesman-problem-mtsp<br>
[3] MIP , pustaka Python untuk optimisasi : https://python-mip.readthedocs.io/en/latest/intro.html<br>
[4] OpenGL untuk Python : https://stackabuse.com/brief-introduction-to-opengl-in-python-with-pyopengl/<br>
[5]  Li, Feifei, Dihan Cheng, Marios Hadjieleftheriou, George Kollios, and Shang-Hua Teng. "On trip planning queries in spatial databases." In International symposium on spatial and temporal databases, pp. 273-290. Springer, Berlin, Heidelberg, 2005.

## Credits
Thank you for Li Fei Fei et. al. for providing the data.
