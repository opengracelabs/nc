from workers.rijksmuseum_adapter.config import settings


def test_rijksmuseum_settings_defaults() -> None:
    assert settings.rijksmuseum_search_base_url == "https://data.rijksmuseum.nl/search/collection"
    assert settings.rijksmuseum_oai_base_url == "https://data.rijksmuseum.nl/oai"
    assert settings.rijksmuseum_iiif_image_base_url == "https://iiif.micr.io"
    assert settings.rijksmuseum_change_discovery_url == "https://data.rijksmuseum.nl/cd/collection.json"
    assert settings.rijksmuseum_dry_run is True
