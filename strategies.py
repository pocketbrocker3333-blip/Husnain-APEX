def build_signal_reason_breakdown(reasons_list, deep_scan_msg, accuracy):
    """
    Husnain APEX PRO - Signal Reason & Confluence Card Formatter
    Generates structured breakdown for UI display.
    """
    breakdown_data = {
        "accuracy_score": f"{accuracy}%",
        "confluence_items": [],
        "deep_scan_status": deep_scan_msg
    }

    # Add each indicator check result with neon checkmark
    for reason in reasons_list:
        breakdown_data["confluence_items"].append({
            "status": "PASS",
            "text": reason
        })

    # Append 8-Min Deep Scan Result
    breakdown_data["confluence_items"].append({
        "status": "PASS" if "🟢" in deep_scan_msg or "🔴" in deep_scan_msg else "WARN",
        "text": deep_scan_msg
    })

    return breakdown_data