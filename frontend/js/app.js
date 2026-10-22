/**
 * CineMatch — TMDB Content-Based Recommendation Engine
 * Editorial Cinema Interface Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  // DOM References
  const searchInput = document.getElementById('movie-search-input');
  const btnRecommend = document.getElementById('btn-recommend');
  const autocompleteDropdown = document.getElementById('autocomplete-dropdown');
  const kSlider = document.getElementById('k-slider');
  const kValDisplay = document.getElementById('k-val-display');
  const toggleExplanations = document.getElementById('toggle-explanations');
  const filmPills = document.querySelectorAll('.film-pill');

  const loadingSpinner = document.getElementById('loading-spinner');
  const errorMessage = document.getElementById('error-message');
  const selectedMovieSection = document.getElementById('selected-movie-section');
  const recommendationsSection = document.getElementById('recommendations-section');
  const recommendationsGrid = document.getElementById('recommendations-grid');
  const resultsCountBadge = document.getElementById('results-count');

  // Hero Profile Elements
  const heroPoster = document.getElementById('hero-poster-img');
  const heroTitle = document.getElementById('hero-movie-title');
  const heroYear = document.getElementById('hero-year');
  const heroRating = document.getElementById('hero-rating');
  const heroGenres = document.getElementById('hero-genres');
  const heroDirector = document.getElementById('hero-director');
  const heroCast = document.getElementById('hero-cast');
  const heroSynopsis = document.getElementById('hero-synopsis');

  // Navigation Tabs
  const navLinks = document.querySelectorAll('.nav-link');
  const tabViews = document.querySelectorAll('.tab-view');

  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      navLinks.forEach(b => b.classList.remove('active'));
      tabViews.forEach(v => v.classList.remove('active'));

      link.classList.add('active');
      const targetTabId = link.getAttribute('data-tab');
      const targetView = document.getElementById(targetTabId);
      if (targetView) {
        targetView.classList.add('active');
      }

      if (targetTabId === 'tab-architecture') {
        fetchSystemSpecs();
      }
    });
  });

  // Slider Input
  kSlider.addEventListener('input', (e) => {
    kValDisplay.textContent = e.target.value;
  });

  // Curated Reference Pills
  filmPills.forEach(pill => {
    pill.addEventListener('click', () => {
      const title = pill.getAttribute('data-title');
      searchInput.value = title;
      fetchRecommendations(title);
    });
  });

  // Recommend Button Click
  btnRecommend.addEventListener('click', () => {
    const query = searchInput.value.trim();
    if (query) {
      fetchRecommendations(query);
    }
  });

  // Enter Key on Search Input
  searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      const query = searchInput.value.trim();
      if (query) {
        autocompleteDropdown.classList.add('hidden');
        fetchRecommendations(query);
      }
    }
  });

  // Autocomplete Query Debounce
  let debounceTimer = null;
  searchInput.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    const query = searchInput.value.trim();
    if (query.length < 2) {
      autocompleteDropdown.innerHTML = '';
      autocompleteDropdown.classList.add('hidden');
      return;
    }

    debounceTimer = setTimeout(async () => {
      try {
        const resp = await fetch(`/api/movies?q=${encodeURIComponent(query)}&limit=8`);
        const data = await resp.json();
        if (data.movies && data.movies.length > 0) {
          renderAutocomplete(data.movies);
        } else {
          autocompleteDropdown.innerHTML = '<div class="autocomplete-item"><span class="autocomplete-title" style="color: var(--text-muted);">No matching titles found in catalog</span></div>';
          autocompleteDropdown.classList.remove('hidden');
        }
      } catch (err) {
        console.error('Autocomplete query error:', err);
      }
    }, 220);
  });

  // Render Autocomplete Dropdown
  function renderAutocomplete(movies) {
    autocompleteDropdown.innerHTML = '';
    movies.forEach(m => {
      const item = document.createElement('div');
      item.className = 'autocomplete-item';
      const year = m.release_year && m.release_year > 0 ? m.release_year : 'N/A';
      item.innerHTML = `
        <span class="autocomplete-title">${m.title}</span>
        <span class="autocomplete-meta">${year} &bull; ★ ${m.vote_average.toFixed(1)}</span>
      `;
      item.addEventListener('click', () => {
        searchInput.value = m.title;
        autocompleteDropdown.classList.add('hidden');
        fetchRecommendations(m.title);
      });
      autocompleteDropdown.appendChild(item);
    });
    autocompleteDropdown.classList.remove('hidden');
  }

  // Dismiss dropdown on outside click
  document.addEventListener('click', (e) => {
    if (!searchInput.contains(e.target) && !autocompleteDropdown.contains(e.target)) {
      autocompleteDropdown.classList.add('hidden');
    }
  });

  // Fetch Recommendations API
  async function fetchRecommendations(title) {
    autocompleteDropdown.classList.add('hidden');
    errorMessage.classList.add('hidden');
    errorMessage.textContent = '';
    loadingSpinner.classList.remove('hidden');
    selectedMovieSection.classList.add('hidden');
    recommendationsSection.classList.add('hidden');

    const topK = parseInt(kSlider.value, 10) || 5;

    try {
      const resp = await fetch(`/api/recommend/${encodeURIComponent(title)}?top_k=${topK}`);
      if (!resp.ok) {
        const errData = await resp.json();
        throw new Error(errData.detail || `Server returned HTTP ${resp.status}`);
      }

      const data = await resp.json();
      renderHeroProfile(data.query_movie);
      renderRecommendationsGrid(data.recommendations);
    } catch (err) {
      errorMessage.textContent = `Catalog query error: ${err.message}`;
      errorMessage.classList.remove('hidden');
    } finally {
      loadingSpinner.classList.add('hidden');
    }
  }

  // Render Selected Query Film Dossier
  function renderHeroProfile(movie) {
    heroTitle.textContent = movie.title;
    heroYear.textContent = movie.release_year && movie.release_year > 0 ? movie.release_year : 'Archive';
    heroRating.textContent = `★ ${movie.vote_average.toFixed(1)} / 10`;

    // Safe poster image loading with typographic fallback
    heroPoster.onerror = () => {
      heroPoster.onerror = null;
      heroPoster.src = generateClientFallbackSvg(movie.title, movie.release_year, movie.genres ? movie.genres[0] : null);
    };
    heroPoster.src = movie.poster_url;

    heroDirector.textContent = movie.director || 'Unknown';
    heroCast.textContent = movie.top_cast && movie.top_cast.length > 0 ? movie.top_cast.join(', ') : 'Not cataloged';
    heroSynopsis.textContent = movie.overview || 'No synopsis recorded in TMDB archive.';

    // Genres
    heroGenres.innerHTML = '';
    if (movie.genres && Array.isArray(movie.genres)) {
      movie.genres.slice(0, 4).forEach(g => {
        const chip = document.createElement('span');
        chip.className = 'genre-chip';
        chip.textContent = g;
        heroGenres.appendChild(chip);
      });
    }

    selectedMovieSection.classList.remove('hidden');
  }

  // Render Recommendations Cards
  function renderRecommendationsGrid(recommendations) {
    recommendationsGrid.innerHTML = '';
    resultsCountBadge.textContent = `K=${recommendations.length} Titles`;

    const showExpl = toggleExplanations.checked;

    recommendations.forEach(rec => {
      const card = document.createElement('div');
      card.className = 'film-card';
      card.tabIndex = 0;

      // Shared lexical tags explanation
      let sharedContextHtml = '';
      if (showExpl && rec.common_tags && rec.common_tags.length > 0) {
        const tags = rec.common_tags.slice(0, 4).map(t => `<span class="shared-chip">${t}</span>`).join('');
        sharedContextHtml = `
          <div class="shared-context-box">
            <span class="shared-context-label">Shared Attributes:</span>
            <div class="shared-chips">${tags}</div>
          </div>
        `;
      }

      const genresText = rec.genres && rec.genres.length > 0 ? rec.genres.slice(0, 2).join(' &bull; ') : 'Feature';
      const yearText = rec.release_year && rec.release_year > 0 ? rec.release_year : 'Archive';
      const simScore = typeof rec.cosine_similarity === 'number' ? rec.cosine_similarity.toFixed(3) : (rec.similarity_percentage ? (rec.similarity_percentage / 100).toFixed(3) : '0.000');

      card.innerHTML = `
        <div class="film-card-poster-wrap">
          <img 
            src="${rec.poster_url}" 
            alt="${rec.title} poster" 
            class="film-card-poster" 
            loading="lazy"
          >
          <div class="film-card-score-badge" title="Vector space cosine similarity metric">
            <span class="score-metric-name">Similarity</span>
            <span class="score-metric-val">${simScore}</span>
          </div>
        </div>
        <div class="film-card-body">
          <h4 class="film-card-title">${rec.title}</h4>
          <div class="film-card-meta">
            <span>${yearText} &bull; ${genresText}</span>
            <span class="card-rating">★ ${rec.vote_average.toFixed(1)}</span>
          </div>
          <div class="film-card-director">
            Dir: ${rec.director || 'Unknown'}
          </div>
          ${sharedContextHtml}
        </div>
      `;

      // Handle broken images gracefully with intentional typographic fallback
      const imgElem = card.querySelector('.film-card-poster');
      imgElem.onerror = () => {
        imgElem.onerror = null;
        imgElem.src = generateClientFallbackSvg(rec.title, rec.release_year, rec.genres ? rec.genres[0] : null);
      };

      // Click card to pivot recommendation query
      card.addEventListener('click', () => {
        searchInput.value = rec.title;
        fetchRecommendations(rec.title);
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });

      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          searchInput.value = rec.title;
          fetchRecommendations(rec.title);
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      });

      recommendationsGrid.appendChild(card);
    });

    recommendationsSection.classList.remove('hidden');
  }

  // Client-side Typographic Archival Fallback SVG
  function generateClientFallbackSvg(title, year, genre) {
    const cleanTitle = (title || 'Feature Film').substring(0, 28)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&apos;');
    const yr = year && year > 0 ? year : 'ARCHIVE';
    const gn = (genre || 'CINEMA').toUpperCase().replace(/&/g, '&amp;');
    const svg = `
      <svg xmlns='http://www.w3.org/2000/svg' width='500' height='750' viewBox='0 0 500 750'>
        <rect width='500' height='750' fill='#12141a'/>
        <rect x='20' y='20' width='460' height='710' fill='none' stroke='#222634' stroke-width='1.5'/>
        <rect x='28' y='28' width='444' height='694' fill='none' stroke='#1a1d28' stroke-width='1'/>
        <text x='250' y='68' fill='#c99a5b' font-family='Georgia, serif' font-size='12' font-weight='600' letter-spacing='4' text-anchor='middle'>CINEMATCH ARCHIVE</text>
        <line x1='190' y1='82' x2='310' y2='82' stroke='#c99a5b' stroke-width='0.75' stroke-opacity='0.4'/>
        <text x='250' y='360' fill='#f4f1ea' font-family='Georgia, serif' font-size='24' font-weight='500' text-anchor='middle'>${cleanTitle}</text>
        <line x1='200' y1='620' x2='300' y2='620' stroke='#3a3f50' stroke-width='1'/>
        <text x='250' y='650' fill='#8a909d' font-family='sans-serif' font-size='13' letter-spacing='2.5' text-anchor='middle'>${yr} &#8226; ${gn}</text>
      </svg>
    `.trim();
    return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`;
  }

  // Fetch Live Diagnostics for Telemetry Tab
  async function fetchSystemSpecs() {
    try {
      const resp = await fetch('/api/stats');
      if (resp.ok) {
        const stats = await resp.json();
        document.getElementById('spec-catalog').textContent = stats.catalog_size.toLocaleString();
        document.getElementById('spec-vocab').textContent = stats.vocabulary_size.toLocaleString();
        if (stats.training_metadata && stats.training_metadata.matrix_sparsity) {
          document.getElementById('spec-sparsity').textContent = (stats.training_metadata.matrix_sparsity * 100).toFixed(2) + '%';
        }
      }
    } catch (err) {
      console.error('Failed to fetch telemetry specs:', err);
    }
  }

  // Initial Seed Discovery Query: The Dark Knight
  fetchRecommendations('The Dark Knight');
});
