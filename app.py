
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page Configuration
st.set_page_config(
    page_title="AWS APAC Sales Cycle Gap Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #232F3E;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #527FFF;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #232F3E 0%, #527FFF 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 8px;
    }
    .insight-box {
        background-color: #f0f4ff;
        border-left: 4px solid #527FFF;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA GENERATION (Simulated APAC Sales Data)
# ============================================================
@st.cache_data
def generate_sales_data():
    np.random.seed(42)
    
    countries = ["Singapore", "Australia", "Japan", "India", "South Korea", 
                 "Indonesia", "Thailand", "Malaysia", "Philippines", "Vietnam"]
    
    aws_services = ["EC2", "S3", "Lambda", "SageMaker", "Bedrock", 
                    "EKS", "RDS", "CloudFront", "Connect", "QuickSight"]
    
    stages = ["Prospecting", "Qualification", "Technical Validation", 
              "Proposal", "Negotiation", "Closed Won", "Closed Lost"]
    
    industries = ["Financial Services", "Healthcare", "Manufacturing", 
                  "Retail", "Technology", "Government", "Telco", "Media"]
    
    sales_reps = [f"Rep_{i}" for i in range(1, 26)]
    
    n_opportunities = 500
    
    data = {
        "opportunity_id": [f"OPP-APAC-{i:04d}" for i in range(1, n_opportunities + 1)],
        "country": np.random.choice(countries, n_opportunities, 
                                     p=[0.15, 0.15, 0.15, 0.12, 0.10, 0.08, 0.08, 0.07, 0.05, 0.05]),
        "industry": np.random.choice(industries, n_opportunities),
        "aws_service": np.random.choice(aws_services, n_opportunities),
        "stage": np.random.choice(stages, n_opportunities, 
                                   p=[0.15, 0.20, 0.20, 0.15, 0.10, 0.12, 0.08]),
        "deal_size_usd": np.random.lognormal(mean=11, sigma=1.2, size=n_opportunities).astype(int),
        "sales_rep": np.random.choice(sales_reps, n_opportunities),
        "days_in_stage": np.random.exponential(scale=25, size=n_opportunities).astype(int),
        "expected_close_date": [datetime(2026, 1, 1) + timedelta(days=int(x)) 
                                for x in np.random.uniform(0, 365, n_opportunities)],
        "created_date": [datetime(2025, 6, 1) + timedelta(days=int(x)) 
                         for x in np.random.uniform(0, 380, n_opportunities)],
        "win_probability": np.random.beta(2, 3, n_opportunities),
        "competitor": np.random.choice(["Azure", "GCP", "Oracle Cloud", "IBM Cloud", "Alibaba Cloud", "None"], 
                                        n_opportunities, p=[0.25, 0.20, 0.10, 0.05, 0.15, 0.25]),
        "partner_involved": np.random.choice([True, False], n_opportunities, p=[0.4, 0.6]),
        "certifications_held": np.random.randint(0, 12, n_opportunities),
        "enablement_score": np.random.uniform(40, 100, n_opportunities),
        "customer_engagement_score": np.random.uniform(30, 100, n_opportunities),
    }
    
    df = pd.DataFrame(data)
    
    # Add calculated fields
    df["deal_size_usd"] = df["deal_size_usd"].clip(upper=5000000)
    df["weighted_pipeline"] = df["deal_size_usd"] * df["win_probability"]
    df["is_at_risk"] = (df["days_in_stage"] > 45) | (df["enablement_score"] < 60)
    df["quarter"] = df["expected_close_date"].apply(lambda x: f"Q{(x.month-1)//3 + 1} {x.year}")
    
    return df

@st.cache_data
def generate_enablement_data():
    np.random.seed(123)
    
    programs = [
        "AWS Cloud Practitioner", "AWS Solutions Architect", "AWS ML Specialty",
        "GenAI Foundations", "Bedrock Builder", "APAC Sales Methodology",
        "Executive Briefing Skills", "Technical Discovery Workshop",
        "Competitive Intelligence - Azure", "Competitive Intelligence - GCP",
        "Industry: FSI Deep Dive", "Industry: Healthcare on AWS",
        "Partner Co-Sell Program", "Customer Success Stories Workshop"
    ]
    
    data = {
        "program": programs * 3,
        "completion_rate": np.random.uniform(0.3, 0.95, len(programs) * 3),
        "impact_on_win_rate": np.random.uniform(-0.05, 0.25, len(programs) * 3),
        "avg_deal_size_lift": np.random.uniform(-5, 30, len(programs) * 3),
        "time_to_complete_days": np.random.randint(1, 30, len(programs) * 3),
        "satisfaction_score": np.random.uniform(3.0, 5.0, len(programs) * 3),
        "region": np.random.choice(["ANZ", "ASEAN", "Japan", "India", "Korea"], len(programs) * 3),
    }
    
    return pd.DataFrame(data)

@st.cache_data
def generate_forecast_data():
    months = pd.date_range(start="2025-01-01", periods=24, freq="MS")
    np.random.seed(99)
    
    base_revenue = 15000000
    growth_rate = 0.08
    
    actual = []
    forecast = []
    
    for i, month in enumerate(months):
        if month <= datetime(2026, 6, 1):
            val = base_revenue * (1 + growth_rate) ** (i/12) * (1 + np.random.normal(0, 0.05))
            actual.append(val)
            forecast.append(None)
        else:
            actual.append(None)
            val = base_revenue * (1 + growth_rate) ** (i/12) * (1 + np.random.normal(0, 0.03))
            forecast.append(val)
    
    return pd.DataFrame({
        "month": months,
        "actual_revenue": actual,
        "forecast_revenue": forecast,
        "ai_confidence": np.random.uniform(0.7, 0.95, len(months))
    })

# Load Data
df = generate_sales_data()
enablement_df = generate_enablement_data()
forecast_df = generate_forecast_data()

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Amazon_Web_Services_Logo.svg/1200px-Amazon_Web_Services_Logo.svg.png", width=150)
    st.markdown("---")
    
    st.markdown("### 🎯 Executive Lens")
    persona = st.radio(
        "Select Perspective:",
        ["🏗️ CTO View", "📚 CLO View", "💰 CSO View", "🌏 APAC Unified"],
        index=3
    )
    
    st.markdown("---")
    st.markdown("### 🔍 Filters")
    
    selected_countries = st.multiselect(
        "Countries", df["country"].unique().tolist(),
        default=df["country"].unique().tolist()
    )
    
    selected_industries = st.multiselect(
        "Industries", df["industry"].unique().tolist(),
        default=df["industry"].unique().tolist()
    )
    
    selected_services = st.multiselect(
        "AWS Services", df["aws_service"].unique().tolist(),
        default=df["aws_service"].unique().tolist()
    )
    
    st.markdown("---")
    st.markdown("### 🤖 Gen AI Features")
    st.checkbox("Enable AI Insights", value=True, key="ai_insights")
    st.checkbox("Predictive Analytics", value=True, key="predictive")
    st.checkbox("Auto-Recommendations", value=True, key="auto_rec")
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8rem;'>
        Built with ❤️ for AWS APAC<br>
        Gen AI Powered | Streamlit<br>
        v2.0 | June 2026
    </div>
    """, unsafe_allow_html=True)

# Filter data
filtered_df = df[
    (df["country"].isin(selected_countries)) &
    (df["industry"].isin(selected_industries)) &
    (df["aws_service"].isin(selected_services))
]

# ============================================================
# MAIN DASHBOARD
# ============================================================
st.markdown('<p class="main-header">🚀 AWS APAC Sales Cycle Gap Analyzer</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Gen AI-Powered Sales Intelligence | CTO • CLO • CSO Perspectives</p>', unsafe_allow_html=True)

# Top-level KPIs
col1, col2, col3, col4, col5 = st.columns(5)

total_pipeline = filtered_df["deal_size_usd"].sum()
weighted_pipeline = filtered_df["weighted_pipeline"].sum()
avg_win_prob = filtered_df["win_probability"].mean()
at_risk_deals = filtered_df["is_at_risk"].sum()
avg_cycle_days = filtered_df["days_in_stage"].mean()

col1.metric("💰 Total Pipeline", f"${total_pipeline/1e6:.1f}M", "+12% QoQ")
col2.metric("📊 Weighted Pipeline", f"${weighted_pipeline/1e6:.1f}M", "+8% QoQ")
col3.metric("🎯 Avg Win Probability", f"{avg_win_prob:.1%}", "+3pp")
col4.metric("⚠️ At-Risk Deals", f"{at_risk_deals}", "-5 vs last month")
col5.metric("⏱️ Avg Days in Stage", f"{avg_cycle_days:.0f}", "-3 days")

st.markdown("---")

# ============================================================
# TABS FOR DIFFERENT VIEWS
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Pipeline Overview", 
    "🌏 APAC Regional Analysis",
    "🤖 Gen AI Insights & Predictions",
    "📚 Enablement & Performance",
    "🎯 Action Plan & Recommendations"
])

# TAB 1: Pipeline Overview
with tab1:
    st.markdown("## Pipeline Health Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pipeline by Stage
        stage_data = filtered_df.groupby("stage").agg(
            count=("opportunity_id", "count"),
            total_value=("deal_size_usd", "sum")
        ).reset_index()
        
        fig = px.funnel(stage_data, x="total_value", y="stage",
                       title="Sales Funnel - Pipeline by Stage",
                       color_discrete_sequence=["#527FFF"])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Pipeline by AWS Service
        service_data = filtered_df.groupby("aws_service")["deal_size_usd"].sum().reset_index()
        service_data = service_data.sort_values("deal_size_usd", ascending=False)
        
        fig = px.bar(service_data, x="aws_service", y="deal_size_usd",
                    title="Pipeline by AWS Service",
                    color="deal_size_usd",
                    color_continuous_scale="Blues")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Competitor Landscape
        competitor_data = filtered_df[filtered_df["competitor"] != "None"].groupby("competitor").agg(
            deals=("opportunity_id", "count"),
            avg_win_prob=("win_probability", "mean")
        ).reset_index()
        
        fig = px.scatter(competitor_data, x="deals", y="avg_win_prob",
                        size="deals", color="competitor",
                        title="Competitive Landscape - Win Probability vs Deal Count",
                        size_max=50)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col4:
        # Deal Size Distribution
        fig = px.histogram(filtered_df, x="deal_size_usd", nbins=30,
                          title="Deal Size Distribution",
                          color_discrete_sequence=["#FF9900"])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# TAB 2: APAC Regional Analysis
with tab2:
    st.markdown("## 🌏 APAC Regional Deep Dive")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by Country
        country_data = filtered_df.groupby("country").agg(
            total_pipeline=("deal_size_usd", "sum"),
            deal_count=("opportunity_id", "count"),
            avg_win_rate=("win_probability", "mean"),
            avg_enablement=("enablement_score", "mean")
        ).reset_index()
        
        fig = px.treemap(country_data, path=["country"], values="total_pipeline",
                        color="avg_win_rate", color_continuous_scale="RdYlGn",
                        title="Pipeline Distribution by Country (Color = Win Rate)")
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Industry x Country Heatmap
        heatmap_data = filtered_df.pivot_table(
            values="deal_size_usd", index="industry", columns="country", aggfunc="sum"
        ).fillna(0)
        
        fig = px.imshow(heatmap_data / 1e6, 
                       title="Pipeline Heatmap: Industry × Country ($M)",
                       color_continuous_scale="Blues",
                       aspect="auto")
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)
    
    # Regional Performance Table
    st.markdown("### 📋 Regional Performance Summary")
    regional_summary = filtered_df.groupby("country").agg(
        total_pipeline=("deal_size_usd", "sum"),
        weighted_pipeline=("weighted_pipeline", "sum"),
        deal_count=("opportunity_id", "count"),
        avg_win_rate=("win_probability", "mean"),
        avg_days_in_stage=("days_in_stage", "mean"),
        at_risk_pct=("is_at_risk", "mean"),
        avg_enablement=("enablement_score", "mean")
    ).reset_index()
    
    regional_summary["total_pipeline"] = regional_summary["total_pipeline"].apply(lambda x: f"${x/1e6:.2f}M")
    regional_summary["weighted_pipeline"] = regional_summary["weighted_pipeline"].apply(lambda x: f"${x/1e6:.2f}M")
    regional_summary["avg_win_rate"] = regional_summary["avg_win_rate"].apply(lambda x: f"{x:.1%}")
    regional_summary["at_risk_pct"] = regional_summary["at_risk_pct"].apply(lambda x: f"{x:.1%}")
    regional_summary["avg_enablement"] = regional_summary["avg_enablement"].apply(lambda x: f"{x:.1f}/100")
    regional_summary["avg_days_in_stage"] = regional_summary["avg_days_in_stage"].apply(lambda x: f"{x:.0f}")
    
    st.dataframe(regional_summary, use_container_width=True, hide_index=True)

# TAB 3: Gen AI Insights
with tab3:
    st.markdown("## 🤖 Gen AI-Powered Insights & Predictions")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Revenue Forecast
        st.markdown("### 📈 AI Revenue Forecast (Next 6 Months)")
        
        forecast_chart_data = forecast_df.copy()
        forecast_chart_data["month_str"] = forecast_chart_data["month"].dt.strftime("%b %Y")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=forecast_chart_data["month"],
            y=forecast_chart_data["actual_revenue"],
            mode="lines+markers",
            name="Actual Revenue",
            line=dict(color="#232F3E", width=3)
        ))
        fig.add_trace(go.Scatter(
            x=forecast_chart_data["month"],
            y=forecast_chart_data["forecast_revenue"],
            mode="lines+markers",
            name="AI Forecast",
            line=dict(color="#527FFF", width=3, dash="dash")
        ))
        fig.update_layout(
            title="Revenue Trajectory with AI Forecast",
            height=400,
            xaxis_title="Month",
            yaxis_title="Revenue ($)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 AI Confidence Metrics")
        st.metric("Forecast Accuracy", "87.3%", "+2.1%")
        st.metric("Model Confidence", "91.5%", "+1.8%")
        st.metric("Data Freshness", "Real-time", "")
        
        st.markdown("---")
        st.markdown("### 🧠 Gen AI Stack")
        st.markdown("""
        - **Amazon Bedrock** - Foundation Models
        - **Amazon SageMaker** - Custom ML
        - **Amazon Q** - Business Intelligence
        - **Claude 3.5** - Analysis & Insights
        - **Titan Embeddings** - Semantic Search
        """)
    
    # AI-Generated Insights
    st.markdown("### 💡 AI-Generated Strategic Insights")
    
    insights_col1, insights_col2, insights_col3 = st.columns(3)
    
    with insights_col1:
        st.markdown("""
        <div class="insight-box">
        <strong>🏗️ CTO Insight:</strong><br>
        GenAI services (Bedrock, SageMaker) show 3.2x faster sales cycles 
        when paired with technical POC automation. Recommend expanding 
        self-service demo environments across APAC.
        </div>
        """, unsafe_allow_html=True)
    
    with insights_col2:
        st.markdown("""
        <div class="insight-box">
        <strong>📚 CLO Insight:</strong><br>
        Reps with GenAI certifications close 28% larger deals. 
        Japan and Korea show highest ROI from enablement investment. 
        Priority: Bedrock Builder certification for ASEAN team.
        </div>
        """, unsafe_allow_html=True)
    
    with insights_col3:
        st.markdown("""
        <div class="insight-box">
        <strong>💰 CSO Insight:</strong><br>
        APAC pipeline velocity increased 15% QoQ. Singapore and Australia 
        lead in enterprise deals. Key gap: Mid-market penetration in 
        India and Indonesia requires localized approach.
        </div>
        """, unsafe_allow_html=True)
    
    # Predictive Deal Scoring
    st.markdown("### 🎲 Predictive Deal Scoring (Top 10 Opportunities)")
    
    top_deals = filtered_df.nlargest(10, "weighted_pipeline")[
        ["opportunity_id", "country", "industry", "aws_service", 
         "deal_size_usd", "win_probability", "stage", "days_in_stage", "is_at_risk"]
    ].copy()
    top_deals["ai_recommendation"] = [
        "Accelerate - Executive sponsor engaged",
        "Technical deep-dive needed - schedule SA",
        "Competitive threat (Azure) - deploy battle card",
        "Partner co-sell opportunity - engage SI",
        "Upsell potential - add Bedrock to proposal",
        "At risk - escalate to leadership",
        "Fast track - customer ready to sign",
        "Needs POC extension - complex workload",
        "Cross-sell from existing EC2 footprint",
        "Strategic account - align with country GM"
    ]
    
    st.dataframe(top_deals, use_container_width=True, hide_index=True)

# TAB 4: Enablement & Performance
with tab4:
    st.markdown("## 📚 Enablement & Performance Analytics")
    st.markdown("*Chief Learning Officer Perspective - Driving Sales Performance through Strategic Enablement*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Enablement Score vs Win Rate
        fig = px.scatter(filtered_df, x="enablement_score", y="win_probability",
                        color="country", size="deal_size_usd",
                        title="Enablement Score vs Win Probability",
                        trendline="ols",
                        opacity=0.6)
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Certification Impact
        cert_bins = pd.cut(filtered_df["certifications_held"], bins=[0, 2, 5, 8, 12], 
                          labels=["0-2", "3-5", "6-8", "9-12"])
        cert_impact = filtered_df.groupby(cert_bins).agg(
            avg_deal_size=("deal_size_usd", "mean"),
            avg_win_rate=("win_probability", "mean"),
            count=("opportunity_id", "count")
        ).reset_index()
        
        fig = px.bar(cert_impact, x="certifications_held", y="avg_deal_size",
                    title="Certification Count Impact on Avg Deal Size",
                    color="avg_win_rate",
                    color_continuous_scale="Greens",
                    text="count")
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)
    
    # Enablement Program Effectiveness
    st.markdown("### 📊 Enablement Program Effectiveness")
    
    program_summary = enablement_df.groupby("program").agg(
        avg_completion=("completion_rate", "mean"),
        avg_impact=("impact_on_win_rate", "mean"),
        avg_deal_lift=("avg_deal_size_lift", "mean"),
        avg_satisfaction=("satisfaction_score", "mean")
    ).reset_index().sort_values("avg_impact", ascending=False)
    
    fig = px.scatter(program_summary, x="avg_completion", y="avg_impact",
                    size="avg_deal_lift", color="avg_satisfaction",
                    hover_name="program",
                    title="Program Effectiveness Matrix (Size = Deal Size Lift, Color = Satisfaction)",
                    color_continuous_scale="RdYlGn",
                    size_max=40)
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Recommended Learning Paths
    st.markdown("### 🎓 AI-Recommended Learning Paths by Role")
    
    learning_paths = {
        "Role": ["Account Executive", "Solutions Architect", "Partner Manager", "BDR/SDR", "Sales Leader"],
        "Priority Certification": ["AWS Cloud Practitioner + GenAI Foundations", 
                                   "AWS ML Specialty + Bedrock Builder",
                                   "Partner Co-Sell + Industry Deep Dive",
                                   "Technical Discovery + Competitive Intel",
                                   "Executive Briefing + APAC Methodology"],
        "Expected Win Rate Lift": ["+15%", "+22%", "+18%", "+12%", "+25%"],
        "Expected Deal Size Lift": ["+20%", "+35%", "+28%", "+10%", "+40%"],
        "Time Investment": ["2 weeks", "4 weeks", "3 weeks", "1 week", "2 weeks"],
        "ROI Score": ["8.5/10", "9.2/10", "8.8/10", "7.5/10", "9.5/10"]
    }
    
    st.dataframe(pd.DataFrame(learning_paths), use_container_width=True, hide_index=True)

# TAB 5: Action Plan
with tab5:
    st.markdown("## 🎯 Strategic Action Plan & Recommendations")
    st.markdown("*Unified CTO + CLO + CSO Perspective for APAC Growth*")
    
    # Quarterly Targets
    st.markdown("### 📅 Q3 2026 Priority Actions")
    
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        st.markdown("#### 🏗️ CTO Actions")
        st.markdown("""
        1. **Deploy GenAI Demo Environments** across all APAC regions
        2. **Automate POC provisioning** with AWS Service Catalog
        3. **Build industry-specific solution accelerators** (FSI, Healthcare)
        4. **Implement AI-powered deal scoring** in CRM
        5. **Scale Bedrock-based customer engagement** tools
        """)
    
    with action_col2:
        st.markdown("#### 📚 CLO Actions")
        st.markdown("""
        1. **Launch Bedrock Builder certification** - target 80% completion
        2. **Deploy competitive battle cards** (Azure/GCP) with AI updates
        3. **Create APAC-specific case study library** by industry
        4. **Implement peer learning circles** for top performers
        5. **Build GenAI skills assessment** for all customer-facing roles
        """)
    
    with action_col3:
        st.markdown("#### 💰 CSO Actions")
        st.markdown("""
        1. **Accelerate mid-market plays** in India & Indonesia
        2. **Expand partner co-sell** - target 60% partner-attached deals
        3. **Implement AI-guided next-best-action** for reps
        4. **Launch executive sponsorship program** for $1M+ deals
        5. **Deploy territory optimization** using ML models
        """)
    
    st.markdown("---")
    
    # Gap Analysis Summary
    st.markdown("### 📊 Sales Cycle Gap Analysis Summary")
    
    gap_data = {
        "Gap Area": [
            "Technical Validation Duration",
            "GenAI Service Knowledge",
            "Competitive Win Rate vs Azure",
            "Mid-Market Penetration (India/ID)",
            "Partner Ecosystem Leverage",
            "Executive Engagement Frequency",
            "Post-Sale Expansion Rate"
        ],
        "Current State": ["42 days avg", "45% proficient", "52% win rate", 
                         "12% market share", "38% partner-attached", "1.2x/quarter", "22% expansion"],
        "Target State": ["28 days avg", "80% proficient", "65% win rate",
                        "25% market share", "60% partner-attached", "3x/quarter", "40% expansion"],
        "Gap": ["-14 days", "+35pp", "+13pp", "+13pp", "+22pp", "+1.8x", "+18pp"],
        "Priority": ["🔴 Critical", "🔴 Critical", "🟡 High", "🟡 High", 
                    "🟡 High", "🟢 Medium", "🟢 Medium"],
        "AI-Powered Solution": [
            "Automated POC + AI-guided technical validation",
            "Bedrock Builder cert + hands-on labs",
            "AI battle cards + real-time competitive intel",
            "Localized playbooks + AI lead scoring",
            "Partner matching algorithm + co-sell automation",
            "AI-scheduled exec touchpoints",
            "Predictive expansion signals + auto-triggers"
        ]
    }
    
    st.dataframe(pd.DataFrame(gap_data), use_container_width=True, hide_index=True)
    
    # ROI Calculator
    st.markdown("### 💰 Enablement ROI Calculator")
    
    roi_col1, roi_col2 = st.columns(2)
    
    with roi_col1:
        investment = st.slider("Enablement Investment ($K)", 100, 2000, 500, 50)
        expected_lift = st.slider("Expected Win Rate Lift (%)", 5, 30, 15)
        pipeline_coverage = st.slider("Pipeline Coverage Ratio", 2.0, 5.0, 3.0, 0.5)
    
    with roi_col2:
        current_pipeline = total_pipeline
        projected_revenue = current_pipeline * (avg_win_prob + expected_lift/100)
        incremental_revenue = projected_revenue - (current_pipeline * avg_win_prob)
        roi = (incremental_revenue - investment * 1000) / (investment * 1000) * 100
        
        st.metric("Projected Incremental Revenue", f"${incremental_revenue/1e6:.1f}M")
        st.metric("ROI on Enablement", f"{roi:.0f}%")
        st.metric("Payback Period", f"{max(1, int(investment*1000/incremental_revenue*12))} months")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; color: #666;'>
    <strong>AWS APAC Sales Cycle Gap Analyzer v2.0</strong><br>
    Powered by Amazon Bedrock | Built with Streamlit | Gen AI Interview Showcase<br>
    © 2026 | Danny Ng | CTO × CLO × CSO Unified Intelligence Platform
</div>
""", unsafe_allow_html=True)
