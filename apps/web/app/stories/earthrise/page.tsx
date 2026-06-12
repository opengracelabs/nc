import type { Metadata } from "next";
import Link from "next/link";
import { EarthriseAttributionBlock } from "@/components/AttributionBlock";
import { getReviewedPageGeneration } from "@/lib/api";

export const metadata: Metadata = {
  title: "Earthrise Story",
  description: "The Apollo 8 Earthrise photograph with NASA attribution."
};

export default async function EarthriseStoryPage() {
  const generated = await getReviewedPageGeneration("story", "earthrise");
  const heroText = generated?.hero_text ?? "The image that made Earth the subject";
  const storyText =
    generated?.story_text ??
    "Earthrise was photographed during Apollo 8 on December 24, 1968. The image became a cultural reference point for seeing Earth as a shared, fragile world.";
  const educationText =
    generated?.education_text ??
    "Nature & Culture presents the image as a verified public-domain work with source, rights, and attribution visible beside the experience.";

  return (
    <article className="page story-page">
      <header className="story-header">
        <p className="eyebrow">Story</p>
        <h1>{heroText}</h1>
        <p className="lead">
          On Christmas Eve 1968, Apollo 8 rounded the Moon and revealed Earth as a blue world rising
          above a gray horizon.
        </p>
      </header>

      <figure className="earthrise-frame story-image-frame">
        <img
          className="earthrise-image"
          src="/images/earthrise-as08-14-2383.jpg"
          alt="Earth rising above the lunar horizon during Apollo 8"
        />
        <figcaption>NASA · Apollo 8 · William Anders · Public Domain</figcaption>
      </figure>

      <div className="story-body story-body-wide">
        <p>{storyText}</p>
        <p>
          The photograph is powerful because of its restraint. There are no cities, borders, roads,
          or monuments in view. The Moon fills the lower edge of the frame as a silent foreground;
          Earth appears small, bright, and alive beyond it.
        </p>
        <p>
          Apollo 8 was a technical mission, but Earthrise became a cultural image. It arrived at a
          moment when spaceflight, environmental awareness, and global media were beginning to shape
          one another. The photograph made planetary scale visible without abstraction.
        </p>
      </div>

      <section className="section editorial-section compact-section">
        <p className="eyebrow">Why Earthrise matters</p>
        <h2>The mission looked outward. The image asked us to look back.</h2>
        <div className="two-column-copy">
          <p>
            Earthrise is often remembered as a turning point because it changed the emotional frame
            of space exploration. The Moon was no longer only a destination; it became the place from
            which Earth could finally be seen whole.
          </p>
          <p>{educationText}</p>
        </div>
        <Link className="text-link" href="/collections/earthrise">
          View the Earthrise Collection
        </Link>
      </section>

      <section className="section feature-section compact-section">
        <div>
          <p className="eyebrow">Collection</p>
          <h2>Earthrise: The Overview Collection</h2>
          <p>
            The collection begins with AS08-14-2383 and connects the photograph, its mission context,
            source record, and launch editions in one focused experience.
          </p>
        </div>
        <div className="collection-teaser">
          <span>NASA source</span>
          <span>Story</span>
          <span>Print</span>
          <span>Digital</span>
        </div>
      </section>

      <section className="section compact-section">
        <h2>Continue with Earthrise</h2>
        <p>Choose the Museum Print for display or the Digital Edition for close study.</p>
        <Link className="button" href="/products/earthrise">
          Explore Earthrise editions
        </Link>
      </section>

      <section className="section attribution-section">
        <EarthriseAttributionBlock />
      </section>
    </article>
  );
}
