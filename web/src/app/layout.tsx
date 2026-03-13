import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Niche Explorer | High-Moat Opportunity Mining for technical entrepreneurs",
  description: "Advanced AI-powered tool to discover underserved market niches and profitable software ideas using deep internet analysis of developer pain points.",
  keywords: ["niche discovery", "market analysis", "software ideas", "developer pain points", "business opportunity", "SaaS ideas"],
  openGraph: {
    title: "Niche Explorer Pro",
    description: "Discover your next high-moat project with AI.",
    type: "website",
    url: "https://niche-explorer.com",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" />
        
        {/* Google Analytics */}
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-HLTZZDJZWT"></script>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              window.dataLayer = window.dataLayer || [];
              function gtag(){dataLayer.push(arguments);}
              gtag('js', new Date());
              gtag('config', 'G-HLTZZDJZWT', {
                page_path: window.location.pathname,
              });
            `,
          }}
        />
      </head>
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
