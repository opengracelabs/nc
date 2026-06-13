import type { Metadata } from "next";
import Link from "next/link";
import { getGraphJourney } from "@/lib/api";

export const metadata: Metadata = {
  title: "Discovery Graph",
  description: "Neo4j-backed discovery graph for Nature & Culture."
};

function nodeClass(label: string) {
  return "graph-table-node graph-table-node-" + label.toLowerCase();
}

export default async function DiscoverGraphPage() {
  const journey = await getGraphJourney("earthrise-collection");
  const byId = new Map(journey.nodes.map((node) => [node.id, node]));

  return (
    <article className="page graph-page">
      <p className="eyebrow">Neo4j graph</p>
      <h1>Discovery graph runtime.</h1>
      <p className="lead">
        Earthrise, Yellowstone, Grand Canyon, and Great Barrier Reef are modeled as connected
        places, collections, assets, people, institutions, themes, events, expeditions, species, and
        products.
      </p>
      <div className="button-row">
        <Link className="button" href="/discover">
          Back to Discover
        </Link>
        <Link className="button secondary-button" href="/collections/earthrise">
          Open Earthrise collection
        </Link>
      </div>

      <section className="graph-runtime-grid" aria-label="Discovery graph nodes and relationships">
        <div className="graph-node-table">
          <div className="section-heading">
            <p className="eyebrow">Nodes</p>
            <h2>{journey.nodes.length} connected records</h2>
          </div>
          <div className="graph-node-list">
            {journey.nodes.map((node) => (
              <article className={nodeClass(node.label)} key={node.id}>
                <span>{node.label}</span>
                <strong>{node.name}</strong>
                <p>{node.summary}</p>
              </article>
            ))}
          </div>
        </div>

        <div className="graph-edge-table">
          <div className="section-heading">
            <p className="eyebrow">Relationships</p>
            <h2>{journey.relationships.length} traversable edges</h2>
          </div>
          <div className="graph-edge-list">
            {journey.relationships.map((relationship) => {
              const source = byId.get(relationship.source);
              const target = byId.get(relationship.target);
              return (
                <article className="graph-edge-row" key={relationship.source + relationship.type + relationship.target}>
                  <span>{relationship.type}</span>
                  <strong>
                    {source?.name ?? relationship.source}{" -> "}{target?.name ?? relationship.target}
                  </strong>
                  <p>{relationship.reason}</p>
                </article>
              );
            })}
          </div>
        </div>
      </section>
    </article>
  );
}
