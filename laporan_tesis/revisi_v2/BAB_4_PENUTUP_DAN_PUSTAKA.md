# BAB IV PENUTUP

## 4.1 Kesimpulan

Berdasarkan hasil penelitian yang telah dilakukan pada dua model *Single Page Application* (SPA) — Sistem Informasi Manajemen Tugas Akhir (SIMTA) dan *Company Profile* — dengan menggunakan kombinasi instrumen pengukuran *W3C PerformanceObserver* dan Google Lighthouse, penelitian ini mengerucut pada kesimpulan berikut:

1. **Efektivitas *Code Splitting* dalam mengurangi ukuran *bundle* awal.**
   Dengan memisahkan pustaka-pustaka besar (seperti Chart.js dan Pinia) ke dalam file terpisah menggunakan fitur `manualChunks` di Vite, ukuran file yang diunduh saat pertama kali membuka SIMTA berhasil direduksi lebih dari 40% — dari 346 KB menjadi sekitar 195 KB. Browser tidak perlu lagi mengunduh kode untuk fitur grafik ketika pengguna hanya membuka halaman login.

2. ***Hybrid Lazy Loading* efektif mengurangi *Total Blocking Time* (TBT).**
   Meskipun waktu tampil pertama (FCP) sedikit bertambah karena *overhead* pencarian rute dinamis, manfaat nyata terlihat pada nilai TBT yang berkurang secara signifikan dalam kondisi normal. Hasil dari Lighthouse mengkonfirmasi temuan ini dengan menunjukkan penurunan TBT sebesar 41,4% pada SIMTA.

3. **Manfaat terbesar terlihat pada perangkat dengan spesifikasi rendah.**
   Ketika diuji pada kondisi CPU diperlambat 4x (mensimulasikan perangkat lawas), teknik *Code Splitting* berhasil menurunkan nilai TBT dari angka berbahaya yang melampaui batas toleransi Google Web Vitals menjadi angka yang lebih aman. Lighthouse *Performance Score* menunjukkan peningkatan dari skor tetap stabil di angka 64-66 meskipun dengan konten dinamis yang berat.

4. **Teknik ini tidak cocok untuk semua jenis website (*Diminishing Returns*).**
   Pada *Company Profile* (website sederhana), penerapan *Code Splitting* tidak memberikan manfaat performa yang berarti karena tidak ada pustaka besar yang perlu dipecah. Sebaliknya, teknik ini justru bisa sedikit memperlambat FCP karena tambahan permintaan file yang tidak perlu. Penelitian ini membuktikan bahwa strategi optimasi harus mempertimbangkan tingkat kompleksitas aplikasi sebagai faktor penentu.

## 4.2 Saran untuk Penelitian Selanjutnya

1. **Integrasi dengan teknologi *Progressive Web App* (PWA):**
   File-file yang sudah diunduh bisa disimpan secara permanen di *cache* browser menggunakan *Service Workers*. Sehingga pengguna yang membuka kembali website tidak perlu mengunduh file apa pun.

2. **Penanganan animasi yang berjalan terus-menerus:**
   Teknik `requestIdleCallback` yang digunakan untuk *prefetching* mungkin tidak bekerja optimal ketika halaman menampilkan animasi konstan. Penelitian lanjutan perlu mengembangkan mekanisme yang lebih cerdas untuk mendeteksi kapan browser benar-benar sedang tidak sibuk.

3. **Perbandingan dengan *Server-Side Rendering* (SSR):**
   Penelitian berikutnya bisa membandingkan apakah kerangka kerja SSR seperti Nuxt.js menghasilkan nilai FCP dan TBT yang lebih baik, karena HTML dikirimkan sudah matang dari server.

4. **Pengujian pada kondisi jaringan yang bervariasi:**
   Penelitian ini fokus pada *CPU throttling*. Penelitian lanjutan dapat menambahkan variabel *network throttling* (3G, 4G) untuk melihat dampak gabungan antara keterbatasan CPU dan jaringan.

5. **Penggunaan *Machine Learning* untuk *automated code splitting*:**
   Penelitian lanjutan dapat mengeksplorasi penggunaan *machine learning* untuk memprediksi *chunk grouping* yang optimal berdasarkan pola navigasi pengguna.

---

# DAFTAR PUSTAKA

Anggraeni, O. S. I., Sugiarto, L., & Agustin, T. (2024). "Studi Komparatif Performa Framework Javascript Modern dalam Pengembangan Aplikasi Web." *Modem: Jurnal Informatika dan Sains Teknologi*, 2(4), 162-177.

Bara, R.-M., Boiangiu, C.-A., & Tudose, C. (2024). "Analysing the Performance Impacts of Lazy Loading in Web Applications." *Journal of Information Systems & Operations Management*, 18(1), 1-15.

Bogner, J., & Merkel, M. (2022). "To Type or Not to Type? A Systematic Comparison of the Software Quality of JavaScript and TypeScript Applications on GitHub." *Proceedings of the 19th International Conference on Mining Software Repositories (MSR '22)*. ACM.

Donvir, A., Jain, A., & Saraswathi, P. K. (2024). "Application State Management (ASM) in the Modern Web and Mobile Applications: A Comprehensive Review." *arXiv preprint* arXiv:2407.19318.

Emmanni, P. S. (2023). "Comparative Analysis of Angular, React, and Vue.js in Single Page Application Development." *International Journal of Science and Research (IJSR)*, 12(6), 2971-2974.

Fauzi, A. Z. (2024). *Analisis Efisiensi Proses Build dan Performa Single-Page Application React, Vue, dan Svelte yang Dikembangkan Menggunakan Vite sebagai Build Tool* [Skripsi]. Yogyakarta: UIN Sunan Kalijaga.

Google. (2020). "Web Vitals: Essential metrics for a healthy site." Retrieved from https://web.dev/vitals/

Google Chrome Developers. (2023). "Core Web Vitals: Metric Definitions, Optimization Guidelines, and Lighthouse Methodologies." *Google Web Dev Official Documentation*. https://web.dev/vitals/

Hasanuddin, U. (2021). *Pedoman Penulisan Tesis dan Disertasi Mahasiswa Pascasarjana Fakultas Teknik Universitas Hasanuddin*. Makassar: Program Studi Magister Teknik Informatika, Universitas Hasanuddin.

Hermanto, R. R., & Engel, M. M. (2025). "Analisis Komparatif Kinerja Next.js, Nuxt.js, dan Remix.js dalam Implementasi Server Side Rendering Website Berita." *TIN: Terapan Informatika Nusantara*, 6(5), 450-463.

Jihadi, H., & Syarabil, A. F. (2023). "Perbandingan React JS dan Vue JS dalam Pengembangan Aplikasi Web Interaktif: Sebuah Studi Komparatif." *Jurnal Sistem Informasi Bisnis (JUNSIBI)*, 4(2), 70-79.

Johannes, D., Khomh, F., & Antoniol, G. (2019). "A Large-Scale Empirical Study of Code Smells in JavaScript Projects." *Software Quality Journal*, 27(3), 1271-1314.

Jonathan, R., & Suprihadi. (2023). "Development of Front-End Web Applications Utilizing Single Page Application Framework and React.js Library." *International Journal Software Engineering and Computer Science (IJSECS)*, 3(3), 529-536.

Khoirurrizal, M. F., Hidayat, C. R., & Ruuhwan. (2024). "Analisis Perbandingan Framework Front-End JavaScript SolidJS dan VueJS pada Pengembangan Website Interaktif." *Jurnal Informatika dan Teknik Elektro Terapan (JITET)*, 12(2).

Kowalczyk, K., & Szandała, T. (2024). "Enhancing SEO in Single-Page Web Applications in Contrast With Multi-Page Applications." *IEEE Access*, 12, 11597-11614. https://doi.org/10.1109/ACCESS.2024.3355740

Kumar, R., Singh, A., & Sharma, P. (2024). "Optimizing Web Performance with Lazy Loading and Code Splitting." *International Journal of Core Engineering & Management*, 11(3), 45-62.

Larissa, T. N., & Suartana, I M. (2026). "Perbandingan Teknik Pemuatan Awal Eager Loading dan Lazy Loading Intersection Observer terhadap Performa Website." *Journal of Informatics and Computer Science (JINACS)*, 7(4).

Noer, M. A., & Suartana, I M. (2024). "Perbandingan Mekanisme Rendering untuk Optimasi Website." *Journal of Informatics and Computer Science (JINACS)*, 6(2).

Piastou, M. (2023). "Comprehensive Performance and Scalability Assessment of Front-End Frameworks: React, Angular, and Vue.js." *World Journal of Advanced Engineering Technology and Sciences*, 9(2), 366-376.

Rezeki, A., Saputro, S. W., Saragih, T. H., Nugroho, R. A., & Abadi, F. (2026). "Empirical Performance of E2E Frameworks in React-Vue SPAs Using DIA." *International Journal of Advances in Data and Information Systems*, 7(1), 317-333.

Saboury, A., Musavi, P., Khomh, F., & Antoniol, G. (2017). "An Empirical Study of Code Smells in JavaScript Projects." *IEEE 24th International Conference on Software Analysis, Evolution and Reengineering (SANER)*, 294-305.

Setiawan, A. A., & Fauzi, E. (2025). "Analisis Komparatif Performa Implementasi Lazy Loading dan Code Splitting pada Framework React, Vue, dan Angular Berdasarkan Skor Lighthouse." *INTECOMS: Journal of Information Technology and Computer Science*, 8(3).

Sofi'ie, F. A. F., & Qoiriah, A. (2023). "Analisis Perbandingan Framework Front-End Javascript React dan Vue pada Pengembangan Website." *Journal of Informatics and Computer Science (JINACS)*, 5(2), 157-164.

Taivalsaari, A., & Mikkonen, T. (2021). "A Roadmap to the Programmable World: Software Challenges in the IoT Era." *IEEE Software*, 38(1), 53-61. https://doi.org/10.1109/MS.2020.3020616

Turcotte, A., Gokhale, S., & Tip, F. (2023). "Increasing the Responsiveness of Web Applications by Introducing Lazy Loading." *Proceedings of the 38th IEEE/ACM International Conference on Automated Software Engineering (ASE)*, 459-470.

Vepsäläinen, J., Hellas, A., & Vuorimaa, P. (2023). "Overview of Web Application Performance Optimization Techniques." *Web Information Systems and Technologies (WEBIST 2023), Lecture Notes in Business Information Processing*. Springer.

Vite Team. (2024). "Why Vite: Next Generation Frontend Tooling." *Vite Official Documentation*. https://vitejs.dev/guide/why.html

W3C (World Wide Web Consortium). (2022). "Performance Timeline Level 2: Web APIs for Navigational Tracing." *W3C Working Draft*. https://www.w3.org/TR/performance-timeline-2/

Wijaya, I., & Farisi, A. (2025). "Analisis Perbandingan Kinerja dan Penggunaan Energi pada Framework React dan Vue." *Techno.Com*, 24(1), 104-116.

You, E., et al. (2023). "Vue.js 3: Design, Implementation, and Ecosystem." *Vue.js Official Documentation*. https://vuejs.org/
