"""Builds the cross-task clinical report (PatientReport) from a patient's raw
Assessment + Observation history.

This is deliberately rule-based, not a trained fusion model -- the blueprint's
explainability requirement (never a black-box score, always traceable to named
measurements) applies even harder here than to a single assessment, since a
report is exactly the artifact a neurologist might act on. Every line in
`recommendation_text` and `supporting_findings` traces back to a specific
measurement or trend computed below, nothing is inferred silently.

Thresholds for vowel/DDK "supporting findings" mirror the ones already used for
their own narrative text in modalities/voice/vowel.py and ddk.py -- kept here as
separate constants rather than imported, because those modules' thresholds are
tuned for single-recording narrative language, while these drive a recommendation
tier and should be changed deliberately, not as a side effect of tuning the other.
"""
from __future__ import annotations

from datetime import datetime, timezone

from .models import Assessment, Patient
from .schemas import (
    AssessmentRead, BiomarkerRead, BiomarkerTrend, PatientRead, PatientReport, TaskSummary, TrendPoint,
)

DISCLAIMER = (
    "This report synthesizes NeuroVoice screening results across the tasks a patient has "
    "completed. It is a screening aid, NOT a diagnosis -- it cannot confirm or rule out "
    "Parkinson's disease or any other condition. All findings should be interpreted by a "
    "qualified clinician alongside a full clinical evaluation."
)

_VOWEL_JITTER = "jitterLocal_sma3nz_amean"
_VOWEL_SHIMMER = "shimmerLocaldB_sma3nz_amean"
_VOWEL_HNR = "HNRdBACF_sma3nz_amean"
_DDK_RATE = "ddk_syllable_rate"
_DDK_REGULARITY = "ddk_regularity"
_DDK_RATE_TYPICAL_LOW = 5.0


def _to_assessment_read(a: Assessment) -> AssessmentRead:
    return AssessmentRead(
        id=a.id, patient_id=a.patient_id, modality=a.modality, task=a.task,
        performer=a.performer, model_name=a.model_name, model_version=a.model_version,
        quality_score=a.quality_score, risk_score=a.risk_score, confidence=a.confidence,
        risk_band=a.risk_band, flagged=a.flagged, narrative=a.narrative,
        voiced_sec=a.voiced_sec, n_windows=a.n_windows, n_recordings=a.n_recordings,
        created_at=a.created_at,
        biomarkers=[BiomarkerRead(code=o.code, label=o.label, value=o.value, shap_contribution=o.shap_contribution)
                    for o in a.observations],
    )


def _trend_direction(points: list[TrendPoint]) -> str:
    """Simple, explainable trend call -- not a regression fit. Compares the mean
    of the first half of the series to the mean of the second half, and requires
    the change to clear a noise floor (5% of the first-half mean, minimum 0.02)
    before calling it a direction at all. Two points is the minimum to have any
    trend; fewer is "insufficient_data" rather than a guess."""
    if len(points) < 2:
        return "insufficient_data"
    values = [p.value for p in points]
    mid = len(values) // 2
    first_half = values[:mid] or values[:1]
    second_half = values[mid:] or values[-1:]
    first_avg = sum(first_half) / len(first_half)
    second_avg = sum(second_half) / len(second_half)
    noise_floor = max(0.02, abs(first_avg) * 0.05)
    delta = second_avg - first_avg
    if abs(delta) < noise_floor:
        return "stable"
    return "increasing" if delta > 0 else "decreasing"


def build_report(patient: Patient, assessments: list[Assessment]) -> PatientReport:
    assessments = sorted(assessments, key=lambda a: a.created_at)

    # --- Per-task summaries ---
    task_summaries: dict[str, TaskSummary] = {}
    for task in ("reading", "vowel", "ddk"):
        task_assessments = [a for a in assessments if a.task == task]
        if not task_assessments:
            task_summaries[task] = TaskSummary(task=task, count=0, last_date=None)
            continue
        last = task_assessments[-1]
        task_summaries[task] = TaskSummary(
            task=task, count=len(task_assessments), last_date=last.created_at,
            latest_risk_score=last.risk_score, latest_risk_band=last.risk_band,
        )

    # --- Reading (the only risk-scored task) trend ---
    reading_assessments = [a for a in assessments if a.task == "reading" and a.risk_score is not None]
    reading_points = [TrendPoint(date=a.created_at, value=a.risk_score) for a in reading_assessments]
    reading_trend_direction = _trend_direction(reading_points) if reading_points else "insufficient_data"
    latest_reading = _to_assessment_read(reading_assessments[-1]) if reading_assessments else None

    # --- Biomarker trends across ALL tasks (any code seen >=2 times) ---
    by_code: dict[str, tuple[str, list[TrendPoint]]] = {}
    for a in assessments:
        for o in a.observations:
            label, points = by_code.get(o.code, (o.label, []))
            points.append(TrendPoint(date=a.created_at, value=o.value))
            by_code[o.code] = (label, points)
    biomarker_trends = [
        BiomarkerTrend(code=code, label=label, points=points, direction=_trend_direction(points))
        for code, (label, points) in by_code.items() if len(points) >= 2
    ]
    biomarker_trends.sort(key=lambda t: t.code)

    # --- Supporting findings from the measurement-only tasks (vowel, ddk) ---
    supporting_findings: list[str] = []
    latest_vowel = next((a for a in reversed(assessments) if a.task == "vowel"), None)
    if latest_vowel:
        vals = {o.code: o.value for o in latest_vowel.observations}
        if vals.get(_VOWEL_HNR) is not None and vals[_VOWEL_HNR] < 7:
            supporting_findings.append(
                f"Sustained vowel: reduced voice clarity (harmonics-to-noise {vals[_VOWEL_HNR]:.1f} dB, "
                f"typically \u2265 7 dB) — consistent with Parkinsonian voice changes."
            )
        if vals.get(_VOWEL_JITTER) is not None and vals[_VOWEL_JITTER] > 0.03:
            supporting_findings.append(
                f"Sustained vowel: elevated pitch instability (jitter {vals[_VOWEL_JITTER]:.3f}, "
                f"typically < 0.03)."
            )
        if vals.get(_VOWEL_SHIMMER) is not None and vals[_VOWEL_SHIMMER] > 1.3:
            supporting_findings.append(
                f"Sustained vowel: elevated loudness instability (shimmer {vals[_VOWEL_SHIMMER]:.2f} dB, "
                f"typically < 1.3 dB)."
            )
    latest_ddk = next((a for a in reversed(assessments) if a.task == "ddk"), None)
    if latest_ddk:
        vals = {o.code: o.value for o in latest_ddk.observations}
        rate = vals.get(_DDK_RATE)
        regularity = vals.get(_DDK_REGULARITY)
        if rate is not None and rate < _DDK_RATE_TYPICAL_LOW:
            supporting_findings.append(
                f"/pa-ta-ka/: repetition rate below typical range ({rate:.1f}/sec, typically "
                f"\u2265 {_DDK_RATE_TYPICAL_LOW:.0f}/sec) — slowed rapid speech can accompany Parkinsonian speech."
            )
        if regularity is not None and regularity < 0.7:
            supporting_findings.append(
                f"/pa-ta-ka/: uneven rhythm (regularity {regularity:.2f}, typically \u2265 0.70)."
            )

    # --- Recommendation tier (rule-based, every branch traces to a stated measurement) ---
    if not reading_assessments:
        tier = "insufficient_data"
        text = (
            "No reading-passage screening has been completed yet -- this is the only task that "
            "produces a risk indicator. Administer the reading-passage task to generate one before "
            "this report can offer a recommendation."
        )
    else:
        latest_band = reading_assessments[-1].risk_band
        elevated_count = sum(1 for a in reading_assessments if a.risk_band == "elevated")
        if latest_band == "elevated" and (elevated_count >= 2 or reading_trend_direction == "increasing"):
            tier = "priority_referral"
            basis = (f"{elevated_count} of {len(reading_assessments)} reading assessments have scored in the "
                     f"elevated range" if elevated_count >= 2 else "the risk indicator has been trending upward")
            text = (
                f"Priority: refer to a neurologist for further evaluation. The most recent reading "
                f"screening scored in the elevated range, and {basis}."
            )
        elif latest_band == "elevated":
            tier = "monitor"
            text = (
                "The most recent reading screening scored in the elevated range on a single assessment. "
                "Recommend a follow-up screening in the next few weeks to see whether this is sustained "
                "before considering referral."
            )
        elif latest_band == "moderate" or reading_trend_direction == "increasing":
            tier = "monitor"
            text = (
                "Continue routine monitoring with a follow-up screening. The risk indicator is in the "
                "moderate range or trending upward, though not yet at a level that on its own suggests "
                "referral."
            )
        else:
            tier = "routine"
            text = (
                "No immediate action indicated by this screening. The reading-task risk indicator is in "
                "the low range and stable or improving. Continue routine monitoring per standard care."
            )
        if supporting_findings and tier in ("monitor", "routine"):
            text += " Note the supporting findings below from the sustained-vowel and /pa-ta-ka/ tasks."

    dated = [a.created_at for a in assessments]
    return PatientReport(
        patient=PatientRead(
            id=patient.id, display_id=patient.display_id, age=patient.age, sex=patient.sex,
            language=patient.language, facility=patient.facility,
            existing_pd_diagnosis=patient.existing_pd_diagnosis, on_pd_medication=patient.on_pd_medication,
            created_at=patient.created_at,
        ),
        generated_at=datetime.now(timezone.utc),
        date_range_start=min(dated) if dated else None,
        date_range_end=max(dated) if dated else None,
        total_assessments=len(assessments),
        task_summaries=[task_summaries[t] for t in ("reading", "vowel", "ddk")],
        latest_reading=latest_reading,
        reading_points=reading_points,
        reading_trend_direction=reading_trend_direction,
        biomarker_trends=biomarker_trends,
        recommendation_tier=tier,
        recommendation_text=text,
        supporting_findings=supporting_findings,
        disclaimer=DISCLAIMER,
    )
