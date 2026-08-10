import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import type Lenis from "lenis";

let registered = false;

/** Register ScrollTrigger once, client-side only. */
export function getGsap() {
  if (typeof window !== "undefined" && !registered) {
    gsap.registerPlugin(ScrollTrigger);
    registered = true;
  }
  return { gsap, ScrollTrigger };
}

export function prefersReducedMotion(): boolean {
  return (
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches
  );
}

/**
 * Height of the fixed nav at its tallest (16px block padding + 37px button).
 * Pinned sections reserve this much top padding so nothing sits under the nav.
 */
export const NAV_HEIGHT = 72;

/**
 * Anchor landing clearance: nav height plus air. Expressed on the targets
 * themselves as `scroll-mt-24` (96px) so native jumps, reduced-motion jumps
 * and Lenis (which honours scroll-margin-top) all land in the same place.
 */
export const ANCHOR_CLEARANCE = 96;

/** The one breakpoint the scroll engine cares about (Tailwind `md`). */
export const MD_BREAKPOINT = 768;

/**
 * Shared media queries for gsap.matchMedia(). Every scroll-driven section
 * splits the same three ways so behaviour can never disagree between them:
 * reduced motion wins outright, then desktop (pinned), then mobile (no pin).
 */
export const MQ: Record<string, string> = {
  reduced: "(prefers-reduced-motion: reduce)",
  desktop: `(prefers-reduced-motion: no-preference) and (min-width: ${MD_BREAKPOINT}px)`,
  mobile: `(prefers-reduced-motion: no-preference) and (max-width: ${MD_BREAKPOINT - 0.02}px)`,
};

let lenisInstance: Lenis | null = null;

/** SmoothScroll registers/unregisters the single Lenis instance here. */
export function setLenis(instance: Lenis | null): void {
  lenisInstance = instance;
}

/** The active Lenis instance, or null (reduced motion / not yet mounted). */
export function getLenis(): Lenis | null {
  return lenisInstance;
}
