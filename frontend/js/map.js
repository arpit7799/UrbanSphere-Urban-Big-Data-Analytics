/**
 * UrbanSphere Frontend — Interactive Gurugram Cartographic & Satellite Map
 * Plots 12 study localities, arterial transit corridors, and real-time AQI heat markers.
 */

export class GurugramMap {
  constructor(containerId, options = {}) {
    this.container = document.getElementById(containerId);
    this.options = options;
    this.mode = 'satellite'; // Match reference image: Satellite active by default
    this.zoomLevel = 1.0;
    this.onLocalitySelect = options.onLocalitySelect || (() => {});
    this.selectedLocality = null;

    // Projected coordinate positions matched to Gurugram geography and reference layout
    this.localities = [
      { name: "Palam Vihar", xPct: 41, yPct: 28, aqi: 102, status: "Moderate", color: "#10b981", type: "Residential", traffic: 186, temp: 25.8 },
      { name: "Udyog Vihar", xPct: 47, yPct: 22, aqi: 168, status: "Moderate", color: "#10b981", type: "Industrial", traffic: 291, temp: 27.0 },
      { name: "Cyber City", xPct: 58, yPct: 23, aqi: 184, status: "Poor", color: "#ef4444", type: "Commercial", traffic: 342, temp: 27.1 },
      { name: "IFFCO Chowk", xPct: 60, yPct: 32, aqi: 172, status: "Poor", color: "#f97316", type: "Commercial", traffic: 318, temp: 27.5 },
      { name: "Sector 56", xPct: 53, yPct: 42, aqi: 138, status: "Moderate", color: "#eab308", type: "Residential", traffic: 240, temp: 26.5 },
      { name: "Golf Course Road", xPct: 64, yPct: 49, aqi: 142, status: "Moderate", color: "#f97316", type: "IT/Corporate", traffic: 265, temp: 26.9 },
      { name: "Sohna Road", xPct: 52, yPct: 50, aqi: 178, status: "Poor", color: "#10b981", type: "Mixed Use", traffic: 310, temp: 27.3 },
      { name: "Sector 29", xPct: 43, yPct: 53, aqi: 156, status: "Moderate", color: "#eab308", type: "Commercial", traffic: 276, temp: 26.8 },
      { name: "Manesar", xPct: 28, yPct: 46, aqi: 98, status: "Good", color: "#10b981", type: "Industrial", traffic: 152, temp: 26.1 },
      { name: "Old Gurgaon", xPct: 38, yPct: 38, aqi: 124, status: "Moderate", color: "#eab308", type: "Mixed Use", traffic: 198, temp: 26.4 },
      { name: "Badshahpur", xPct: 48, yPct: 62, aqi: 134, status: "Moderate", color: "#eab308", type: "Residential", traffic: 176, temp: 26.7 },
      { name: "Millennium City Centre", xPct: 56, yPct: 36, aqi: 160, status: "Moderate", color: "#f97316", type: "Transit Hub", traffic: 285, temp: 27.2 }
    ];

    this.init();
  }

  getAQIColor(aqi) {
    if (aqi <= 50) return '#10b981';
    if (aqi <= 100) return '#eab308';
    if (aqi <= 200) return '#f97316';
    if (aqi <= 300) return '#ef4444';
    return '#881337';
  }

  setMode(mode) {
    this.mode = mode;
    this.render();
  }

  zoomIn() {
    this.zoomLevel = Math.min(1.6, this.zoomLevel + 0.15);
    this.render();
  }

  zoomOut() {
    this.zoomLevel = Math.max(0.85, this.zoomLevel - 0.15);
    this.render();
  }

  setSelectedLocality(name) {
    this.selectedLocality = name;
    this.render();
  }

  updateLocalityData(dataList) {
    if (!dataList || !dataList.length) return;
    this.localities.forEach(loc => {
      const match = dataList.find(d => (d.location_name || d.name) === loc.name);
      if (match) {
        if (match.aqi !== undefined) loc.aqi = Math.round(match.aqi);
        if (match.vehicle_count !== undefined) loc.traffic = Math.round(match.vehicle_count);
        if (match.temperature_c !== undefined) loc.temp = Number(match.temperature_c).toFixed(1);
        if (match.status) loc.status = match.status;
      }
    });
    this.render();
  }

  init() {
    this.render();
  }

  render() {
    if (!this.container) return;
    const width = this.container.clientWidth || 700;
    const height = this.container.clientHeight || 340;

    let pinsSvg = '';
    this.localities.forEach(loc => {
      const px = (loc.xPct / 100) * width;
      const py = (loc.yPct / 100) * height;
      const isSelected = this.selectedLocality === loc.name;
      const dotColor = loc.color || this.getAQIColor(loc.aqi);

      pinsSvg += `
        <g class="map-locality-pin ${isSelected ? 'selected' : ''}" data-name="${loc.name}" style="cursor: pointer;">
          <!-- Glowing pulse ring -->
          <circle cx="${px}" cy="${py}" r="${isSelected ? 20 : 12}" fill="${dotColor}" opacity="0.3">
            <animate attributeName="r" values="8;${isSelected ? 20 : 14};8" dur="2.5s" repeatCount="indefinite" />
            <animate attributeName="opacity" values="0.4;0.05;0.4" dur="2.5s" repeatCount="indefinite" />
          </circle>
          <!-- Pin circle -->
          <circle cx="${px}" cy="${py}" r="${isSelected ? 8 : 6}" fill="${dotColor}" stroke="#ffffff" stroke-width="${isSelected ? 2.5 : 1.2}" />
          <!-- Locality Name Tag -->
          <text x="${px + 10}" y="${py + 4}" fill="#ffffff" font-size="11" font-weight="600" class="map-loc-label" style="text-shadow: 0 1px 4px rgba(0,0,0,0.95); font-family: inherit;">
            ${loc.name}
          </text>
        </g>
      `;
    });

    const isSatellite = this.mode === 'satellite';
    const bgStyle = isSatellite 
      ? `background: linear-gradient(rgba(8, 12, 22, 0.45), rgba(8, 12, 22, 0.65)), url('public/images/gurugram_satellite_map.jpg'); background-size: cover; background-position: center;`
      : `background: radial-gradient(circle at 50% 50%, #0d172e 0%, #080c14 100%);`;

    this.container.innerHTML = `
      <div class="map-view-wrapper" style="width: 100%; height: 100%; position: relative; overflow: hidden; border-radius: 0 0 14px 14px; ${bgStyle}">
        <svg width="100%" height="100%" viewBox="0 0 ${width} ${height}" class="map-svg-canvas" style="transform: scale(${this.zoomLevel}); transform-origin: center center; transition: transform 0.2s ease;">
          <!-- Central City Label -->
          <text x="${width * 0.44}" y="${height * 0.46}" fill="#f8fafc" font-size="18" font-weight="700" letter-spacing="0.5px" opacity="0.9" style="text-shadow: 0 2px 8px rgba(0,0,0,0.9);">
            Gurugram
          </text>

          <!-- Localities Pins -->
          ${pinsSvg}
        </svg>

        <!-- Left Vertical Zoom Buttons (Matching reference image) -->
        <div style="position: absolute; top: 16px; left: 16px; display: flex; flex-direction: column; gap: 4px; z-index: 10;">
          <button id="map-zoom-in" style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255,255,255,0.12); color: #ffffff; width: 26px; height: 26px; border-radius: 4px; font-weight: bold; cursor: pointer;">+</button>
          <button id="map-zoom-out" style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255,255,255,0.12); color: #ffffff; width: 26px; height: 26px; border-radius: 4px; font-weight: bold; cursor: pointer;">−</button>
        </div>

        <!-- Top Right Map View / Satellite Toggle (Matching reference image) -->
        <div style="position: absolute; top: 16px; right: 16px; display: flex; align-items: center; gap: 6px; z-index: 10;">
          <div style="background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(8px); border: 1px solid rgba(255,255,255,0.12); border-radius: 6px; padding: 3px; display: flex; gap: 2px;">
            <button class="map-mode-btn ${!isSatellite ? 'active' : ''}" data-mode="map" style="padding: 4px 10px; font-size: 11px; border-radius: 4px; border: none; cursor: pointer; color: ${!isSatellite ? '#fff' : '#94a3b8'}; background: ${!isSatellite ? '#2563eb' : 'transparent'}; font-weight: 500;">Map View</button>
            <button class="map-mode-btn ${isSatellite ? 'active' : ''}" data-mode="satellite" style="padding: 4px 10px; font-size: 11px; border-radius: 4px; border: none; cursor: pointer; color: ${isSatellite ? '#fff' : '#94a3b8'}; background: ${isSatellite ? '#2563eb' : 'transparent'}; font-weight: 500;">Satellite</button>
          </div>
          <button style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255,255,255,0.12); color: #94a3b8; width: 28px; height: 28px; border-radius: 6px; display: flex; align-items: center; justify-content: center; cursor: pointer;" title="Fullscreen">
            <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" fill="none" stroke-width="2"><polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg>
          </button>
        </div>

        <!-- AQI Level Legend Box (Matching reference image) -->
        <div class="map-aqi-legend" style="position: absolute; bottom: 16px; right: 16px; background: rgba(15, 23, 42, 0.88); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 10px 14px; font-size: 11px; z-index: 10;">
          <div style="font-weight: 700; color: #ffffff; margin-bottom: 6px; font-size: 11.5px;">AQI Level</div>
          <div class="legend-row" style="margin-bottom: 3px;"><span class="legend-dot" style="background-color: #10b981;"></span> Good (0-50)</div>
          <div class="legend-row" style="margin-bottom: 3px;"><span class="legend-dot" style="background-color: #eab308;"></span> Moderate (51-100)</div>
          <div class="legend-row" style="margin-bottom: 3px;"><span class="legend-dot" style="background-color: #f97316;"></span> Poor (101-200)</div>
          <div class="legend-row" style="margin-bottom: 3px;"><span class="legend-dot" style="background-color: #ef4444;"></span> Very Poor (201-300)</div>
          <div class="legend-row"><span class="legend-dot" style="background-color: #881337;"></span> Severe (301-500)</div>
        </div>

        <!-- Tooltip -->
        <div id="map-tooltip" class="map-tooltip-card" style="display: none;"></div>
      </div>
    `;

    this.bindEvents();
  }

  bindEvents() {
    const tooltip = this.container.querySelector('#map-tooltip');

    const pins = this.container.querySelectorAll('.map-locality-pin');
    pins.forEach(pin => {
      const name = pin.getAttribute('data-name');
      const loc = this.localities.find(l => l.name === name);

      pin.addEventListener('click', () => {
        this.selectedLocality = (this.selectedLocality === name) ? null : name;
        this.render();
        this.onLocalitySelect(this.selectedLocality);
      });

      pin.addEventListener('mouseenter', (e) => {
        if (!loc || !tooltip) return;
        const color = loc.color || this.getAQIColor(loc.aqi);
        tooltip.innerHTML = `
          <div class="tt-header">
            <strong>${loc.name}</strong>
            <span class="tt-badge" style="background-color: ${color}20; color: ${color}; border: 1px solid ${color};">${loc.status}</span>
          </div>
          <div class="tt-row"><span>Type:</span> <span>${loc.type}</span></div>
          <div class="tt-row"><span>AQI Index:</span> <strong>${loc.aqi}</strong></div>
          <div class="tt-row"><span>Traffic:</span> <strong>${loc.traffic} veh/hr</strong></div>
          <div class="tt-row"><span>Temperature:</span> <strong>${loc.temp} °C</strong></div>
        `;
        tooltip.style.display = 'block';
        tooltip.style.left = `${e.offsetX + 15}px`;
        tooltip.style.top = `${e.offsetY - 20}px`;
      });

      pin.addEventListener('mousemove', (e) => {
        if (!tooltip) return;
        tooltip.style.left = `${e.offsetX + 15}px`;
        tooltip.style.top = `${e.offsetY - 20}px`;
      });

      pin.addEventListener('mouseleave', () => {
        if (tooltip) tooltip.style.display = 'none';
      });
    });

    const modeBtns = this.container.querySelectorAll('.map-mode-btn');
    modeBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        this.setMode(e.target.getAttribute('data-mode'));
      });
    });

    const zoomIn = this.container.querySelector('#map-zoom-in');
    const zoomOut = this.container.querySelector('#map-zoom-out');
    if (zoomIn) zoomIn.addEventListener('click', () => this.zoomIn());
    if (zoomOut) zoomOut.addEventListener('click', () => this.zoomOut());
  }
}
