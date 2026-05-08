import gradio as gr
import threading
import queue
import contextlib
import json
import re
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from main import run_stock_analysis

# =========================================================
# CONFIGURABLE COLORS / THEME
# Edit any value below to retheme the entire app instantly.
# =========================================================

APP_BACKGROUND      = "#0a0a0f"   # Page outermost background
CARD_BACKGROUND     = "#13131a"   # Report card background
CARD_BORDER         = "#2a2a3d"   # Report card border
SECTION_BACKGROUND  = "#1c1c28"   # Inner metric card background
SECTION_BORDER      = "#2e2e45"   # Inner metric card border

TEXT_COLOR          = "#e2e8f0"   # Body text
SUBTEXT_COLOR       = "#8892a4"   # Muted / secondary text
HEADING_COLOR       = "#ffffff"   # H1 / H2 headings

ACCENT_PRIMARY      = "#6c63ff"   # Purple  – primary accent / button
ACCENT_SECONDARY    = "#00d2ff"   # Cyan    – secondary accent
ACCENT_SUCCESS      = "#22c55e"   # Green   – bullish / positive
ACCENT_WARNING      = "#f59e0b"   # Amber   – caution
ACCENT_ERROR        = "#ef4444"   # Red     – bearish / error

BUTTON_BG           = "#6c63ff"   # Analyze button background
BUTTON_TEXT         = "#ffffff"   # Analyze button label

INPUT_BG            = "#13131a"   # Textbox background
INPUT_BORDER        = "#2a2a3d"   # Textbox border
INPUT_FOCUS_BORDER  = "#6c63ff"   # Textbox focus ring
INPUT_TEXT          = "#e2e8f0"   # Textbox text
INPUT_PLACEHOLDER   = "#4a5568"   # Placeholder text

LOG_BACKGROUND      = "#050510"   # Terminal log background
LOG_TEXT_COLOR      = "#a8ff78"   # Terminal log text  ← keep monospace/green
LOG_BORDER          = "#1e3a1e"   # Terminal border

BADGE_BG            = "#1e1e2e"   # Pill / badge background
DIVIDER_COLOR       = "#1e1e2e"   # <hr> divider

DISPLAY_FONT  = "'Inter', 'Segoe UI', Arial, sans-serif"
TERMINAL_FONT = "'Cascadia Code', 'Fira Code', 'Consolas', 'Courier New', monospace"
Name = ""
period = "1Y"
# =========================================================
# GLOBAL QUEUE
# =========================================================

q = queue.Queue()

# =========================================================
# STOCK VALIDATION
# =========================================================

def validate_stock(stock_name):
    try:
        global Name
        search = yf.Search(stock_name, max_results=10)
        if not search.quotes:
            return {"valid": False, "error": f"No matching stocks found for '{stock_name}'"}
        for result in search.quotes:
            symbol = result.get("symbol", "")
            if symbol.endswith(".NS"):
                Name = symbol
                return {"valid": True, "symbol": symbol,
                        "company": result.get("shortname", stock_name)}
        first = search.quotes[0]
        return {"valid": True, "symbol": first.get("symbol"),
                "company": first.get("shortname", stock_name)}
    except Exception as e:
        return {"valid": False, "error": str(e)}

# =========================================================
# STOCK PRICE CHART
# =========================================================

PERIOD_CONFIG = {
    "1W":  {"period": "5d",    "interval": "1d",  "x_ticks": 5},
    "1M":  {"period": "1mo",   "interval": "1d",  "x_ticks": 6},
    "3M":  {"period": "3mo",   "interval": "1d",  "x_ticks": 6},
    "6M":  {"period": "6mo",   "interval": "1d",  "x_ticks": 6},
    "9M":  {"period": "9mo",   "interval": "1d",  "x_ticks": 6},
    "1Y":  {"period": "1y",    "interval": "1wk", "x_ticks": 6},
    "3Y":  {"period": "3y",    "interval": "1wk", "x_ticks": 6},
    "5Y":  {"period": "5y",    "interval": "1mo", "x_ticks": 6},
    "10Y": {"period": "10y",   "interval": "1mo", "x_ticks": 6},
    "All": {"period": "max",   "interval": "1mo", "x_ticks": 6},
}

def fetch_and_plot(stock_name: str, tab_label: str):
    """Fetch OHLC data for *stock_name* and return a Plotly Figure."""
    if not stock_name or not stock_name.strip():
        return go.Figure()

    cfg = PERIOD_CONFIG.get(tab_label, PERIOD_CONFIG["6M"])

    try:

        ticker = yf.Ticker(Name)
        df = ticker.history(period=cfg["period"], interval=cfg["interval"])
        if df.empty:
            raise ValueError("No data returned")

        df = df[["Open"]].copy()
        df.index = pd.to_datetime(df.index)
        df = df.reset_index()
        df.columns = ["Date", "Price"]
        df["Date"] = pd.to_datetime(df["Date"], utc=True).dt.tz_localize(None)

        # Evenly-spaced tick positions
        n_ticks = min(cfg["x_ticks"], len(df))
        tick_indices = np.linspace(0, len(df) - 1, n_ticks, dtype=int)
        tick_vals = df["Date"].iloc[tick_indices].tolist()
        tick_text = [d.strftime("%d %b '%y") for d in tick_vals]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["Date"],
            y=df["Price"],
            mode="lines",
            name="Price",
            line=dict(color=ACCENT_PRIMARY, width=2),
            fill="tozeroy",
            fillcolor=f"rgba(108,99,255,0.08)",
            hovertemplate="%{x|%d %b %Y}<br>₹%{y:,.2f}<extra></extra>",
        ))

        fig.update_layout(
            plot_bgcolor=APP_BACKGROUND,
            paper_bgcolor=CARD_BACKGROUND,
            font=dict(color=TEXT_COLOR, family=DISPLAY_FONT),
            margin=dict(l=16, r=16, t=36, b=16),
            xaxis=dict(
                showgrid=False,
                tickvals=tick_vals,
                ticktext=tick_text,
                tickfont=dict(color=SUBTEXT_COLOR, size=11),
                linecolor=SECTION_BORDER,
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor=SECTION_BORDER,
                tickprefix="₹",
                tickfont=dict(color=SUBTEXT_COLOR, size=11),
                linecolor=SECTION_BORDER,
            ),
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor=SECTION_BACKGROUND,
                bordercolor=CARD_BORDER,
                font=dict(color=TEXT_COLOR),
            ),
            height=300,
        )
        return fig

    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(
            text=f"Could not load chart: {e}",
            xref="paper", yref="paper", x=0.5, y=0.5,
            showarrow=False, font=dict(color=SUBTEXT_COLOR, size=13),
        )
        fig.update_layout(
            plot_bgcolor=APP_BACKGROUND, paper_bgcolor=CARD_BACKGROUND, height=300,
        )
        return fig

# =========================================================
# LOG WRITER
# =========================================================

class QueueWriter:
    def write(self, text):
        q.put(("log", text))
    def flush(self):
        pass

# =========================================================
# EXTRACT JSON
# =========================================================

def extract_json_from_raw(raw_result):
    try:
        cleaned = re.sub(r"```json|```", "", raw_result).strip()
        return json.loads(cleaned)
    except Exception:
        return {"error": "Failed to parse JSON"}

# =========================================================
# REPORT RENDERER
# =========================================================

def create_beautiful_report(data):
    if not data:
        return ""

    if "error" in data:
        return f"""
        <div style="font-family:{DISPLAY_FONT};background:{CARD_BACKGROUND};
                    border:1px solid {ACCENT_ERROR}55;border-left:4px solid {ACCENT_ERROR};
                    padding:28px 32px;border-radius:16px;color:{TEXT_COLOR};margin-top:8px;">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
                <span style="font-size:28px;">⚠️</span>
                <h2 style="margin:0;color:{ACCENT_ERROR};font-size:20px;font-weight:700;">
                    Analysis Error
                </h2>
            </div>
            <p style="color:{SUBTEXT_COLOR};margin:0;font-size:15px;">{data['error']}</p>
        </div>"""

    # ── helpers ──────────────────────────────────────────────────────────────

    def list_items(key, icon, color):
        items = data.get(key, [])
        if not items:
            return f"<li style='color:{SUBTEXT_COLOR}'>No data available</li>"
        return "".join(
            f"<li style='margin-bottom:8px;color:{color}'>"
            f"<span style='color:{ACCENT_SECONDARY};margin-right:6px;'>{icon}</span>{item}</li>"
            for item in items
        )

    def kpi_card(label, value, color):
        return f"""
        <div style="background:{SECTION_BACKGROUND};border:1px solid {SECTION_BORDER};
                    border-top:3px solid {color};padding:20px 24px;border-radius:14px;
                    min-width:180px;flex:1;">
            <div style="font-size:11px;text-transform:uppercase;letter-spacing:1.2px;
                        color:{SUBTEXT_COLOR};font-weight:600;margin-bottom:10px;">
                {label}
            </div>
            <div style="font-size:18px;font-weight:700;color:{color};">{value}</div>
        </div>"""

    def section(title, content, icon, title_color):
        return f"""
        <div style="margin-bottom:28px;">
            <h2 style="font-size:16px;font-weight:700;color:{title_color};margin:0 0 10px 0;">
                {icon} {title}
            </h2>
            <p style="margin:0;color:{TEXT_COLOR};font-size:15px;line-height:1.75;">{content}</p>
        </div>"""

    def list_card(title, items_html, color):
        return f"""
        <div style="background:{SECTION_BACKGROUND};border:1px solid {SECTION_BORDER};
                    border-radius:14px;padding:20px;">
            <h3 style="margin:0 0 14px 0;font-size:13px;font-weight:700;color:{color};
                       text-transform:uppercase;letter-spacing:1px;">{title}</h3>
            <ul style="margin:0;padding-left:4px;list-style:none;
                       font-size:14px;line-height:1.8;">{items_html}</ul>
        </div>"""

    # ── action pill ──────────────────────────────────────────────────────────
    action = data.get("suggested_action", "N/A").upper()
    action_color = (ACCENT_SUCCESS if "BUY" in action
                    else ACCENT_ERROR if "SELL" in action
                    else ACCENT_WARNING)
    action_pill = (
        f"<span style='background:{action_color}22;color:{action_color};"
        f"border:1px solid {action_color}55;padding:6px 18px;border-radius:999px;"
        f"font-size:13px;font-weight:700;letter-spacing:1px;white-space:nowrap;'>"
        f"{action}</span>"
    )

    return f"""
    <div style="font-family:{DISPLAY_FONT};background:{CARD_BACKGROUND};
                border:1px solid {CARD_BORDER};padding:36px 40px;border-radius:20px;
                color:{TEXT_COLOR};box-shadow:0 8px 40px rgba(0,0,0,0.6);margin-top:8px;">

        <!-- HEADER -->
        <div style="display:flex;align-items:flex-start;justify-content:space-between;
                    flex-wrap:wrap;gap:16px;margin-bottom:28px;">
            <div>
                <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
                    <span style="font-size:32px;">📈</span>
                    <h1 style="margin:0;font-size:34px;font-weight:800;
                               color:{HEADING_COLOR};letter-spacing:-0.5px;">
                        {data.get("stock","N/A")}
                    </h1>
                </div>
                <span style="background:{BADGE_BG};color:{SUBTEXT_COLOR};
                             border:1px solid {SECTION_BORDER};padding:3px 12px;
                             border-radius:999px;font-size:12px;font-weight:600;
                             letter-spacing:0.5px;margin-left:44px;">
                    {data.get("resolved_ticker","")}
                </span>
            </div>
            {action_pill}
        </div>
        
        <!-- KPI ROW -->
        <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:32px;">
            {kpi_card("Confidence",      data.get("confidence","N/A"),       ACCENT_PRIMARY)}
            {kpi_card("Risk Level",      data.get("risk_level","N/A"),       ACCENT_WARNING)}
            {kpi_card("Suggested Action",data.get("suggested_action","N/A"), action_color)}
        </div>

        <hr style="border:none;border-top:1px solid {DIVIDER_COLOR};margin:0 0 28px 0;">

        <!-- ANALYSIS SECTIONS -->
        {section("Technical View",   data.get("technical_view",""),      "📊", ACCENT_SECONDARY)}
        {section("Fundamental View", data.get("fundamental_view",""),    "🏦", ACCENT_PRIMARY)}
        {section("News Sentiment",   data.get("news_sentiment_view",""), "📰", ACCENT_WARNING)}
        {section("Final Reasoning",  data.get("final_reasoning",""),     "🧠", HEADING_COLOR)}

        <hr style="border:none;border-top:1px solid {DIVIDER_COLOR};margin:0 0 28px 0;">

        <!-- LIST CARDS -->
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
                    gap:20px;margin-bottom:28px;">
            {list_card("Growth Drivers", list_items("key_growth_drivers","↑",ACCENT_SUCCESS), ACCENT_SUCCESS)}
            {list_card("Key Risks",      list_items("key_risks","↓",ACCENT_ERROR),            ACCENT_ERROR)}
            {list_card("Further Research",list_items("further_research","→",ACCENT_WARNING),   ACCENT_WARNING)}
        </div>

        <!-- DISCLAIMER -->
        <div style="background:{BADGE_BG};border:1px solid {DIVIDER_COLOR};
                    border-left:4px solid {ACCENT_WARNING};border-radius:12px;
                    padding:18px 22px;font-size:13px;color:{SUBTEXT_COLOR};line-height:1.7;">
            <span style="color:{ACCENT_WARNING};font-weight:700;">⚠ Disclaimer &nbsp;</span>
            {data.get("disclaimer","")}
        </div>
    </div>"""

# =========================================================
# MAIN ANALYSIS GENERATOR
# =========================================================

def analyze(stock_name):
    while not q.empty():
        q.get()

    validation = validate_stock(stock_name)
    if not validation["valid"]:
        yield create_beautiful_report({"error": validation["error"]}), "Validation failed.", None
        return

    logs = (
        f"[INFO]  Stock   : {validation['company']} ({validation['symbol']})\n"
        f"[INFO]  Status  : Validated ✓\n"
        f"[INFO]  Engine  : Starting multi-agent analysis...\n"
        f"{'─'*60}\n"
    )
    yield None, logs, None

    def worker():
        try:
            import builtins
            original_input = builtins.input
            builtins.input = lambda _: stock_name
            log_stream = QueueWriter()
            with contextlib.redirect_stdout(log_stream):
                result = run_stock_analysis()
            builtins.input = original_input
            q.put(("json", result))
        except Exception as e:
            q.put(("json", {"error": str(e)}))

    threading.Thread(target=worker, daemon=True).start()

    while True:
        item_type, data = q.get()
        if item_type == "log":
            logs += data
            yield None, logs, None
        elif item_type == "json":
            final_data = data
            if isinstance(data, dict) and "raw_result" in data:
                final_data = extract_json_from_raw(data["raw_result"])
            yield create_beautiful_report(final_data), logs, final_data
            break

# =========================================================
# CUSTOM CSS
# =========================================================

CUSTOM_CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

body, .gradio-container {{
    background:{APP_BACKGROUND} !important;
    font-family:{DISPLAY_FONT};
}}

/* ── All inputs except the log box ── */
input, .gr-textbox:not(#logs-box) textarea {{
    background:{INPUT_BG} !important;
    color:{INPUT_TEXT} !important;
    border:1px solid {INPUT_BORDER} !important;
    border-radius:10px !important;
    font-family:{DISPLAY_FONT} !important;
    font-size:15px !important;
    transition:border-color 0.2s;
}}
input:focus, .gr-textbox:not(#logs-box) textarea:focus {{
    border-color:{INPUT_FOCUS_BORDER} !important;
    outline:none !important;
    box-shadow:0 0 0 3px {ACCENT_PRIMARY}22 !important;
}}
input::placeholder, textarea::placeholder {{
    color:{INPUT_PLACEHOLDER} !important;
}}

/* ── Terminal log box (font/color locked) ── */
#logs-box textarea {{
    font-family:{TERMINAL_FONT} !important;
    font-size:13px !important;
    line-height:1.6 !important;
    background:{LOG_BACKGROUND} !important;
    color:{LOG_TEXT_COLOR} !important;
    border:1px solid {LOG_BORDER} !important;
    border-radius:12px !important;
    padding:16px !important;
}}

/* ── Primary / Analyze button ── */
.analyze-btn button, button.primary {{
    background:linear-gradient(135deg, {BUTTON_BG}, {ACCENT_SECONDARY}) !important;
    color:{BUTTON_TEXT} !important;
    border:none !important;
    border-radius:10px !important;
    font-family:{DISPLAY_FONT} !important;
    font-size:15px !important;
    font-weight:700 !important;
    letter-spacing:0.5px !important;
    padding:12px 28px !important;
    cursor:pointer !important;
    transition:opacity 0.2s, transform 0.15s !important;
    box-shadow:0 4px 20px {BUTTON_BG}55 !important;
}}
.analyze-btn button:hover, button.primary:hover {{
    opacity:0.88 !important;
    transform:translateY(-1px) !important;
}}

/* ── Labels ── */
label span {{
    color:{SUBTEXT_COLOR} !important;
    font-size:12px !important;
    font-weight:600 !important;
    letter-spacing:0.5px !important;
    text-transform:uppercase !important;
}}

/* ── Markdown header ── */
.gr-markdown h1 {{
    color:{HEADING_COLOR} !important;
    font-size:26px !important;
    font-weight:800 !important;
    font-family:{DISPLAY_FONT} !important;
}}
.gr-markdown p {{
    color:{SUBTEXT_COLOR} !important;
    font-size:14px !important;
}}

/* ── Custom scrollbar ── */
::-webkit-scrollbar {{ width:6px; height:6px; }}
::-webkit-scrollbar-track {{ background:{APP_BACKGROUND}; }}
::-webkit-scrollbar-thumb {{ background:{INPUT_BORDER}; border-radius:3px; }}
::-webkit-scrollbar-thumb:hover {{ background:{ACCENT_PRIMARY}; }}
"""

# =========================================================
# UI LAYOUT
# =========================================================

with gr.Blocks(
    title="AI Stock Analyzer",
    theme=gr.themes.Base(
        primary_hue=gr.themes.colors.purple,
        secondary_hue=gr.themes.colors.cyan,
        neutral_hue=gr.themes.colors.slate,
        font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "sans-serif"],
    ),
    css=CUSTOM_CSS,
) as demo:

    # ── Hero ─────────────────────────────────────────────────────────────────
    gr.Markdown("""
    # 📊 AI Stock Analyzer
    Powered by multi-agent AI · Technical · Fundamental · Sentiment
    """)

    # ── Input row ────────────────────────────────────────────────────────────
    with gr.Row(equal_height=True):
        stock_input = gr.Textbox(
            label="Stock Name or Symbol",
            placeholder="e.g. ONGC, Reliance, TCS, Infosys…",
            scale=4,
        )
        analyze_btn = gr.Button(
            "🔍  Analyze",
            variant="primary",
            scale=1,
            elem_classes=["analyze-btn"],
        )

    # ── Quick-pick chips ─────────────────────────────────────────────────────
    gr.Markdown("<small style='color:#2d3748;'>⚡ Quick picks</small>")
    with gr.Row():
        for ticker in ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ONGC", "WIPRO"]:
            chip = gr.Button(ticker, size="sm", variant="secondary")
            chip.click(fn=lambda t=ticker: t, outputs=stock_input)


    # Wire up each tab's plot to refresh when Analyze runs
    # (also triggered per-tab via tab select below)

    # ── Output tabs ──────────────────────────────────────────────────────────
    with gr.Tabs():

        # ── Stock Price Chart ─────────────────────────────────────────────────────
        gr.Markdown(
            f"<h3 style='color:{HEADING_COLOR};font-family:{DISPLAY_FONT};"
            f"font-size:16px;font-weight:700;margin:24px 0 4px 0;'>📉 Price Chart</h3>"
        )

        with gr.Tabs() as chart_tabs:
            chart_plot = None
            chart_periods = ["1W", "1M", "3M", "6M", "9M", "1Y", "3Y", "5Y", "10Y", "All"]
            chart_plots = {}

            tab_items = {}

            for period in chart_periods:
                with gr.TabItem(period) as tab:
                    tab_items[period] = tab

                    chart_plots[period] = gr.Plot(
                        label=f"Stock Price – {period}",
                        value=go.Figure()  # EMPTY INITIAL FIGURE
                    )

        with gr.TabItem("📄  Report"):
            report_output = gr.HTML(
                value=(
                    f"<div style='padding:48px;text-align:center;"
                    f"color:{SUBTEXT_COLOR};font-family:{DISPLAY_FONT};font-size:15px;'>"
                    f"Enter a stock name above and click "
                    f"<b style='color:{ACCENT_PRIMARY}'>Analyze</b> to get started."
                    f"</div>"
                )
            )

        with gr.TabItem("🖥️  Live Logs"):
            logs_output = gr.Textbox(
                label="Agent Activity Log",
                lines=28,
                max_lines=28,
                autoscroll=True,
                # show_copy_button=True,
                elem_id="logs-box",
            )

        with gr.TabItem("{ }  Raw JSON"):
            json_output = gr.JSON(label="Structured Output")

    # ── Footer ───────────────────────────────────────────────────────────────
    gr.Markdown(
        "<small style='color:#1a202c;font-size:11px;'>"
        "Not financial advice. For educational purposes only.</small>"
    )

    # ── Wire-up ──────────────────────────────────────────────────────────────

    # When Analyze runs, populate the default chart period (6M) first.
    # Each chart tab also re-fetches its own period when clicked.

    def make_chart_updater(period):
        def _update(stock_name):
            return fetch_and_plot(stock_name, period)
        return _update

    analyze_btn.click(
        fn=analyze,
        inputs=stock_input,
        outputs=[report_output, logs_output, json_output],
    )

    # Populate all chart tabs when Analyze is clicked
    for period, plot_component in chart_plots.items():
        tab_items[period].select(
            fn=make_chart_updater(period),
            inputs=stock_input,
            outputs=plot_component,
        )

    # Also allow quick-pick chips to trigger chart refresh (optional convenience)
    # Tab select re-fetch: clicking a tab re-draws that period's chart
    for period, plot_component in chart_plots.items():
        tab_items[period].select(
            fn=make_chart_updater(period),
            inputs=stock_input,
            outputs=plot_component,
        )

demo.launch(share=True)
