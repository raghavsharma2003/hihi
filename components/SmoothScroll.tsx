"use client";

import { useEffect } from "react";
import Lenis from "lenis";
import { getGsap, prefersReducedMotion, setLenis } from "@/lib/gsap";

/**
 * The scroll engine. One Lenis instance for the whole page, driven by gsap's
 * ticker so scrubbed ScrollTriggers and the smoothing run on the same clock
 * (two rAF loops = the jitter we're fixing).
 *
 * Smoothing is deliberately short (≈1.1s, exponential-out): enough to take the
 * step out of a wheel notch, not enough to feel like ice. Touch is left native
 * — Lenis only syncs touch when asked, and hijacking it costs more than it
 * buys. Reduced motion gets no Lenis at all.
 */
export default function SmoothScroll() {
  useEffect(() => {
    if (prefersReducedMotion()) return;

    const { gsap, ScrollTrigger } = getGsap();
    const root = document.documentElement;

    // globals.css sets `html { scroll-behavior: smooth }`, which fights Lenis
    // (native smooth scroll + Lenis animation = two competing positions).
    // Inline style wins over the stylesheet; restored on unmount.
    const previousScrollBehavior = root.style.scrollBehavior;
    root.style.scrollBehavior = "auto";

    // Lenis' own class hooks, injected here because globals.css is off-limits.
    const style = document.createElement("style");
    style.setAttribute("data-lenis-runtime", "");
    style.textContent = [
      "html.lenis,html.lenis body{height:auto}",
      ".lenis.lenis-smooth{scroll-behavior:auto !important}",
      ".lenis.lenis-smooth [data-lenis-prevent]{overscroll-behavior:contain}",
      ".lenis.lenis-stopped{overflow:hidden}",
      ".lenis.lenis-smooth iframe{pointer-events:none}",
    ].join("");
    document.head.appendChild(style);

    const lenis = new Lenis({
      duration: 1.1,
      easing: (t: number) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      // gsap's ticker drives raf below — Lenis must not run its own loop.
      autoRaf: false,
      // `#` links scroll smoothly. No extra offset here on purpose: Lenis
      // subtracts the target's own scroll-margin-top, and every anchor target
      // on this page already carries scroll-mt-24 (96px) to clear the 72px
      // nav. Stacking another -80 on top would land each section ~176px down
      // — a hole under the nav. Smooth and native anchor jumps now agree.
      anchors: true,
    });
    setLenis(lenis);

    // Canonical gsap <-> Lenis wiring.
    const onScroll = () => ScrollTrigger.update();
    lenis.on("scroll", onScroll);

    const raf = (time: number) => lenis.raf(time * 1000);
    gsap.ticker.add(raf);
    gsap.ticker.lagSmoothing(0);

    // Web fonts change every measurement on the page (pin lengths, the
    // CurrentLine station positions). Re-measure once they've landed.
    let disposed = false;
    document.fonts.ready
      .then(() => {
        if (disposed) return;
        ScrollTrigger.refresh();
      })
      .catch(() => {
        /* font loading is best-effort; ScrollTrigger refreshes on load anyway */
      });

    return () => {
      disposed = true;
      lenis.off("scroll", onScroll);
      gsap.ticker.remove(raf);
      gsap.ticker.lagSmoothing(500, 33); // gsap's defaults
      lenis.destroy();
      setLenis(null);
      style.remove();
      root.style.scrollBehavior = previousScrollBehavior;
    };
  }, []);

  return null;
}
