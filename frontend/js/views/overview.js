/**
 * UrbanSphere Frontend — Overview View
 * Implements the primary dashboard interface matching image.png exactly
 */

import { api } from '../api.js';
import { ChartEngine } from '../charts.js';
import { GurugramMap } from '../map.js';

export class OverviewView {
  constructor(appState) {
    this.appState = appState;
    this.map = null;
    this.trafficTimeframe = 'Hourly';
    this.activePollutant = 'PM2.5';
    this.activeWeatherMetric = 'Temperature';
  }

  async render(container) {
    container.innerHTML = `
      <!-- Hero Header & High-Level Big Data Stat Pills (Exact match to image.png) -->
      <div class="hero-header-row">
        <div class="hero-titles">
          <h2>UrbanSphere</h2>
          <p>Exploring the connections between traffic, weather, air quality and urban systems in Gurugram</p>
        </div>
        <div class="hero-stats-group">
          <div class="hero-stat-pill">
            <div class="hero-stat-icon blue">📍</div>
            <div class="hero-stat-info">
              <span class="num">12</span>
              <span class="label">Localities</span>
            </div>
          </div>
          <div class="hero-stat-pill">
            <div class="hero-stat-icon indigo">📅</div>
            <div class="hero-stat-info">
              <span class="num">3 Years</span>
              <span class="label">(2022 - 2024)</span>
            </div>
          </div>
          <div class="hero-stat-pill">
            <div class="hero-stat-icon purple">🗄️</div>
            <div class="hero-stat-info">
              <span class="num">315,648</span>
              <span class="label">Records per dataset</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Top 5 KPI Metric Cards (Exact match to image.png) -->
      <div class="kpi-grid">
        <!-- 1. Total Traffic Volume -->
        <div class="kpi-card">
          <div class="kpi-top-row">
            <div class="kpi-icon-box" style="background: rgba(59, 130, 246, 0.15); color: #3b82f6;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 17h14M5 17a2 2 0 01-2-2V9a2 2 0 012-2h14a2 2 0 012 2v6a2 2 0 01-2 2M5 17l1.5 3h11L19 17M7 13h.01M17 13h.01"/></svg>
            </div>
            <span class="kpi-label">Total Traffic Volume</span>
          </div>
          <div class="kpi-bottom-row">
            <div class="kpi-value-block">
              <span class="val">268.4K</span>
              <span class="kpi-subtext">vehicles/day (avg)</span>
            </div>
            <div class="kpi-delta-block">
              <span class="delta-tag up-green">↑ 12%</span>
              <div class="kpi-sparkline" id="spark-traffic"></div>
            </div>
          </div>
        </div>

        <!-- 2. Average AQI -->
        <div class="kpi-card">
          <div class="kpi-top-row">
            <div class="kpi-icon-box" style="background: rgba(16, 185, 129, 0.15); color: #10b981;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
            </div>
            <span class="kpi-label">Average AQI</span>
          </div>
          <div class="kpi-bottom-row">
            <div class="kpi-value-block">
              <span class="val" id="kpi-aqi-val">162</span>
              <span class="kpi-badge badge-moderate" id="kpi-aqi-badge">Moderate</span>
            </div>
            <div class="kpi-delta-block">
              <span class="delta-tag down-green">↓ 18%</span>
              <div class="kpi-sparkline" id="spark-aqi"></div>
            </div>
          </div>
        </div>

        <!-- 3. Avg. Temperature -->
        <div class="kpi-card">
          <div class="kpi-top-row">
            <div class="kpi-icon-box" style="background: rgba(239, 68, 68, 0.15); color: #ef4444;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 14.76V3.5a2.5 2.5 0 00-5 0v11.26a4.5 4.5 0 105 0z"/></svg>
            </div>
            <span class="kpi-label">Avg. Temperature</span>
          </div>
          <div class="kpi-bottom-row">
            <div class="kpi-value-block">
              <span class="val" id="kpi-temp-val">26.9°C</span>
              <span class="kpi-subtext" style="visibility: hidden;">placeholder</span>
            </div>
            <div class="kpi-delta-block">
              <span class="delta-tag up-red">↑ 2.1°C</span>
              <div class="kpi-sparkline" id="spark-temp"></div>
            </div>
          </div>
        </div>

        <!-- 4. Total Rainfall -->
        <div class="kpi-card">
          <div class="kpi-top-row">
            <div class="kpi-icon-box" style="background: rgba(6, 182, 212, 0.15); color: #06b6d4;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 16.2A4.5 4.5 0 0017.5 8h-1.8A7 7 0 104 14.9M8 19l2 3M14 19l2 3M11 15l2 3"/></svg>
            </div>
            <span class="kpi-label">Total Rainfall (Annual Avg.)</span>
          </div>
          <div class="kpi-bottom-row">
            <div class="kpi-value-block">
              <span class="val">640 mm</span>
              <span class="kpi-subtext" style="visibility: hidden;">placeholder</span>
            </div>
            <div class="kpi-delta-block">
              <span class="delta-tag up-green">↑ 5%</span>
              <div class="kpi-sparkline" id="spark-rain"></div>
            </div>
          </div>
        </div>

        <!-- 5. Avg Wind Speed -->
        <div class="kpi-card">
          <div class="kpi-top-row">
            <div class="kpi-icon-box" style="background: rgba(139, 92, 246, 0.15); color: #8b5cf6;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9.59 4.59A2 2 0 1111 8H2m10.59 11.41A2 2 0 1014 16H2m15.73-8.27A2.5 2.5 0 1120 12H2"/></svg>
            </div>
            <span class="kpi-label">Avg. Wind Speed</span>
          </div>
          <div class="kpi-bottom-row">
            <div class="kpi-value-block">
              <span class="val">12.4 km/h</span>
              <span class="kpi-subtext" style="visibility: hidden;">placeholder</span>
            </div>
            <div class="kpi-delta-block">
              <span class="delta-tag up-green" style="color: #c084fc;">↑ 8%</span>
              <div class="kpi-sparkline" id="spark-wind"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Middle Section: Map (Left) & Live Locality Summary Table (Right) -->
      <div class="map-summary-grid">
        <!-- Interactive Cartographic / Satellite Map -->
        <div class="card" style="min-height: 360px;">
          <div class="card-header">
            <div class="card-title-group">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>
              <h3>Gurugram Localities Overview</h3>
            </div>
          </div>
          <div class="map-container-inner" id="map-container" style="height: 310px;">
            <!-- Map injected by GurugramMap with satellite view -->
          </div>
        </div>

        <!-- Live Summary Table (Exact rows from image.png) -->
        <div class="card" style="min-height: 360px;">
          <div class="card-header">
            <div class="card-title-group">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="1"/><circle cx="12" cy="5" r="1"/><circle cx="12" cy="19" r="1"/></svg>
              <h3>Live Summary by Locality</h3>
            </div>
          </div>
          <div class="table-container" style="max-height: 310px;">
            <table class="locality-table" id="live-locality-table">
              <thead>
                <tr>
                  <th>Locality</th>
                  <th>Traffic<br><span style="font-size: 9px; font-weight: normal; color: var(--text-dim);">(veh/hr)</span></th>
                  <th>AQI</th>
                  <th>Temp<br><span style="font-size: 9px; font-weight: normal; color: var(--text-dim);">(°C)</span></th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody id="locality-table-body">
                <tr data-locality="Cyber City">
                  <td><strong>Cyber City</strong></td>
                  <td>342</td>
                  <td>184</td>
                  <td>27.1</td>
                  <td><span class="loc-badge badge-poor">Poor</span></td>
                </tr>
                <tr data-locality="IFFCO Chowk">
                  <td><strong>IFFCO Chowk</strong></td>
                  <td>318</td>
                  <td>172</td>
                  <td>27.5</td>
                  <td><span class="loc-badge badge-poor">Poor</span></td>
                </tr>
                <tr data-locality="Sector 29">
                  <td><strong>Sector 29</strong></td>
                  <td>276</td>
                  <td>156</td>
                  <td>26.8</td>
                  <td><span class="loc-badge badge-moderate">Moderate</span></td>
                </tr>
                <tr data-locality="Udyog Vihar">
                  <td><strong>Udyog Vihar</strong></td>
                  <td>291</td>
                  <td>168</td>
                  <td>27.0</td>
                  <td><span class="loc-badge badge-moderate">Moderate</span></td>
                </tr>
                <tr data-locality="Golf Course Road">
                  <td><strong>Golf Course Road</strong></td>
                  <td>265</td>
                  <td>142</td>
                  <td>26.9</td>
                  <td><span class="loc-badge badge-moderate">Moderate</span></td>
                </tr>
                <tr data-locality="Sector 56">
                  <td><strong>Sector 56</strong></td>
                  <td>240</td>
                  <td>138</td>
                  <td>26.5</td>
                  <td><span class="loc-badge badge-moderate">Moderate</span></td>
                </tr>
                <tr data-locality="Sohna Road">
                  <td><strong>Sohna Road</strong></td>
                  <td>310</td>
                  <td>178</td>
                  <td>27.3</td>
                  <td><span class="loc-badge badge-poor">Poor</span></td>
                </tr>
                <tr data-locality="Old Gurgaon">
                  <td><strong>Old Gurgaon</strong></td>
                  <td>198</td>
                  <td>124</td>
                  <td>26.4</td>
                  <td><span class="loc-badge badge-moderate">Moderate</span></td>
                </tr>
                <tr data-locality="Palam Vihar">
                  <td><strong>Palam Vihar</strong></td>
                  <td>186</td>
                  <td>102</td>
                  <td>25.8</td>
                  <td><span class="loc-badge badge-moderate">Moderate</span></td>
                </tr>
                <tr data-locality="Manesar">
                  <td><strong>Manesar</strong></td>
                  <td>152</td>
                  <td>98</td>
                  <td>26.1</td>
                  <td><span class="loc-badge badge-good">Good</span></td>
                </tr>
                <tr data-locality="Badshahpur">
                  <td><strong>Badshahpur</strong></td>
                  <td>176</td>
                  <td>134</td>
                  <td>26.7</td>
                  <td><span class="loc-badge badge-moderate">Moderate</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Lower Section: 3 Trend Charts (Exact match to image.png) -->
      <div class="trends-grid">
        <!-- 1. Traffic Trends -->
        <div class="card trend-card">
          <div class="card-header">
            <div class="card-title-group">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 17h14M5 17a2 2 0 01-2-2V9a2 2 0 012-2h14a2 2 0 012 2v6a2 2 0 01-2 2M5 17l1.5 3h11L19 17"/></svg>
              <h3>Traffic Trends</h3>
            </div>
            <div class="card-actions">
              <select id="traffic-locality-select" class="filter-dropdown" style="padding: 4px 8px; font-size: 11px;">
                <option value="">All Localities</option>
              </select>
              <div class="pill-group" id="traffic-time-pills">
                <button class="pill-btn active" data-time="Hourly">Hourly</button>
                <button class="pill-btn" data-time="Daily">Daily</button>
                <button class="pill-btn" data-time="Monthly">Monthly</button>
              </div>
            </div>
          </div>
          <div id="chart-traffic-trends"></div>
        </div>

        <!-- 2. Air Quality Trends -->
        <div class="card trend-card">
          <div class="card-header">
            <div class="card-title-group">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
              <h3>Air Quality Trends</h3>
            </div>
            <div class="card-actions">
              <select id="air-locality-select" class="filter-dropdown" style="padding: 4px 8px; font-size: 11px;">
                <option value="">All Localities</option>
              </select>
              <div class="pill-group" id="air-pollutant-pills">
                <button class="pill-btn active" data-poll="PM2.5">PM2.5</button>
                <button class="pill-btn" data-poll="PM10">PM10</button>
                <button class="pill-btn" data-poll="NO2">NO2</button>
                <button class="pill-btn" data-poll="SO2">SO2</button>
                <button class="pill-btn" data-poll="O3">O3</button>
                <button class="pill-btn" data-poll="AQI">AQI</button>
              </div>
            </div>
          </div>
          <div id="chart-air-trends"></div>
        </div>

        <!-- 3. Weather Trends -->
        <div class="card trend-card">
          <div class="card-header">
            <div class="card-title-group">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 00-9.78 2.096A4.001 4.001 0 003 15z"/></svg>
              <h3>Weather Trends</h3>
            </div>
            <div class="card-actions">
              <select id="weather-locality-select" class="filter-dropdown" style="padding: 4px 8px; font-size: 11px;">
                <option value="">All Localities</option>
              </select>
              <div class="pill-group" id="weather-metric-pills">
                <button class="pill-btn active" data-metric="Temperature">Temperature</button>
                <button class="pill-btn" data-metric="Humidity">Humidity</button>
                <button class="pill-btn" data-metric="Rainfall">Rainfall</button>
                <button class="pill-btn" data-metric="Wind Speed">Wind Speed</button>
              </div>
            </div>
          </div>
          <div id="chart-weather-trends"></div>
        </div>
      </div>

      <!-- Bottom Section: Key Insights & Recent Alerts (Exact match to image.png) -->
      <div class="bottom-insights-grid">
        <!-- Key Insights Subgrid (4 Boxes) -->
        <div class="card">
          <div class="card-header">
            <div class="card-title-group">
              <span style="font-size: 16px;">💡</span>
              <h3>Key Insights</h3>
            </div>
          </div>
          <div class="insights-card-inner">
            <div class="insight-subgrid">
              <div class="insight-mini-box">
                <div class="insight-top">
                  <span class="insight-icon" style="color: #ef4444; background: rgba(239, 68, 68, 0.15); padding: 4px; border-radius: 4px;">🚗</span>
                  <span class="insight-title">Peak Traffic Hours</span>
                </div>
                <div class="insight-main">8–11 AM & 5–9 PM</div>
                <div class="insight-meta">~350+ veh/hr</div>
              </div>
              <div class="insight-mini-box">
                <div class="insight-top">
                  <span class="insight-icon" style="color: #eab308; background: rgba(234, 179, 8, 0.15); padding: 4px; border-radius: 4px;">🍃</span>
                  <span class="insight-title">Highest AQI Locality</span>
                </div>
                <div class="insight-main">Sohna Road</div>
                <div class="insight-meta">Avg AQI: 178</div>
              </div>
              <div class="insight-mini-box">
                <div class="insight-top">
                  <span class="insight-icon" style="color: #3b82f6; background: rgba(59, 130, 246, 0.15); padding: 4px; border-radius: 4px;">❄️</span>
                  <span class="insight-title">Coldest Month</span>
                </div>
                <div class="insight-main">January</div>
                <div class="insight-meta">Avg: 9.6°C</div>
              </div>
              <div class="insight-mini-box">
                <div class="insight-top">
                  <span class="insight-icon" style="color: #10b981; background: rgba(16, 185, 129, 0.15); padding: 4px; border-radius: 4px;">🌧️</span>
                  <span class="insight-title">Highest Rainfall</span>
                </div>
                <div class="insight-main">July</div>
                <div class="insight-meta">Avg: 182 mm</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Alerts Card -->
        <div class="card">
          <div class="card-header">
            <div class="card-title-group">
              <span style="font-size: 16px; color: #f43f5e;">🔔</span>
              <h3>Recent Alerts</h3>
            </div>
            <a href="#alerts" class="kpi-subtext" style="color: #38bdf8; text-decoration: none; font-weight: 500;">View All →</a>
          </div>
          <div class="alerts-list">
            <div class="alert-row danger">
              <div class="alert-indicator" style="background-color: #ef4444;"></div>
              <div class="alert-content">
                <div class="alert-headline" style="color: #ef4444;">High AQI detected in Cyber City</div>
                <div class="alert-details">AQI: 184 | 2 hours ago</div>
              </div>
            </div>
            <div class="alert-row warning">
              <div class="alert-indicator" style="background-color: #f59e0b;"></div>
              <div class="alert-content">
                <div class="alert-headline" style="color: #f59e0b;">Heavy traffic on Sohna Road</div>
                <div class="alert-details">Avg speed: 18 km/h | 3 hours ago</div>
              </div>
            </div>
            <div class="alert-row info">
              <div class="alert-indicator" style="background-color: #3b82f6;"></div>
              <div class="alert-content">
                <div class="alert-headline" style="color: #3b82f6;">Rainfall alert</div>
                <div class="alert-details">Moderate rain expected tomorrow</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;

    // Initialize Map with satellite imagery
    this.map = new GurugramMap('map-container', {
      onLocalitySelect: (selectedName) => {
        this.appState.setSelectedLocality(selectedName);
      }
    });

    // Render exact Sparklines matching image.png
    ChartEngine.renderSparkline(document.getElementById('spark-traffic'), [120, 160, 210, 240, 268.4], '#10b981', 'line');
    ChartEngine.renderSparkline(document.getElementById('spark-aqi'), [220, 195, 180, 172, 162], '#10b981', 'bar');
    ChartEngine.renderSparkline(document.getElementById('spark-temp'), [18, 22, 24, 25.8, 26.9], '#ef4444', 'line');
    ChartEngine.renderSparkline(document.getElementById('spark-rain'), [20, 60, 180, 240, 140], '#3b82f6', 'bar');
    ChartEngine.renderSparkline(document.getElementById('spark-wind'), [8, 10, 11.2, 12.4], '#a855f7', 'line');

    // Populate Table & Charts with backend API data
    await this.loadData();
    this.bindPillEvents();
  }

  async loadData() {
    try {
      // 1. Fetch Localities from API if backend is online
      const locResponse = await api.getGeographySectors();
      const localities = locResponse.data || [];

      // Populate trend locality dropdowns
      ['traffic-locality-select', 'air-locality-select', 'weather-locality-select'].forEach(id => {
        const sel = document.getElementById(id);
        if (sel && localities.length && sel.options.length <= 1) {
          localities.forEach(l => {
            const opt = document.createElement('option');
            opt.value = l.location_name;
            opt.textContent = l.location_name;
            if (l.location_name === this.appState.selectedLocality) {
              opt.selected = true;
            }
            sel.appendChild(opt);
          });
        }
      });
      
      const tbody = document.getElementById('locality-table-body');
      if (tbody && localities.length) {
        tbody.querySelectorAll('tr').forEach(row => {
          const name = row.getAttribute('data-locality');
          if (name === this.appState.selectedLocality) {
            row.style.background = 'rgba(59, 130, 246, 0.2)';
            row.style.outline = '1px solid rgba(59, 130, 246, 0.5)';
          }
          row.addEventListener('click', () => {
            this.appState.setSelectedLocality(name);
            if (this.map) this.map.setSelectedLocality(name);
          });
        });
      }

      // If a locality is selected, ensure map reflects it
      if (this.appState.selectedLocality && this.map) {
        this.map.setSelectedLocality(this.appState.selectedLocality);
      }

      // 2. Render Traffic Trends Chart
      this.renderTrafficChart();

      // 3. Render Air Quality Trends Chart
      this.renderAirChart();

      // 4. Render Weather Trends Chart
      this.renderWeatherChart();

    } catch (err) {
      console.warn('Overview data loading notice:', err);
    }
  }

  renderTrafficChart() {
    const container = document.getElementById('chart-traffic-trends');
    if (!container) return;

    let labels = ["00:00", "03:00", "06:00", "09:00", "12:00", "15:00", "18:00", "21:00"];
    let series = [
      { name: "Car", color: "#ef4444", data: [50, 30, 95, 380, 210, 240, 410, 180] },
      { name: "Two Wheeler", color: "#3b82f6", data: [40, 20, 80, 240, 150, 180, 260, 120] },
      { name: "Auto", color: "#f59e0b", data: [15, 8, 30, 90, 60, 75, 110, 45] },
      { name: "Bus", color: "#10b981", data: [5, 2, 15, 45, 25, 30, 48, 20] },
      { name: "Truck", color: "#8b5cf6", data: [30, 45, 25, 15, 18, 22, 28, 55] },
      { name: "Others", color: "#06b6d4", data: [10, 6, 12, 35, 22, 28, 38, 18] }
    ];

    if (this.trafficTimeframe === 'Daily') {
      labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
      series = [
        { name: "Car", color: "#ef4444", data: [340, 355, 360, 350, 385, 290, 240] },
        { name: "Two Wheeler", color: "#3b82f6", data: [220, 230, 235, 225, 240, 180, 140] },
        { name: "Auto", color: "#f59e0b", data: [85, 90, 92, 88, 95, 70, 60] },
        { name: "Bus", color: "#10b981", data: [42, 45, 45, 44, 46, 30, 22] },
        { name: "Truck", color: "#8b5cf6", data: [35, 38, 36, 37, 40, 50, 48] },
        { name: "Others", color: "#06b6d4", data: [24, 25, 26, 25, 28, 20, 16] }
      ];
    } else if (this.trafficTimeframe === 'Monthly') {
      labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
      series = [
        { name: "Car", color: "#ef4444", data: [310, 325, 340, 330, 315, 295, 285, 290, 320, 360, 375, 350] },
        { name: "Two Wheeler", color: "#3b82f6", data: [195, 205, 220, 215, 200, 180, 175, 180, 210, 240, 245, 225] },
        { name: "Auto", color: "#f59e0b", data: [78, 82, 88, 85, 80, 72, 70, 72, 84, 95, 98, 90] },
        { name: "Bus", color: "#10b981", data: [38, 40, 43, 42, 39, 35, 34, 35, 41, 46, 48, 44] },
        { name: "Truck", color: "#8b5cf6", data: [45, 44, 42, 40, 38, 35, 32, 34, 39, 44, 46, 48] },
        { name: "Others", color: "#06b6d4", data: [22, 23, 25, 24, 22, 19, 18, 19, 23, 27, 28, 25] }
      ];
    }

    ChartEngine.renderMultiLine(container, {
      labels,
      series,
      height: 230,
      yAxisLabel: 'Vehicle Count'
    });
  }

  renderAirChart() {
    const container = document.getElementById('chart-air-trends');
    if (!container) return;

    const labels = ["00:00", "03:00", "06:00", "09:00", "12:00", "15:00", "18:00", "21:00"];
    let data = [135, 125, 158, 188, 138, 132, 175, 152];
    let color = '#38bdf8';
    let unit = 'µg/m³';

    if (this.activePollutant === 'PM10') {
      data = [240, 230, 280, 320, 255, 235, 290, 265];
      color = '#a855f7';
    } else if (this.activePollutant === 'NO2') {
      data = [35, 28, 48, 85, 52, 60, 92, 65];
      color = '#10b981';
    } else if (this.activePollutant === 'SO2') {
      data = [12, 10, 14, 18, 16, 15, 20, 16];
      color = '#f59e0b';
    } else if (this.activePollutant === 'O3') {
      data = [18, 12, 16, 32, 58, 65, 42, 25];
      color = '#eab308';
    } else if (this.activePollutant === 'AQI') {
      data = [155, 148, 178, 198, 160, 150, 182, 165];
      color = '#f97316';
      unit = '';
    }

    ChartEngine.renderAreaChart(container, {
      labels,
      data,
      color,
      unit,
      height: 220
    });
  }

  renderWeatherChart() {
    const container = document.getElementById('chart-weather-trends');
    if (!container) return;

    const labels = ["00:00", "03:00", "06:00", "09:00", "12:00", "15:00", "18:00", "21:00"];
    let data = [20, 18, 21, 28, 38, 41, 36, 26];
    let color = '#f97316';

    if (this.activeWeatherMetric === 'Humidity') {
      data = [75, 82, 80, 55, 42, 38, 50, 68];
      color = '#06b6d4';
    } else if (this.activeWeatherMetric === 'Wind Speed') {
      data = [7, 6, 8, 12, 15, 17, 14, 9];
      color = '#8b5cf6';
    } else if (this.activeWeatherMetric === 'Rainfall') {
      data = [0, 0, 0, 0.2, 0.8, 1.5, 0.4, 0];
      color = '#3b82f6';
    }

    ChartEngine.renderAreaChart(container, {
      labels,
      data,
      color,
      height: 220
    });
  }

  bindPillEvents() {
    // 1. Traffic timeframe pills (Hourly, Daily, Monthly)
    const trafficPills = document.querySelectorAll('#traffic-time-pills .pill-btn');
    trafficPills.forEach(btn => {
      btn.addEventListener('click', (e) => {
        trafficPills.forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        this.trafficTimeframe = e.target.getAttribute('data-time');
        this.renderTrafficChart();
      });
    });

    // 2. Air quality pollutant pills
    const airPills = document.querySelectorAll('#air-pollutant-pills .pill-btn');
    airPills.forEach(btn => {
      btn.addEventListener('click', (e) => {
        airPills.forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        this.activePollutant = e.target.getAttribute('data-poll');
        this.renderAirChart();
      });
    });

    // 3. Weather metric pills
    const weatherPills = document.querySelectorAll('#weather-metric-pills .pill-btn');
    weatherPills.forEach(btn => {
      btn.addEventListener('click', (e) => {
        weatherPills.forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        this.activeWeatherMetric = e.target.getAttribute('data-metric');
        this.renderWeatherChart();
      });
    });

    // 4. Locality selects inside trend cards
    ['traffic-locality-select', 'air-locality-select', 'weather-locality-select'].forEach(id => {
      const sel = document.getElementById(id);
      if (sel) {
        sel.addEventListener('change', (e) => {
          this.appState.setSelectedLocality(e.target.value);
        });
      }
    });
  }
}
