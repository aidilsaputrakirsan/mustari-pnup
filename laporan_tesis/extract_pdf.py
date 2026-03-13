import PyPDF2
import sys

pdf_path = r"C:\laragon\www\Materi-Presentasi\mustari-pnup\laporan_tesis\Proposal Mustari Optimasi SPA dengan Hybrid Lazy Loading.pdf"
output_path = r"C:\laragon\www\Materi-Presentasi\mustari-pnup\laporan_tesis\proposal_extracted.txt"

with open(pdf_path, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    print(f"Total pages: {len(reader.pages)}")
    
    all_text = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        all_text.append(f"\n--- PAGE {i+1} ---\n{text}")
    
    full_text = "\n".join(all_text)
    
    with open(output_path, 'w', encoding='utf-8') as out:
        out.write(full_text)
    
    print(f"Extracted {len(full_text)} characters to {output_path}")
