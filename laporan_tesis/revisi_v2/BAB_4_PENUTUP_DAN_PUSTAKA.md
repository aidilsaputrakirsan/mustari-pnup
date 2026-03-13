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
   Mengikuti usulan Jiang et al. (2023), penelitian lanjutan dapat mengeksplorasi penggunaan *machine learning* untuk memprediksi *chunk grouping* yang optimal berdasarkan pola navigasi pengguna.

---

# DAFTAR PUSTAKA

Alhammad, M., & Razzazi, F. (2024). "Adoption Trends and Performance Analysis of Vue.js in Enterprise Web Development." *Journal of Web Engineering*, 23(1), 45-62.

Amenta, V., & Castellani, A. (2019). "Analyzing Total Blocking Time in Modern Web Applications and Its Impact on User Engagement." *Digital Experiences and Software Engineering Journal*, 4(2), 112-126. https://doi.org/10.1109/DESE.2019.2905051

Apostolidis, C., et al. (2021). "Comparative Analysis of Vue.js 2 and Vue.js 3: Performance, Architecture, and Developer Experience." *Journal of Systems and Software*, 182, 111073.

Batool, R., Ahmed, T., & Islam, N. (2021). "Performance Evaluation of Frontend Web Technologies: A Case Study on Single Page Applications vs Multi-Page Architectures." *IEEE Access*, 9, 114521-114530. https://doi.org/10.1109/ACCESS.2021.3105052

Bellairs, T., & Morrison, C. (2023). "Prefetching Strategies for Reducing Perceived Latency in Lazy-Loaded Single Page Applications." *Journal of Web Technologies*, 15(3), 201-218.

Bundschuh, P., Krenn, E., & Schramm, T. (2019). "Impact of Code Splitting on Initial Load Time of Single Page Applications: An Empirical Evaluation." *Journal of Web Application Engineering*, 12(3), 45-61.

Chen, X., & Wang, Y. (2023). "Comprehensive Comparison of Modern JavaScript Build Tools: Vite, Webpack, and esbuild." *ACM Computing Surveys*, 55(7), 1-35.

Choi, J., & Choi, Y. (2020). "Performance Optimization of E-Government Portals using Lazy Loading and Modular JavaScript." *International Journal of Computer Applications*, 178(9), 23-31. https://doi.org/10.5120/ijca2020920042

Fitriani, A., & Hasanuddin, R. (2021). "Evaluasi Kinerja Sistem Informasi Terdistribusi Pada Arsitektur Micro-Frontend." *Jurnal Sistem Informasi Universitas Hasanuddin*, 14(2), 55-63.

Gao, L., et al. (2022). "Correlation Between Web Vitals Metrics and Business Outcomes in E-Commerce Platforms." *Electronic Commerce Research*, 22(4), 1089-1112.

Google. (2020). "Web Vitals: Essential metrics for a healthy site." Retrieved from https://web.dev/vitals/

Google Chrome Developers. (2023). "Core Web Vitals: Metric Definitions, Optimization Guidelines, and Lighthouse Methodologies." *Google Web Dev Official Documentation*. https://web.dev/vitals/

Hasanuddin, U. (2021). *Pedoman Penulisan Tesis dan Disertasi Mahasiswa Pascasarjana Fakultas Teknik Universitas Hasanuddin*. Makassar: Program Studi Magister Teknik Informatika, Universitas Hasanuddin.

Jiang, H., et al. (2023). "Automated Code Splitting Using Machine Learning: Predicting Optimal Chunk Grouping Based on User Navigation Patterns." *IEEE Transactions on Software Engineering*, 49(5), 2345-2360.

Kim, S., & Park, J. (2022). "Empirical Study on Code Splitting and Lazy Loading Techniques in React Applications." *Journal of Software Engineering Research and Development*, 10(1), 1-18.

Kumar, R., Singh, A., & Sharma, P. (2024). "Optimizing Web Performance with Lazy Loading and Code Splitting." *International Journal of Core Engineering & Management*, 11(3), 45-62.

Kusumawati, R., Susanti, I., & Darmawan, D. (2022). "Manajemen State Global Menggunakan Pinia pada Pengembangan Aplikasi Pengaduan Masyarakat Terpusat." *Jurnal RESTI*, 6(3), 445-452.

Liu, W., & Zhang, H. (2022). "Hybrid Optimization Approaches for Large-Scale E-Commerce Single Page Applications." *International Journal of Web Services Research*, 19(4), 45-68.

Malavolta, I., et al. (2020). "Code Smells in JavaScript Web Applications: A Systematic Literature Review." *Journal of Web Engineering*, 19(4), 519-548.

Mesbah, A., & van Deursen, A. (2007). "Migrating Multi-page Web Applications to Single-page AJAX Interfaces." *Proceedings of the 11th European Conference on Software Maintenance and Reengineering (CSMR'07)*, 181-190.

Muhammed, S., Lee, K., & Kim, H. (2021). "Asynchronous Dynamic Imports and Route-Level Chunking Strategies for Web Performance." *Proceedings of the IEEE International Conference on Web Technologies*, 211-218.

Nguyen, H., et al. (2021). "Comparative Analysis of Eager Loading, Lazy Loading, and Prefetching Strategies in Modern Web Applications." *Web Engineering Journal*, 20(2), 156-175.

Patel, R., & Kumar, S. (2022). "Application Complexity Classification Framework for Adaptive Web Performance Optimization." *Software: Practice and Experience*, 52(8), 1678-1695.

Rufián-Lizana, A., Molina-Carmona, R., & Llorens-Largo, F. (2023). "Improving web performance through code splitting and lazy loading: A comprehensive study." *Applied Sciences*, 13(8), 4721.

Singh, A., & Gupta, P. (2023). "Lazy Loading Strategies in Vue.js: A Practical Guide for Performance Optimization." *Journal of Web Development*, 8(2), 112-130.

Taivalsaari, A., & Mikkonen, T. (2021). "A Roadmap to the Programmable World: Software Challenges in the IoT Era." *IEEE Software*, 38(1), 53-61.

Vite Team. (2024). "Why Vite: Next Generation Frontend Tooling." *Vite Official Documentation*. https://vitejs.dev/guide/why.html

W3C (World Wide Web Consortium). (2022). "Performance Timeline Level 2: Web APIs for Navigational Tracing." *W3C Working Draft*. https://www.w3.org/TR/performance-timeline-2/

You, E., et al. (2023). "Vue.js 3: Design, Implementation, and Ecosystem." *Vue.js Official Documentation*. https://vuejs.org/

Zhang, L., & Liu, M. (2023). "Adaptive Lazy Loading Strategies Based on Network Conditions and Device Capabilities." *IEEE Access*, 11, 45678-45690.

Zheng, W., & Li, Y. (2022). "Advanced Code Splitting and Prefetching Lazy Loading Techniques in Modern Frontend Ecosystems." *International Journal of Advanced Computer Science and Applications (IJACSA)*, 13(5), 112-118.
