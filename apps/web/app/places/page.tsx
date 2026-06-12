import type { Metadata } from "next";
import { getPlaceTeasers } from "@/lib/api";

export const metadata: Metadata = {
  title: "Places",
  description: "Pilot places for the Nature & Culture public website."
};

export default async function PlacesPage() {
  const places = await getPlaceTeasers();

  return (
    <section className="page">
      <p className="eyebrow">Places</p>
      <h1>Explore public-domain heritage by place.</h1>
      <p className="lead">
        Phase 0 keeps place pages as governed previews while source authority gates complete.
      </p>
      <div className="grid">
        {places.map((place) => (
          <article className="card" key={place.slug}>
            <h2>{place.title}</h2>
            <p>{place.status}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
