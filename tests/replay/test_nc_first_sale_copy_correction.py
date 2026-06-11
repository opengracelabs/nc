"""NC-FIRST-SALE copy correction replay tests."""
from pathlib import Path

CAMPAIGN = Path("docs/implementation/nc_first_sale_campaign_package.md")
PLAYBOOK = Path("docs/implementation/nc_first_sale_playbook.md")
CATALOG = Path("data/exports/first_commercial_catalog.md")
COA_TEMPLATE = Path("docs/governance/NC-FIRST-SALE_COA_template.md")
PRODUCTION_PACKAGE_SQL = Path(
    "infrastructure/postgres/init/42_nc_first_sale_production_package.sql"
)

FIRST_SALE_COPY_SURFACES = (CAMPAIGN, PLAYBOOK, COA_TEMPLATE)
FORBIDDEN_FIRST_SALE_COPY = (
    "Verified by NASA",
    "Sourced from NARA",
    "NASA / NARA",
    "National Archives",
    "NARA",
)
NASA_ATTRIBUTION = "Image credit: NASA."
NASA_NONENDORSEMENT = "Image credit: NASA. NASA does not endorse this product."
NASA_SOURCE_RECORD = "AS08-14-2383"
NASA_SOURCE_LANGUAGE = "NASA public-domain"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_first_sale_copy_surfaces_exist() -> None:
    for path in FIRST_SALE_COPY_SURFACES:
        assert path.exists(), path


def test_first_sale_copy_removes_nara_and_verification_claims() -> None:
    for path in FIRST_SALE_COPY_SURFACES:
        text = _read(path)
        for forbidden in FORBIDDEN_FIRST_SALE_COPY:
            assert forbidden not in text, f"{forbidden!r} remained in {path}"


def test_first_sale_copy_inserts_nasa_attribution_and_nonendorsement() -> None:
    campaign = _read(CAMPAIGN)
    playbook = _read(PLAYBOOK)

    for text in (campaign, playbook):
        assert NASA_ATTRIBUTION in text
        assert NASA_NONENDORSEMENT in text
        assert NASA_SOURCE_LANGUAGE in text

    assert f"NASA Image and Video Library record {NASA_SOURCE_RECORD}" in campaign
    assert f"NASA public-domain source record {NASA_SOURCE_RECORD}" in playbook


def test_first_sale_catalog_earthrise_copy_has_required_nasa_language() -> None:
    catalog = _read(CATALOG)
    earthrise_section = catalog.split("## 2. Yellowstone", maxsplit=1)[0]

    assert "Earthrise: The Master Restoration" in earthrise_section
    assert NASA_ATTRIBUTION in earthrise_section
    assert NASA_NONENDORSEMENT in earthrise_section
    for forbidden in ("Verified by NASA", "Sourced from NARA", "NASA / NARA"):
        assert forbidden not in earthrise_section


def test_coa_template_contains_required_first_sale_fields() -> None:
    text = _read(COA_TEMPLATE)

    assert "NC-PROD-001" in text
    assert "NASA AS08-14-2383" in text
    assert "17 U.S.C. § 105" in text
    assert NASA_ATTRIBUTION in text
    assert NASA_NONENDORSEMENT in text
    assert "Source: NASA Image and Video Library" in text
    assert "Curator:" in text
    assert "Principal Architect:" in text


def test_production_package_attribution_manifest_uses_nasa_nonendorsement() -> None:
    sql = _read(PRODUCTION_PACKAGE_SQL)

    assert "attribution_manifest" in sql
    assert "disclaimer_manifest" in sql
    assert NASA_NONENDORSEMENT in sql
    assert "United States government work; no NASA endorsement." in sql
    for forbidden in ("Verified by NASA", "Sourced from NARA", "NASA / NARA"):
        assert forbidden not in sql
