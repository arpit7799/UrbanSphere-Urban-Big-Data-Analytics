/**
 * UrbanSphere Frontend — API Service
 * Connects directly to FastAPI backend (/api/v1)
 */

class UrbanSphereAPI {
  constructor(baseUrl = '') {
    // If hosted on same origin as backend, baseUrl can be empty or relative
    this.baseUrl = baseUrl || (window.location.origin.includes(':8000') ? '' : 'http://localhost:8000');
    this.apiPrefix = `${this.baseUrl}/api/v1`;
  }

  async fetchJson(endpoint, options = {}) {
    try {
      const url = `${this.apiPrefix}${endpoint}`;
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API Error ${response.status}: ${errorText}`);
      }

      const json = await response.json();
      return json;
    } catch (err) {
      console.warn(`Fetch error for ${endpoint}:`, err);
      throw err;
    }
  }

  // 1. Health & Metadata
  async getHealth() {
    return this.fetchJson('/health');
  }

  async getMetadataSummary() {
    return this.fetchJson('/metadata/summary');
  }

  // 2. Geography
  async getGeographySectors() {
    return this.fetchJson('/geography/sectors');
  }

  async getTransitCorridors() {
    return this.fetchJson('/geography/corridors');
  }

  // 3. Traffic
  async getTrafficCorridors() {
    return this.fetchJson('/traffic/corridors');
  }

  async getVehicleModalSplit() {
    return this.fetchJson('/traffic/modal-split');
  }

  async getTrafficLocations() {
    return this.fetchJson('/traffic/locations');
  }

  // 4. Weather
  async getMonthlyClimate() {
    return this.fetchJson('/weather/monthly');
  }

  async getWindDispersion() {
    return this.fetchJson('/weather/wind-dispersion');
  }

  // 5. Air Quality
  async getSeasonalAirQuality(locality = null) {
    const query = locality ? `?locality=${encodeURIComponent(locality)}` : '';
    return this.fetchJson(`/air-quality/seasonal${query}`);
  }

  async getDailyTimeline(locality = null, year = null, limit = 50, offset = 0) {
    const params = new URLSearchParams();
    if (locality) params.append('locality', locality);
    if (year) params.append('year', year);
    params.append('limit', limit);
    params.append('offset', offset);
    return this.fetchJson(`/air-quality/daily-timeline?${params.toString()}`);
  }

  // 6. Analytics & Machine Learning
  async getClusters() {
    return this.fetchJson('/analytics/clusters');
  }

  async getAnomalies(phenotype = null, limit = 50) {
    const params = new URLSearchParams();
    if (phenotype) params.append('phenotype', phenotype);
    params.append('limit', limit);
    return this.fetchJson(`/analytics/anomalies?${params.toString()}`);
  }

  async getCorrelations(subset = null) {
    const query = subset ? `?subset=${encodeURIComponent(subset)}` : '';
    return this.fetchJson(`/analytics/correlations${query}`);
  }

  async getFeatureImportances() {
    return this.fetchJson('/analytics/feature-importances');
  }

  // 7. Live Machine Learning Predictions
  async predictAQI(weatherData) {
    return this.fetchJson('/predict/aqi', {
      method: 'POST',
      body: JSON.stringify(weatherData),
    });
  }

  async predictRegime(pollutantData) {
    return this.fetchJson('/predict/regime', {
      method: 'POST',
      body: JSON.stringify(pollutantData),
    });
  }
}

export const api = new UrbanSphereAPI();

