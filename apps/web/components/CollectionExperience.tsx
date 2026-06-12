import Link from "next/link";
import type {
  CollectionMetadata,
  CollectionWork,
  NextJourney,
  ProvenanceGlanceItem
} from "@/lib/collections";

export function Breadcrumbs({ items }: { items: Array<{ href?: string; label: string }> }) {
  return (
    <nav className="breadcrumbs" aria-label="Breadcrumb">
      {items.map((item, index) => (
        <span key={item.label}>
          {item.href ? <Link href={item.href}>{item.label}</Link> : item.label}
          {index < items.length - 1 ? <span aria-hidden="true">/</span> : null}
        </span>
      ))}
    </nav>
  );
}

export function ProvenanceGlance({ items }: { items: ProvenanceGlanceItem[] }) {
  return (
    <section className="section provenance-glance-section">
      <p className="eyebrow">Provenance glance</p>
      <div className="provenance-glance-grid">
        {items.map((item) => (
          <div className="provenance-glance-card" key={item.label}>
            <span>{item.label}</span>
            <strong>{item.value}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}

export function FeaturedWorksGrid({
  collection,
  works
}: {
  collection: CollectionMetadata;
  works: CollectionWork[];
}) {
  return (
    <div className="collection-card-grid featured-works-grid">
      {works.map((work) => (
        <article className="collection-card image-card featured-work-card" key={work.title}>
          <div className={"featured-work-image work-treatment-" + work.imageTreatment}>
            <img src={work.imageSrc} alt={work.imageAlt} />
          </div>
          <div>
            <span className="masterwork-badge">{work.label}</span>
            <h3>{work.title}</h3>
            <p>{work.copy}</p>
          </div>
        </article>
      ))}
    </div>
  );
}

export function NextJourneys({ journeys }: { journeys: NextJourney[] }) {
  return (
    <section className="section next-journeys-section">
      <div className="section-heading wide-heading">
        <p className="eyebrow">Next journeys</p>
        <h2>Continue through the collection.</h2>
      </div>
      <div className="next-journey-grid">
        {journeys.map((journey) => (
          <article className="next-journey-card" key={journey.title}>
            <p className="eyebrow">{journey.eyebrow}</p>
            <h3>{journey.title}</h3>
            <p>{journey.copy}</p>
            <Link href={journey.href}>Continue</Link>
          </article>
        ))}
      </div>
    </section>
  );
}
