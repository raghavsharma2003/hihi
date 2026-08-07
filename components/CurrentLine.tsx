"use client";

import { useEffect, useRef } from "react";
import { getGsap, prefersReducedMotion } from "@/lib/gsap";

/**
 * THE signature element: one continuous 2px path of electricity running the
 * whole page, drawn by scroll (stroke-dashoffset scrub). It enters from a
 * pylon glyph at the hero, swings through every section station, forks into
 * the diesel bar (turns clay, dead-ends with a burn mark), and terminates at
 * the final CTA button, whose border pulses once. Reduced motion: fully
 * drawn, static.
 */
export default function CurrentLine() {
  const svgRef = useRef<SVGSVGElement>(null);
  const mainRef = useRef<SVGPathElement>(null);
  const forkRef = useRef<SVGPathElement>(null);
  const burnRef = useRef<SVGCircleElement>(null);
  const pylonRef = useRef<SVGGElement>(null);

  useEffect(() => {
    const svg = svgRef.current;
    const main = mainRef.current;
    const fork = forkRef.current;
    const burn = burnRef.current;
    if (!svg || !main || !fork || !burn) return;

    const reduced = prefersReducedMotion();
    const { ScrollTrigger } = getGsap();
    let triggers: { kill: () => void }[] = [];

    const build = () => {
      const docH = document.documentElement.scrollHeight;
      const vw = document.documentElement.clientWidth;
      svg.setAttribute("viewBox", `0 0 ${vw} ${docH}`);
      svg.style.height = `${docH}px`;
      svg.style.width = `${vw}px`;

      const wide = vw >= 1296;
      const railX = wide ? (vw - 1200) / 2 - 44 : vw >= 768 ? 14 : 7;
      const swayA = wide ? 22 : 5;
      const swayB = wide ? -10 : -3;
      const at = (el: Element | null) => {
        if (!el) return null;
        const r = el.getBoundingClientRect();
        return {
          x: r.left + r.width / 2 + window.scrollX,
          top: r.top + window.scrollY,
          bottom: r.bottom + window.scrollY,
        };
      };

      const stations = Array.from(
        document.querySelectorAll("[data-station]"),
      ).map((el) => at(el)!.top);
      const cta = at(document.getElementById("final-cta-button"));
      const diesel = at(document.getElementById("diesel-bar"));

      // pylon at the very start of the rail; on narrow screens the line
      // enters below the hero copy, next to the streetscape
      const scene = at(document.getElementById("hero-scene"));
      const startY =
        vw >= 768 ? 140 : scene ? scene.bottom + 16 : 240;
      if (pylonRef.current) {
        pylonRef.current.setAttribute(
          "transform",
          `translate(${Math.max(0, railX - 14)}, ${startY - 38})`,
        );
      }

      // main path: down the rail, one gentle sway per station
      let d = `M ${railX} ${startY}`;
      let prevY = startY;
      stations.forEach((y, i) => {
        const sway = i % 2 === 0 ? swayA : swayB;
        const mid = (prevY + y) / 2;
        d += ` C ${railX} ${mid}, ${railX + sway} ${mid}, ${railX + sway} ${y}`;
        d += ` C ${railX + sway} ${y + 40}, ${railX} ${y + 40}, ${railX} ${y + 80}`;
        prevY = y + 80;
      });
      if (cta) {
        const endY = cta.top - 10;
        const mid = (prevY + endY) / 2;
        d += ` C ${railX} ${mid}, ${cta.x} ${mid}, ${cta.x} ${endY}`;
      } else {
        d += ` L ${railX} ${docH - 80}`;
      }
      main.setAttribute("d", d);

      // diesel fork: a short clay branch that splits off the rail beside the
      // price ladder and dead-ends with a burn mark — it never reaches the
      // grid, and never crosses the content
      if (diesel) {
        const fy = diesel.top;
        const fx = railX + (wide ? 34 : 16);
        const burnY = fy + 96;
        fork.setAttribute(
          "d",
          `M ${railX} ${fy - 40} C ${railX} ${fy + 10}, ${fx} ${fy + 26}, ${fx} ${burnY - 8}`,
        );
        burn.setAttribute("cx", String(fx));
        burn.setAttribute("cy", String(burnY));
        fork.style.visibility = "visible";
        burn.style.visibility = "visible";
      } else {
        fork.style.visibility = "hidden";
        burn.style.visibility = "hidden";
      }

      // draw-by-scroll
      const mainLen = main.getTotalLength();
      const forkLen = fork.getTotalLength();
      main.style.strokeDasharray = String(mainLen);
      fork.style.strokeDasharray = String(forkLen);

      triggers.forEach((t) => t.kill());
      triggers = [];

      if (reduced) {
        main.style.strokeDashoffset = "0";
        fork.style.strokeDashoffset = "0";
        burn.style.opacity = "1";
        return;
      }

      main.style.strokeDashoffset = String(mainLen);
      fork.style.strokeDashoffset = String(forkLen);
      burn.style.opacity = "0";

      triggers.push(
        ScrollTrigger.create({
          start: 0,
          end: () => docH - window.innerHeight,
          scrub: 0.6,
          onUpdate: (self) => {
            // stay a beat ahead of the viewport so the head is visible
            const p = Math.min(1, self.progress * 1.08);
            main.style.strokeDashoffset = String(mainLen * (1 - p));
          },
        }),
      );

      const priceSection = document.getElementById("diesel-bar");
      if (priceSection) {
        triggers.push(
          ScrollTrigger.create({
            trigger: priceSection,
            start: "top 85%",
            end: "top 35%",
            scrub: 0.6,
            onUpdate: (self) => {
              fork.style.strokeDashoffset = String(forkLen * (1 - self.progress));
              burn.style.opacity = self.progress > 0.95 ? "1" : "0";
            },
          }),
        );
      }
    };

    // build after layout settles (fonts, pin-spacers), rebuild on refresh/resize
    const rebuild = () => requestAnimationFrame(build);
    const t = setTimeout(rebuild, 100);
    ScrollTrigger.addEventListener("refreshInit", () => {});
    ScrollTrigger.addEventListener("refresh", rebuild);
    window.addEventListener("resize", rebuild);

    // CTA pulse, once, when the terminal arrives
    const ctaBtn = document.getElementById("final-cta-button");
    let io: IntersectionObserver | undefined;
    if (ctaBtn && !reduced) {
      io = new IntersectionObserver(
        ([e]) => {
          if (e.isIntersecting) {
            ctaBtn.classList.add("cta-pulse");
            io?.disconnect();
          }
        },
        { threshold: 0.9 },
      );
      io.observe(ctaBtn);
    }

    return () => {
      clearTimeout(t);
      triggers.forEach((tr) => tr.kill());
      ScrollTrigger.removeEventListener("refresh", rebuild);
      window.removeEventListener("resize", rebuild);
      io?.disconnect();
    };
  }, []);

  return (
    <svg
      ref={svgRef}
      aria-hidden="true"
      className="pointer-events-none absolute left-0 top-0 z-30"
      style={{ overflow: "visible" }}
    >
      {/* pylon glyph: where the electricity enters the page */}
      <g ref={pylonRef} stroke="#1847C9" strokeWidth="2" fill="none">
        <path d="M6 34 L14 4 M22 34 L14 4" />
        <path d="M8 26 H20 M10 18 H18 M11 11 H17" />
      </g>
      <path
        ref={mainRef}
        fill="none"
        stroke="#1847C9"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <path
        ref={forkRef}
        fill="none"
        stroke="#B3402F"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <circle ref={burnRef} r="5" fill="#B3402F" style={{ transition: "opacity 250ms" }} />
    </svg>
  );
}
