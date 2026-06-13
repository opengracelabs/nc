import type { Metadata } from "next";
import Link from "next/link";
import {
  collectionGraph,
  discoveryPlaces,
  featuredRecommendation,
  relatedJourneys
} from "@/lib/discovery";

export const metadata: Metadata = {
  title: "Discover",
  description: "Place-led discovery journeys from Nature & Culture."
};

export default function DiscoverPage() {
  const livePlace = discoveryPlaces[0];

  return (
    <article className="discover-page">
      <section className="section discover-journey-hero">
        <div className="discover-hero-copy">
          <p className="eyebrow">Discover</p>
          <h1>Start with a journey, then follow the relationships.</h1>
          <p className="lead">
            Browse public-domain nature and culture by place, story, collection, and edition. The
            first screen behaves like a travel map, a museum trail, and a playlist of connected
            records.
          </p>
          <div className="button-row">
            <Link className="button" href={featuredRecommendation.href}>
              Start with Earthrise
            </Link>
            <Link className="button secondary-button" href="/discover/graph">
              View graph
            </Link>
          </div>
        </div>

        <div className="discovery-map-panel" aria-label="Featured discovery places">
          <div className="discovery-map">
            {discoveryPlaces.map((place) => (
              <Link
                aria-label={place.title + " discovery marker"}
                className={"map-marker " + (place.status === "Live" ? "is-live" : "")}
                href={place.status === "Live" ? "/collections/earthrise" : "#nearby-places"}
                key={place.slug}
                style={{ left: `${place.mapPosition.x}%`, top: `${place.mapPosition.y}%` }}
              >
                <span>{place.title}</span>
              </Link>
            ))}
          </div>
          <div className="map-panel-caption">
            <strong>{livePlace.title}</strong>
            <span>{livePlace.summary}</span>
          </div>
        </div>
      </section>

      <section className="section discovery-workbench">
        <aside className="recommendation-panel" aria-labelledby="recommendation-title">
          <img src={featuredRecommendation.imageSrc} alt={featuredRecommendation.imageAlt} />
          <div>
            <p className="eyebrow">{featuredRecommendation.eyebrow}</p>
            <h2 id="recommendation-title">{featuredRecommendation.title}</h2>
            <p>{featuredRecommendation.summary}</p>
            <ul>
              {featuredRecommendation.reasons.map((reason) => (
                <li key={reason}>{reason}</li>
              ))}
            </ul>
            <Link className="text-link" href={featuredRecommendation.href}>
              Open recommendation
            </Link>
          </div>
        </aside>

        <div className="journey-stack">
          <div className="section-heading">
            <p className="eyebrow">Related journeys</p>
            <h2>Continue from the record in three directions.</h2>
          </div>
          <div className="related-journey-list">
            {relatedJourneys.map((journey) => (
              <Link className="journey-row" href={journey.href} key={journey.title}>
                <span>{journey.eyebrow}</span>
                <strong>{journey.title}</strong>
                <em>{journey.summary}</em>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="section nearby-places-section" id="nearby-places">
        <div className="section-heading wide-heading">
          <p className="eyebrow">Nearby places</p>
          <h2>Place discovery should feel spatial before it feels technical.</h2>
          <p className="lead">
            Nearby means physical proximity, shared bioregion, or expedition continuity depending on
            the journey.
          </p>
        </div>
        <div className="nearby-place-grid">
          {discoveryPlaces.map((place) => (
            <article className="nearby-place-card" key={place.slug}>
              <div>
                <span className="masterwork-badge">{place.status}</span>
                <h3>{place.title}</h3>
                <p>{place.region}</p>
              </div>
              <dl>
                <div>
                  <dt>Category</dt>
                  <dd>{place.category}</dd>
                </div>
                <div>
                  <dt>Works</dt>
                  <dd>{place.works}</dd>
                </div>
                <div>
                  <dt>Journeys</dt>
                  <dd>{place.journeys}</dd>
                </div>
              </dl>
              <ul>
                {place.nearby.map((nearby) => (
                  <li key={nearby.title}>
                    <strong>{nearby.title}</strong>
                    <span>
                      {nearby.distance} - {nearby.reason}
                    </span>
                  </li>
                ))}
              </ul>
            </article>
          ))}
        </div>
      </section>

      <section className="section collection-graph-section" id="collection-graph">
        <div className="section-heading wide-heading">
          <p className="eyebrow">Collection graph</p>
          <h2>The collection is the hub, not the endpoint.</h2>
          <p className="lead">
            Earthrise connects source record, story, place, and editions. Future graph traversal
            should preserve this user-facing shape.
          </p>
        </div>
        <div className="collection-graph" aria-label="Earthrise collection graph">
          {collectionGraph.edges.map((edge) => {
            const from = collectionGraph.nodes.find((node) => node.id === edge.from);
            const to = collectionGraph.nodes.find((node) => node.id === edge.to);
            if (!from || !to) {
              return null;
            }
            const x1 = from.x;
            const y1 = from.y;
            const x2 = to.x;
            const y2 = to.y;
            const length = Math.hypot(x2 - x1, y2 - y1);
            const angle = (Math.atan2(y2 - y1, x2 - x1) * 180) / Math.PI;
            return (
              <span
                aria-hidden="true"
                className="graph-edge"
                key={edge.from + edge.to}
                style={{
                  left: `${x1}%`,
                  top: `${y1}%`,
                  width: `${length}%`,
                  transform: `rotate(${angle}deg)`
                }}
              />
            );
          })}
          {collectionGraph.nodes.map((node) => (
            <Link
              className={"graph-node graph-node-" + node.type}
              href={node.type === "edition" ? "/products/earthrise" : "/collections/earthrise"}
              key={node.id}
              style={{ left: `${node.x}%`, top: `${node.y}%` }}
            >
              <span>{node.type}</span>
              <strong>{node.label}</strong>
            </Link>
          ))}
        </div>
      </section>
    </article>
  );
}
