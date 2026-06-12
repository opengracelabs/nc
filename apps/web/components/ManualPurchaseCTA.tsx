type ManualPurchaseCTAProps = {
  productName?: string;
};

export function ManualPurchaseCTA({ productName = "Earthrise" }: ManualPurchaseCTAProps) {
  return (
    <div className="purchase-panel">
      <p className="eyebrow">Availability</p>
      <h2>Contact for availability</h2>
      <p>
        Ask about {productName}. We will reply with availability, payment, and fulfillment details.
      </p>
      <a className="button" href="mailto:natureandculture@protonmail.com?subject=Earthrise availability inquiry">
        Contact us
      </a>
    </div>
  );
}
