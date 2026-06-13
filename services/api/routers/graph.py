from fastapi import APIRouter, HTTPException, Query

from ..graph_runtime import (
    get_graph_journey,
    get_graph_place,
    get_graph_recommendations,
    get_graph_related,
)

router = APIRouter(prefix="/graph", tags=["graph"])

DEFAULT_GRAPH_SLUG = "earthrise-collection"


def _required(result: dict | None, detail: str) -> dict:
    if result is None:
        raise HTTPException(status_code=404, detail=detail)
    return result


@router.get("/recommendations")
def graph_recommendations(slug: str = Query(DEFAULT_GRAPH_SLUG, min_length=1)) -> dict:
    return _required(get_graph_recommendations(slug), "Graph subject not found")


@router.get("/journey")
def graph_journey(slug: str = Query(DEFAULT_GRAPH_SLUG, min_length=1)) -> dict:
    return _required(get_graph_journey(slug), "Graph journey not found")


@router.get("/related")
def graph_related(slug: str = Query(DEFAULT_GRAPH_SLUG, min_length=1)) -> dict:
    return _required(get_graph_related(slug), "Graph related subject not found")


@router.get("/place/{slug}")
def graph_place(slug: str) -> dict:
    return _required(get_graph_place(slug), "Graph place not found")


@router.get("/recommendations/{slug}")
def graph_recommendations_by_slug(slug: str) -> dict:
    return graph_recommendations(slug)


@router.get("/journey/{slug}")
def graph_journey_by_slug(slug: str) -> dict:
    return graph_journey(slug)


@router.get("/related/{slug}")
def graph_related_by_slug(slug: str) -> dict:
    return graph_related(slug)
