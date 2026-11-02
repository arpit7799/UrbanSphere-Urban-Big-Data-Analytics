/**
 * UrbanSphere Frontend — Interactive Vector & Canvas Charting Engine
 * Self-contained, lightweight, zero-dependency data visualization library.
 */

export class ChartEngine {
  /**
   * Render a sleek SVG sparkline for KPI cards
   * @param {HTMLElement} container
   * @param {number[]} values
   * @param {string} strokeColor
   * @param {'line' | 'bar'} type
   */
  static renderSparkline(container, values = [], strokeColor = '#3b82f6', type = 'line') {
    if (!container || !values.length) return;
    const width = container.clientWidth || 90;
    const height = container.clientHeight || 28;
    const min = Math.min(...values);
    const max = Math.max(...values);
    const range = max - min || 1;

    if (type === 'bar') {
      const barWidth = Math.max(3, (width / values.length) - 2);
      let svg = `<svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" class="sparkline-svg">`;
      values.forEach((v, i) => {
        const h = Math.max(3, ((v - min) / range) * (height - 4));
        const x = i * (barWidth + 2);
        const y = height - h;
        svg += `<rect x="${x}" y="${y}" width="${barWidth}" height="${h}" rx="1" fill="${strokeColor}" opacity="${0.4 + (i / values.length) * 0.6}" />`;
      });
      svg += `</svg>`;
      container.innerHTML = svg;
      return;
    }

    // Line / Area sparkline
    const points = values.map((v, i) => {
      const x = (i / (values.length - 1)) * width;
      const y = height - 2 - (((v - min) / range) * (height - 6));
      return { x, y };
    });

    let d = `M ${points[0].x} ${points[0].y}`;
    for (let i = 1; i < points.length; i++) {
      // Smooth cubic bezier
      const prev = points[i - 1];
      const curr = points[i];
      const cx = (prev.x + curr.x) / 2;
      d += ` C ${cx} ${prev.y}, ${cx} ${curr.y}, ${curr.x} ${curr.y}`;
    }

    const gradId = `spark-grad-${Math.random().toString(36).substr(2, 9)}`;
    const areaD = `${d} L ${width} ${height} L 0 ${height} Z`;

    container.innerHTML = `
      <svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" class="sparkline-svg">
        <defs>
          <linearGradient id="${gradId}" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="${strokeColor}" stop-opacity="0.35" />
            <stop offset="100%" stop-color="${strokeColor}" stop-opacity="0.0" />
          </linearGradient>
        </defs>
        <path d="${areaD}" fill="url(#${gradId})" />
        <path d="${d}" fill="none" stroke="${strokeColor}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
    `;
  }

  /**
   * Render Multi-Line Chart (Used for Traffic & Trends)
   */
  static renderMultiLine(container, options = {}) {
    if (!container) return;
    const {
      labels = [],
      series = [], // [{ name, color, data: [] }]
      yAxisLabel = '',
      xAxisLabel = '',
      height = 240,
    } = options;

    if (!series.length || !labels.length) {
      container.innerHTML = '<div class="chart-empty">No series data available</div>';
      return;
    }

    const padding = { top: 20, right: 20, bottom: 35, left: 45 };
    const width = container.clientWidth || 450;
    const chartW = width - padding.left - padding.right;
    const chartH = height - padding.top - padding.bottom;

    // Determine Y range across all series
    let allVals = [];
    series.forEach(s => (allVals = allVals.concat(s.data)));
    const minY = 0;
    const maxY = Math.max(...allVals) * 1.15 || 100;

    // Y ticks
    const yTicksCount = 5;
    let yTicksSvg = '';
    for (let i = 0; i <= yTicksCount; i++) {
      const val = Math.round(minY + (i / yTicksCount) * (maxY - minY));
      const y = padding.top + chartH - (i / yTicksCount) * chartH;
      yTicksSvg += `
        <line x1="${padding.left}" y1="${y}" x2="${width - padding.right}" y2="${y}" stroke="rgba(255,255,255,0.06)" stroke-dasharray="3,3" />
        <text x="${padding.left - 8}" y="${y + 4}" fill="#64748b" font-size="10" text-anchor="end">${val}</text>
      `;
    }

    // X ticks
    let xTicksSvg = '';
    const step = Math.ceil(labels.length / 8);
    labels.forEach((lbl, i) => {
      if (i % step === 0 || i === labels.length - 1) {
        const x = padding.left + (i / (labels.length - 1)) * chartW;
        xTicksSvg += `
          <text x="${x}" y="${height - padding.bottom + 18}" fill="#64748b" font-size="10" text-anchor="middle">${lbl}</text>
        `;
      }
    });

    // Render each series line
    let linesSvg = '';
    series.forEach((s) => {
      const points = s.data.map((v, i) => {
        const x = padding.left + (i / (labels.length - 1)) * chartW;
        const y = padding.top + chartH - ((v - minY) / (maxY - minY)) * chartH;
        return { x, y, val: v };
      });

      let d = `M ${points[0].x} ${points[0].y}`;
      for (let i = 1; i < points.length; i++) {
        const prev = points[i - 1];
        const curr = points[i];
        const cx = (prev.x + curr.x) / 2;
        d += ` C ${cx} ${prev.y}, ${cx} ${curr.y}, ${curr.x} ${curr.y}`;
      }

      // Draw dots on peaks
      let dotsSvg = '';
      points.forEach((p, idx) => {
        if (idx % 2 === 0 || p.val === Math.max(...s.data)) {
          dotsSvg += `<circle cx="${p.x}" cy="${p.y}" r="3.5" fill="${s.color}" stroke="#0f172a" stroke-width="1.5" />`;
        }
      });

      linesSvg += `
        <path d="${d}" fill="none" stroke="${s.color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />
        ${dotsSvg}
      `;
    });

    // Legends
    let legendHtml = '<div class="chart-legend">';
    series.forEach(s => {
      legendHtml += `
        <span class="legend-item">
          <span class="legend-dot" style="background-color: ${s.color};"></span>
          <span class="legend-text">${s.name}</span>
        </span>
      `;
    });
    legendHtml += '</div>';

    container.innerHTML = `
      <div class="chart-wrapper">
        <svg width="100%" height="${height}" viewBox="0 0 ${width} ${height}" preserveAspectRatio="none">
          ${yTicksSvg}
          ${xTicksSvg}
          ${linesSvg}
        </svg>
        ${legendHtml}
      </div>
    `;
  }

  /**
   * Render Smooth Spline Area Chart (Air Quality / Weather Trends)
   */
  static renderAreaChart(container, options = {}) {
    if (!container) return;
    const {
      labels = [],
      data = [],
      color = '#3b82f6',
      unit = '',
      height = 220,
    } = options;

    if (!data.length || !labels.length) {
      container.innerHTML = '<div class="chart-empty">No data available</div>';
      return;
    }

    const padding = { top: 20, right: 20, bottom: 35, left: 45 };
    const width = container.clientWidth || 450;
    const chartW = width - padding.left - padding.right;
    const chartH = height - padding.top - padding.bottom;

    const minY = 0;
    const maxY = Math.max(...data) * 1.2 || 100;
    const gradId = `area-grad-${Math.random().toString(36).substr(2, 9)}`;

    let yTicksSvg = '';
    for (let i = 0; i <= 4; i++) {
      const val = Math.round(minY + (i / 4) * (maxY - minY));
      const y = padding.top + chartH - (i / 4) * chartH;
      yTicksSvg += `
        <line x1="${padding.left}" y1="${y}" x2="${width - padding.right}" y2="${y}" stroke="rgba(255,255,255,0.06)" stroke-dasharray="3,3" />
        <text x="${padding.left - 8}" y="${y + 4}" fill="#64748b" font-size="10" text-anchor="end">${val}</text>
      `;
    }

    let xTicksSvg = '';
    const step = Math.ceil(labels.length / 8);
    labels.forEach((lbl, i) => {
      if (i % step === 0 || i === labels.length - 1) {
        const x = padding.left + (i / (labels.length - 1)) * chartW;
        xTicksSvg += `
          <text x="${x}" y="${height - padding.bottom + 18}" fill="#64748b" font-size="10" text-anchor="middle">${lbl}</text>
        `;
      }
    });

    const points = data.map((v, i) => {
      const x = padding.left + (i / (labels.length - 1)) * chartW;
      const y = padding.top + chartH - ((v - minY) / (maxY - minY)) * chartH;
      return { x, y, val: v };
    });

    let d = `M ${points[0].x} ${points[0].y}`;
    for (let i = 1; i < points.length; i++) {
      const prev = points[i - 1];
      const curr = points[i];
      const cx = (prev.x + curr.x) / 2;
      d += ` C ${cx} ${prev.y}, ${cx} ${curr.y}, ${curr.x} ${curr.y}`;
    }

    const areaD = `${d} L ${points[points.length - 1].x} ${padding.top + chartH} L ${points[0].x} ${padding.top + chartH} Z`;

    container.innerHTML = `
      <div class="chart-wrapper">
        <svg width="100%" height="${height}" viewBox="0 0 ${width} ${height}" preserveAspectRatio="none">
          <defs>
            <linearGradient id="${gradId}" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="${color}" stop-opacity="0.45" />
              <stop offset="100%" stop-color="${color}" stop-opacity="0.0" />
            </linearGradient>
          </defs>
          ${yTicksSvg}
          ${xTicksSvg}
          <path d="${areaD}" fill="url(#${gradId})" />
          <path d="${d}" fill="none" stroke="${color}" stroke-width="2.5" stroke-linecap="round" />
          ${points.map((p, i) => i % 2 === 0 ? `<circle cx="${p.x}" cy="${p.y}" r="4" fill="${color}" stroke="#0f172a" stroke-width="2" />` : '').join('')}
        </svg>
      </div>
    `;
  }

  /**
   * Render Donut Chart for Modal Split
   */
  static renderDonut(container, items = [], options = {}) {
    if (!container || !items.length) return;
    const { size = 220, strokeWidth = 32 } = options;
    const total = items.reduce((acc, it) => acc + (it.value || 0), 0) || 1;

    let cumulativeAngle = 0;
    const radius = (size - strokeWidth) / 2;
    const cx = size / 2;
    const cy = size / 2;
    const circumference = 2 * Math.PI * radius;

    let slicesSvg = '';
    items.forEach((it) => {
      const pct = it.value / total;
      const strokeDash = pct * circumference;
      const strokeOffset = -cumulativeAngle * circumference;

      slicesSvg += `
        <circle cx="${cx}" cy="${cy}" r="${radius}" fill="none"
          stroke="${it.color}" stroke-width="${strokeWidth}"
          stroke-dasharray="${strokeDash} ${circumference - strokeDash}"
          stroke-dashoffset="${strokeOffset}"
          class="donut-slice"
        >
          <title>${it.name}: ${(pct * 100).toFixed(1)}%</title>
        </circle>
      `;
      cumulativeAngle += pct;
    });

    let legendHtml = '<div class="donut-legend">';
    items.forEach((it) => {
      const pct = ((it.value / total) * 100).toFixed(1);
      legendHtml += `
        <div class="donut-legend-row">
          <span class="legend-dot" style="background-color: ${it.color}"></span>
          <span class="donut-legend-label">${it.name}</span>
          <span class="donut-legend-pct">${pct}%</span>
        </div>
      `;
    });
    legendHtml += '</div>';

    container.innerHTML = `
      <div class="donut-container">
        <svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" style="transform: rotate(-90deg);">
          ${slicesSvg}
        </svg>
        ${legendHtml}
      </div>
    `;
  }

  /**
   * Render Horizontal Bar Ranking (Corridors / Localities)
   */
  static renderHorizontalBars(container, items = [], options = {}) {
    if (!container || !items.length) return;
    const { valueKey = 'value', labelKey = 'label', unit = '', color = '#3b82f6' } = options;
    const max = Math.max(...items.map(it => it[valueKey] || 0)) || 1;

    let html = '<div class="hbar-list">';
    items.forEach((it) => {
      const val = it[valueKey] || 0;
      const pct = Math.min(100, (val / max) * 100);
      const barColor = it.color || color;
      html += `
        <div class="hbar-row">
          <div class="hbar-header">
            <span class="hbar-label">${it[labelKey]}</span>
            <span class="hbar-val">${typeof val === 'number' ? val.toLocaleString() : val} ${unit}</span>
          </div>
          <div class="hbar-track">
            <div class="hbar-fill" style="width: ${pct}%; background-color: ${barColor};"></div>
          </div>
        </div>
      `;
    });
    html += '</div>';
    container.innerHTML = html;
  }
}

