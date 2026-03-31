"""
The Selective AI Frost: MNDY Short Thesis Dashboard
Built with Streamlit + Plotly | Data hardcoded from the investment memo
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Selective AI Frost — MNDY Short Thesis",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Design Tokens ──────────────────────────────────────────────────────────
NAVY = "#0D1B2A"
SURFACE = "#152535"
BORDER = "#1E3348"
TEXT = "#E8E6E1"
TEXT_MUTED = "#8A8A8A"
TEAL = "#20808D"
CRIMSON = "#C62828"
GOLD = "#B8860B"
AMBER = "#FFC553"
WHITE = "#FFFFFF"

PLOTLY_LAYOUT = dict(
    paper_bgcolor=NAVY,
    plot_bgcolor=SURFACE,
    font=dict(family="Inter, -apple-system, sans-serif", color=TEXT, size=13),
    margin=dict(l=60, r=30, t=60, b=50),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(0,0,0,0)",
        font=dict(size=12, color=TEXT_MUTED),
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
    ),
)

DEFAULT_AXIS = dict(gridcolor=BORDER, zerolinecolor=BORDER, tickfont=dict(color=TEXT_MUTED))


def styled_axis(fig):
    """Apply consistent axis styling without overwriting existing settings."""
    defaults = dict(gridcolor=BORDER, zerolinecolor=BORDER, tickfont=dict(color=TEXT_MUTED, size=12))
    for ax_key in ["xaxis", "yaxis", "xaxis2", "yaxis2"]:
        ax = getattr(fig.layout, ax_key, None)
        if ax is not None:
            # Only set defaults where not already explicitly set
            current = ax.to_plotly_json()
            for k, v in defaults.items():
                if k not in current or current[k] is None:
                    ax[k] = v
    return fig


# ─── Global CSS ─────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=DM+Sans:wght@700&display=swap');

    .stApp {{
        background-color: {NAVY};
        color: {TEXT};
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0px;
        background-color: {SURFACE};
        border-radius: 8px;
        padding: 4px;
        border: 1px solid {BORDER};
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent;
        color: {TEXT_MUTED};
        border-radius: 6px;
        padding: 10px 24px;
        font-weight: 600;
        font-size: 14px;
        font-family: 'Inter', sans-serif;
        border: none;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {NAVY} !important;
        color: {WHITE} !important;
        border: 1px solid {BORDER} !important;
    }}
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
        color: {WHITE};
        font-family: 'DM Sans', 'Inter', sans-serif;
    }}
    .stMarkdown p, .stMarkdown li {{
        color: {TEXT};
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
    }}

    /* KPI cards */
    .kpi-row {{
        display: flex;
        gap: 16px;
        margin-bottom: 24px;
    }}
    .kpi-card {{
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 8px;
        padding: 20px 24px;
        flex: 1;
        text-align: center;
    }}
    .kpi-label {{
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        color: {TEXT_MUTED};
        margin-bottom: 6px;
        font-family: 'Inter', sans-serif;
    }}
    .kpi-value {{
        font-size: 28px;
        font-weight: 700;
        font-family: 'DM Sans', sans-serif;
        line-height: 1.2;
    }}
    .kpi-delta {{
        font-size: 12px;
        margin-top: 4px;
        font-family: 'Inter', sans-serif;
    }}
    .teal {{ color: {TEAL}; }}
    .crimson {{ color: {CRIMSON}; }}
    .gold {{ color: {GOLD}; }}
    .white {{ color: {WHITE}; }}

    /* Takeaway box */
    .takeaway {{
        background: {SURFACE};
        border-left: 3px solid {CRIMSON};
        border-radius: 0 6px 6px 0;
        padding: 16px 20px;
        margin: 16px 0 24px 0;
        font-size: 14px;
        line-height: 1.6;
        color: {TEXT};
        font-family: 'Inter', sans-serif;
    }}
    .takeaway strong {{
        color: {WHITE};
    }}
    .takeaway .signal {{
        color: {CRIMSON};
        font-weight: 600;
    }}
    .takeaway .positive {{
        color: {TEAL};
        font-weight: 600;
    }}

    /* Dividers */
    hr {{
        border: none;
        border-top: 1px solid {BORDER};
        margin: 24px 0;
    }}

    /* Hide Streamlit chrome */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    div[data-testid="stMetric"] {{
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 8px;
        padding: 16px;
    }}
    div[data-testid="stMetric"] label {{
        color: {TEXT_MUTED} !important;
        font-size: 12px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
        color: {WHITE} !important;
        font-family: 'DM Sans', sans-serif !important;
    }}
</style>
""", unsafe_allow_html=True)


# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 8px 0 4px 0;">
    <h1 style="font-size: 36px; margin-bottom: 4px; font-family: 'DM Sans', sans-serif; letter-spacing: -0.5px;">
        The Selective AI Frost
    </h1>
    <p style="font-size: 16px; color: #8A8A8A; margin-top: 0; font-family: 'Inter', sans-serif;">
        Short monday.com (NASDAQ: MNDY) &nbsp;·&nbsp; March 2026 &nbsp;·&nbsp; Confidential
    </p>
</div>
""", unsafe_allow_html=True)

# KPI row
st.markdown(f"""
<div class="kpi-row">
    <div class="kpi-card">
        <div class="kpi-label">MNDY Price</div>
        <div class="kpi-value white">$67.88</div>
        <div class="kpi-delta crimson">▼ 79% from highs</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">P/E Multiple</div>
        <div class="kpi-value crimson">30.3x</div>
        <div class="kpi-delta" style="color:{TEXT_MUTED}">2.4x peer average</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">AI Capex (2026)</div>
        <div class="kpi-value teal">$630B</div>
        <div class="kpi-delta teal">▲ 4.5x since 2023</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">SaaS Market Cap Wiped</div>
        <div class="kpi-value crimson">-$1T+</div>
        <div class="kpi-delta" style="color:{TEXT_MUTED}">IGV worst day since COVID</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Base Target</div>
        <div class="kpi-value gold">$45</div>
        <div class="kpi-delta crimson">▼ 34% downside</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─── Tabs ───────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📊  Macro Frost", "📉  The MNDY Collapse", "⚖️  Valuation Disconnect"])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — MACRO FROST
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### Two Economies, One Buzzword")
    st.markdown(
        f'<p style="color:{TEXT_MUTED}; font-size:14px; margin-top:-8px;">'
        "AI infrastructure spending explodes while SaaS application growth decelerates — "
        "every dollar going to AI capex is a dollar NOT going to another SaaS seat.</p>",
        unsafe_allow_html=True,
    )

    # --- Dual-axis chart: AI Capex vs SaaS ARR Growth ---
    years = ["2023", "2024", "2025", "2026E"]
    ai_capex = [140, 245, 388, 630]  # $B — from memo
    saas_arr_growth = [17, 14, 10.5, 8]  # % — 2023 industry ~17%, memo shows 14→10.5, projected 8%

    fig1 = make_subplots(specs=[[{"secondary_y": True}]])

    # AI Capex bars
    fig1.add_trace(
        go.Bar(
            x=years,
            y=ai_capex,
            name="AI Infrastructure Capex ($B)",
            marker=dict(
                color=[TEAL, TEAL, TEAL, TEAL],
                opacity=[0.5, 0.65, 0.8, 1.0],
                line=dict(width=0),
            ),
            text=[f"${v}B" for v in ai_capex],
            textposition="outside",
            textfont=dict(color=TEAL, size=13, family="DM Sans"),
            width=0.45,
        ),
        secondary_y=False,
    )

    # SaaS ARR growth line
    fig1.add_trace(
        go.Scatter(
            x=years,
            y=saas_arr_growth,
            name="SaaS ARR Growth (%)",
            mode="lines+markers+text",
            line=dict(color=CRIMSON, width=3),
            marker=dict(size=10, color=CRIMSON, line=dict(width=2, color=NAVY)),
            text=[f"{v}%" for v in saas_arr_growth],
            textposition="bottom center",
            textfont=dict(color=CRIMSON, size=13, family="DM Sans"),
        ),
        secondary_y=True,
    )

    fig1.update_layout(
        **PLOTLY_LAYOUT,
        height=440,
        title=dict(
            text="AI Capex Explodes While SaaS Growth Collapses",
            font=dict(size=16, color=WHITE, family="DM Sans"),
            x=0.01, xanchor="left",
        ),
        barmode="group",
        showlegend=True,
    )
    fig1.update_yaxes(
        title_text="AI Capex ($B)",
        secondary_y=False,
        range=[0, 780],
        gridcolor=BORDER,
        tickfont=dict(color=TEXT_MUTED),
        title_font=dict(color=TEAL, size=12),
    )
    fig1.update_yaxes(
        title_text="SaaS ARR Growth (%)",
        secondary_y=True,
        range=[0, 25],
        gridcolor="rgba(0,0,0,0)",
        tickfont=dict(color=TEXT_MUTED),
        title_font=dict(color=CRIMSON, size=12),
    )
    styled_axis(fig1)
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown(f"""
    <div class="takeaway">
        <strong>The Divergence:</strong> Hyperscaler capex grew from $140B to 
        <span class="positive">$630B in 3 years</span> — a 4.5x increase. Meanwhile, 
        SaaS ARR growth fell from 14% to <span class="signal">10.5%</span> as 82% of 
        companies cut vendors. Jason Lemkin: <em>"Every AI dollar equals one less SaaS dollar."</em>
    </div>
    """, unsafe_allow_html=True)

    # --- Revenue Deceleration Chart ---
    quarters = ["Q4'24", "Q1'25", "Q2'25", "Q3'25", "Q4'25", "FY26E"]
    revenue = [268, 282, 299, 317, 334, 363]  # $M (FY26E ≈ 1457/4)
    yoy_growth = [32, 30, 27, 26, 25, 18.5]

    fig1b = make_subplots(specs=[[{"secondary_y": True}]])

    fig1b.add_trace(
        go.Bar(
            x=quarters,
            y=revenue,
            name="Revenue ($M)",
            marker=dict(
                color=[TEAL if q != "FY26E" else BORDER for q in quarters],
                opacity=0.7,
                line=dict(width=0),
            ),
            text=[f"${v}M" for v in revenue],
            textposition="outside",
            textfont=dict(color=TEXT_MUTED, size=11),
            width=0.5,
        ),
        secondary_y=False,
    )

    fig1b.add_trace(
        go.Scatter(
            x=quarters,
            y=yoy_growth,
            name="YoY Growth (%)",
            mode="lines+markers+text",
            line=dict(color=CRIMSON, width=3),
            marker=dict(size=10, color=CRIMSON, line=dict(width=2, color=NAVY)),
            text=[f"{v}%" for v in yoy_growth],
            textposition="bottom center",
            textfont=dict(color=CRIMSON, size=12, family="DM Sans"),
        ),
        secondary_y=True,
    )

    fig1b.update_layout(
        **PLOTLY_LAYOUT,
        height=400,
        title=dict(
            text="MNDY Revenue Growth Decelerating Into the Frost",
            font=dict(size=16, color=WHITE, family="DM Sans"),
            x=0.01, xanchor="left",
        ),
    )
    fig1b.update_yaxes(
        title_text="Revenue ($M)", secondary_y=False,
        range=[0, 450], gridcolor=BORDER,
        tickfont=dict(color=TEXT_MUTED),
        title_font=dict(color=TEAL, size=12),
    )
    fig1b.update_yaxes(
        title_text="YoY Growth (%)", secondary_y=True,
        range=[10, 40], gridcolor="rgba(0,0,0,0)",
        tickfont=dict(color=TEXT_MUTED),
        title_font=dict(color=CRIMSON, size=12),
    )
    styled_axis(fig1b)
    st.plotly_chart(fig1b, use_container_width=True)

    st.markdown(f"""
    <div class="takeaway">
        <strong>The Deceleration:</strong> Revenue growth slid from <span class="signal">32% → 25% → guided 18-19%</span>. 
        Management cut their own $1.5B target just 3 months after endorsing it. 
        2027 targets entirely withdrawn. NDR trending toward 100% — the line between expansion and contraction.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — THE MNDY COLLAPSE
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### Three Pillars of Deterioration")

    col_a, col_b = st.columns(2)

    # --- Chart 1: SEO vs PPC (Pillar 1) ---
    with col_a:
        categories = ["SEO Traffic\n(Organic)", "PPC Spend\n(Paid)", "Self-Serve\nARR"]
        values = [-25.3, 46, -7]
        colors = [CRIMSON, AMBER, CRIMSON]

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=categories,
            y=values,
            marker=dict(
                color=colors,
                line=dict(width=0),
            ),
            text=[f"{v:+.1f}%" for v in values],
            textposition=["inside" if v < 0 else "outside" for v in values],
            textfont=dict(size=15, family="DM Sans", color=WHITE),
            width=0.55,
        ))

        fig2.update_layout(
            paper_bgcolor=NAVY,
            plot_bgcolor=SURFACE,
            font=dict(family="Inter, -apple-system, sans-serif", color=TEXT, size=13),
            margin=dict(l=60, r=30, t=60, b=50),
            height=420,
            title=dict(
                text="Self-Serve Engine Breaking — The CAC Death Spiral",
                font=dict(size=15, color=WHITE, family="DM Sans"),
                x=0.02, xanchor="left",
            ),
            yaxis=dict(
                title="YoY Change (%)",
                range=[-35, 60],
                gridcolor=BORDER,
                zerolinecolor=TEXT_MUTED,
                zerolinewidth=1,
                tickfont=dict(color=TEXT_MUTED),
                title_font=dict(color=TEXT_MUTED, size=12),
            ),
            xaxis=dict(
                gridcolor=BORDER,
                tickfont=dict(color=TEXT, size=12),
            ),
            showlegend=False,
        )
        # Add zero line annotation
        fig2.add_hline(y=0, line_dash="dot", line_color=TEXT_MUTED, line_width=1)

        st.plotly_chart(fig2, use_container_width=True)

        st.markdown(f"""
        <div class="takeaway">
            <strong>Pillar 1 — Self-Serve Engine Breaking:</strong> SEO traffic collapsed 
            <span class="signal">-25.3% YoY</span> as AI Overviews cannibalize discovery queries. 
            PPC spend surged <span class="signal">+46%</span> to compensate — a textbook CAC death spiral. 
            Self-serve gross ARR contracted <span class="signal">-7%</span> in Q2 2025.
        </div>
        """, unsafe_allow_html=True)

    # --- Chart 2: Margins Compression (Pillar 2 + 3) ---
    with col_b:
        margin_labels = ["Gross\nMargin", "Op\nMargin", "FCF\nMargin", "R&D\n(% of Rev)"]
        before_vals = [90, 14, 30.6, 22]
        after_vals = [85, 11.5, 25.4, 26]
        labels_before = ["90%", "14%", "30.6%", "22%"]
        labels_after = ["~85%", "11.5%", "25.4%", "26%"]

        fig3 = go.Figure()

        fig3.add_trace(go.Bar(
            x=margin_labels,
            y=before_vals,
            name="FY2025 (Actual)",
            marker=dict(color=TEAL, opacity=0.65, line=dict(width=0)),
            text=labels_before,
            textposition="outside",
            textfont=dict(size=13, color=TEAL, family="DM Sans"),
            width=0.3,
            offset=-0.16,
        ))
        fig3.add_trace(go.Bar(
            x=margin_labels,
            y=after_vals,
            name="FY2026 (Guided)",
            marker=dict(color=CRIMSON, opacity=0.85, line=dict(width=0)),
            text=labels_after,
            textposition="outside",
            textfont=dict(size=13, color=CRIMSON, family="DM Sans"),
            width=0.3,
            offset=0.16,
        ))

        fig3.update_layout(
            paper_bgcolor=NAVY,
            plot_bgcolor=SURFACE,
            font=dict(family="Inter, -apple-system, sans-serif", color=TEXT, size=13),
            margin=dict(l=60, r=30, t=60, b=50),
            height=420,
            title=dict(
                text="AI Costs Compress Every Margin Line",
                font=dict(size=15, color=WHITE, family="DM Sans"),
                x=0.02, xanchor="left",
            ),
            barmode="group",
            legend=dict(
                bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)",
                font=dict(size=12, color=TEXT_MUTED),
                orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
            ),
            yaxis=dict(
                title="Percentage (%)",
                range=[0, 105],
                gridcolor=BORDER,
                tickfont=dict(color=TEXT_MUTED),
                title_font=dict(color=TEXT_MUTED, size=12),
            ),
            xaxis=dict(gridcolor=BORDER, tickfont=dict(color=TEXT, size=12)),
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown(f"""
        <div class="takeaway">
            <strong>Pillar 2 — AI Features Destroy Value:</strong> Gross margins guided 
            <span class="signal">DOWN from 90% to mid-80s</span> — specifically due to AI compute costs. 
            R&D surging to <span class="signal">26% of revenue</span> while Monday Magic = only 10.7% of ARR. 
            Users: <em>"It's quicker to do it manually than use the automation."</em>
        </div>
        """, unsafe_allow_html=True)

    # --- NDR Decline Chart ---
    st.markdown("---")
    ndr_quarters = ["Q4'24", "Q1'25", "Q2'25", "Q3'25", "Q4'25"]
    ndr_all = [112, 112, 111, 111, 110]
    ndr_enterprise = [116, 117, 117, 117, 116]

    fig4 = go.Figure()

    # Critical threshold line
    fig4.add_hline(
        y=105, line_dash="dash", line_color=CRIMSON, line_width=1,
        annotation_text="Critical Inflection (105%)",
        annotation_position="bottom right",
        annotation_font=dict(size=11, color=CRIMSON),
    )
    fig4.add_hline(
        y=100, line_dash="dot", line_color=TEXT_MUTED, line_width=1,
        annotation_text="Contraction Zone",
        annotation_position="bottom right",
        annotation_font=dict(size=11, color=TEXT_MUTED),
    )

    fig4.add_trace(go.Scatter(
        x=ndr_quarters, y=ndr_all,
        name="NDR (All Customers)",
        mode="lines+markers+text",
        line=dict(color=CRIMSON, width=3),
        marker=dict(size=10, color=CRIMSON, line=dict(width=2, color=NAVY)),
        text=[f"{v}%" for v in ndr_all],
        textposition="top center",
        textfont=dict(size=12, color=CRIMSON, family="DM Sans"),
    ))
    fig4.add_trace(go.Scatter(
        x=ndr_quarters, y=ndr_enterprise,
        name="NDR (Enterprise 100K+)",
        mode="lines+markers+text",
        line=dict(color=AMBER, width=2, dash="dash"),
        marker=dict(size=8, color=AMBER, line=dict(width=2, color=NAVY)),
        text=[f"{v}%" for v in ndr_enterprise],
        textposition="top center",
        textfont=dict(size=11, color=AMBER, family="DM Sans"),
    ))

    fig4.update_layout(
        **PLOTLY_LAYOUT,
        height=380,
        title=dict(
            text="Net Dollar Retention Trending Toward Contraction",
            font=dict(size=16, color=WHITE, family="DM Sans"),
            x=0.01, xanchor="left",
        ),
        yaxis=dict(
            title="NDR (%)",
            range=[97, 120],
            gridcolor=BORDER,
            tickfont=dict(color=TEXT_MUTED),
            title_font=dict(color=TEXT_MUTED, size=12),
        ),
    )
    styled_axis(fig4)
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown(f"""
    <div class="takeaway">
        <strong>Pillar 3 — NDR Fading:</strong> All-customer NDR declined from 
        <span class="signal">112% → 110%</span> in 5 quarters, trending toward 100% — the line between 
        expansion and contraction. Even Enterprise 100K+ peaked and started declining.
        Below 105% triggers a re-rating event.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — VALUATION DISCONNECT
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### Still Priced Like a Growth Story")
    st.markdown(
        f'<p style="color:{TEXT_MUTED}; font-size:14px; margin-top:-8px;">'
        "MNDY trades at 2.4x the peer average P/E multiple despite decelerating to "
        "peer-level growth rates. The premium is unsustainable.</p>",
        unsafe_allow_html=True,
    )

    # --- Scatter: P/E vs Growth ---
    companies = ["MNDY", "ZM", "FRSH", "ASAN"]
    pe_ratios = [30.3, 12.7, 12.8, None]  # ASAN is negative earnings
    growth_rates = [18.5, 4, 18, 10]
    mkt_caps = [3.5, 23.3, 2.3, 1.5]  # $B
    colors_scatter = [CRIMSON, TEAL, TEAL, TEXT_MUTED]
    sizes_scatter = [24, 20, 16, 14]

    fig5 = go.Figure()

    # Plot peers (ZM, FRSH)
    for i, comp in enumerate(companies):
        if pe_ratios[i] is None:
            continue
        fig5.add_trace(go.Scatter(
            x=[growth_rates[i]],
            y=[pe_ratios[i]],
            mode="markers+text",
            name=comp,
            marker=dict(
                size=mkt_caps[i] * 8 + 10,
                color=colors_scatter[i],
                opacity=0.85,
                line=dict(width=2, color=NAVY),
            ),
            text=[comp],
            textposition="top center",
            textfont=dict(
                size=15 if comp == "MNDY" else 13,
                color=WHITE if comp == "MNDY" else TEXT,
                family="DM Sans",
            ),
            hovertemplate=(
                f"<b>{comp}</b><br>"
                f"P/E: {pe_ratios[i]}x<br>"
                f"Growth: {growth_rates[i]}%<br>"
                f"Mkt Cap: ${mkt_caps[i]}B"
                "<extra></extra>"
            ),
            showlegend=False,
        ))

    # Add "fair value" zone
    fig5.add_shape(
        type="rect",
        x0=0, x1=25, y0=10, y1=16,
        fillcolor=TEAL, opacity=0.08,
        line=dict(width=0),
    )
    fig5.add_annotation(
        x=22, y=13,
        text="Peer Valuation Zone",
        font=dict(size=11, color=TEAL),
        showarrow=False,
    )

    # Add MNDY arrow to fair value
    fig5.add_annotation(
        x=18.5, y=30.3,
        ax=18.5, ay=16,
        arrowhead=3, arrowsize=1.2, arrowwidth=2,
        arrowcolor=CRIMSON,
        opacity=0.5,
    )
    fig5.add_annotation(
        x=18.5, y=22,
        text="~55% downside<br>to peer multiple",
        font=dict(size=11, color=CRIMSON),
        showarrow=False,
    )

    fig5.update_layout(
        **PLOTLY_LAYOUT,
        height=480,
        title=dict(
            text="P/E Multiple vs. Revenue Growth — MNDY is the Outlier",
            font=dict(size=16, color=WHITE, family="DM Sans"),
            x=0.01, xanchor="left",
        ),
        xaxis=dict(
            title="Revenue Growth (%)",
            range=[-1, 28],
            gridcolor=BORDER,
            tickfont=dict(color=TEXT_MUTED),
            title_font=dict(color=TEXT_MUTED, size=12),
        ),
        yaxis=dict(
            title="P/E Multiple (x)",
            range=[0, 38],
            gridcolor=BORDER,
            tickfont=dict(color=TEXT_MUTED),
            title_font=dict(color=TEXT_MUTED, size=12),
        ),
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown(f"""
    <div class="takeaway">
        <strong>The Disconnect:</strong> MNDY trades at <span class="signal">30.3x P/E</span> — 
        2.4x the peer average of ~12.7x. Yet its growth has decelerated to 18%, 
        roughly matching FRSH (18%, 12.8x P/E). ZM at 4% growth trades at 12.7x. 
        <strong>At peer multiples, MNDY is a $33-$45 stock.</strong>
    </div>
    """, unsafe_allow_html=True)

    # --- Price Target Scenarios ---
    st.markdown("---")
    col_x, col_y = st.columns(2)

    with col_x:
        scenarios = ["Bear Case", "Base Case", "Bull Case"]
        multiples = [15, 20, 25]
        implied_prices = [33, 45, 56]
        downsides = [-51, -34, -18]
        bar_colors = [CRIMSON, GOLD, TEAL]

        fig6 = go.Figure()
        fig6.add_trace(go.Bar(
            x=scenarios,
            y=implied_prices,
            marker=dict(color=bar_colors, opacity=0.85, line=dict(width=0)),
            text=[f"${p} ({d:+d}%)" for p, d in zip(implied_prices, downsides)],
            textposition="outside",
            textfont=dict(size=14, color=WHITE, family="DM Sans"),
            width=0.5,
        ))

        # Current price line
        fig6.add_hline(
            y=67.88, line_dash="dash", line_color=TEXT_MUTED, line_width=1.5,
            annotation_text="Current: $67.88",
            annotation_position="top left",
            annotation_font=dict(size=12, color=TEXT_MUTED),
        )

        fig6.update_layout(
            **PLOTLY_LAYOUT,
            height=380,
            title=dict(
                text="Price Target Scenarios (All Below Current Price)",
                font=dict(size=15, color=WHITE, family="DM Sans"),
                x=0.02, xanchor="left",
            ),
            yaxis=dict(
                title="Implied Price ($)",
                range=[0, 85],
                gridcolor=BORDER,
                tickfont=dict(color=TEXT_MUTED),
                title_font=dict(color=TEXT_MUTED, size=12),
            ),
            showlegend=False,
        )
        st.plotly_chart(fig6, use_container_width=True)

    with col_y:
        # Price history waterfall
        events = [
            "Oct '24\nPre-Frost", "Feb '25\nPeak", "Aug '25\nBofA Cut",
            "Dec '25\nDecline", "Feb '26\nEarnings", "Mar '26\nCurrent"
        ]
        prices = [288, 318.50, 175, 150, 78, 67.88]
        price_colors = [TEAL if i < 2 else CRIMSON for i in range(len(prices))]

        fig7 = go.Figure()
        fig7.add_trace(go.Scatter(
            x=events,
            y=prices,
            mode="lines+markers+text",
            line=dict(color=CRIMSON, width=3),
            marker=dict(
                size=[10, 14, 10, 10, 10, 14],
                color=price_colors,
                line=dict(width=2, color=NAVY),
            ),
            text=[f"${p:.0f}" if p > 100 else f"${p:.2f}" for p in prices],
            textposition="top center",
            textfont=dict(size=12, color=TEXT, family="DM Sans"),
            fill="tozeroy",
            fillcolor="rgba(198, 40, 40, 0.08)",
        ))

        fig7.update_layout(
            **PLOTLY_LAYOUT,
            height=380,
            title=dict(
                text="MNDY Price Collapse: -79% From Highs",
                font=dict(size=15, color=WHITE, family="DM Sans"),
                x=0.02, xanchor="left",
            ),
            yaxis=dict(
                title="Stock Price ($)",
                range=[0, 380],
                gridcolor=BORDER,
                tickfont=dict(color=TEXT_MUTED),
                title_font=dict(color=TEXT_MUTED, size=12),
            ),
            showlegend=False,
        )
        st.plotly_chart(fig7, use_container_width=True)

    st.markdown(f"""
    <div class="takeaway">
        <strong>Asymmetric Setup:</strong> Even the <span class="positive">bull case</span> (25x P/E → $56) 
        implies <span class="signal">-18% downside</span> from current. The base case at peer-level 
        20x P/E implies <span class="signal">$45 (-34%)</span>. With Q1'26 earnings in May as the 
        next catalyst — guide-down risk is high. 
        <strong>Every scenario points down.</strong>
    </div>
    """, unsafe_allow_html=True)


# ─── Footer ─────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(f"""
<div style="text-align:center; padding: 12px 0 24px 0;">
    <p style="color:{TEXT_MUTED}; font-size:11px; font-style:italic; font-family:'Inter',sans-serif;">
        This is research and analysis only, not personalized financial advice. 
        Past performance is not indicative of future results. Short selling involves 
        substantial risk including unlimited loss potential.
    </p>
    <p style="color:{BORDER}; font-size:10px; font-family:'Inter',sans-serif; margin-top:4px;">
        Data sourced from: BofA/Similarweb, G2, Reddit, Trustpilot, Intellectia, Goldman Sachs, 
        Morgan Stanley, Gartner, Forbes, Yahoo Finance &nbsp;·&nbsp; March 2026
    </p>
</div>
""", unsafe_allow_html=True)
