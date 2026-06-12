import type { Metadata } from "next";
import Link from "next/link";
import "./styles.css";

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000"),
  title: {
    default: "Nature & Culture",
    template: "%s | Nature & Culture"
  },
  description: "Source-traceable public-domain stories, collections, and editions."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <header className="site-header">
          <Link className="brand" href="/">
            Nature & Culture
          </Link>
          <nav aria-label="Primary navigation">
            <Link href="/collections">Collections</Link>
            <Link href="/places">Discover</Link>
            <Link href="/products">Editions</Link>
            <Link href="/about">About</Link>
          </nav>
        </header>
        <main>{children}</main>
        <footer className="site-footer">
          <p>Public-domain sources, visible attribution, source-traceable editions.</p>
        </footer>
      </body>
    </html>
  );
}
