# Feature Engineering & Representation Methodology

**Project**: CineMatch — TMDB Content-Based Movie Recommendation System  
**Date**: October 22, 2026  
**Reference**: CampusX TMDB Recommender Methodology  

---

## 1. Feature Selection Rationalization

In strict accordance with the CampusX methodology, only content-bearing textual and categorical metadata attributes are selected for computing semantic movie similarities:
1. **`genres`**: The thematic classifications of the movie (e.g., Action, Science Fiction, Thriller).
2. **`keywords`**: Topic and plot descriptors assigned by editors and users (e.g., culture clash, space travel, alien).
3. **`overview`**: The synopsis summarizing the narrative premise.
4. **`cast`**: The top 3 credited actors (billing order 0, 1, 2), capturing leading star power and tone.
5. **`crew`**: The film Director (`job == 'Director'`), representing the primary creative and stylistic visionary.

### Explicitly Excluded Fields:
- `budget`, `revenue`: Financial metrics that do not indicate narrative or thematic content similarity.
- `popularity`, `vote_average`, `vote_count`: Behavioral and quality metrics. Including these would introduce popularity bias rather than content similarity.
- `release_date`: While valuable for contextual display and homonym disambiguation, release date is excluded from the text vectorizer to avoid biasing recommendations purely toward contemporary films.
- `movie_id`, `id`: Database keys with no semantic meaning.

---

## 2. Structured Metadata Parsing & Entity Disambiguation

Raw columns (`genres`, `keywords`, `cast`, `crew`) are stored as JSON-serialized lists of key-value dictionaries.

### 2.1 Extraction Logic
- **Genres & Keywords**: All item `"name"` attributes are parsed via `safe_literal_eval()`.
- **Cast**: Truncated to the first 3 items:
  $$\text{cast}_{\text{selected}} = [a_0, a_1, a_2]$$
- **Crew**: Filtered for director role:
  $$\text{directors} = [c.\text{name} \mid c \in \text{crew}, c.\text{job} = \text{'Director'}]$$

### 2.2 Whitespace Collapse for Named Entity Integrity
A crucial innovation in the reference methodology is interior whitespace removal:
$$\text{collapse}(\text{"Sam Worthington"}) \rightarrow \text{"SamWorthington"}$$
$$\text{collapse}(\text{"Sam Mendes"}) \rightarrow \text{"SamMendes"}$$

**Why this is necessary**:
A standard unigram `CountVectorizer` splits text on whitespace. If left uncollapsed:
- `"Sam Worthington"` yields tokens `['sam', 'worthington']`.
- `"Sam Mendes"` yields tokens `['sam', 'mendes']`.
The common token `'sam'` would generate false similarity between a sci-fi blockbuster starring Sam Worthington (*Avatar*) and a British drama directed by Sam Mendes (*American Beauty*).
Collapsing spaces ensures that each person or multi-word genre becomes an atomic unigram token.

---

## 3. Tag Combination & Stemming

### 3.1 Synthesis Equation
For each movie $i$, the final content profile $\text{tags}_i$ is synthesized by concatenating token lists:
$$\text{tags}_i = \text{overview\_tokens}_i + \text{genres\_collapsed}_i + \text{keywords\_collapsed}_i + \text{cast\_collapsed}_i + \text{crew\_collapsed}_i$$

The resulting sequence of tokens is joined by spaces into a single normalized lowercase document.

### 3.2 Morphological Normalization (Porter Stemming)
Words across overviews frequently appear in differing inflected forms (e.g., *dance*, *dancing*, *danced*; *alien*, *aliens*).
To collapse these into canonical lexical stems, CineMatch applies the Porter Stemming algorithm:
$$\text{stem}(\text{"actions"}) \rightarrow \text{"action"}$$
$$\text{stem}(\text{"adventures"}) \rightarrow \text{"adventur"}$$
$$\text{stem}(\text{"directing"}) \rightarrow \text{"direct"}$$

---

## 4. Vector Space Representation

The synthesized documents are vectorized into a Bag-of-Words representation using Scikit-Learn's `CountVectorizer`:
- **Vocabulary Size**: $V = 5,000$ most frequent unigrams across the corpus.
- **Stopwords**: Standard English stopword removal (`stop_words='english'`).
- **Binary / Count**: Term frequency counts within each movie profile.
- **Matrix Dimension**: $N \times V = 4,800 \times 5,000$.
- **Matrix Sparsity**: $> 98.5\%$ sparse, making compressed sparse row (`scipy.sparse.csr_matrix`) representations highly memory efficient.
