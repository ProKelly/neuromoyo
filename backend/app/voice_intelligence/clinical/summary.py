from __future__ import annotations


def build_summary(findings: list[dict], neuro_signal: dict | None) -> str:
    present = [f["concept"] for f in findings if f["status"] == "present"]
    mentioned = [f["concept"] for f in findings if f["status"] in {"mentioned", "reported"}]

    parts = []
    if present:
        parts.append("Patient-reported speech or neurological symptoms include " + ", ".join(present[:4]) + ".")
    if mentioned:
        parts.append("Additional context mentioned during speech includes " + ", ".join(mentioned[:4]) + ".")
    if neuro_signal:
        band = neuro_signal.get("risk_band")
        if band:
            parts.append(f"The separate neurological voice screen produced a {band} screening signal.")
    if not parts:
        parts.append("No predefined clinical findings were confidently extracted from the recorded speech.")

    parts.append("These findings are decision-support evidence only and require clinical interpretation; they do not establish a diagnosis.")
    return " ".join(parts)
