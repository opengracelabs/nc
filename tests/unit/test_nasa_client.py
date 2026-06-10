import pytest

from workers.nasa_adapter.client import (
    build_asset_url,
    build_metadata_url,
    build_search_params,
    build_search_url,
    choose_asset_url,
    extract_asset_urls,
    reject_api_nasa_url,
)


def test_nasa_client_uses_images_api_only() -> None:
    assert build_search_url() == "https://images-api.nasa.gov/search"
    assert build_asset_url("abc") == "https://images-api.nasa.gov/asset/abc"
    assert build_metadata_url("abc") == "https://images-api.nasa.gov/metadata/abc"
    with pytest.raises(ValueError, match="api_nasa_gov_excluded"):
        reject_api_nasa_url("https://api.nasa.gov/planetary/apod")


def test_nasa_search_params_are_deterministic_and_image_scoped() -> None:
    assert build_search_params(query="apollo", page=2, page_size=5) == {
        "media_type": "image",
        "page": "2",
        "page_size": "5",
        "q": "apollo",
    }


def test_nasa_asset_resolution_uses_manifest_urls_without_pattern_construction() -> None:
    manifest = {
        "collection": {
            "items": [
                {"href": "https://images-assets.nasa.gov/image/x/x~large.jpg"},
                {"href": "https://images-assets.nasa.gov/image/x/x~orig.jpg"},
            ]
        }
    }
    urls = extract_asset_urls(manifest)

    assert choose_asset_url(urls) == "https://images-assets.nasa.gov/image/x/x~orig.jpg"


def test_nasa_asset_manifest_urls_are_normalized_to_https() -> None:
    manifest = {
        "collection": {
            "items": [
                {"href": "http://images-assets.nasa.gov/image/x/x~orig.jpg"},
            ]
        }
    }

    assert extract_asset_urls(manifest) == [
        "https://images-assets.nasa.gov/image/x/x~orig.jpg"
    ]
