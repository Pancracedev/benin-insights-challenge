import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
 
# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Benin Media Intelligence",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #21262d;
    }
    .kpi-card {
        background: linear-gradient(135deg, #1c2128, #21262d);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px 24px;
        text-align: center;
        transition: transform 0.2s;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: #58a6ff;
    }
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #58a6ff;
        line-height: 1;
        margin-bottom: 6px;
    }
    .kpi-label {
        font-size: 0.82rem;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .kpi-delta { font-size: 0.85rem; margin-top: 6px; }
    .kpi-delta.pos { color: #3fb950; }
    .kpi-delta.neg { color: #f85149; }
    .kpi-delta.neu { color: #d29922; }
    .section-header {
        font-size: 1.05rem;
        font-weight: 600;
        color: #c9d1d9;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        border-bottom: 2px solid #21262d;
        padding-bottom: 8px;
        margin-bottom: 16px;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: #161b22;
        border-radius: 8px;
        gap: 4px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #8b949e;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 500;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background: #21262d !important;
        color: #58a6ff !important;
    }
    .js-plotly-plot { border-radius: 12px; }
    .page-header {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #1c2128 100%);
        border: 1px solid #21262d;
        border-radius: 16px;
        padding: 32px 40px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
    }
    .page-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #58a6ff, #3fb950, #d29922, #f85149);
    }
    .page-title {
        font-size: 2rem;
        font-weight: 800;
        color: #e6edf3;
        margin: 0;
    }
    .page-subtitle {
        color: #8b949e;
        font-size: 0.95rem;
        margin-top: 8px;
    }
    .insight-box {
        background: #161b22;
        border-left: 4px solid #58a6ff;
        border-radius: 0 8px 8px 0;
        padding: 14px 18px;
        margin-bottom: 12px;
        font-size: 0.88rem;
        color: #c9d1d9;
    }
    .insight-box.warning { border-left-color: #d29922; }
    .insight-box.danger  { border-left-color: #f85149; }
    .insight-box.success { border-left-color: #3fb950; }
</style>
""", unsafe_allow_html=True)
 
# ============================================================
# PLOTLY THEME
# ============================================================
PLOTLY_TEMPLATE = dict(
    layout=dict(
        paper_bgcolor="#161b22",
        plot_bgcolor="#0d1117",
        font=dict(color="#c9d1d9", family="Inter"),
        title_font=dict(size=14, color="#e6edf3"),
        xaxis=dict(
            gridcolor="#21262d", linecolor="#30363d",
            tickfont=dict(color="#8b949e"), title_font=dict(color="#8b949e")
        ),
        yaxis=dict(
            gridcolor="#21262d", linecolor="#30363d",
            tickfont=dict(color="#8b949e"), title_font=dict(color="#8b949e")
        ),
        legend=dict(
            bgcolor="#1c2128", bordercolor="#30363d",
            borderwidth=1, font=dict(color="#c9d1d9")
        ),
        colorway=["#58a6ff", "#3fb950", "#d29922", "#f85149",
                  "#bc8cff", "#79c0ff", "#56d364", "#ffa657"],
        margin=dict(t=50, b=40, l=50, r=20),
    )
)
 
COLORS = {
    "positive": "#3fb950",
    "negative": "#f85149",
    "neutral":  "#d29922",
    "blue":     "#58a6ff",
    "purple":   "#bc8cff",
    "crisis":   "#f85149",
    "normal":   "#3fb950",
}
 
# ============================================================
# DATA LOADING
# ============================================================
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, '..', 'data', 'clean', 'benin_gdelt_clean.csv')
 
    if not os.path.exists(csv_path):
        csv_path = os.path.join(base_dir, 'benin_gdelt_clean.csv')
 
    df = pd.read_csv(csv_path)
 
    df['event_date']       = pd.to_datetime(df['event_date'],  format='mixed', errors='coerce')
    df['DATEADDED']        = pd.to_datetime(df['DATEADDED'],   format='mixed', errors='coerce')
    df['week']             = df['event_date'].dt.to_period('W').apply(lambda r: r.start_time)
    df['month_label']      = df['event_date'].dt.to_period('M').astype(str)
    df['is_crisis_period'] = df['is_crisis_period'].astype(bool)
 
    def goldstein_bucket(v):
        if v >= 5:  return "Tres stabilisant"
        if v >= 1:  return "Stabilisant"
        if v >= -1: return "Neutre"
        if v >= -5: return "Destabilisant"
        return "Tres destabilisant"
 
    df['goldstein_bucket'] = df['GoldsteinScale'].apply(goldstein_bucket)
    return df
 
df = load_data()
 
# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### Filtres")
    st.markdown("---")
 
    quarters = sorted(df['event_quarter'].dropna().unique().tolist())
    sel_quarters = st.multiselect("Trimestre", quarters, default=quarters)
 
    tones = df['tone_category'].dropna().unique().tolist()
    sel_tones = st.multiselect("Tonalite", tones, default=tones)
 
    stab_cats = df['stability_category'].dropna().unique().tolist()
    sel_stab = st.multiselect("Stabilite", stab_cats, default=stab_cats)
 
    roles = df['benin_role'].dropna().unique().tolist()
    sel_roles = st.multiselect("Role du Benin", roles, default=roles)
 
    goldstein_range = st.slider(
        "Echelle de Goldstein",
        float(df['GoldsteinScale'].min()),
        float(df['GoldsteinScale'].max()),
        (float(df['GoldsteinScale'].min()), float(df['GoldsteinScale'].max()))
    )
 
    crisis_filter = st.radio(
        "Periode de crise",
        ["Toutes", "Crise uniquement", "Hors crise"],
        index=0
    )
 
    st.markdown("---")
    st.markdown(
        "<div style='color:#8b949e;font-size:0.78rem;text-align:center'>"
        "Benin Insights Challenge 2026<br>Source : GDELT Project</div>",
        unsafe_allow_html=True
    )
 
# ============================================================
# FILTERING
# ============================================================
dff = df.copy()
 
if sel_quarters:
    dff = dff[dff['event_quarter'].isin(sel_quarters)]
if sel_tones:
    dff = dff[dff['tone_category'].isin(sel_tones)]
if sel_stab:
    dff = dff[dff['stability_category'].isin(sel_stab)]
if sel_roles:
    dff = dff[dff['benin_role'].isin(sel_roles)]
 
dff = dff[
    (dff['GoldsteinScale'] >= goldstein_range[0]) &
    (dff['GoldsteinScale'] <= goldstein_range[1])
]
 
if crisis_filter == "Crise uniquement":
    dff = dff[dff['is_crisis_period'] == True]
elif crisis_filter == "Hors crise":
    dff = dff[dff['is_crisis_period'] == False]
 
# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="page-header">
    <div class="page-title">Benin Media Intelligence Dashboard</div>
    <div class="page-subtitle">
        Analyse des evenements mediatiques relatifs au Benin | GDELT 2025 |
        Benin Insights Challenge 2026
    </div>
</div>
""", unsafe_allow_html=True)
 
# ============================================================
# KPI CARDS
# ============================================================
total_events   = len(dff)
avg_tone       = dff['AvgTone'].mean()
crisis_pct     = dff['is_crisis_period'].mean() * 100
avg_goldstein  = dff['GoldsteinScale'].mean()
total_articles = dff['NumArticles'].sum()
unique_sources = dff['source_domain'].nunique()
 
col1, col2, col3, col4, col5, col6 = st.columns(6)
 
def kpi(col, value, label):
    col.markdown(
        f"""<div class="kpi-card">
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>""",
        unsafe_allow_html=True
    )
 
kpi(col1, f"{total_events:,}",    "Evenements")
kpi(col2, f"{total_articles:,}",  "Articles")
kpi(col3, f"{avg_tone:+.2f}",     "Ton moyen")
kpi(col4, f"{avg_goldstein:+.2f}","Goldstein moyen")
kpi(col5, f"{crisis_pct:.1f}%",   "Periode de crise")
kpi(col6, f"{unique_sources}",    "Sources uniques")
 
st.markdown("<br>", unsafe_allow_html=True)
 
# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Chronologie",
    "Tonalite",
    "Stabilite",
    "Acteurs & Roles",
    "Types d'evenements",
    "Sources",
    "Geographie"
])
 
# -----------------------------------------------------------
# TAB 1 - CHRONOLOGIE
# -----------------------------------------------------------
with tab1:
    st.markdown('<div class="section-header">Evolution temporelle de la couverture</div>', unsafe_allow_html=True)
 
    col_a, col_b = st.columns([2, 1])
 
    with col_a:
        weekly_total = dff.groupby('week').agg(
            articles=('NumArticles', 'sum'),
            avg_tone=('AvgTone', 'mean')
        ).reset_index()
 
        fig = make_subplots(specs=[[{"secondary_y": True}]])
 
        crisis_weeks = dff[dff['is_crisis_period']]['week'].unique()
        for cw in crisis_weeks:
            fig.add_vrect(
                x0=str(cw), x1=str(cw + pd.Timedelta(days=7)),
                fillcolor="#f85149", opacity=0.06,
                layer="below", line_width=0
            )
 
        fig.add_trace(
            go.Bar(
                x=weekly_total['week'], y=weekly_total['articles'],
                name="Articles", marker_color="#58a6ff",
                marker_opacity=0.7, marker_line_width=0
            ),
            secondary_y=False
        )
        fig.add_trace(
            go.Scatter(
                x=weekly_total['week'], y=weekly_total['avg_tone'],
                name="Ton moyen", line=dict(color="#d29922", width=2),
                mode='lines+markers', marker_size=4
            ),
            secondary_y=True
        )
 
        fig.update_layout(
            **PLOTLY_TEMPLATE['layout'],
            title="Volume d'articles et ton moyen par semaine",
            height=380,
            barmode='overlay',
        )
        fig.update_yaxes(title_text="Nombre d'articles", secondary_y=False,
                         gridcolor="#21262d", tickfont_color="#8b949e")
        fig.update_yaxes(title_text="Ton moyen", secondary_y=True,
                         gridcolor=None, tickfont_color="#d29922", zeroline=False)
        st.plotly_chart(fig, use_container_width=True)
 
    with col_b:
        q_agg = dff.groupby('event_quarter').agg(
            events=('NumArticles', 'count'),
            articles=('NumArticles', 'sum'),
            avg_tone=('AvgTone', 'mean'),
            avg_gold=('GoldsteinScale', 'mean')
        ).reset_index().sort_values('event_quarter')
 
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=q_agg['event_quarter'], y=q_agg['events'],
            marker_color="#bc8cff", name="Evenements",
            text=q_agg['events'], textposition='outside',
            textfont=dict(color="#c9d1d9", size=11)
        ))
        fig2.update_layout(
            **PLOTLY_TEMPLATE['layout'],
            title="Evenements par trimestre",
            height=380, showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)
 
    st.markdown('<div class="section-header">Intensite mensuelle par type d\'evenement</div>', unsafe_allow_html=True)
 
    heat_data = dff.groupby(['month_label', 'event_root_label'])['NumArticles'].sum().reset_index()
    top_event_types = dff['event_root_label'].value_counts().head(8).index.tolist()
    heat_data = heat_data[heat_data['event_root_label'].isin(top_event_types)]
    heat_pivot = heat_data.pivot(index='event_root_label', columns='month_label', values='NumArticles').fillna(0)
 
    fig3 = px.imshow(
        heat_pivot,
        color_continuous_scale=[[0, "#0d1117"], [0.3, "#1c3a6e"], [0.7, "#2d6be4"], [1, "#58a6ff"]],
        aspect="auto",
        labels=dict(color="Articles")
    )
    fig3.update_layout(
        **PLOTLY_TEMPLATE['layout'],
        title="Heatmap : articles par type d'evenement et par mois",
        height=320,
    )
    fig3.update_xaxes(tickangle=-45)
    st.plotly_chart(fig3, use_container_width=True)
 
# -----------------------------------------------------------
# TAB 2 - TONALITE
# -----------------------------------------------------------
with tab2:
    st.markdown('<div class="section-header">Analyse de la tonalite mediatique</div>', unsafe_allow_html=True)
 
    col_a, col_b = st.columns(2)
 
    with col_a:
        tone_counts = dff['tone_category'].value_counts().reset_index()
        tone_counts.columns = ['tone', 'count']
 
        fig = px.pie(
            tone_counts, names='tone', values='count',
            hole=0.55,
            color='tone',
            color_discrete_map={
                "Positif": COLORS["positive"],
                "Negatif": COLORS["negative"],
                "Neutre":  COLORS["neutral"]
            }
        )
        fig.update_traces(
            textposition='outside',
            textfont=dict(color="#c9d1d9", size=13),
            marker=dict(line=dict(color="#0d1117", width=3))
        )
        fig.update_layout(
            **PLOTLY_TEMPLATE['layout'],
            title="Distribution des tonalites",
            height=380,
            annotations=[dict(
                text=f"{len(dff):,}<br>evenements",
                x=0.5, y=0.5, font_size=14, font_color="#e6edf3",
                showarrow=False
            )]
        )
        st.plotly_chart(fig, use_container_width=True)
 
    with col_b:
        tone_q = dff.groupby(['event_quarter', 'tone_category'])['NumArticles'].count().reset_index()
        tone_q.columns = ['quarter', 'tone', 'count']
 
        fig2 = px.bar(
            tone_q, x='quarter', y='count', color='tone',
            barmode='group',
            color_discrete_map={
                "Positif": COLORS["positive"],
                "Negatif": COLORS["negative"],
                "Neutre":  COLORS["neutral"]
            }
        )
        fig2.update_layout(
            **PLOTLY_TEMPLATE['layout'],
            title="Tonalite par trimestre",
            height=380,
            xaxis_title="Trimestre", yaxis_title="Nombre d'evenements"
        )
        st.plotly_chart(fig2, use_container_width=True)
 
    col_c, col_d = st.columns(2)
 
    with col_c:
        fig3 = px.violin(
            dff, x='benin_role', y='AvgTone',
            color='benin_role', box=True, points=False,
            color_discrete_sequence=["#58a6ff", "#3fb950", "#d29922", "#bc8cff"]
        )
        fig3.update_layout(
            **PLOTLY_TEMPLATE['layout'],
            title="Distribution du ton selon le role du Benin",
            height=380,
            showlegend=False,
            xaxis_title="Role", yaxis_title="Ton moyen"
        )
        fig3.add_hline(y=0, line_dash="dot", line_color="#8b949e", opacity=0.6)
        st.plotly_chart(fig3, use_container_width=True)
 
    with col_d:
        sample = dff.sample(min(3000, len(dff)), random_state=42)
        fig4 = px.scatter(
            sample,
            x='GoldsteinScale', y='AvgTone',
            color='tone_category',
            opacity=0.5,
            color_discrete_map={
                "Positif": COLORS["positive"],
                "Negatif": COLORS["negative"],
                "Neutre":  COLORS["neutral"]
            }
        )
        fig4.add_vline(x=0, line_dash="dot", line_color="#8b949e", opacity=0.5)
        fig4.add_hline(y=0, line_dash="dot", line_color="#8b949e", opacity=0.5)
        fig4.update_layout(
            **PLOTLY_TEMPLATE['layout'],
            title="Goldstein vs Ton moyen (echantillon 3 000 evenements)",
            height=380,
            xaxis_title="Echelle de Goldstein", yaxis_title="Ton moyen"
        )
        st.plotly_chart(fig4, use_container_width=True)
 
# -----------------------------------------------------------
# TAB 3 - STABILITE
# -----------------------------------------------------------
with tab3:
    st.markdown('<div class="section-header">Analyse de la stabilite geopolitique</div>', unsafe_allow_html=True)
 
    col_a, col_b = st.columns([3, 2])
 
    with col_a:
        gold_weekly = dff.groupby('week').agg(
            avg_gold=('GoldsteinScale', 'mean'),
            std_gold=('GoldsteinScale', 'std'),
            count=('GoldsteinScale', 'count')
        ).reset_index()
 
        gold_weekly['upper'] = gold_weekly['avg_gold'] + gold_weekly['std_gold'].fillna(0)
        gold_weekly['lower'] = gold_weekly['avg_gold'] - gold_weekly['std_gold'].fillna(0)
 
        fig = go.Figure()
 
        crisis_weeks = dff[dff['is_crisis_period'] == True]['week'].unique()
        for cw in crisis_weeks:
            fig.add_vrect(
                x0=str(cw), x1=str(pd.to_datetime(cw) + pd.Timedelta(days=7)),
                fillcolor="#f85149", opacity=0.08,
                layer="below", line_width=0
            )
 
        fig.add_trace(go.Scatter(
            x=gold_weekly['week'], y=gold_weekly['upper'],
            mode='lines', line=dict(width=0), showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=gold_weekly['week'], y=gold_weekly['lower'],
            fill='tonexty', mode='lines', line=dict(width=0),
            fillcolor='rgba(88,166,255,0.15)',
            name='Variabilite (Std Dev)'
        ))
        fig.add_trace(go.Scatter(
            x=gold_weekly['week'], y=gold_weekly['avg_gold'],
            mode='lines+markers',
            line=dict(color='#58a6ff', width=3),
            marker=dict(size=4),
            name='Score Goldstein Moyen'
        ))
 
        fig.update_layout(
            **PLOTLY_TEMPLATE['layout'],
            title="Evolution de l'indice de stabilite (Goldstein)",
            height=450,
            yaxis_title="Score de Goldstein",
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)
 
    with col_b:
        st.markdown("**Impact par type d'evenement**")
        event_impact = dff.groupby('event_root_label')['GoldsteinScale'].mean().sort_values().reset_index()
 
        fig_bar = px.bar(
            event_impact, x='GoldsteinScale', y='event_root_label',
            orientation='h',
            color='GoldsteinScale',
            color_continuous_scale='RdYlGn'
        )
        fig_bar.update_layout(**PLOTLY_TEMPLATE['layout'], height=400)
        st.plotly_chart(fig_bar, use_container_width=True)
 
# -----------------------------------------------------------
# TAB 4 - ACTEURS & ROLES
# -----------------------------------------------------------
with tab4:
    st.markdown('<div class="section-header">Analyse des Acteurs et des Interactions</div>', unsafe_allow_html=True)
 
    col_a, col_b = st.columns(2)
 
    with col_a:
        role_dist = dff['benin_role'].value_counts().reset_index()
        role_dist.columns = ['Role', 'Nombre']
        fig = px.pie(
            role_dist, names='Role', values='Nombre',
            hole=0.5,
            color_discrete_sequence=[COLORS["blue"], COLORS["purple"], COLORS["neutral"]]
        )
        fig.update_layout(
            **PLOTLY_TEMPLATE['layout'],
            title="Le Benin en tant qu'Acteur Principal vs Cible"
        )
        st.plotly_chart(fig, use_container_width=True)
 
    with col_b:
        role_tone = dff.groupby('benin_role')['AvgTone'].mean().reset_index()
        fig_bar = px.bar(
            role_tone, x='benin_role', y='AvgTone',
            color='AvgTone', color_continuous_scale='RdYlGn',
            title="Perception (Ton moyen) selon le role"
        )
        fig_bar.update_layout(**PLOTLY_TEMPLATE['layout'])
        st.plotly_chart(fig_bar, use_container_width=True)
 
# -----------------------------------------------------------
# TAB 5 - TYPES D'EVENEMENTS
# -----------------------------------------------------------
with tab5:
    st.markdown('<div class="section-header">Classification des evenements (CAMEO)</div>', unsafe_allow_html=True)
 
    tree_data = dff.groupby(['event_root_label', 'tone_category']).size().reset_index(name='count')
 
    fig = px.treemap(
        tree_data,
        path=[px.Constant("Tous les evenements"), 'event_root_label', 'tone_category'],
        values='count',
        color='event_root_label',
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig.update_layout(
    **PLOTLY_TEMPLATE['layout'],
    height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.info("Le Treemap permet de voir en un coup d'oeil les thematiques dominantes et leur tonalite associee.")
 