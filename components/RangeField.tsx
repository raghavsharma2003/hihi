"use client";

import { useId } from "react";

/**
 * Slider + synced number field. Keyboard operable via both controls;
 * the slider fill is painted through the --fill custom property.
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

  const clamp = (v: number) => Math.min(max, Math.max(min, v));

  return (
    <div className={disabled ? "opacity-40" : ""}>
      <div className="flex items-baseline justify-between gap-4">
        <label htmlFor={id} className="text-14 font-semibold">
          {label}
        </label>
        <output
          htmlFor={id}
          className="tabular font-mono text-14 font-medium text-midnight"
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
