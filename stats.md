---
layout: default
---

<div id = "password_overlay" class = "password-overlay">
	<div class = "password-box">
		<h3>
			enter password
		</h3>
		<input type = "password" id = "password_input" placeholder = "password (press enter)">
		<p id = "password_error" class = "password-error">
			incorrect password
		</p>
	</div>
</div>

<div class = "stats-page" id = "stats_content" style = "display:none;">
	<p class = "intro">
		<i> Billable Hours. </i>
		Upload a .xlsx in the correct format and perform a statistical summary of the billable hours.
	</p>

	<div class = "upload">
		<label for = "xlsxFile" class = "action-btn file-label">
			choose .xlsx
		</label>
		<input id = "xlsxFile" class = "file-input" type = "file" accept = ".xlsx,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet">
		<div id = "status" class = "status" aria-live = "polite"></div>
	</div>

	<div class = "grid" id = "chartGrid" style = "display:none;">
		<section class = "card">
			<h2>
				weekly
			</h2>
			<canvas id = "chartWeekly" height = "150"></canvas>
			<div class = "card-actions">
				<button class = "action-btn table-toggle" type = "button" data-target = "tableWeeklyWrap">
					show table
				</button>
				<button class = "action-btn export-btn" type = "button" data-target = "tableWeekly">
					export .csv
				</button>
			</div>
			<div class = "table-wrap" id = "tableWeeklyWrap" hidden>
				<table id = "tableWeekly" class = "data-table">
					<thead>
						<tr>
							<th>
								week
							</th>
							<th>
								hours
							</th>
						</tr>
					</thead>
					<tbody></tbody>
				</table>
			</div>
		</section>

		<section class = "card">
			<h2>
				biweekly (14 days)
			</h2>
			<canvas id = "chartBiweekly" height = "150"></canvas>
			<div class = "card-actions">
				<button class = "action-btn table-toggle" type = "button" data-target = "tableBiweeklyWrap">
					show table
				</button>
				<button class = "action-btn export-btn" type = "button" data-target = "tableBiweekly">
					export .csv
				</button>
			</div>
			<div class = "table-wrap" id = "tableBiweeklyWrap" hidden>
				<table id = "tableBiweekly" class = "data-table">
					<thead>
						<tr>
							<th>
								two_weeks
							</th>
							<th>
								hours
							</th>
						</tr>
					</thead>
					<tbody></tbody>
				</table>
			</div>
		</section>

		<section class = "card">
			<h2>
				monthly
			</h2>
			<canvas id = "chartMonthly" height = "150"></canvas>
			<div class = "card-actions">
				<button class = "action-btn table-toggle" type = "button" data-target = "tableMonthlyWrap">
					show table
				</button>
				<button class = "action-btn export-btn" type = "button" data-target = "tableMonthly">
					export .csv
				</button>
			</div>
			<div class = "table-wrap" id = "tableMonthlyWrap" hidden>
				<table id = "tableMonthly" class = "data-table">
					<thead>
						<tr>
							<th>
								month
							</th>
							<th>
								hours
							</th>
						</tr>
					</thead>
					<tbody></tbody>
				</table>
			</div>
		</section>
	</div>
</div>

<style>
	.stats-page {
		max-width: 900px;
		margin: 0 auto;
	}
	.stats-page h1,
	.stats-page h2 {
		font-weight: 400;
	}
	#author-name {
		font-family: "Inconsolata", monospace;
		text-transform: none;
	}
	.navbar-ul { display: none; }
	.upload {
		margin: 1rem 0 1.5rem 0;
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.5rem;
	}
	.file-input {
		position: absolute;
		left: -9999px;
	}
	.file-label {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		min-width: 120px;
	}
	.status {
		font-size: 0.9rem;
		color: #333;
	}
	.grid {
		display: grid;
		gap: 1.5rem;
	}
	.card {
		padding: 1rem;
		border: 1px solid #e5e5e5;
		border-radius: 8px;
		background: #fafafa;
	}
	.card canvas {
		width: 100%;
		max-height: 275px;
	}
	.card-actions {
		margin-top: 0.5rem;
		display: flex;
		gap: 0.5rem;
		flex-wrap: wrap;
	}
	.action-btn {
		padding: 8px 15px;
		background: #4a4a4a;
		color: white;
		border: none;
		border-radius: 3px;
		cursor: pointer;
		font-family: "Inconsolata", monospace;
		transition: all 0.3s;
	}
	.action-btn:hover { background: #333; }
	.action-btn:disabled { background: #ccc; cursor: not-allowed; }
	.password-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: white;
		z-index: 10000;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	.password-box {
		text-align: center;
		padding: 30px;
		border: 1px solid #ddd;
		border-radius: 5px;
		background: #f9f9f9;
	}
	.password-box h3 { margin-bottom: 20px; }
	.password-box input {
		padding: 10px;
		border: 1px solid #ddd;
		border-radius: 3px;
		font-family: "Inconsolata", monospace;
		margin-bottom: 10px;
		width: 200px;
	}
	.password-error {
		color: #ff4444;
		margin-top: 10px;
		display: none;
	}
	.table-wrap {
		overflow-x: auto;
		margin-top: 0.75rem;
	}
	.data-table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.9rem;
	}
	.data-table th,
	.data-table td {
		text-align: left;
		padding: 0.2rem 0.35rem;
		border-bottom: 1px solid #ddd;
		white-space: nowrap;
	}
	.intro {
		margin: 0 0 1rem 0;
	}
	@media (min-width: 900px) {
		.grid {
			grid-template-columns: 1fr;
		}
	}
</style>

<script src = "stats/xlsx.full.min.js"></script>
<script src = "https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script>
	const keepTypes = new Set([
		"billable",
		"pro_bono",
		"recruitment",
		"management",
		"practice_development",
	]);

	const typeMap = {
		"OTH": "others",
		"BIL": "billable",
		"PSQ": "pro_bono",
		"REC": "recruitment",
		"MAN": "management",
		"ADM": "administrative",
		"PD": "practice_development",
		"SICK": "sick",
		"VAC": "vacation",
	};

	const statusEl = document.getElementById("status");
	const fileInput = document.getElementById("xlsxFile");
	const chartGrid = document.getElementById("chartGrid");

	let chartWeekly = null;
	let chartBiweekly = null;
	let chartMonthly = null;
	let lastDateKey = "";
	const STATS_PASSWORD = "fands_2025";

	function setStatus(msg) {
		statusEl.textContent = msg;
	}

	function checkPassword() {
		if (sessionStorage.getItem("stats_authenticated") === "true") {
			document.getElementById("password_overlay").style.display = "none";
			document.getElementById("stats_content").style.display = "block";
			return true;
		}
		return false;
	}

	function authenticate() {
		const input = document.getElementById("password_input").value;
		if (input === STATS_PASSWORD) {
			sessionStorage.setItem("stats_authenticated", "true");
			document.getElementById("password_overlay").style.display = "none";
			document.getElementById("stats_content").style.display = "block";
		} else {
			document.getElementById("password_error").style.display = "block";
			document.getElementById("password_input").value = "";
			document.getElementById("password_input").focus();
		}
	}

	document.addEventListener("DOMContentLoaded", () => {
		const author = document.getElementById("author-name");
		if (author) author.textContent = "\\keller";
		const footerLink = document.querySelector(".container.content p a");
		if (footerLink) {
			const span = document.createElement("span");
			span.innerHTML = footerLink.innerHTML;
			footerLink.replaceWith(span);
		}
		if (!checkPassword()) {
			const input = document.getElementById("password_input");
			input.focus();
			input.addEventListener("keypress", (e) => {
				if (e.key === "Enter") authenticate();
			});
			return;
		}
	});

	function pad2(n) {
		return String(n).padStart(2, "0");
	}

	function formatDateUTC(dt) {
		return `${dt.getUTCFullYear()}-${pad2(dt.getUTCMonth() + 1)}-${pad2(dt.getUTCDate())}`;
	}

	function parseDate(raw) {
		if (!raw) return null;
		if (raw instanceof Date && !isNaN(raw)) {
			return new Date(Date.UTC(raw.getFullYear(), raw.getMonth(), raw.getDate()));
		}
		if (typeof raw === "number" && Number.isFinite(raw) && typeof XLSX !== "undefined" && XLSX && XLSX.SSF) {
			const p = XLSX.SSF.parse_date_code(raw);
			if (p && p.y && p.m && p.d) {
				return new Date(Date.UTC(p.y, p.m - 1, p.d));
			}
		}
		const s = String(raw).trim();
		let m = s.match(/^(\d{4})[-/](\d{2})[-/](\d{2})(?:[ T].*)?$/);
		if (m) {
			const y = Number(m[1]);
			const mo = Number(m[2]);
			const d = Number(m[3]);
			if (!y || !mo || !d) return null;
			return new Date(Date.UTC(y, mo - 1, d));
		}
		m = s.match(/^(\d{1,2})\/(\d{1,2})\/(\d{2,4})(?:[ T].*)?$/);
		if (m) {
			const mo = Number(m[1]);
			const d = Number(m[2]);
			let y = Number(m[3]);
			if (y < 100) y += 2000;
			if (!y || !mo || !d) return null;
			return new Date(Date.UTC(y, mo - 1, d));
		}
		return null;
	}

	function weekStartMondayUTC(dt) {
		const day = dt.getUTCDay();
		const diff = (day + 6) % 7;
		return new Date(Date.UTC(dt.getUTCFullYear(), dt.getUTCMonth(), dt.getUTCDate() - diff));
	}

	function biweekStartMondayUTC(dt) {
		const weekStart = weekStartMondayUTC(dt);
		const epoch = Date.UTC(1970, 0, 5);
		const weeksSince = Math.floor((weekStart.getTime() - epoch) / (7 * 86400000));
		const biweekIndex = Math.floor(weeksSince / 2);
		return new Date(epoch + biweekIndex * 2 * 7 * 86400000);
	}

	function monthKeyUTC(dt) {
		return `${dt.getUTCFullYear()}-${pad2(dt.getUTCMonth() + 1)}`;
	}

	function normalizeHeaders(fields) {
		const map = {};
		for (const f of fields) {
			const key = String(f).trim().toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
			if (key === "date" || key === "work date") map.date = f;
			if (key === "hours" || key === "work hours") map.hours = f;
			if (key === "type" || key === "work type") map.type = f;
		}
		return map;
	}

	function fromXlsxFile(file) {
		return new Promise((resolve, reject) => {
			const reader = new FileReader();
			reader.onload = (e) => {
				try {
					const data = new Uint8Array(e.target.result);
					const wb = XLSX.read(data, { type: "array", cellDates: true });
					if (!wb.SheetNames || !wb.SheetNames.length) {
						throw new Error("No sheets found.");
					}
					const ws = wb.Sheets[wb.SheetNames[0]];
					const rows = XLSX.utils.sheet_to_json(ws, { header: 1, defval: "", raw: false });
					resolve(rows);
				} catch (err) {
					reject(err);
				}
			};
			reader.onerror = () => reject(new Error("Failed to read file."));
			reader.readAsArrayBuffer(file);
		});
	}

	function toFloat(v) {
		const num = Number(v);
		return Number.isFinite(num) ? num : null;
	}

	function parseRows(rows, headerMap) {
		const cleaned = [];
		for (const row of rows) {
			const rawDate = row[headerMap.date];
			const rawHours = row[headerMap.hours];
			const rawType = row[headerMap.type];
			const dt = parseDate(rawDate);
			const hours = toFloat(rawHours);
			if (!dt || hours === null || rawType === undefined || rawType === null) continue;
			const code = String(rawType).trim().toUpperCase();
			const mapped = typeMap[code] || String(rawType).trim().toLowerCase();
			cleaned.push({ dt, hours, type: mapped });
		}
		return cleaned;
	}

	function aggregate(cleaned) {
		const weekly = new Map();
		const biweekly = new Map();
		const monthly = new Map();
		let maxDate = null;

		for (const row of cleaned) {
			if (!keepTypes.has(row.type)) continue;
			if (!maxDate || row.dt > maxDate) maxDate = row.dt;
			const w = formatDateUTC(weekStartMondayUTC(row.dt));
			const bw = formatDateUTC(biweekStartMondayUTC(row.dt));
			const m = monthKeyUTC(row.dt);

			weekly.set(w, (weekly.get(w) || 0) + row.hours);
			biweekly.set(bw, (biweekly.get(bw) || 0) + row.hours);
			monthly.set(m, (monthly.get(m) || 0) + row.hours);
		}

		const toSortedArray = (map) => {
			return Array.from(map.entries())
				.sort((a, b) => a[0].localeCompare(b[0]))
				.map(([k, v]) => ({ key: k, value: v }));
		};

		return {
			weekly: toSortedArray(weekly),
			biweekly: toSortedArray(biweekly),
			monthly: toSortedArray(monthly),
			maxDate,
		};
	}

	function renderTable(tableId, rows) {
		const tbody = document.querySelector(`#${tableId} tbody`);
		tbody.innerHTML = "";
		for (const row of rows) {
			const tr = document.createElement("tr");
			const tdKey = document.createElement("td");
			const tdVal = document.createElement("td");
			tdKey.textContent = row.key;
			tdVal.textContent = row.value.toFixed(2);
			tr.appendChild(tdKey);
			tr.appendChild(tdVal);
			tbody.appendChild(tr);
		}
	}

	function renderChart(canvasId, rows, base) {
		const labels = rows.map((r) => r.key);
		const data = rows.map((r) => Number(r.value.toFixed(2)));
		const ctx = document.getElementById(canvasId).getContext("2d");
		return new Chart(ctx, {
			type: "line",
			data: {
				labels,
				datasets: [{
					label: `hours (${base})`,
					data,
					borderColor: "#111",
					backgroundColor: "rgba(0,0,0,0.05)",
					borderWidth: 1.5,
					pointRadius: 1.0,
					tension: 0.1,
				}],
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				plugins: {
					legend: { display: false },
					tooltip: {
						callbacks: {
							label: (ctx) => {
								const val = Number.isFinite(ctx.parsed.y) ? ctx.parsed.y.toFixed(2) : ctx.parsed.y;
								return `hours (${base}) = ${val}`;
							},
						},
					},
				},
				font: {
					family: "\"Inconsolata\", monospace",
				},
				scales: {
					x: {
						ticks: {
							maxRotation: 30,
							minRotation: 30,
							font: {
								family: "\"Inconsolata\", monospace",
							},
						},
						title: {
							display: true,
							text: `t (${base})`,
							font: {
								family: "\"Inconsolata\", monospace",
							},
						},
					},
					y: {
						beginAtZero: true,
						title: {
							display: true,
							text: "h (hours)",
							font: {
								family: "\"Inconsolata\", monospace",
							},
						},
						ticks: {
							font: {
								family: "\"Inconsolata\", monospace",
							},
						},
					},
				},
			},
		});
	}

	function destroyCharts() {
		if (chartWeekly) chartWeekly.destroy();
		if (chartBiweekly) chartBiweekly.destroy();
		if (chartMonthly) chartMonthly.destroy();
		chartWeekly = chartBiweekly = chartMonthly = null;
	}

	function findHeaderRow(rows) {
		for (let i = 0; i < rows.length; i++) {
			const row = rows[i] || [];
			const headerMap = normalizeHeaders(row);
			if (headerMap.date && headerMap.hours && headerMap.type) return i;
		}
		return -1;
	}

	function rowsToObjects(rows, headerIndex) {
		const header = rows[headerIndex].map((h) => String(h).trim());
		const out = [];
		for (let i = headerIndex + 1; i < rows.length; i++) {
			const r = rows[i] || [];
			if (!r.length) continue;
			const obj = {};
			for (let c = 0; c < header.length; c++) {
				if (!header[c]) continue;
				obj[header[c]] = r[c];
			}
			out.push(obj);
		}
		return { data: out, fields: header };
	}

	function toCsvLine(values) {
		return values.map((v) => {
			const s = v === null || v === undefined ? "" : String(v);
			if (/[",\n]/.test(s)) {
				return `"${s.replace(/"/g, "\"\"")}"`;
			}
			return s;
		}).join(",");
	}

	function exportTableCsv(tableId) {
		const table = document.getElementById(tableId);
		if (!table) return;
		const headerCells = Array.from(table.querySelectorAll("thead th"));
		const headers = headerCells.map((h) => h.textContent.trim());
		const rows = Array.from(table.querySelectorAll("tbody tr")).map((tr) => {
			return Array.from(tr.querySelectorAll("td")).map((td) => td.textContent.trim());
		});
		const csvLines = [toCsvLine(headers)].concat(rows.map((r) => toCsvLine(r))).join("\n");
		const blob = new Blob([csvLines], { type: "text/csv;charset=utf-8;" });
		const url = URL.createObjectURL(blob);
		const link = document.createElement("a");
		link.href = url;
		const baseMap = {
			"tableWeekly": "week",
			"tableBiweekly": "two_weeks",
			"tableMonthly": "month",
		};
		const base = baseMap[tableId] || tableId;
		const dateSuffix = lastDateKey ? `_${lastDateKey}` : "";
		link.download = `billable_hours_${base}_table${dateSuffix}.csv`;
		document.body.appendChild(link);
		link.click();
		link.remove();
		URL.revokeObjectURL(url);
	}

	function handleRows(rows, fields) {
		const headerMap = normalizeHeaders(fields);
		if (!headerMap.date || !headerMap.hours || !headerMap.type) {
			const shown = fields.slice(0, 10).join(", ");
			setStatus(`Missing columns. Need date, hours, type (or Work Date, Work Hours, Work Type). Found: ${shown}`);
			return;
		}

		const cleaned = parseRows(rows, headerMap);
		const agg = aggregate(cleaned);
		lastDateKey = agg.maxDate ? formatDateUTC(agg.maxDate) : "";
		destroyCharts();

		renderTable("tableWeekly", agg.weekly);
		renderTable("tableBiweekly", agg.biweekly);
		renderTable("tableMonthly", agg.monthly);

		chartWeekly = renderChart("chartWeekly", agg.weekly, "week");
		chartBiweekly = renderChart("chartBiweekly", agg.biweekly, "two_weeks");
		chartMonthly = renderChart("chartMonthly", agg.monthly, "month");

		if (chartGrid) chartGrid.style.display = "grid";
		setStatus(`loaded ${cleaned.length} rows (showing billable only, billable/pro bono/recruitment/management/practice development).`);
	}

	fileInput.addEventListener("change", () => {
		const file = fileInput.files[0];
		if (!file) return;
		const name = (file.name || "").toLowerCase();
		if (!name.endsWith(".xlsx")) {
			setStatus("Please upload a .xlsx file only.");
			return;
		}
		if (typeof XLSX === "undefined") {
			setStatus("XLSX parser not loaded.");
			return;
		}
		setStatus("Parsing .xlsx...");
		fromXlsxFile(file).then((rows) => {
			if (!rows.length) {
				setStatus(".xlsx appears empty.");
				return;
			}
			const headerIndex = findHeaderRow(rows);
			let parsed = null;
			if (headerIndex !== -1) {
				parsed = rowsToObjects(rows, headerIndex);
				handleRows(parsed.data, parsed.fields);
				return;
			}
			const firstNonEmpty = rows.findIndex((r) => (r || []).some((v) => String(v).trim() !== ""));
			if (firstNonEmpty !== -1) {
				parsed = rowsToObjects(rows, firstNonEmpty);
				handleRows(parsed.data, parsed.fields);
				return;
			}
			setStatus("Missing header row in .xlsx. Need Work Date/Work Hours/Work Type.");
		}).catch((err) => {
			const msg = err && err.message ? err.message : "unknown error";
			setStatus(`Failed to parse .xlsx: ${msg}`);
		});
	});

	document.querySelectorAll(".table-toggle").forEach((btn) => {
		btn.addEventListener("click", () => {
			const targetId = btn.getAttribute("data-target");
			const wrap = document.getElementById(targetId);
			const isHidden = wrap.hasAttribute("hidden");
			if (isHidden) {
				wrap.removeAttribute("hidden");
				btn.textContent = "hide table";
			} else {
				wrap.setAttribute("hidden", "");
				btn.textContent = "show table";
			}
		});
	});

	document.querySelectorAll(".export-btn").forEach((btn) => {
		btn.addEventListener("click", () => {
			const targetId = btn.getAttribute("data-target");
			exportTableCsv(targetId);
		});
	});

</script>
