/**
 * UrbanSphere Frontend — Reports & System Synthesis View
 */

export class ReportsView {
  constructor(appState) {
    this.appState = appState;
  }

  async render(container) {
    container.innerHTML = `
      <div class="view-header">
        <div class="view-header-titles">
          <h2>📑 Analytical Reports & Executive Summaries</h2>
          <p>Scientific publications, comprehensive EDA notebook documentation, and architecture audits</p>
        </div>
      </div>

      <div class="two-col-grid">
        <div class="card">
          <div class="card-header">
            <div class="card-title-group">
              <span style="font-size: 16px;">📓</span>
              <h3>Exploratory Data Analysis Notebook</h3>
            </div>
            <span class="kpi-badge badge-good">13 Sections Executed</span>
          </div>
          <div class="card-body">
            <p style="font-size: 13px; color: var(--text-muted); line-height: 1.5;">
              The canonical EDA notebook <code>notebooks/01_urban_data_exploration.ipynb</code> contains the complete 13-section empirical profiling of Gurugram across mobility, meteorology, air quality, and spatial topology.
            </p>
            <div style="margin-top: 14px; font-size: 12px; color: #ffffff;">
              <div>• <strong>59 Notebook Cells</strong> (34 code cells executed with 0 errors)</div>
              <div>• <strong>24 High-Resolution Figures</strong> embedded inline</div>
              <div>• <strong>17 Formatted Tables</strong> verifying invariants & correlations</div>
              <div>• <strong>Critical AQI Analysis</strong> comparing weather-modeled vs criteria-derived AQI</div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div class="card-title-group">
              <span style="font-size: 16px;">🏛️</span>
              <h3>System Architecture & Big Data Standards</h3>
            </div>
          </div>
          <div class="card-body">
            <div style="font-size: 12.5px; color: var(--text-muted); display: flex; flex-direction: column; gap: 8px;">
              <div>• <strong>Hadoop MapReduce:</strong> 4 streaming jobs for corridor volume, modal split, weather extremes, and seasonal profiling.</div>
              <div>• <strong>Apache Spark / PySpark:</strong> Distributed ETL, window aggregations, and broadcast hash-joins.</div>
              <div>• <strong>Machine Learning:</strong> Random Forest AQI classification, K-Means clustering, Isolation Forest anomaly detection.</div>
              <div>• <strong>FastAPI Backend:</strong> High-performance async REST API with CORS and model serving.</div>
            </div>
          </div>
        </div>
      </div>
    `;
  }
}

