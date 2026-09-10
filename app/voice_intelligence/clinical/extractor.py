from __future__ import annotations

import re
import uuid
from .ontology import SYMPTOMS, MEDICATION_TERMS, FUNCTION_TERMS, SEVERITY_TERMS, TEMPORAL_TERMS

_NEGATIONS = ("no ", "not ", "never ", "don't ", "do not ", "doesn't ", "does not ", "cannot ", "can't ")


def _normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def _match_phrase(text: str, phrase: str):
    escaped = re.escape(phrase)
    if phrase[0].isalnum() and phrase[-1].isalnum():
        return re.search(r"\b" + escaped + r"\b", text)
    return re.search(escaped, text)


def _evidence_sentence(text: str, start: int, end: int) -> str:
    left = max(0, text.rfind('.', 0, start) + 1)
    right = text.find('.', end)
    right = len(text) if right < 0 else right
    return text[left:right].strip()[:240]


def _negated(text: str, start: int) -> bool:
    window = text[max(0, start - 28):start]
    return any(term in window for term in _NEGATIONS)


def _add(finding_list, category, concept, status, confidence, evidence=None, value=None):
    finding_list.append({
        "id": str(uuid.uuid4()),
        "category": category,
        "concept": concept,
        "value": value,
        "status": status,
        "confidence": round(max(0.0, min(1.0, confidence)), 2),
        "evidence": evidence,
        "source": "patient_speech",
    })


def extract(text: str) -> list[dict]:
    raw = text.strip()
    t = _normalise(raw)
    findings: list[dict] = []

    for concept, phrases in SYMPTOMS.items():
        for phrase in phrases:
            m = _match_phrase(t, phrase)
            if not m:
                continue
            negated = _negated(t, m.start())
            evidence = _evidence_sentence(raw, m.start(), m.end())
            _add(findings, "symptom", concept, "absent" if negated else "present", 0.92 if not negated else 0.88, evidence)
            break

    for concept, phrases in FUNCTION_TERMS.items():
        for phrase in phrases:
            m = _match_phrase(t, phrase)
            if m:
                _add(findings, "function", concept, "mentioned", 0.70, _evidence_sentence(raw, m.start(), m.end()))
                break

    for term in MEDICATION_TERMS:
        m = re.search(r"\b" + re.escape(term) + r"\b", t)
        if m:
            _add(findings, "medication", term, "mentioned", 0.94, _evidence_sentence(raw, m.start(), m.end()), value=term)
            break

    for concept, phrases in SEVERITY_TERMS.items():
        for phrase in phrases:
            m = _match_phrase(t, phrase)
            if m:
                _add(findings, "severity", concept, "reported", 0.72, _evidence_sentence(raw, m.start(), m.end()), value=concept)
                break

    for concept, phrases in TEMPORAL_TERMS.items():
        for phrase in phrases:
            m = _match_phrase(t, phrase)
            if m:
                _add(findings, "temporal_pattern", concept, "reported", 0.78, _evidence_sentence(raw, m.start(), m.end()), value=concept)
                break

    # Deduplicate by category/concept/status.
    unique = {}
    for f in findings:
        unique[(f["category"], f["concept"], f["status"])] = f
    return list(unique.values())
