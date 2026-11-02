/**
 * UrbanSphere Frontend — Main Application Controller & Router
 */

import { api } from './api.js';
import { OverviewView } from './views/overview.js';
import { TrafficView } from './views/traffic.js';
import { AirQualityView } from './views/air_quality.js';
import { WeatherView } from './views/weather.js';
import { GeographyView } from './views/geography.js';
import { AnalyticsView } from './views/analytics.js';
import { ExplorerView } from './views/explorer.js';
import { ReportsView } from './views/reports.js';

class UrbanSphereApp {
  constructor() {
    this.currentViewId = 'overview';
    this.selectedLocality = '';
    this.views = {};
    this.stateListeners = [];
  }

  init() {
    // Instantiate views
    this.views = {
      'overview': new OverviewView(this),
      'traffic': new TrafficView(this),
      'air-quality': new AirQualityView(this),
      'weather': new WeatherView(this),
      'geography': new GeographyView(this),
      'analytics': new AnalyticsView(this),
      'explorer': new ExplorerView(this),
      'reports': new ReportsView(this),
    };

    this.bindNavigation();
    this.bindGlobalFilters();
    this.checkBackendHealth();
    this.loadGlobalLocalities();

    // Initial render
    this.switchView('overview');
  }

  setSelectedLocality(name) {
    this.selectedLocality = name || '';
    const select = document.getElementById('global-locality-select');
    if (select) select.value = this.selectedLocality;

    // Refresh current view if it supports locality updates
    const viewContainer = document.getElementById('view-content-area');
    if (this.views[this.currentViewId]?.render) {
      this.views[this.currentViewId].render(viewContainer);
    }
  }

  switchView(viewId) {
    if (!this.views[viewId]) return;
    this.currentViewId = viewId;

    // Update nav items
    document.querySelectorAll('.nav-item').forEach(item => {
      if (item.getAttribute('data-view') === viewId) {
        item.classList.add('active');
      } else {
        item.classList.remove('active');
      }
    });

    // Render active view
    const viewContainer = document.getElementById('view-content-area');
    if (viewContainer) {
      this.views[viewId].render(viewContainer);
    }
  }

  bindNavigation() {
    document.querySelectorAll('.nav-item').forEach(item => {
      item.addEventListener('click', (e) => {
        e.preventDefault();
        const viewId = item.getAttribute('data-view');
        this.switchView(viewId);
      });
    });
  }

  bindGlobalFilters() {
    const locSelect = document.getElementById('global-locality-select');
    if (locSelect) {
      locSelect.addEventListener('change', (e) => {
        this.setSelectedLocality(e.target.value);
      });
    }

    const themeToggle = document.getElementById('theme-toggle-btn');
    if (themeToggle) {
      themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('light-theme');
      });
    }
  }

  async checkBackendHealth() {
    const statusText = document.getElementById('backend-status-text');
    const statusDot = document.getElementById('backend-status-dot');

    try {
      const res = await api.getHealth();
      if (res.status === 'healthy') {
        if (statusText) statusText.textContent = 'Backend Connected';
        if (statusDot) {
          statusDot.style.backgroundColor = '#10b981';
          statusDot.style.boxShadow = '0 0 8px #10b981';
        }
      }
    } catch (err) {
      if (statusText) statusText.textContent = 'Backend Offline';
      if (statusDot) {
        statusDot.style.backgroundColor = '#ef4444';
        statusDot.style.boxShadow = '0 0 8px #ef4444';
      }
    }
  }

  async loadGlobalLocalities() {
    try {
      const res = await api.getGeographySectors();
      const localities = res.data || [];
      const select = document.getElementById('global-locality-select');
      if (select && localities.length) {
        localities.forEach(l => {
          const opt = document.createElement('option');
          opt.value = l.location_name;
          opt.textContent = l.location_name;
          select.appendChild(opt);
        });
      }
    } catch (e) {}
  }
}

// Bootstrap on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  window.app = new UrbanSphereApp();
  window.app.init();
});

