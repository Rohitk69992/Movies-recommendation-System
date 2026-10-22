"""
CineMatch — Academic Mini Project Report DOCX Generator
Constructs the complete editable Word Document (.docx) matching the 21-page report structure.
Embeds LaTeX equation images, high-contrast diagrams, and complete academic theory.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)


def create_docx_report():
    doc = Document()
    output_docx = "CineMatch_Machine_Learning_Mini_Project_Report.docx"

    # Set standard margins (0.75 in)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        section.page_width = Inches(8.27)  # A4
        section.page_height = Inches(11.69)

    # -------------------------------------------------------------
    # PAGE 1: COVER PAGE
    # -------------------------------------------------------------
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Peoples Empowerment Group’s\n")
    r.font.name = "Arial"; r.font.size = Pt(11); r.bold = True
    r2 = p.add_run("ISBM COLLEGE OF ENGINEERING, NANDE, PUNE\n")
    r2.font.name = "Arial"; r2.font.size = Pt(13); r2.bold = True
    r3 = p.add_run("DEPARTMENT OF ARTIFICIAL INTELLIGENCE AND DATA SCIENCE\n\n")
    r3.font.name = "Arial"; r3.font.size = Pt(10.5); r3.bold = True

    logo_path = "reports/college_logo.png"
    if os.path.exists(logo_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(logo_path, width=Inches(1.3))

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(20)
    p_title.paragraph_format.space_after = Pt(20)
    r_sub = p_title.add_run("A MINI PROJECT REPORT ON\n\n")
    r_sub.font.name = "Arial"; r_sub.font.size = Pt(10); r_sub.bold = True
    r_main = p_title.add_run("“CineMatch: TMDB Content-Based Movie Recommendation System”\n\n")
    r_main.font.name = "Arial"; r_main.font.size = Pt(16); r_main.bold = True; r_main.font.color.rgb = RGBColor(15, 23, 42)

    p_req = doc.add_paragraph()
    p_req.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_req.add_run("SUBMITTED IN PARTIAL FULFILMENT OF THE REQUIREMENTS FOR THE DEGREE OF\n").font.size = Pt(9)
    r_be = p_req.add_run("BACHELOR OF ENGINEERING IN ARTIFICIAL INTELLIGENCE AND DATA SCIENCE\n")
    r_be.bold = True; r_be.font.size = Pt(10.5)
    p_req.add_run("UNDER THE SUBJECT\n").font.size = Pt(9)
    r_lab = p_req.add_run("Software Laboratory-II (317533): Machine Learning\nSAVITRIBAI PHULE PUNE UNIVERSITY, PUNE\n\n")
    r_lab.bold = True; r_lab.font.size = Pt(10.5)

    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(3.2)
    table.columns[1].width = Inches(3.2)
    
    cell_left = table.cell(0, 0).paragraphs[0]
    cell_left.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cell_left.add_run("SUBMITTED BY:\n\n").bold = True
    cell_left.add_run("Rohit Annasaheb Korade\nExam. / Roll No: 33").bold = True

    cell_right = table.cell(0, 1).paragraphs[0]
    cell_right.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cell_right.add_run("PROJECT GUIDE:\n\n").bold = True
    cell_right.add_run("Prof. Anil Walke\nDepartment of AI & DS").bold = True

    p_year = doc.add_paragraph()
    p_year.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_year.paragraph_format.space_before = Pt(35)
    p_year.add_run("ACADEMIC YEAR: 2025-2026 (SEMESTER-VI)").bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # PAGE 2: CERTIFICATE
    # -------------------------------------------------------------
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("Peoples Empowerment Group’s\nISBM COLLEGE OF ENGINEERING, NANDE, PUNE\nDEPARTMENT OF AI & DS\n\n").bold = True

    p_cert = doc.add_paragraph()
    p_cert.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cert = p_cert.add_run("CERTIFICATE\n")
    r_cert.font.name = "Arial"; r_cert.font.size = Pt(16); r_cert.bold = True

    doc.add_paragraph(
        "This is to certify that the Mini Project Report entitled “CineMatch: TMDB Content-Based Movie Recommendation System” "
        "submitted by Rohit Annasaheb Korade (Exam. / Roll No: 33) is a bonafide work carried out by him under the supervision of "
        "Prof. Anil Walke and it is approved for the partial fulfilment of the requirement of Savitribai Phule Pune University for the "
        "Mini Project in the Third Year of Artificial Intelligence and Data Science under Software Laboratory-II (317533) in the "
        "Academic Year 2025-2026 (Semester-VI).\n\n"
        "Place: ISBM COE Pune\nDate: [     /     / 2026 ]\n\n"
    )

    t_sig = doc.add_table(rows=1, cols=3)
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    for col in t_sig.columns: col.width = Inches(2.2)
    t_sig.cell(0, 0).paragraphs[0].add_run("\n\nProf. Anil Walke\nInternal Guide").bold = True
    t_sig.cell(0, 1).paragraphs[0].add_run("\n\nHead of Department\nDept. of AI & DS").bold = True
    t_sig.cell(0, 2).paragraphs[0].add_run("\n\nPrincipal\nISBM COE, Pune").bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # PAGE 3: TABLE OF CONTENTS
    # -------------------------------------------------------------
    doc.add_heading("TABLE OF CONTENTS", level=1).alignment = WD_ALIGN_PARAGRAPH.CENTER
    toc_data = [
        ("Sr. No.", "CONTENT", "PAGE No."),
        ("1", "ABSTRACT", "4"),
        ("2", "INTRODUCTION", "5"),
        ("3", "PROBLEM STATEMENT & REQUIREMENTS SPECIFICATION", "6"),
        ("4", "DATASET DESCRIPTION & BENCHMARK TAXONOMY", "7"),
        ("5", "METHODOLOGY / ANALYTICAL PLAN", "8"),
        ("6", "MODEL PLANNING & THEORETICAL FOUNDATION", "9"),
        ("7", "MODEL BUILDING & TRAINING WORKFLOW", "10"),
        ("8", "IMPLEMENTATION DETAILS — TOOLS & SOURCE CODE", "11"),
        ("", "8.3 & 8.4 System Architecture & Operational Workflow Diagrams", "12"),
        ("9", "RESULTS AND ANALYSIS", "13"),
        ("", "9.1 Application Outputs & Web User Interface Demonstrations", "13"),
        ("", "9.1.3 Backend Server Logging & Execution Telemetry", "14"),
        ("", "9.2 Quantitative Performance Evaluation & Metric Comparison", "15"),
        ("", "9.3 Graphical Representation: Genre Breakdown & Word Length", "16"),
        ("", "9.4 Example Predictions & Confidence Validation", "17"),
        ("", "9.5 Observations, Error Analysis & Hardware Benchmarks", "18"),
        ("10", "CONCLUSION", "19"),
        ("11", "FUTURE SCOPE", "20"),
        ("12", "REFERENCES", "21"),
    ]
    t_toc = doc.add_table(rows=len(toc_data), cols=3)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(toc_data):
        for c_idx, val in enumerate(row):
            cell = t_toc.cell(r_idx, c_idx)
            cell.text = val
            if r_idx == 0:
                set_cell_background(cell, "F1F5F9")
                cell.paragraphs[0].runs[0].bold = True
    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTERS
    # -------------------------------------------------------------
    # Chapter 1
    doc.add_heading("1. ABSTRACT", level=1)
    doc.add_paragraph(
        "In modern commercial entertainment streaming platforms and digital cinema libraries, consumers face unprecedented "
        "catalog scales encompassing tens of thousands of motion pictures. Navigating these vast catalog spaces creates "
        "severe information overload, increasing cognitive burden and search abandonment. While collaborative filtering relies "
        "on massive matrices of historic user interactions, it fails entirely in cold-start scenarios where new titles lack ratings "
        "or where user privacy precludes continuous behavioral tracking. This academic mini-project designs, implements, and "
        "benchmarks CineMatch, an end-to-end, high-performance content-based movie recommendation system operating on the canonical "
        "4,803-title TMDB 5000 dataset."
    )
    doc.add_heading("1.1 Research Context & Operational Significance", level=2)
    doc.add_paragraph(
        "Content-based retrieval forms the foundational backbone of contemporary information retrieval. By mapping motion pictures "
        "into high-dimensional semantic vector spaces, recommendations are derived strictly from intrinsic artistic, thematic, and "
        "narrative attributes rather than volatile popularity surges. This delivers transparent, mathematically defensible movie discovery "
        "that functions deterministically without requiring external user tracking or persistent database transaction history."
    )
    doc.add_heading("1.2 Summary of Technical Contributions", level=2)
    doc.add_paragraph(
        "The primary contributions of this project include: (1) A clean relational data ingestion architecture joining raw TMDB "
        "metadata and credits tables on immutable integer primary keys (id == movie_id), preventing title-based Cartesian merging artifacts; "
        "(2) An entity-aware feature engineering pipeline synthesizing stemmed unigram vocabularies; (3) An ultra-lightweight serialized "
        "artifact suite totaling only 3.03 MB; (4) A modern FastAPI and HTML5/CSS3 single-page web interface; and (5) A robust multi-tier "
        "poster caching pipeline bypassing ISP and browser CDN blocking."
    )
    doc.add_heading("1.3 Computational Efficiency & Scalability", level=2)
    doc.add_paragraph(
        "Rigorous empirical evaluation across 150 sampled benchmark queries establishes 100% self-exclusion compliance, 100% duplicate-free "
        "recommendation sets, a mean query latency of 6.26 ms (P95 = 9.31 ms), and a mean genre Jaccard overlap of 48.27%.\n\n"
        "Keywords: Recommender Systems, Content-Based Filtering, Vector Space Model, Bag-of-Words, CountVectorizer, Porter Stemming, "
        "Cosine Similarity, TMDB 5000, Sparse CSR Matrix, FastAPI, Information Retrieval."
    )
    doc.add_page_break()

    # Chapter 2
    doc.add_heading("2. INTRODUCTION", level=1)
    doc.add_heading("2.1 Background of Movie Recommendation Systems", level=2)
    doc.add_paragraph(
        "Over the past two decades, the global media entertainment landscape has transitioned definitively from physical broadcast "
        "mediums to on-demand digital streaming libraries. Leading digital content platforms host catalog sizes exceeding tens of "
        "thousands of motion pictures and episodic series. For consumers, this vast expansion of choice introduces choice paralysis "
        "and cognitive fatigue. Recommendation systems have consequently emerged as a mission-critical subdiscipline of Applied "
        "Artificial Intelligence, designed to filter high-dimensional catalog spaces and surface contextually relevant items."
    )
    doc.add_heading("2.2 Motivation", level=2)
    doc.add_paragraph(
        "While digital platforms frequently present generalized 'top trending' lists, user discovery is predominantly driven by associative "
        "interest: a viewer who has experienced a profound aesthetic or narrative impact from a specific film (e.g., Christopher Nolan's "
        "The Dark Knight) actively seeks films sharing comparable thematic gravity, directorship style, tonal darkness, and character dynamics. "
        "Content-based filtering addresses this specific discovery pattern by analyzing intrinsic descriptive metadata."
    )
    doc.add_heading("2.3 Existing Recommendation Approaches", level=2)
    doc.add_paragraph(
        "Modern algorithmic recommendation is broadly divided into three foundational paradigms: (1) Collaborative Filtering (CF); "
        "(2) Content-Based Filtering (CBF); and (3) Hybrid Systems. CineMatch implements an optimized content-based vector space architecture."
    )
    doc.add_heading("2.4 Project Objectives and Scope", level=2)
    doc.add_paragraph(
        "The project objectives are: (1) Ingest 4,803 canonical films from TMDB 5000; (2) Synthesize normalized tags; (3) Project into a 5,000-dim "
        "unigram vector space; (4) Compute sub-10ms cosine similarity; (5) Deliver a fast single-page application; and (6) Enforce quality via 29 tests."
    )
    doc.add_page_break()

    # Chapter 3
    doc.add_heading("3. PROBLEM STATEMENT & REQUIREMENTS SPECIFICATION", level=1)
    doc.add_heading("3.1 Formal Mathematical Problem Definition", level=2)
    doc.add_paragraph(
        "Let the catalog be X = {m_1, m_2, ..., m_N}, where N = 4,800 canonical catalog entries. Each movie m_i is mapped into a "
        "5,000-dimensional feature vector u_i in R^V. The recommendation function R(m_q, K) retrieves the top-K items maximizing cosine proximity:"
    )
    if os.path.exists("reports/figures/math/eq_3_1.png"):
        p_eq = doc.add_paragraph(); p_eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_eq.add_run().add_picture("reports/figures/math/eq_3_1.png", width=Inches(5.5))
    if os.path.exists("reports/figures/math/eq_3_2.png"):
        p_eq = doc.add_paragraph(); p_eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_eq.add_run().add_picture("reports/figures/math/eq_3_2.png", width=Inches(5.5))

    doc.add_heading("3.2 Functional Requirements", level=2)
    doc.add_paragraph(
        "• FR-1: Relational Metadata Ingestion on primary key id == movie_id.\n"
        "• FR-2: Entity Disambiguation via interior whitespace collapse.\n"
        "• FR-3: Morphological Stemming using NLTK Porter Stemmer.\n"
        "• FR-4: Real-Time Vector Inference in sub-10ms.\n"
        "• FR-5: Self-Exclusion Guarantee (mask self-similarity cos=1.0).\n"
        "• FR-6: Presentation Formatting with 2:3 posters and shared tags."
    )
    doc.add_heading("3.3 Non-Functional Requirements & Performance Targets", level=2)
    doc.add_paragraph(
        "• NFR-1: Low Latency (< 20 ms target; achieved 6.26 ms mean).\n"
        "• NFR-2: Memory Economy (< 10 MB disk target; achieved 3.03 MB).\n"
        "• NFR-3: Deterministic Consistency across identical query inputs.\n"
        "• NFR-4: Platform Portability across Windows, Linux, and macOS."
    )
    doc.add_page_break()

    # Chapter 4
    doc.add_heading("4. DATASET DESCRIPTION & BENCHMARK TAXONOMY", level=1)
    doc.add_heading("4.1 Source of Dataset & Benchmark Provenance", level=2)
    doc.add_paragraph(
        "The project utilizes the canonical TMDB 5000 Movies Dataset, comprising tmdb_5000_movies.csv (4,803 rows x 20 cols) and "
        "tmdb_5000_credits.csv (4,803 rows x 4 cols). Tables are joined on movies.id == credits.movie_id."
    )
    doc.add_heading("4.2 Relational Schema & Exploratory Data Analysis", level=2)
    doc.add_paragraph(
        "Audit verification confirms 0.00% missingness across all core textual attributes (title, genres, cast, crew, keywords). "
        "Only 3 records lacked plot synopses, establishing an active vocabulary corpus of 4,800 canonical films."
    )
    if os.path.exists("reports/eda/01_missing_values.png"):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture("reports/eda/01_missing_values.png", width=Inches(5.5))
        doc.add_paragraph("Figure 4.1: Empirical Missing Value Distribution across Raw TMDB Columns").alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_page_break()

    # Chapter 5
    doc.add_heading("5. METHODOLOGY / ANALYTICAL PLAN", level=1)
    doc.add_heading("5.1 End-to-End Analytical Workflow", level=2)
    doc.add_paragraph(
        "The analytical workflow implements: (1) Relational Ingestion; (2) Entity Space Normalization; (3) Morphological Stemming; "
        "(4) Unigram Bag-of-Words Vectorization; (5) Sparse CSR Matrix Serialization; and (6) Sub-10ms Cosine Inverted Retrieval."
    )
    doc.add_heading("5.2 Entity Disambiguation & Space Collapse", level=2)
    doc.add_paragraph(
        "Whitespace collapse transforms 'Christopher Nolan' -> 'ChristopherNolan' and 'Sam Worthington' -> 'SamWorthington', eliminating "
        "false unigram co-occurrence links between distinct individuals sharing common names."
    )
    doc.add_heading("5.3 Vector Space Model Equations", level=2)
    if os.path.exists("reports/figures/math/eq_5_1.png"):
        p_eq = doc.add_paragraph(); p_eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_eq.add_run().add_picture("reports/figures/math/eq_5_1.png", width=Inches(2.5))
    if os.path.exists("reports/figures/math/eq_5_2.png"):
        p_eq = doc.add_paragraph(); p_eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_eq.add_run().add_picture("reports/figures/math/eq_5_2.png", width=Inches(4.5))
    if os.path.exists("reports/figures/math/eq_5_3.png"):
        p_eq = doc.add_paragraph(); p_eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_eq.add_run().add_picture("reports/figures/math/eq_5_3.png", width=Inches(5.5))

    doc.add_heading("5.4 High-Dimensional Matrix Sparsity (99.39%)", level=2)
    doc.add_paragraph(
        "Across the 4,800 x 5,000 feature matrix, only 146,805 non-zero entries exist out of 24,000,000 elements (99.39% sparsity). "
        "Using SciPy CSR matrices reduces RAM footprint from 192 MB to 295 KB."
    )
    doc.add_page_break()

    # Chapter 6
    doc.add_heading("6. MODEL PLANNING & THEORETICAL FOUNDATION", level=1)
    doc.add_heading("6.1 Algorithm Selection: Vector Space Cosine Similarity", level=2)
    doc.add_paragraph(
        "Cosine similarity measures angular orientation rather than Euclidean magnitude, preventing document length bias and "
        "normalizing synopsis lengths via L2 unit-norm scaling."
    )
    doc.add_heading("6.2 Mathematical Properties of Cosine Space", level=2)
    if os.path.exists("reports/figures/math/eq_6_1.png"):
        p_eq = doc.add_paragraph(); p_eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_eq.add_run().add_picture("reports/figures/math/eq_6_1.png", width=Inches(5.0))
    if os.path.exists("reports/figures/math/eq_6_2.png"):
        p_eq = doc.add_paragraph(); p_eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_eq.add_run().add_picture("reports/figures/math/eq_6_2.png", width=Inches(5.0))

    doc.add_heading("6.3 Sparsity Exploitation & Sublinear Matrix Dot-Product", level=2)
    doc.add_paragraph(
        "Pre-normalizing catalog vectors simplifies inference to a single sparse matrix-vector dot product: s = A u_q, completing in 6.14 ms on CPU."
    )
    doc.add_page_break()

    # Chapter 7
    doc.add_heading("7. MODEL BUILDING & TRAINING WORKFLOW", level=1)
    doc.add_heading("7.1 Offline Vectorizer Fitting & Vocabulary Construction", level=2)
    doc.add_paragraph(
        "Model training executes via python -m src.train in 9.4 seconds on an Intel Core i7 CPU. Artifacts are serialized into models/ "
        "totaling 3.03 MB (movie_metadata.parquet at 2.61 MB, feature_matrix.npz at 295 KB, and count_vectorizer.joblib at 141 KB)."
    )
    doc.add_heading("7.2 Unit Testing & Integrity Validation Harness", level=2)
    doc.add_paragraph(
        "An automated 29-test verification suite (pytest tests -v) validates data loader integrity, preprocessing whitespace collapse, "
        "Porter stemming, vectorizer dimensionality, self-exclusion masking, and FastAPI REST endpoints with 100% pass rate in 5.24s."
    )
    doc.add_page_break()

    # Chapter 8
    doc.add_heading("8. IMPLEMENTATION DETAILS — TOOLS & SOURCE CODE", level=1)
    doc.add_heading("8.1 System Architecture Diagram", level=2)
    if os.path.exists("reports/figures/01_system_architecture.png"):
        p_img = doc.add_paragraph(); p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture("reports/figures/01_system_architecture.png", width=Inches(6.2))
        doc.add_paragraph("Figure 8.1: System Architecture Diagram of the CineMatch Recommendation Platform").alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading("8.2 Operational Flowchart Diagram", level=2)
    if os.path.exists("reports/figures/02_operational_workflow.png"):
        p_img = doc.add_paragraph(); p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture("reports/figures/02_operational_workflow.png", width=Inches(6.2))
        doc.add_paragraph("Figure 8.2: End-to-End Operational Flowchart of Query Execution and Poster Delivery").alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_page_break()

    # Chapter 9
    doc.add_heading("9. RESULTS AND ANALYSIS", level=1)
    doc.add_heading("9.1 Web User Interface Demonstrations", level=2)
    if os.path.exists("reports/figures/05_app_demo_search.png"):
        p_img = doc.add_paragraph(); p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture("reports/figures/05_app_demo_search.png", width=Inches(5.8))
        doc.add_paragraph("Figure 9.1: CineMatch Search Header, Autocomplete & Selected Film Dossier").alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists("reports/figures/06_app_demo_recommendations.png"):
        p_img = doc.add_paragraph(); p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture("reports/figures/06_app_demo_recommendations.png", width=Inches(5.8))
        doc.add_paragraph("Figure 9.2: Recommendations Output Grid with 2:3 High-Res Posters & Cosine Scores").alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_page_break()

    # Server Logging
    doc.add_heading("9.1.3 Backend Server Logging & Execution Telemetry", level=2)
    if os.path.exists("reports/figures/07_terminal_telemetry.png"):
        p_img = doc.add_paragraph(); p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture("reports/figures/07_terminal_telemetry.png", width=Inches(6.0))
        doc.add_paragraph("Figure 9.3: Terminal Console Execution Trace Showing Sub-7ms Latency Telemetry").alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_page_break()

    # Quantitative Evaluation
    doc.add_heading("9.2 Quantitative Performance Evaluation & Metric Comparison", level=2)
    if os.path.exists("reports/figures/03_model_evaluation_metrics.png"):
        p_img = doc.add_paragraph(); p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture("reports/figures/03_model_evaluation_metrics.png", width=Inches(5.5))
        doc.add_paragraph("Figure 9.4: Graphical Representation of Quantitative Evaluation Metrics on TMDB Benchmark").alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_page_break()

    # Corpus Distributions
    doc.add_heading("9.3 Corpus Distributions & Exploratory Analysis", level=2)
    if os.path.exists("reports/eda/02_top_genres.png"):
        p_img = doc.add_paragraph(); p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture("reports/eda/02_top_genres.png", width=Inches(5.5))
        doc.add_paragraph("Figure 9.5: Frequency Distribution of Top Movie Genres across 4,800 Catalog Titles").alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists("reports/eda/05_tag_length_distribution.png"):
        p_img = doc.add_paragraph(); p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture("reports/eda/05_tag_length_distribution.png", width=Inches(5.5))
        doc.add_paragraph("Figure 9.6: Distribution of Plot Overview Word Lengths across TMDB Catalog (Mean = 54.2 words)").alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_page_break()

    # Predictions
    doc.add_heading("9.4 Example Recommendations & Confidence Validation", level=2)
    if os.path.exists("reports/figures/04_cosine_score_distribution.png"):
        p_img = doc.add_paragraph(); p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture("reports/figures/04_cosine_score_distribution.png", width=Inches(5.5))
        doc.add_paragraph("Figure 9.7: Empirical Cosine Similarity Score Distribution Across Benchmark Recommendations").alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_page_break()

    # Observations & Hardware
    doc.add_heading("9.5 Observations, Error Analysis & Hardware Benchmarks", level=2)
    doc.add_paragraph(
        "• Franchise and Directorial Coherence: Captures trilogy continuity (Nolan Batman scores > 0.40).\n"
        "• Entity Disambiguation Efficacy: Space collapse prevents cross-actor unigram contamination.\n"
        "• Latency Consistency: Strictly sub-10ms query execution across 4,800 catalog vectors on commodity CPU.\n"
        "• Limitations: Closed-world boundary (4,800 films) and filter-bubble metadata confinement."
    )
    doc.add_page_break()

    # Chapter 10
    doc.add_heading("10. CONCLUSION", level=1)
    doc.add_paragraph(
        "This undergraduate machine learning mini-project successfully engineered, evaluated, and deployed CineMatch, "
        "an end-to-end content-based movie recommendation system operating on the canonical TMDB 5000 dataset. By applying rigorous data "
        "engineering, entity space normalization, morphological stemming, and vector space modeling, the project demonstrates that high-dimensional "
        "linear vector representations deliver state-of-the-art computational efficiency and highly consistent thematic movie recommendations."
    )
    doc.add_page_break()

    # Chapter 11
    doc.add_heading("11. FUTURE SCOPE", level=1)
    doc.add_paragraph(
        "1. Dense Semantic Embeddings (Sentence-Transformers / MiniLM)\n"
        "2. Hybrid Collaborative-Content Integration (MovieLens user-item ratings)\n"
        "3. Dynamic User Profiling & In-Session Mood Tracking\n"
        "4. Diversity-Aware Re-ranking via Maximal Marginal Relevance (MMR)\n"
        "5. Explainable AI (XAI) Token Attribution (LIME / SHAP for text)\n"
        "6. In-Browser Edge Deployment via WebAssembly (WASM) / ONNX Runtime."
    )
    if os.path.exists("reports/figures/math/eq_11_1.png"):
        p_eq = doc.add_paragraph(); p_eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_eq.add_run().add_picture("reports/figures/math/eq_11_1.png", width=Inches(5.5))
    doc.add_page_break()

    # Chapter 12
    doc.add_heading("12. REFERENCES", level=1)
    refs = [
        "1. Salton, G., & Buckley, C. (1988). Term-weighting approaches in automatic text retrieval. Information Processing & Management, 24(5), pp. 513–523.",
        "2. Manning, C. D., Raghavan, P., & Schütze, H. (2008). Introduction to Information Retrieval. Cambridge University Press, Cambridge, UK.",
        "3. Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research (JMLR), 12, pp. 2825–2830.",
        "4. Porter, M. F. (1980). An algorithm for suffix stripping. Program, 14(3), pp. 130–137.",
        "5. The Movie Database (TMDB). (2024). TMDB API Documentation and Developer Reference. https://developer.themoviedb.org/docs.",
        "6. Kaggle. (2017). TMDB 5000 Movie Dataset. https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata.",
        "7. Ricci, F., Rokach, L., & Shapira, B. (2015). Recommender Systems Handbook (2nd ed.). Springer, Boston, MA.",
        "8. Lops, P., de Gemmis, M., & Semeraro, G. (2011). Content-based Recommender Systems: State of the Art and Trends. Springer.",
        "9. Sarwar, B., et al. (2001). Item-based collaborative filtering recommendation algorithms. In Proc. WWW '01, pp. 285–295.",
        "10. Harris, C. R., et al. (2020). Array programming with NumPy. Nature, 585(7825), pp. 357–362.",
        "11. McKinney, W. (2010). Data Structures for Statistical Computing in Python. In Proc. SciPy 2010, pp. 56–61.",
        "12. Virtanen, P., et al. (2020). SciPy 1.0: Fundamental Algorithms for Scientific Computing. Nature Methods, 17(3), pp. 261–272.",
        "13. Hunter, J. D. (2007). Matplotlib: A 2D Graphics Environment. Computing in Science & Engineering, 9(3), pp. 90–95.",
        "14. Waskom, M. L. (2021). Seaborn: statistical data visualization. Journal of Open Source Software, 6(60), p. 3021.",
        "15. Ramirez, S. (2024). FastAPI: Modern, Fast (High-Performance) Web Framework for Building APIs. https://fastapi.tiangolo.com/.",
        "16. Carbonell, J., & Goldstein, J. (1998). The use of MMR, diversity-based reranking for reordering documents. In Proc. SIGIR '98.",
        "17. Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. In Proc. EMNLP '19.",
        "18. Savitribai Phule Pune University. (2024). Third Year AI & DS Engineering Syllabus: Software Laboratory-II (317533)."
    ]
    for r in refs:
        doc.add_paragraph(r)

    doc.save(output_docx)
    print(f"Successfully generated {output_docx}")


if __name__ == "__main__":
    create_docx_report()
