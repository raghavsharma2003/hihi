"use client";

import { useEffect, useId, useState } from "react";

/**
 * Slider + synced number field. Keyboard operable via both controls;
 * the slider fill is painted through the --fill custom property.
 *
 * While the thumb is held, the mono readout takes the interactive blue —
 * colour only, no movement, so the number stays readable as it ticks.
 */
export default function RangeField({
  label,
  value,
  min,
  max,
  step,
  onChange,
  format,
  disabled = false,
}: {
  label: string;
  value: number;
  min: number;
  max: number;
  step: number;
  onChange: (v: number) => void;
  format: (v: number) => string;
  disabled?: boolean;
}) {
  const id = useId();
  const fill = ((value - min) / (max - min)) * 100;
  const [dragging, setDragging] = useState(false);

  // Release can land outside the input (or the pointer can be cancelled),
  // so the end of the drag is watched on the window.
  useEffect(() => {
    if (!dragging) return;
    const end = () => setDragging(false);
    window.addEventListener("pointerup", end);
    window.addEventListener("pointercancel", end);
    return () => {
      window.removeEventListener("pointerup", end);
      window.removeEventListener("pointercancel", end);
    };
  }, [dragging]);

  const clamp = (v: number) => Math.min(max, Math.max(min, v));

  return (
    <div className={disabled ? "opacity-40" : ""}>
      <div className="flex items-baseline justify-between gap-4">
        <label htmlFor={id} className="text-14 font-semibold">
          {label}
        </label>
        <output
          htmlFor={id}
          className={`tabular font-mono text-14 font-medium transition-colors duration-150 ease-[ease] ${
            dragging ? "text-current" : "text-midnight"
          }`}
        >
          {format(value)}
        </output>
      </div>
      <input
        id={id}
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        disabled={disabled}
        aria-label={label}
        onChange={(e) => onChange(clamp(Number(e.target.value)))}
        onPointerDown={() => !disabled && setDragging(true)}
        style={{ "--fill": `${fill}%` } as React.CSSProperties}
        className="mt-2"
      />
      <div className="flex justify-between font-mono text-12 text-midnight/50">
        <span>{format(min)}</span>
        <span>{format(max)}</span>
      </div>
    </div>
  );
}
