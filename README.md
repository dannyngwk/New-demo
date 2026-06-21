# 🚀 AWS APAC Sales Cycle Gap Analyzer v2.0

## Gen AI-Powered Sales Intelligence Platform

> **Interview Showcase**: Demonstrating Gen AI fluency through a multi-persona executive dashboard combining CTO, CLO, and CSO perspectives for AWS APAC sales optimization.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36-red)
![AWS](https://img.shields.io/badge/AWS-Powered-orange)
![GenAI](https://img.shields.io/badge/GenAI-Enabled-purple)

---

## 🎯 Overview

This dashboard provides a comprehensive **Sales Cycle Gap Analysis** tool designed for AWS APAC leadership, offering:

- **CTO View**: Technology architecture decisions, GenAI integration opportunities, and scalability insights
- **CLO View**: Enablement program effectiveness, certification impact analysis, and learning path recommendations
- **CSO View**: Pipeline health, win rate optimization, competitive intelligence, and revenue forecasting
- **APAC Unified**: Cross-functional strategic alignment with AI-powered recommendations

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                      │
├─────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │ Pipeline │  │  APAC    │  │  GenAI   │  │Enable- │ │
│  │ Overview │  │ Regional │  │ Insights │  │  ment  │ │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘ │
├─────────────────────────────────────────────────────────┤
│              Data Processing Layer (Pandas/NumPy)         │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────┐   │
│  │         Amazon Bedrock (Foundation Models)        │   │
│  │    Claude 3.5 | Titan Embeddings | Jurassic      │   │
│  └──────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────────┐   │
│  │  CRM   │  │  LMS   │  │Partner │  │  Revenue   │   │
│  │  Data  │  │  Data  │  │  Data  │  │  Forecast  │   │
│  └────────┘  └────────┘  └────────┘  └────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip or conda

### Installation

```bash
# Clone the repository
git clone https://github.com/dannyngwk/sales-cycle-gap-analyzer.git
cd sales-cycle-gap-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

### Docker (Optional)

```bash
docker build -t sales-gap-analyzer .
docker run -p 8501:8501 sales-gap-analyzer
```

## 📊 Dashboard Features

### Tab 1: Pipeline Overview
- Sales funnel visualization
- Pipeline by AWS service
- Competitive landscape analysis
- Deal size distribution

### Tab 2: APAC Regional Analysis
- Country-level pipeline treemap
- Industry x Country heatmap
- Regional performance scorecard
- Market penetration metrics

### Tab 3: Gen AI Insights and Predictions
- AI-powered revenue forecasting
- Predictive deal scoring
- Multi-persona strategic insights (CTO/CLO/CSO)
- Next-best-action recommendations

### Tab 4: Enablement and Performance
- Enablement score vs win probability correlation
- Certification impact analysis
- Program effectiveness matrix
- AI-recommended learning paths

### Tab 5: Action Plan and Recommendations
- Quarterly priority actions by persona
- Sales cycle gap analysis summary
- Enablement ROI calculator
- AI-powered solution mapping

## 🤖 Gen AI Integration Points

| Component | AWS Service | Purpose |
|-----------|-------------|---------|
| Deal Scoring | Amazon SageMaker | Predictive win probability |
| Insights Generation | Amazon Bedrock (Claude) | Strategic narrative |
| Competitive Intel | Amazon Bedrock (Titan) | Real-time battle cards |
| Forecast | Amazon Forecast | Revenue prediction |
| Search | Amazon Kendra | Knowledge retrieval |
| Recommendations | Amazon Personalize | Next-best-action |

## 📁 Project Structure

```
sales-cycle-gap-analyzer/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── Dockerfile             # Container configuration
├── .streamlit/
│   └── config.toml        # Streamlit configuration
├── data/
│   └── sample_data.py     # Sample data generators
├── utils/
│   ├── ai_insights.py     # Gen AI insight generation
│   ├── forecasting.py     # Revenue forecasting models
│   └── gap_analysis.py    # Gap analysis calculations
└── assets/
    └── aws_logo.png       # AWS branding assets
```

## 🌏 APAC Markets Covered

- 🇸🇬 Singapore
- 🇦🇺 Australia
- 🇯🇵 Japan
- 🇮🇳 India
- 🇰🇷 South Korea
- 🇮🇩 Indonesia
- 🇹🇭 Thailand
- 🇲🇾 Malaysia
- 🇵🇭 Philippines
- 🇻🇳 Vietnam

## 👤 Author

**Danny Ng** - AWS APAC Sales Intelligence
Built for Gen AI Fluency Interview Showcase | June 2026

## 📄 License

MIT License - See LICENSE file for details
