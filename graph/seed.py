from __future__ import annotations

from typing import Literal, TypedDict

NodeLabel = Literal[
    "Place",
    "Collection",
    "Product",
    "Asset",
    "Species",
    "Person",
    "Institution",
    "Theme",
    "Event",
    "Expedition",
]

RelationshipType = Literal[
    "RELATED_TO",
    "PART_OF",
    "LOCATED_IN",
    "DISCOVERED_BY",
    "EXPLORED_BY",
    "ILLUSTRATED_BY",
    "INSPIRED",
    "FEATURES",
    "RECOMMENDS",
]


class GraphNode(TypedDict):
    id: str
    slug: str
    label: NodeLabel
    name: str
    summary: str
    status: str


class GraphRelationship(TypedDict):
    source: str
    target: str
    type: RelationshipType
    reason: str
    weight: float


NODES: list[GraphNode] = [
    {"id": "place:earthrise", "slug": "earthrise", "label": "Place", "name": "Earthrise", "summary": "Apollo 8 lunar-orbit viewpoint where Earth became the subject of exploration.", "status": "live"},
    {"id": "place:yellowstone", "slug": "yellowstone", "label": "Place", "name": "Yellowstone", "summary": "National park landscape connecting expedition art, geology, wildlife, and preservation.", "status": "coming_soon"},
    {"id": "place:grand-canyon", "slug": "grand-canyon", "label": "Place", "name": "Grand Canyon", "summary": "Deep-time landscape of survey cartography, geology, and public-domain visual records.", "status": "coming_soon"},
    {"id": "place:great-barrier-reef", "slug": "great-barrier-reef", "label": "Place", "name": "Great Barrier Reef", "summary": "Marine ecosystem connecting coral, navigation, biodiversity, and conservation evidence.", "status": "coming_soon"},
    {"id": "collection:earthrise", "slug": "earthrise-collection", "label": "Collection", "name": "Earthrise: The Oasis Collection", "summary": "A source-traceable collection around NASA AS08-14-2383 and the overview effect.", "status": "live"},
    {"id": "collection:yellowstone", "slug": "yellowstone-collection", "label": "Collection", "name": "Yellowstone Discovery Collection", "summary": "A reserved journey through park-making, survey images, and expedition art.", "status": "coming_soon"},
    {"id": "collection:grand-canyon", "slug": "grand-canyon-collection", "label": "Collection", "name": "Grand Canyon Deep Time Collection", "summary": "A reserved journey through geologic time, survey maps, and canyon imagery.", "status": "coming_soon"},
    {"id": "collection:great-barrier-reef", "slug": "great-barrier-reef-collection", "label": "Collection", "name": "Great Barrier Reef Living Reef Collection", "summary": "A reserved journey through coral systems, marine species, and reef evidence.", "status": "coming_soon"},
    {"id": "product:earthrise-print", "slug": "earthrise-museum-print", "label": "Product", "name": "Earthrise Museum Giclee", "summary": "Museum-grade print derived from the Apollo 8 Earthrise source image.", "status": "live"},
    {"id": "product:earthrise-digital", "slug": "earthrise-digital-edition", "label": "Product", "name": "Earthrise Digital Download", "summary": "High-resolution digital edition for study, reference, and display.", "status": "live"},
    {"id": "asset:earthrise-as08-14-2383", "slug": "as08-14-2383", "label": "Asset", "name": "NASA AS08-14-2383", "summary": "The Apollo 8 Earthrise frame photographed by William Anders on December 24, 1968.", "status": "live"},
    {"id": "asset:yellowstone-survey", "slug": "yellowstone-survey-record", "label": "Asset", "name": "Yellowstone Survey Record", "summary": "Reserved survey-era visual record for the Yellowstone journey.", "status": "coming_soon"},
    {"id": "asset:grand-canyon-map", "slug": "grand-canyon-map-record", "label": "Asset", "name": "Grand Canyon Survey Map", "summary": "Reserved geological cartography anchor for the Grand Canyon journey.", "status": "coming_soon"},
    {"id": "asset:reef-coral-record", "slug": "reef-coral-record", "label": "Asset", "name": "Great Barrier Reef Coral Record", "summary": "Reserved marine evidence anchor for reef biodiversity journeys.", "status": "coming_soon"},
    {"id": "species:bison", "slug": "american-bison", "label": "Species", "name": "American Bison", "summary": "Keystone Yellowstone species for conservation and place identity journeys.", "status": "evidence"},
    {"id": "species:grizzly", "slug": "grizzly-bear", "label": "Species", "name": "Grizzly Bear", "summary": "Yellowstone predator species connecting ecology, place, and public imagination.", "status": "evidence"},
    {"id": "species:coral", "slug": "reef-building-coral", "label": "Species", "name": "Reef-building Coral", "summary": "Marine life foundation for the Great Barrier Reef discovery path.", "status": "evidence"},
    {"id": "person:william-anders", "slug": "william-anders", "label": "Person", "name": "William Anders", "summary": "Apollo 8 astronaut who photographed Earthrise.", "status": "source_credit"},
    {"id": "person:thomas-moran", "slug": "thomas-moran", "label": "Person", "name": "Thomas Moran", "summary": "Artist associated with Yellowstone's visual preservation history.", "status": "reserved"},
    {"id": "person:john-wesley-powell", "slug": "john-wesley-powell", "label": "Person", "name": "John Wesley Powell", "summary": "Explorer associated with Grand Canyon expedition history.", "status": "reserved"},
    {"id": "institution:nasa", "slug": "nasa", "label": "Institution", "name": "NASA", "summary": "Source institution for Apollo 8 Earthrise public-domain material.", "status": "active"},
    {"id": "institution:usgs", "slug": "usgs", "label": "Institution", "name": "United States Geological Survey", "summary": "Survey authority for western landscape and geologic records.", "status": "reserved"},
    {"id": "institution:aims", "slug": "aims", "label": "Institution", "name": "Australian Institute of Marine Science", "summary": "Reef science reference institution for marine evidence paths.", "status": "reserved"},
    {"id": "theme:overview-effect", "slug": "overview-effect", "label": "Theme", "name": "Overview Effect", "summary": "Planetary awareness created by seeing Earth from space.", "status": "active"},
    {"id": "theme:preservation", "slug": "preservation", "label": "Theme", "name": "Preservation", "summary": "The cultural and ecological argument for protecting places.", "status": "active"},
    {"id": "theme:biodiversity", "slug": "biodiversity", "label": "Theme", "name": "Biodiversity", "summary": "Species, habitat, and ecosystem evidence that enrich place journeys.", "status": "active"},
    {"id": "event:apollo-8", "slug": "apollo-8", "label": "Event", "name": "Apollo 8", "summary": "1968 lunar-orbit mission that produced Earthrise.", "status": "active"},
    {"id": "event:yellowstone-1872", "slug": "yellowstone-1872", "label": "Event", "name": "Yellowstone National Park Established", "summary": "The 1872 legal creation of Yellowstone as a national park.", "status": "reserved"},
    {"id": "expedition:apollo-8", "slug": "apollo-8-expedition", "label": "Expedition", "name": "Apollo 8 Lunar Mission", "summary": "First crewed mission to orbit the Moon.", "status": "active"},
    {"id": "expedition:hayden-survey", "slug": "hayden-survey", "label": "Expedition", "name": "Hayden Geological Survey", "summary": "Survey expedition central to Yellowstone's preservation story.", "status": "reserved"},
    {"id": "expedition:powell-expedition", "slug": "powell-expedition", "label": "Expedition", "name": "Powell Colorado River Expedition", "summary": "Grand Canyon exploration route associated with John Wesley Powell.", "status": "reserved"},
]

RELATIONSHIPS: list[GraphRelationship] = [
    {"source": "collection:earthrise", "target": "asset:earthrise-as08-14-2383", "type": "FEATURES", "reason": "The source image anchors the live collection.", "weight": 1.0},
    {"source": "asset:earthrise-as08-14-2383", "target": "institution:nasa", "type": "PART_OF", "reason": "NASA is the source institution for the asset.", "weight": 1.0},
    {"source": "asset:earthrise-as08-14-2383", "target": "person:william-anders", "type": "DISCOVERED_BY", "reason": "William Anders photographed the Earthrise frame during Apollo 8.", "weight": 0.95},
    {"source": "asset:earthrise-as08-14-2383", "target": "person:william-anders", "type": "ILLUSTRATED_BY", "reason": "The public artifact is credited to Anders as image-maker.", "weight": 0.9},
    {"source": "asset:earthrise-as08-14-2383", "target": "place:earthrise", "type": "LOCATED_IN", "reason": "The viewpoint is Apollo 8 lunar orbit.", "weight": 1.0},
    {"source": "asset:earthrise-as08-14-2383", "target": "event:apollo-8", "type": "PART_OF", "reason": "The image was made during Apollo 8.", "weight": 1.0},
    {"source": "event:apollo-8", "target": "expedition:apollo-8", "type": "PART_OF", "reason": "Apollo 8 is modeled as both event and expedition journey.", "weight": 0.9},
    {"source": "expedition:apollo-8", "target": "place:earthrise", "type": "EXPLORED_BY", "reason": "The mission explored lunar orbit as a human viewpoint.", "weight": 0.8},
    {"source": "collection:earthrise", "target": "product:earthrise-print", "type": "RECOMMENDS", "reason": "The museum print is the primary live edition.", "weight": 0.92},
    {"source": "collection:earthrise", "target": "product:earthrise-digital", "type": "RECOMMENDS", "reason": "The digital edition supports study and close viewing.", "weight": 0.84},
    {"source": "product:earthrise-print", "target": "asset:earthrise-as08-14-2383", "type": "PART_OF", "reason": "The product derives from the source asset.", "weight": 1.0},
    {"source": "product:earthrise-digital", "target": "asset:earthrise-as08-14-2383", "type": "PART_OF", "reason": "The product derives from the source asset.", "weight": 1.0},
    {"source": "collection:earthrise", "target": "theme:overview-effect", "type": "INSPIRED", "reason": "Earthrise is a canonical overview-effect artifact.", "weight": 1.0},
    {"source": "theme:overview-effect", "target": "theme:preservation", "type": "RELATED_TO", "reason": "Planetary awareness connects to preservation.", "weight": 0.75},
    {"source": "collection:earthrise", "target": "collection:great-barrier-reef", "type": "RECOMMENDS", "reason": "Continue from planetary awareness to marine planetary systems.", "weight": 0.68},
    {"source": "collection:earthrise", "target": "collection:yellowstone", "type": "RECOMMENDS", "reason": "Continue from planetary stewardship to preservation landscapes.", "weight": 0.64},
    {"source": "collection:yellowstone", "target": "place:yellowstone", "type": "LOCATED_IN", "reason": "The collection is anchored at Yellowstone.", "weight": 1.0},
    {"source": "collection:yellowstone", "target": "asset:yellowstone-survey", "type": "FEATURES", "reason": "Survey record anchors the reserved journey.", "weight": 0.8},
    {"source": "asset:yellowstone-survey", "target": "person:thomas-moran", "type": "ILLUSTRATED_BY", "reason": "Moran is the priority artist relationship for Yellowstone.", "weight": 0.7},
    {"source": "person:thomas-moran", "target": "expedition:hayden-survey", "type": "EXPLORED_BY", "reason": "Moran's Yellowstone story is tied to survey exploration.", "weight": 0.8},
    {"source": "expedition:hayden-survey", "target": "place:yellowstone", "type": "EXPLORED_BY", "reason": "The Hayden Survey explored Yellowstone.", "weight": 1.0},
    {"source": "place:yellowstone", "target": "species:bison", "type": "FEATURES", "reason": "Bison are a Yellowstone keystone species.", "weight": 0.86},
    {"source": "place:yellowstone", "target": "species:grizzly", "type": "FEATURES", "reason": "Grizzly bears are a Yellowstone ecology signal.", "weight": 0.78},
    {"source": "place:yellowstone", "target": "theme:preservation", "type": "INSPIRED", "reason": "Yellowstone anchors the public preservation story.", "weight": 0.94},
    {"source": "event:yellowstone-1872", "target": "place:yellowstone", "type": "LOCATED_IN", "reason": "The establishment event belongs to Yellowstone.", "weight": 1.0},
    {"source": "collection:grand-canyon", "target": "place:grand-canyon", "type": "LOCATED_IN", "reason": "The collection is anchored at Grand Canyon.", "weight": 1.0},
    {"source": "collection:grand-canyon", "target": "asset:grand-canyon-map", "type": "FEATURES", "reason": "The survey map anchors the deep-time journey.", "weight": 0.82},
    {"source": "asset:grand-canyon-map", "target": "institution:usgs", "type": "PART_OF", "reason": "USGS is the survey authority for the record path.", "weight": 0.82},
    {"source": "person:john-wesley-powell", "target": "expedition:powell-expedition", "type": "EXPLORED_BY", "reason": "Powell anchors the Grand Canyon exploration journey.", "weight": 0.88},
    {"source": "expedition:powell-expedition", "target": "place:grand-canyon", "type": "EXPLORED_BY", "reason": "The expedition route passes through the canyon.", "weight": 0.95},
    {"source": "place:grand-canyon", "target": "theme:preservation", "type": "INSPIRED", "reason": "Grand Canyon continues the western preservation arc.", "weight": 0.82},
    {"source": "place:yellowstone", "target": "place:grand-canyon", "type": "RELATED_TO", "reason": "Both places share survey-era western landscape history.", "weight": 0.74},
    {"source": "collection:great-barrier-reef", "target": "place:great-barrier-reef", "type": "LOCATED_IN", "reason": "The collection is anchored at the reef.", "weight": 1.0},
    {"source": "collection:great-barrier-reef", "target": "asset:reef-coral-record", "type": "FEATURES", "reason": "The coral record anchors the marine journey.", "weight": 0.84},
    {"source": "asset:reef-coral-record", "target": "institution:aims", "type": "PART_OF", "reason": "AIMS is modeled as the marine science reference institution.", "weight": 0.72},
    {"source": "place:great-barrier-reef", "target": "species:coral", "type": "FEATURES", "reason": "Reef-building coral is the ecosystem foundation.", "weight": 0.96},
    {"source": "species:coral", "target": "theme:biodiversity", "type": "PART_OF", "reason": "Coral evidence belongs to biodiversity discovery.", "weight": 0.9},
    {"source": "collection:great-barrier-reef", "target": "theme:biodiversity", "type": "INSPIRED", "reason": "The reef journey is organized around biodiversity.", "weight": 0.88},
    {"source": "place:great-barrier-reef", "target": "place:earthrise", "type": "RELATED_TO", "reason": "The reef extends the planetary stewardship thread opened by Earthrise.", "weight": 0.66},
]

NODE_BY_ID = {node["id"]: node for node in NODES}
NODE_BY_SLUG = {node["slug"]: node for node in NODES}


def node_by_slug(slug: str) -> GraphNode | None:
    return NODE_BY_SLUG.get(slug)


def relationships_for(node_id: str) -> list[GraphRelationship]:
    return [rel for rel in RELATIONSHIPS if rel["source"] == node_id or rel["target"] == node_id]


def recommendations_for(slug: str) -> list[dict]:
    node = node_by_slug(slug)
    if not node:
        return []
    recommendations = []
    for rel in RELATIONSHIPS:
        if rel["source"] != node["id"] or rel["type"] != "RECOMMENDS":
            continue
        target = NODE_BY_ID[rel["target"]]
        recommendations.append({"node": target, "relationship": rel})
    return sorted(recommendations, key=lambda item: item["relationship"]["weight"], reverse=True)


def journey_for(slug: str, depth: int = 2) -> dict:
    start = node_by_slug(slug)
    if not start:
        return {"nodes": [], "relationships": []}

    seen_nodes = {start["id"]}
    frontier = {start["id"]}
    selected_relationships: list[GraphRelationship] = []

    for _ in range(depth):
        next_frontier: set[str] = set()
        for rel in RELATIONSHIPS:
            if rel["source"] in frontier or rel["target"] in frontier:
                selected_relationships.append(rel)
                if rel["source"] not in seen_nodes:
                    next_frontier.add(rel["source"])
                if rel["target"] not in seen_nodes:
                    next_frontier.add(rel["target"])
        seen_nodes.update(next_frontier)
        frontier = next_frontier
        if not frontier:
            break

    deduped_relationships = []
    seen_edges = set()
    for rel in selected_relationships:
        edge_key = (rel["source"], rel["target"], rel["type"])
        if edge_key not in seen_edges:
            deduped_relationships.append(rel)
            seen_edges.add(edge_key)

    return {
        "nodes": [node for node in NODES if node["id"] in seen_nodes],
        "relationships": deduped_relationships,
    }
