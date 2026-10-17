"""Experimental 27-nakshatra / 9-Tara helper."""
from __future__ import annotations

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
    "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]
TARA_CYCLE = [
    ("Janma", 50), ("Sampat", 80), ("Vipat", 25), ("Kshema", 75),
    ("Pratyak", 30), ("Sadhana", 85), ("Naidhana", 20),
    ("Mitra", 70), ("Parama Mitra", 90)
]

def tara_bala(birth_nakshatra: str, event_nakshatra: str) -> dict:
    """Return Tara category and illustrative score, using 1-based count from birth star."""
    try:
        birth_index = next(i for i, n in enumerate(NAKSHATRAS) if n.casefold() == birth_nakshatra.strip().casefold())
        event_index = next(i for i, n in enumerate(NAKSHATRAS) if n.casefold() == event_nakshatra.strip().casefold())
    except StopIteration as exc:
        raise ValueError("Use a recognized English nakshatra name from the NAKSHATRAS list") from exc
    count = ((event_index - birth_index) % 27) + 1
    tara_name, illustrative_score = TARA_CYCLE[(count - 1) % 9]
    return {
        "birth_nakshatra": NAKSHATRAS[birth_index],
        "event_nakshatra": NAKSHATRAS[event_index],
        "tara_count": count,
        "tara_category": tara_name,
        "illustrative_score_0_to_100": illustrative_score,
        "experimental_only": True,
        "note": "Illustrative mapping, not a universally agreed quantitative scale and not validated for sports outcomes."
    }
