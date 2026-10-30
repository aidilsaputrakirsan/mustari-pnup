/**
 * Membangun seluruh varian studi ablasi (lihat vite.config.ablasi.js)
 * lalu mencatat ukuran berkas JavaScript tiap varian.
 * Keluaran: laporan_tesis/data_pengukuran/ablasi/ukuran_bundle.json
 */
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

const VARIAN = ['A0-kontrol', 'A1-splitting', 'A2-lazy', 'A3-prefetch', 'A4-gzip', 'A5-gabungan'];
const OUTPUT_DIR = path.join(__dirname, 'laporan_tesis', 'data_pengukuran', 'ablasi');
fs.mkdirSync(OUTPUT_DIR, { recursive: true });

const hasil = {};
for (const nama of VARIAN) {
    console.log(`\n=== Build ${nama}`);
    execSync('npx vite build --config vite.config.ablasi.js', {
        cwd: __dirname, stdio: 'inherit', env: { ...process.env, VARIAN: nama },
    });
    const jsDir = path.join(__dirname, 'dist-ablasi', nama, 'assets', 'js');
    const berkas = fs.readdirSync(jsDir).filter((f) => f.endsWith('.js')).map((f) => {
        const isi = fs.readFileSync(path.join(jsDir, f));
        return {
            nama: f,
            mentah_KB: +(isi.length / 1024).toFixed(2),
            gzip_KB: +(zlib.gzipSync(isi, { level: 9 }).length / 1024).toFixed(2),
            gz_disajikan: fs.existsSync(path.join(jsDir, f + '.gz')),
        };
    });
    hasil[nama] = {
        jumlah_berkas_js: berkas.length,
        total_mentah_KB: +berkas.reduce((a, b) => a + b.mentah_KB, 0).toFixed(2),
        total_gzip_KB: +berkas.reduce((a, b) => a + b.gzip_KB, 0).toFixed(2),
        berkas,
    };
}
fs.writeFileSync(path.join(OUTPUT_DIR, 'ukuran_bundle.json'), JSON.stringify(hasil, null, 2));
console.log('\n✅ Tersimpan: ukuran_bundle.json');
for (const [k, v] of Object.entries(hasil)) console.log(k, v.jumlah_berkas_js, 'berkas', v.total_mentah_KB, 'KB');
