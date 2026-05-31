import re
from typing import Any

from .sources.base import RawRecord


def _strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text).strip()


def _parse_criteria(raw: str) -> list[str]:
    """'(i)(ii)(vii)' → ['i', 'ii', 'vii']"""
    return re.findall(r"\(([ivx]+)\)", raw.lower())


def _sparql_value(binding: dict, key: str) -> str | None:
    node = binding.get(key)
    return node["value"] if node else None


def normalize_unesco_whc(record: RawRecord) -> dict[str, Any]:
    p = record.payload
    
    # UNESCO API sometimes provides multiple languages in separate fields or nested structures
    # For now, we capture 'site' (EN) and look for 'site_fr' or similar if available
    name_en = (p.get("site") or "").strip()
    name_fr = (p.get("site_fr") or "").strip()
    
    out: dict[str, Any] = {
        "source": "unesco_whc",
        "source_id": record.source_id,
        "unesco_ref_id": str(p["id_number"]) if p.get("id_number") is not None else None,
        "wikidata_qid": None,
        "name": {},
        "description": {},
        "statement_of_ouv": {},
        "justification": {},
        "country_codes": [],
        "heritage_type": None,
        "ouv_criteria": [],
        "inscription_year": None,
        "centroid": None,
        "boundary": None,
        "transboundary": False,
        "core_area_ha": None,
        "buffer_area_ha": None,
        "spatial_precision": None,
    }

    if name_en:
        out["name"]["en"] = name_en
    if name_fr:
        out["name"]["fr"] = name_fr

    if desc_en := p.get("short_description"):
        out["description"]["en"] = _strip_html(desc_en)
    if desc_fr := p.get("short_description_fr"):
        out["description"]["fr"] = _strip_html(desc_fr)

    # Capture OUV and Justification if available in the summary payload
    if ouv_en := p.get("ouv_statement"):
        out["statement_of_ouv"]["en"] = _strip_html(ouv_en)
    
    if justification_en := p.get("justification"):
        out["justification"]["en"] = _strip_html(justification_en)

    if criteria_txt := p.get("criteria_txt"):
        out["ouv_criteria"] = _parse_criteria(criteria_txt)

    if date := p.get("date_inscribed"):
        try:
            out["inscription_year"] = int(str(date)[:4])
        except (ValueError, TypeError):
            pass

    category = str(p.get("category", "")).lower()
    if "mixed" in category or ("cultural" in category and "natural" in category):
        out["heritage_type"] = "mixed"
    elif "natural" in category:
        out["heritage_type"] = "natural"
    elif "cultural" in category:
        out["heritage_type"] = "cultural"

    lat = p.get("latitude")
    lon = p.get("longitude")
    if lat is not None and lon is not None:
        try:
            out["centroid"] = {
                "type": "Point",
                "coordinates": [float(lon), float(lat)],
            }
        except (ValueError, TypeError):
            pass

    if states := p.get("states", []):
        out["country_codes"] = [s.get("iso_code", "").upper() for s in states if s.get("iso_code")]
        if len(out["country_codes"]) > 1:
            out["transboundary"] = True

    # Capture area metrics if provided in the API payload
    # Note: API field names vary; these are placeholders for common UNESCO patterns
    if core_area := p.get("area_core"):
        try:
            out["core_area_ha"] = float(core_area)
        except (ValueError, TypeError):
            pass
    
    if buffer_area := p.get("area_buffer"):
        try:
            out["buffer_area_ha"] = float(buffer_area)
        except (ValueError, TypeError):
            pass

    return out


def normalize_wikidata(record: RawRecord) -> dict[str, Any]:
    b = record.payload
    qid = record.source_id

    out: dict[str, Any] = {
        "source": "wikidata",
        "source_id": qid,
        "wikidata_qid": qid,
        "name": {},
        "description": {},
        "country_codes": [],
        "heritage_type": None,
        "ouv_criteria": [],
        "inscription_year": None,
        "centroid": None,
        "boundary": None,
    }

    if label := _sparql_value(b, "siteLabel"):
        out["name"]["en"] = label

    if whc_id := _sparql_value(b, "whc_id"):
        out["external_ids"] = {"whc_id": whc_id}

    if code := _sparql_value(b, "countryCode"):
        out["country_codes"] = [code.upper()]

    lat = _sparql_value(b, "lat")
    lon = _sparql_value(b, "lon")
    if lat and lon:
        try:
            out["centroid"] = {
                "type": "Point",
                "coordinates": [float(lon), float(lat)],
            }
        except (ValueError, TypeError):
            pass

    if year := _sparql_value(b, "inscriptionYear"):
        try:
            out["inscription_year"] = int(year)
        except (ValueError, TypeError):
            pass

    return out


_NORMALIZERS = {
    "unesco_whc": normalize_unesco_whc,
    "wikidata": normalize_wikidata,
}


def normalize(source: str, record: RawRecord) -> dict[str, Any]:
    fn = _NORMALIZERS.get(source)
    if fn is None:
        raise ValueError(f"No normalizer for source: {source}")
    return fn(record)
