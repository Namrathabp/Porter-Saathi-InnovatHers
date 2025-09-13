def rule_based_reply(query: str) -> str:
    q = query.lower()
    if "kamaya" in q or "earning" in q:
        return "Aaj aapne 1200 rupaye kharche kaat ke kamaye. 🚚"
    elif "penalty" in q:
        return "Penalty isliye lagi kyunki delivery 30 minute late hui thi."
    elif "business" in q or "behtar" in q:
        return "Aapka vyapar pichle hafte se 15% behtar hai. 👍"
    elif "help" in q or "sahayata" in q:
        return "Emergency ke liye 1 dabaiye, aur turant call connect hoga."
    else:
        return "Maaf kijiye, main aapka prashn samajh nahi paaya. Kripya phir se koshish kijiye."
