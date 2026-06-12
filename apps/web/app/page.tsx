import Link from "next/link";
import { EarthriseAttributionBlock } from "@/components/AttributionBlock";
import { getEarthriseProducts, getPlaceTeasers } from "@/lib/api";

export default async function HomePage() {
  const [products, places] = await Promise.all([getEarthriseProducts(), getPlaceTeasers()]);

  return (
    <>
      <section className="full-bleed-hero" aria-label="Earthrise hero">
        <img
          className="full-bleed-hero-image"
          src="/images/earthrise-as08-14-2383.jpg"
          alt="Earth rising above the lunar horizon during Apollo 8"
        />
        <div className="full-bleed-hero-copy">
          <p className="eyebrow light-eyebrow">Apollo 8 · December 24, 1968</p>
          <h1>The world seen whole.</h1>
          <p className="lead hero-lead">
            A source-traceable edition of Earthrise, the photograph that turned lunar exploration
            into a portrait of home.
          </p>
          <div className="button-row">
            <Link className="button light-button" href="/stories/earthrise">
              Explore Earthrise
            </Link>
            <Link className="button ghost-button" href="/products/earthrise">
              View editions
            </Link>
          </div>
        </div>
        <p className="hero-credit">NASA · Apollo 8 · William Anders · Public Domain</p>
      </section>

      <section className="section editorial-section premium-editorial">
        <p className="eyebrow">Why Earthrise matters</p>
        <h2>A photograph that turned exploration back toward home.</h2>
        <div className="two-column-copy editorial-copy">
          <p>
            Taken from lunar orbit by William Anders, Earthrise gave the public a new view of the
            planet: bright, finite, and suspended above an airless horizon. Its power comes from that
            reversal. The mission was aimed at the Moon, but the image made Earth the subject.
          </p>
          <p>
            Nature & Culture begins here because Earthrise is both a scientific record and a cultural
            artifact. The image carries mission history, environmental memory, and a product story in
            one frame.
          </p>
        </div>
      </section>

      <section className="section collection-section" id="collections">
        <div className="section-heading wide-heading">
          <p className="eyebrow">Collections</p>
          <h2>Earthrise: The Oasis Collection</h2>
          <p className="lead">
            One NASA source image, three ways into the work: the story, the Museum Print, and the
            Digital Edition.
          </p>
        </div>
        <div className="collection-card-grid">
          <article className="collection-card image-card">
            <img src="/images/earthrise-work-masterwork.jpg" alt="Earthrise masterwork crop from Apollo 8" />
            <div>
              <span className="masterwork-badge">MASTERWORK</span>
              <h3>Story</h3>
              <p>The Apollo 8 image as a cultural turning point and source record.</p>
              <Link href="/collections/earthrise">Enter collection</Link>
            </div>
          </article>
          <article className="collection-card image-card">
            <img src="/images/earthrise-work-horizon.jpg" alt="Earthrise lunar horizon crop for museum print preview" />
            <div>
              <span className="masterwork-badge">MASTERWORK</span>
              <h3>Museum Print</h3>
              <p>For framed display, collecting, gifting, and source-backed presentation.</p>
              <Link href="/collections/earthrise">View in collection</Link>
            </div>
          </article>
          <article className="collection-card image-card">
            <img src="/images/earthrise-work-folio.jpg" alt="Earthrise archival folio crop for digital edition preview" />
            <div>
              <span className="masterwork-badge">MASTERWORK</span>
              <h3>Digital Edition</h3>
              <p>For close viewing, teaching, reference, and personal archival use.</p>
              <Link href="/collections/earthrise">View in collection</Link>
            </div>
          </article>
        </div>
      </section>

      <section className="section">
        <div className="section-heading">
          <p className="eyebrow">Editions</p>
          <h2>Available Earthrise editions</h2>
        </div>
        <div className="grid">
          {products.map((product) => (
            <article className="card product-card" key={product.code}>
              <span className="masterwork-badge">MASTERWORK</span>
              <h3>{product.title}</h3>
              <p>{product.description}</p>
              <Link href={product.route}>Compare editions</Link>
            </article>
          ))}
        </div>
      </section>

      <section className="section discover-section">
        <div className="section-heading">
          <p className="eyebrow">Discover</p>
          <h2>Next journeys</h2>
        </div>
        <div className="grid">
          {places.map((place) => (
            <article className="card" key={place.slug}>
              <h3>{place.title}</h3>
              <p>Source-led stories, collections, and editions connected to this place.</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section attribution-section">
        <EarthriseAttributionBlock />
      </section>
    </>
  );
}
