"""
Sales Cycle Gap Analysis Module
Identifies and quantifies gaps in the sales process
"""

import pandas as pd
import numpy as np
from typing import Dict, List

def identify_gaps(df: pd.DataFrame, benchmarks: dict = None) -> List[Dict]:
    """
    Identify gaps between current performance and targets
    
    Args:
        df: Sales opportunity dataframe
        benchmarks: Industry/internal benchmarks for comparison
    
    Returns:
        List of gap dictionaries with severity and recommendations
    """
    
    if benchmarks is None:
        benchmarks = {
            "avg_cycle_days": 28,
            "win_rate": 0.35,
            "enablement_score": 80,
            "partner_attach_rate": 0.60,
            "expansion_rate": 0.40,
            "executive_engagement": 3.0
        }
    
    gaps = []
    
    # Cycle Time Gap
    current_cycle = df["days_in_stage"].mean()
    if current_cycle > benchmarks["avg_cycle_days"]:
        gaps.append({
            "area": "Sales Cycle Duration",
            "current": f"{current_cycle:.0f} days",
            "target": f"{benchmarks['avg_cycle_days']} days",
            "gap": f"{current_cycle - benchmarks['avg_cycle_days']:.0f} days over",
            "severity": "critical" if current_cycle > benchmarks["avg_cycle_days"] * 1.5 else "high",
            "recommendation": "Implement AI-guided technical validation and automated POC provisioning",
            "estimated_impact": "+$2.3M pipeline acceleration"
        })
    
    # Win Rate Gap
    current_win_rate = df["win_probability"].mean()
    if current_win_rate < benchmarks["win_rate"]:
        gaps.append({
            "area": "Win Rate",
            "current": f"{current_win_rate:.1%}",
            "target": f"{benchmarks['win_rate']:.1%}",
            "gap": f"{(benchmarks['win_rate'] - current_win_rate)*100:.1f}pp below target",
            "severity": "critical",
            "recommendation": "Deploy competitive battle cards and enhance discovery methodology",
            "estimated_impact": "+$4.1M incremental revenue"
        })
    
    # Enablement Gap
    current_enablement = df["enablement_score"].mean()
    if current_enablement < benchmarks["enablement_score"]:
        gaps.append({
            "area": "Enablement Proficiency",
            "current": f"{current_enablement:.0f}/100",
            "target": f"{benchmarks['enablement_score']}/100",
            "gap": f"{benchmarks['enablement_score'] - current_enablement:.0f} points below",
            "severity": "high",
            "recommendation": "Accelerate GenAI certification program and industry-specific training",
            "estimated_impact": "+28% avg deal size"
        })
    
    # Partner Attach Gap
    current_partner = df["partner_involved"].mean()
    if current_partner < benchmarks["partner_attach_rate"]:
        gaps.append({
            "area": "Partner Ecosystem",
            "current": f"{current_partner:.1%}",
            "target": f"{benchmarks['partner_attach_rate']:.1%}",
            "gap": f"{(benchmarks['partner_attach_rate'] - current_partner)*100:.0f}pp below",
            "severity": "high",
            "recommendation": "Implement partner matching algorithm and co-sell incentives",
            "estimated_impact": "+1.8x win rate on partner deals"
        })
    
    return gaps


def calculate_gap_score(gaps: List[Dict]) -> float:
    """Calculate overall gap score (0-100, lower = more gaps)"""
    severity_weights = {"critical": 3, "high": 2, "medium": 1, "low": 0.5}
    
    total_weight = sum(severity_weights.get(g["severity"], 1) for g in gaps)
    max_possible = len(gaps) * 3  # All critical
    
    score = max(0, 100 - (total_weight / max_possible * 100)) if max_possible > 0 else 100
    return score


def generate_action_plan(gaps: List[Dict], persona: str = "unified") -> Dict:
    """Generate prioritized action plan based on identified gaps"""
    
    actions = {
        "immediate": [],  # This week
        "short_term": [],  # This month
        "medium_term": [],  # This quarter
        "long_term": []  # Next 2 quarters
    }
    
    for gap in sorted(gaps, key=lambda x: {"critical": 0, "high": 1, "medium": 2, "low": 3}[x["severity"]]):
        if gap["severity"] == "critical":
            actions["immediate"].append(gap["recommendation"])
        elif gap["severity"] == "high":
            actions["short_term"].append(gap["recommendation"])
        else:
            actions["medium_term"].append(gap["recommendation"])
    
    return actions
