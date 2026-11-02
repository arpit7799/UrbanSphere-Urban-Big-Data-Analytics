/**
 * UrbanSphere Frontend — Data Explorer View
 * Searchable multi-dataset schema explorer
 */

import { api } from '../api.js';

export class ExplorerView {
  constructor(appState) {
    this.appState = appState;
  }

  async render(container) {
    container.innerHTML = `
      <div class="view-header">
        <div class="view-header-titles">
          <h2>🗂️ Urban Big Data Explorer</h2>
          <p>Direct schema inspection across canonical and integrated datasets in UrbanSphere</p>
        </div>
      </div>

      <div class="two-col-grid">
        <div class="card">
          <div class="card-header">
            <div class="card-title-group">
              <span style="font-size: 16px;">📦</span>
              <h3>Canonical Datasets Inventory</h3>
            </div>
          </div>
          <div class="card-body">
            <div class="hbar-list">
              <div class="hbar-row">
                <div class="hbar-header">
                  <span class="hbar-label">Traffic Mobility (dataset_traffic_gurugram.csv)</span>
                  <span class="hbar-val">315,648 rows × 18 cols</span>
                </div>
              </div>
              <div class="hbar-row">
                <div class="hbar-header">
                  <span class="hbar-label">Weather & Meteorology (dataset_weather_gurugram_with_aqi.csv)</span>
                  <span class="hbar-val">315,648 rows × 15 cols</span>
                </div>
              </div>
              <div class="hbar-row">
                <div class="hbar-header">
                  <span class="hbar-label">Air Quality (dataset_air_quality_gurugram.csv)</span>
                  <span class="hbar-val">315,648 rows × 14 cols</span>
                </div>
              </div>
              <div class="hbar-row">
                <div class="hbar-header">
                  <span class="hbar-label">Geography Metadata (dataset_geography_gurugram.csv)</span>
                  <span class="hbar-val">12 localities × 11 cols</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div class="card-title-group">
              <span style="font-size: 16px;">⚡</span>
              <h3>PySpark & MapReduce Data Products</h3>
            </div>
          </div>
          <div class="card-body">
            <div class="hbar-list">
              <div class="hbar-row">
                <div class="hbar-header">
                  <span class="hbar-label">Daily Integrated Master (urban_integrated_daily.parquet)</span>
                  <span class="hbar-val">13,152 daily records</span>
                </div>
              </div>
              <div class="hbar-row">
                <div class="hbar-header">
                  <span class="hbar-label">Corridor Capacity Stress (corridor_capacity_stress.csv)</span>
                  <span class="hbar-val">Spark SQL Aggregation</span>
                </div>
              </div>
              <div class="hbar-row">
                <div class="hbar-header">
                  <span class="hbar-label">Seasonal Air Quality Profiles (seasonal_air_quality_profiles.csv)</span>
                  <span class="hbar-val">Hadoop MapReduce Job 4</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
  }
}

