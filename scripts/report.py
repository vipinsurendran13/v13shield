"""
Generates an ultra-premium, interactive HTML clinical dashboard for V13Shield.
Uses Tailwind CSS and Chart.js for smooth animations and high-end visual appeal.
"""
import json
from datetime import datetime

# Kept for backward compatibility with main.py structure
def make_risk_plot(gene_risk):
    return ""

def generate_report(result, output_path):
    from analyze import classify_overall_risk
    gene_risk = classify_overall_risk(result["findings"])
    sample_name = result["findings"][0]["sample"] if result["findings"] else "Unknown"

    # Pre-serialize fields to clean JSON strings
    findings_json_str = json.dumps(result["findings"])
    gene_risk_json_str = json.dumps(gene_risk)

    # Building the dynamic findings HTML rows purely in Python
    findings_html = ""
    for f in result["findings"]:
        raw_risk = gene_risk.get(f["gene"], "Low-Moderate risk")
        
        # Color mapping configuration
        styles = {
            'High risk': {'card': 'border-red-200 bg-gradient-to-r from-red-50/30 to-transparent shadow-red-100', 'badge': 'bg-red-50 text-red-700 border-red-200'},
            'Moderate-High risk': {'card': 'border-orange-200 bg-gradient-to-r from-orange-50/20 to-transparent shadow-orange-100', 'badge': 'bg-orange-50 text-orange-700 border-orange-200'},
            'Moderate risk': {'card': 'border-amber-200 bg-gradient-to-r from-amber-50/20 to-transparent', 'badge': 'bg-amber-50 text-amber-700 border-amber-200'},
            'Low-Moderate risk': {'card': 'border-emerald-200 bg-gradient-to-r from-emerald-50/20 to-transparent', 'badge': 'bg-emerald-50 text-emerald-700 border-emerald-200'}
        }.get(raw_risk, {'card': 'border-slate-200 bg-white', 'badge': 'bg-slate-50 text-slate-700 border-slate-200'})

        drugs_badges = "".join([f'<span class="bg-slate-900 text-white font-medium text-xs px-2.5 py-1 rounded-md tracking-tight shadow-sm mr-1.5 mb-1 inline-block">{d}</span>' for d in f["drugs"]])

        findings_html += f"""
        <div class="bg-white border rounded-2xl p-6 shadow-sm transition duration-300 hover:-translate-y-0.5 hover:shadow-md {styles['card']}">
            <div class="flex flex-wrap items-start justify-between gap-4 border-b border-slate-100 pb-4 mb-4">
                <div class="space-y-1">
                    <div class="flex items-center gap-2.5">
                        <h3 class="text-xl font-bold text-slate-900 tracking-tight">{f['gene']}</h3>
                        <span class="bg-indigo-50 text-indigo-700 border border-indigo-100 text-[11px] font-mono font-bold px-2 py-0.5 rounded-md shadow-sm">{f['star_allele']}</span>
                    </div>
                    <div class="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs font-mono text-slate-500">
                        <span>ID: <strong class="text-slate-700 font-medium">{f['rsid']}</strong></span>
                        <span class="text-slate-300">•</span>
                        <span>Genotype: <strong class="text-slate-700 font-semibold">{f['genotype_raw']}</strong></span>
                        <span class="text-slate-300">•</span>
                        <span>Zygosity: <strong class="text-slate-700 font-semibold">{f['zygosity']}</strong></span>
                    </div>
                </div>
                <span class="px-3.5 py-1 text-xs font-bold rounded-full border shadow-sm tracking-wide shrink-0 {styles['badge']}">
                    {raw_risk}
                </span>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm mt-2">
                <div class="space-y-1">
                    <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Contraindicated Agents</span>
                    <div class="flex flex-wrap items-start">{drugs_badges}</div>
                </div>
                <div class="md:col-span-2 space-y-3">
                    <div class="space-y-0.5">
                        <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Patient Safety Guidance Translation</span>
                        <p class="text-slate-700 leading-relaxed font-normal text-sm">{f['risk_summary']}</p>
                    </div>
                    <div class="bg-slate-50 border border-slate-100 rounded-xl p-3 text-xs text-slate-600 font-normal">
                        <span class="text-[9px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Functional Molecular Gene Phenotype Variant Mechanics</span>
                        {f['effect']}
                    </div>
                </div>
            </div>
        </div>
        """

    if not result["findings"]:
        findings_html = """
        <div class="text-center py-16 bg-white border border-slate-200 rounded-2xl p-8 shadow-sm max-w-3xl mx-auto">
            <div class="h-14 w-14 rounded-2xl bg-emerald-50 border border-emerald-200 text-emerald-500 flex items-center justify-center font-bold text-2xl mx-auto mb-4 shadow-sm">✓</div>
            <h3 class="text-lg font-bold text-slate-900 tracking-tight">No Actionable Toxicity Targets Flagged</h3>
            <p class="text-xs text-slate-400 mt-1.5 max-w-md mx-auto leading-relaxed">
                No validated clinical risk polymorphisms were found within the assay operational target panel spectrum (DPYD, TPMT, NUDT15, UGT1A1). This drops downstream inherited therapeutic risk profiles but normal patient monitor sequencing is required.
            </p>
        </div>
        """

    generated_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Clean standard string (No 'f' prefix!) to avoid any bracket parsing bugs
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>V13Shield Dashboard &mdash; PGx Safety Report</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
        body { font-family: 'Plus Jakarta Sans', sans-serif; }
        .mono { font-family: 'JetBrains Mono', monospace; }
    </style>
</head>
<body class="bg-[#f8fafc] text-slate-900 min-h-screen pb-24 antialiased">

    <header class="bg-slate-950 text-white relative overflow-hidden border-b border-slate-800">
        <div class="absolute inset-0 bg-[radial-gradient(circle_at_30%_30%,#1e1b4b,transparent_60%)] opacity-70"></div>
        <div class="max-w-6xl mx-auto px-6 py-10 relative z-10 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-8">
            <div>
                <div class="flex items-center gap-3">
                    <div class="h-10 w-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center font-black text-xl tracking-tighter shadow-lg shadow-indigo-500/30">V</div>
                    <div>
                        <div class="flex items-center gap-2">
                            <h1 class="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-100 to-slate-300 bg-clip-text text-transparent">V13Shield</h1>
                            <span class="bg-indigo-500/20 text-indigo-400 text-[10px] font-bold tracking-widest uppercase px-2 py-0.5 rounded border border-indigo-500/30 font-mono">v1.0</span>
                        </div>
                        <p class="text-slate-400 text-sm mt-0.5 font-medium">Precision Pharmacogenomics (PGx) Safety Diagnostic Interface</p>
                    </div>
                </div>
            </div>
            
            <div class="grid grid-cols-2 sm:grid-cols-4 lg:flex gap-4 sm:gap-6 text-xs font-mono">
                <div class="bg-white/5 border border-white/10 rounded-xl px-4 py-3 min-w-[130px]">
                    <span class="text-slate-500 block text-[10px] uppercase tracking-wider mb-1 font-sans font-bold">Patient Sample</span>
                    <span class="text-indigo-300 font-bold text-sm block truncate">__SAMPLE_NAME__</span>
                </div>
                <div class="bg-white/5 border border-white/10 rounded-xl px-4 py-3 min-w-[130px]">
                    <span class="text-slate-500 block text-[10px] uppercase tracking-wider mb-1 font-sans font-bold">Analysis Run</span>
                    <span class="text-slate-200 text-sm block font-medium">__GENERATED_DATE__</span>
                </div>
                <div class="bg-white/5 border border-white/10 rounded-xl px-4 py-3 min-w-[130px]">
                    <span class="text-slate-500 block text-[10px] uppercase tracking-wider mb-1 font-sans font-bold">DB Snapshot</span>
                    <span class="text-slate-200 text-sm block font-medium">__DB_VERSION__</span>
                </div>
                <div class="bg-white/5 border border-white/10 rounded-xl px-4 py-3 min-w-[130px]">
                    <span class="text-slate-500 block text-[10px] uppercase tracking-wider mb-1 font-sans font-bold">Total Scanned</span>
                    <span class="text-emerald-400 font-bold text-sm block font-medium">__TOTAL_SCANNED__ Variants</span>
                </div>
            </div>
        </div>
    </header>

    <main class="max-w-6xl mx-auto px-6 mt-10 space-y-8">
        
        <div class="relative bg-white/80 backdrop-blur-md border border-slate-200 rounded-2xl p-6 shadow-sm overflow-hidden group">
            <div class="absolute -right-24 -bottom-24 w-48 h-48 bg-amber-500/5 rounded-full blur-2xl"></div>
            
            <div class="flex flex-col md:flex-row gap-5 items-center relative z-10">
                <div class="bg-gradient-to-tr from-amber-500 to-orange-400 text-white rounded-2xl h-14 w-14 flex items-center justify-center shrink-0 shadow-lg shadow-amber-500/20 border border-amber-400/20">
                    <svg class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                    </svg>
                </div>
                
                <div class="space-y-1.5 flex-1 w-full text-center md:text-left">
                    <div class="flex flex-col sm:flex-row sm:items-baseline gap-2 justify-center md:justify-start">
                        <h4 class="text-xl font-extrabold tracking-tight text-slate-900">V13Shield PGx</h4>
                        <span class="text-xs font-bold text-amber-600 tracking-wider uppercase bg-amber-50 border border-amber-200/60 px-2 py-0.5 rounded-md">
                            A Precision Diagnostic Screening Aid
                        </span>
                    </div>
                    <p class="text-sm text-slate-600 leading-relaxed font-normal">
                        __DISCLAIMER__
                    </p>
                    
                    <div class="pt-2 flex justify-center md:justify-start">
                        <span class="text-[10px] font-mono tracking-widest text-slate-400 uppercase border-t border-slate-100 pt-1.5 block w-full sm:w-auto">
                            Architect Identity: V13
                        </span>
                    </div>
                </div>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div class="lg:col-span-2 bg-white border border-slate-200/80 rounded-2xl p-6 shadow-sm flex flex-col justify-between">
                <div class="mb-4">
                    <h2 class="text-lg font-bold text-slate-900 tracking-tight">Systemic Toxicity Risk Profile Mapping</h2>
                    <p class="text-xs text-slate-400 mt-0.5">Real-time normalized computational variant metabolic index scores</p>
                </div>
                <div class="relative w-full h-52 flex items-center justify-center">
                    <canvas id="v13NativeChart"></canvas>
                </div>
            </div>
            
            <div class="bg-slate-900 text-white border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between relative overflow-hidden">
                <div>
                    <h3 class="text-sm font-bold text-indigo-400 uppercase tracking-wider mb-4">Screening Diagnostics Matrix</h3>
                    <div class="space-y-3.5 text-xs">
                        <div class="flex justify-between items-center border-b border-slate-800 pb-2.5">
                            <span class="text-slate-400 font-medium">Assay Target Status</span>
                            <span class="bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded font-bold font-mono">SUCCESSFUL</span>
                        </div>
                        <div class="flex justify-between items-center border-b border-slate-800 pb-2.5">
                            <span class="text-slate-400 font-medium">Core Genes Queried</span>
                            <span class="text-slate-200 font-bold">4 Framework Genes</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span class="text-slate-400 font-medium">Flagged Risks Found</span>
                            <span class="font-mono text-sm font-bold text-indigo-400">
                                __FINDINGS_COUNT__ Genes
                            </span>
                        </div>
                    </div>
                </div>
                <div class="bg-white/5 border border-white/10 rounded-xl p-3 text-center mt-6">
                    <span class="text-[10px] text-slate-500 uppercase font-bold tracking-wider block">Pipeline Architecture Node</span>
                    <p class="text-xs font-mono font-bold text-slate-300 mt-0.5">V13Shield-PGx-Engine-v1.0</p>
                </div>
            </div>
        </div>

        <div class="space-y-4">
            <h2 class="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
                Actionable Genomic Findings Overview
                <span class="h-2 w-2 rounded-full bg-indigo-600"></span>
            </h2>
            __FINDINGS_ROWS__
        </div>

        <div class="bg-white border border-slate-200/80 rounded-2xl overflow-hidden shadow-sm">
            <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50">
                <h3 class="text-sm font-bold text-slate-800 tracking-tight">V13Shield Reference Core Assay Target Scope</h3>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full text-left text-xs border-collapse">
                    <thead>
                        <tr class="text-slate-400 border-b border-slate-200/60 font-bold uppercase tracking-wider bg-white">
                            <th class="px-6 py-3.5 font-bold">Assay Gene Axis</th>
                            <th class="px-6 py-3.5 font-bold">Primary Therapeutic Group Category</th>
                            <th class="px-6 py-3.5 font-bold">Monitored Chemotherapeutic Drug Agents</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100 font-medium text-slate-700">
                        <tr class="hover:bg-slate-50/40 transition">
                            <td class="px-6 py-3.5 font-bold mono text-slate-900 text-sm">DPYD</td>
                            <td class="px-6 py-3.5 text-slate-500">Fluoropyrimidines</td>
                            <td class="px-6 py-3.5"><span class="bg-slate-100 text-slate-700 border border-slate-200/50 rounded px-2 py-0.5 mr-1">5-Fluorouracil (5-FU)</span><span class="bg-slate-100 text-slate-700 border border-slate-200/50 rounded px-2 py-0.5">Capecitabine</span></td>
                        </tr>
                        <tr class="hover:bg-slate-50/40 transition">
                            <td class="px-6 py-3.5 font-bold mono text-slate-900 text-sm">TPMT</td>
                            <td class="px-6 py-3.5 text-slate-500">Thiopurines</td>
                            <td class="px-6 py-3.5"><span class="bg-slate-100 text-slate-700 border border-slate-200/50 rounded px-2 py-0.5 mr-1">6-Mercaptopurine</span><span class="bg-slate-100 text-slate-700 border border-slate-200/50 rounded px-2 py-0.5 mr-1">Azathioprine</span><span class="bg-slate-100 text-slate-700 border border-slate-200/50 rounded px-2 py-0.5">Thioguanine</span></td>
                        </tr>
                        <tr class="hover:bg-slate-50/40 transition">
                            <td class="px-6 py-3.5 font-bold mono text-slate-900 text-sm">NUDT15</td>
                            <td class="px-6 py-3.5 text-slate-500">Thiopurines</td>
                            <td class="px-6 py-3.5"><span class="bg-slate-100 text-slate-700 border border-slate-200/50 rounded px-2 py-0.5 mr-1">6-Mercaptopurine</span><span class="bg-slate-100 text-slate-700 border border-slate-200/50 rounded px-2 py-0.5 mr-1">Azathioprine</span><span class="bg-slate-100 text-slate-700 border border-slate-200/50 rounded px-2 py-0.5">Thioguanine</span></td>
                        </tr>
                        <tr class="hover:bg-slate-50/40 transition">
                            <td class="px-6 py-3.5 font-bold mono text-slate-900 text-sm">UGT1A1</td>
                            <td class="px-6 py-3.5 text-slate-500">Topoisomerase inhibitors</td>
                            <td class="px-6 py-3.5"><span class="bg-slate-100 text-slate-700 border border-slate-200/50 rounded px-2 py-0.5">Irinotecan</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

    </main>

    <footer class="max-w-6xl mx-auto px-6 mt-16 pt-6 border-t border-slate-200 flex flex-col sm:flex-row justify-between items-center gap-4 text-xs text-slate-400 font-medium">
        <p>© 2026 V13Shield System Diagnostic Application Axis &bull; Engineering Lead: Vipin surendra kumar</p>
        <p class="text-right sm:text-right text-[11px] text-slate-300 bg-slate-900 rounded-lg border border-slate-800 px-3 py-1 font-mono">NODE ENGINE STATUS: ONLINE</p>
    </footer>

    <script>
        const backendRisks = __RISK_JSON__;
        const scoreMetrics = { "High risk": 4, "Moderate-High risk": 3, "Moderate risk": 2, "Low-Moderate risk": 1 };
        const colorPalette = { "High risk": "#ef4444", "Moderate-High risk": "#f97316", "Moderate risk": "#eab308", "Low-Moderate risk": "#22c55e" };
        
        const labels = [];
        const dataValues = [];
        const backgroundColors = [];
        
        Object.keys(backendRisks).forEach(gene => {
            labels.push(gene);
            dataValues.push(scoreMetrics[backendRisks[gene]] || 0);
            backgroundColors.push(colorPalette[backendRisks[gene]] || "#cbd5e1");
        });
        
        if(labels.length === 0) {
            labels.push("No Risks Flagged");
            dataValues.push(0);
            backgroundColors.push("#94a3b8");
        }

        const ctx = document.getElementById('v13NativeChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    data: dataValues,
                    backgroundColor: backgroundColors,
                    borderRadius: 8,
                    borderSkipped: false,
                    barThickness: 16
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return ' Risk State: ' + backendRisks[context.label];
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        min: 0,
                        max: 4.5,
                        grid: { color: '#f1f5f9', drawTicks: false },
                        border: { display: false },
                        ticks: {
                            stepSize: 1,
                            callback: function(val) {
                                return ['', 'Low-Mod', 'Moderate', 'Mod-High', 'High'][val] || '';
                            },
                            color: '#64748b',
                            font: { family: 'Plus Jakarta Sans', size: 10, weight: 600 }
                        }
                    },
                    y: {
                        grid: { display: false },
                        border: { display: false },
                        ticks: {
                            color: '#1e293b',
                            font: { family: 'JetBrains Mono', size: 12, weight: 700 }
                        }
                    }
                }
            }
        });
    </script>
</body>
</html>
"""

    # Bulletproof text replacements at execution time
    html_content = html_content.replace("__SAMPLE_NAME__", sample_name)
    html_content = html_content.replace("__GENERATED_DATE__", generated_date)
    html_content = html_content.replace("__DB_VERSION__", str(result['db_version']))
    html_content = html_content.replace("__TOTAL_SCANNED__", str(result['total_variants_scanned']))
    html_content = html_content.replace("__DISCLAIMER__", result['disclaimer'])
    html_content = html_content.replace("__FINDINGS_COUNT__", str(len(result["findings"])))
    html_content = html_content.replace("__FINDINGS_ROWS__", findings_html)
    html_content = html_content.replace("__RISK_JSON__", gene_risk_json_str)

    with open(output_path, "w") as f:
        f.write(html_content)

    return output_path
