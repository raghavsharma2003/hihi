import type { Metadata, Viewport } from "next";
import {
  Bricolage_Grotesque,
  IBM_Plex_Sans,
  IBM_Plex_Mono,
} from "next/font/google";
import { BRAND } from "@/config/business";
import "./globals.css";

const display = Bricolage_Grotesque({
  subsets: ["latin"],
  weight: ["700", "800"],
  variable: "--font-display",
  display: "swap",
});

const body = IBM_Plex_Sans({
  subsets: ["latin"],
  weight: ["400", "600"],
  variable: "--font-body",
  display: "swap",
});

const mono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400", "500"],
  variable: "--font-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: `${BRAND.name} — Cut your diesel bill by half or more`,
  description:
    "Your genset sells you power at ₹32 a unit. We serve the same hour at ₹13 — from a battery we design, our software runs, and a contract guarantees.",
};

export const viewport: Viewport = {
  themeColor: "#F6F8FB",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body
        className={`${display.variable} ${body.variable} ${mono.variable} font-body bg-daylight text-midnight`}
      >
        {children}
      </body>
    </html>
  );
}
