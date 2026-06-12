import type { Metadata } from "next";
import Link from "next/link";
import "./styles.css";

export const metadata: Metadata = {
  title: {
    default: "Nature & Culture",
    template: "%s | Nature & Culture"
  },
  description: "Verified public-domain heritage stories, places, and products."
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
            <Link href="/places">Places</Link>
            <Link href="/stories/earthrise">Stories</Link>
            <Link href="/products">Products</Link>
            <Link href="/about">About</Link>
          </nav>
        </header>
        <main>{children}</main>
        <footer className="site-footer">
          <p>Verified public-domain sources, visible attribution, manual commerce only.</p>
        </footer>
      </body>
    </html>
  );
}
