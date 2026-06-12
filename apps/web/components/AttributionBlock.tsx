import { NASA_EARTHRISE_CREDIT, NASA_NONENDORSEMENT } from "@/lib/governed-content";

export function EarthriseAttributionBlock() {
  return (
    <section className="attribution-block" aria-label="Earthrise attribution">
      <p>{NASA_EARTHRISE_CREDIT}</p>
      <p>{NASA_NONENDORSEMENT}</p>
    </section>
  );
}
