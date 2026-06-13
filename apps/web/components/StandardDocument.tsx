import Link from "next/link";
import type { NatureCultureStandard } from "@/lib/standards";

type StandardDocumentProps = {
  standard: NatureCultureStandard;
};

export function StandardDocument({ standard }: StandardDocumentProps) {
  return (
    <section className="page standard-document-page">
      <div className="standard-hero">
        <p className="eyebrow">Public standard</p>
        <h1>{standard.title}</h1>
        <p className="lead">{standard.shortTitle}</p>
        <p>{standard.purpose}</p>
        <div className="standard-hero-actions">
          <Link className="button" href="/standards">All standards</Link>
          <Link className="button secondary-button" href={standard.schemaUrl}>Open public JSON schema</Link>
          <Link className="button secondary-button" href="/certificate">View trust surfaces</Link>
        </div>
      </div>

      <section className="standard-doc-grid" aria-labelledby={`${standard.slug}-documentation`}>
        <div>
          <p className="eyebrow">Public documentation</p>
          <h2 id={`${standard.slug}-documentation`}>Visitor-readable rules</h2>
        </div>
        <div className="standard-copy-stack">
          {standard.documentation.map((paragraph) => (
            <p key={paragraph}>{paragraph}</p>
          ))}
        </div>
      </section>

      <section className="standard-schema-section" aria-labelledby={`${standard.slug}-schema`}>
        <p className="eyebrow">Public schema</p>
        <h2 id={`${standard.slug}-schema`}>Required public fields</h2>
        <div className="standard-schema-table-wrap">
          <table className="standard-schema-table">
            <thead>
              <tr>
                <th>Field</th>
                <th>Type</th>
                <th>Required</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {standard.schema.map((field) => (
                <tr key={field.name}>
                  <td><code>{field.name}</code></td>
                  <td>{field.type}</td>
                  <td>{field.required ? "Yes" : "Conditional"}</td>
                  <td>{field.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="standard-example" aria-labelledby={`${standard.slug}-example`}>
        <p className="eyebrow">Public example</p>
        <h2 id={`${standard.slug}-example`}>{standard.example.title}</h2>
        <pre><code>{JSON.stringify(standard.example.code, null, 2)}</code></pre>
      </section>
    </section>
  );
}
