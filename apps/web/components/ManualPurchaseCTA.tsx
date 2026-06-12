type ManualPurchaseCTAProps = {
  productName?: string;
};

export function ManualPurchaseCTA({ productName = "Earthrise" }: ManualPurchaseCTAProps) {
  return (
    <div className="purchase-panel">
      <p className="eyebrow">Manual purchase</p>
      <h2>Request purchase</h2>
      <p>
        Send a purchase request for {productName}. A manual invoice and fulfillment details will
        follow after review.
      </p>
      <a className="button" href="mailto:natureandculture@protonmail.com?subject=Earthrise purchase request">
        Request purchase
      </a>
    </div>
  );
}
