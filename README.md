
# Adobe Hackathon – Round 1A: PDF Outline Extractor

## 🎯 Objective
Build a solution that extracts a structured outline (Title, H1, H2, H3 headings) from PDF files using on-device intelligence and outputs it in a clean, hierarchical JSON format.

---

## 🧠 Approach

This solution uses **[PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)** — a powerful PDF parsing library — to analyze the font size, layout, and position of text blocks to identify document structure.

### Key Steps:
1. **Font Size Distribution** is calculated to identify top heading levels (H1, H2, H3)
2. **Title Detection** happens only on Page 1, using the largest non-junk line
3. **Junk Filtering** removes metadata like `arXiv:`, copyright lines, and license info
4. A **two-pass extraction** approach is used:
   - First pass → collect font size stats and title
   - Second pass → tag lines as H1/H2/H3 and collect page info

> This solution uses **no ML model** — ensuring fast execution, <200MB image size, and 100% offline compatibility.

---

## 🛠️ Technologies Used

- Python 3.10
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)
- Docker (Linux/AMD64 platform)
- Runs 100% offline (no internet access)

---

## 📂 Folder Structure

```
adobe-hackathon-round1a/
├── app/
│   ├── main.py
│   ├── heading_extractor.py
├── Dockerfile
├── requirements.txt
├── README.md
├── input/             # PDF files go here
├── output/            # JSON outputs appear here
```

---

## ⚙️ How to Build and Run

### ✅ 1. Build the Docker Image
```bash
docker build --platform linux/amd64 -t pdfextractor:adobe25 .
```

### ✅ 2. Run the Extractor

#### Windows PowerShell:
```powershell
docker run --rm -v "${PWD}\input:/app/input" -v "${PWD}\output:/app/output" --network none pdfextractor:adobe25
```

#### Linux/macOS (Bash):
```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pdfextractor:adobe25
```

This processes all `.pdf` files in `/app/input/` and saves `.json` outputs in `/app/output/`.

---

## 🧾 Example Output Format

```json
{
  "title": "Training Compute-Optimal Large Language Models",
  "outline": [
    { "level": "H1", "text": "Appendix", "page": 22 },
    { "level": "H2", "text": "1. Introduction", "page": 1 },
    { "level": "H3", "text": "A. Training dataset", "page": 22 }
  ]
}
```

---

## ✅ Constraints Met

| Constraint                     | Status |
|-------------------------------|--------|
| Runs on CPU (no GPU)          | ✅     |
| Model size ≤ 200MB (none)     | ✅     |
| No internet access required   | ✅     |
| Works with ≤ 50-page PDFs     | ✅     |
| Outputs JSON in <10 seconds   | ✅     |
| Dockerfile targets AMD64 CPU  | ✅     |

---

## 📝 Notes

- This extractor is layout-aware but does not rely on hardcoded font sizes.
- It filters noisy content (e.g., arXiv metadata).
- Robust to academic and technical PDFs.
- Reusable for Round 1B as foundation for intelligent reading.

---

> ✅ Built for **Adobe India Hackathon 2025 – “Connecting the Dots” Challenge**
