import { Platform } from 'react-native';

/**
 * Echo's design language.
 *
 * The app is a place you talk to, so it leans warm rather than clinical: ink and
 * paper rather than grey-on-grey, one ember accent reserved exclusively for the
 * live-voice state, and a sage accent reserved exclusively for machine-authored
 * content. Reserving each accent for exactly one meaning is what lets a glance
 * tell you "this is recording" or "the assistant wrote this" with no label.
 */

export type ColorScheme = 'light' | 'dark';

export interface Palette {
  /** Page background. */
  bg: string;
  /** Cards, sheets, rows sitting on `bg`. */
  surface: string;
  /** Controls and inputs sitting on `surface`. */
  surfaceRaised: string;
  /** Pressed/hover feedback fill. */
  surfacePressed: string;

  /** Hairline dividers and card outlines. */
  border: string;
  /** Slightly stronger border for focused/active elements. */
  borderStrong: string;

  /** Primary reading colour. */
  text: string;
  /** Secondary copy, metadata, timestamps. */
  textMuted: string;
  /** Placeholders and disabled copy. */
  textFaint: string;
  /** Text drawn on top of `ember`/`sage` fills. */
  textOnAccent: string;

  /** Live voice. Recording, waveform, the record button. Nothing else. */
  ember: string;
  emberSoft: string;
  emberBorder: string;

  /** Assistant-authored content: summaries, suggestions, action items. */
  sage: string;
  sageSoft: string;
  sageBorder: string;

  /** Pinned / starred. */
  gold: string;
  goldSoft: string;

  /** Destructive actions and sync failures. */
  danger: string;
  dangerSoft: string;

  /** Scrims behind modals. */
  scrim: string;
  /** Shadow colour (iOS). */
  shadow: string;
}

const dark: Palette = {
  bg: '#100F0C',
  surface: '#191713',
  surfaceRaised: '#221F19',
  surfacePressed: '#2B271F',

  border: 'rgba(244, 241, 233, 0.09)',
  borderStrong: 'rgba(244, 241, 233, 0.18)',

  text: '#F4F1E9',
  textMuted: '#A29C8E',
  textFaint: '#6E695D',
  textOnAccent: '#12110E',

  ember: '#F0653A',
  emberSoft: 'rgba(240, 101, 58, 0.16)',
  emberBorder: 'rgba(240, 101, 58, 0.34)',

  sage: '#7FC8A9',
  sageSoft: 'rgba(127, 200, 169, 0.14)',
  sageBorder: 'rgba(127, 200, 169, 0.30)',

  gold: '#E8B84B',
  goldSoft: 'rgba(232, 184, 75, 0.16)',

  danger: '#F0575C',
  dangerSoft: 'rgba(240, 87, 92, 0.15)',

  scrim: 'rgba(8, 7, 5, 0.72)',
  shadow: '#000000',
};

const light: Palette = {
  bg: '#FBF9F4',
  surface: '#FFFFFF',
  surfaceRaised: '#FFFFFF',
  surfacePressed: '#F1EDE4',

  border: 'rgba(22, 21, 15, 0.09)',
  borderStrong: 'rgba(22, 21, 15, 0.18)',

  text: '#16150F',
  textMuted: '#6B6659',
  textFaint: '#9A9486',
  textOnAccent: '#FFFFFF',

  ember: '#D9451B',
  emberSoft: 'rgba(217, 69, 27, 0.10)',
  emberBorder: 'rgba(217, 69, 27, 0.26)',

  sage: '#1F6B4F',
  sageSoft: 'rgba(31, 107, 79, 0.09)',
  sageBorder: 'rgba(31, 107, 79, 0.22)',

  gold: '#9A6F0F',
  goldSoft: 'rgba(154, 111, 15, 0.12)',

  danger: '#C4292E',
  dangerSoft: 'rgba(196, 41, 46, 0.10)',

  scrim: 'rgba(22, 21, 15, 0.42)',
  shadow: '#2B2416',
};

export const palettes: Record<ColorScheme, Palette> = { light, dark };

/** 4pt base scale. Use these instead of raw numbers. */
export const space = {
  xxs: 2,
  xs: 4,
  sm: 8,
  md: 12,
  base: 16,
  lg: 20,
  xl: 24,
  xxl: 32,
  xxxl: 48,
  huge: 64,
} as const;

export const radius = {
  sm: 8,
  md: 12,
  lg: 16,
  xl: 22,
  xxl: 28,
  pill: 999,
} as const;

/**
 * A serif for anything the user authored or the app presents as *writing*
 * (note titles, transcripts), a sans for chrome (labels, buttons, tabs). The
 * split is what keeps a screen full of text from reading like a settings panel.
 */
export const fontFamily = {
  serif: Platform.select({ ios: 'Georgia', android: 'serif', default: 'Georgia, serif' })!,
  sans: Platform.select({
    ios: 'System',
    android: 'sans-serif',
    default: 'system-ui, -apple-system, sans-serif',
  })!,
  mono: Platform.select({
    ios: 'Menlo',
    android: 'monospace',
    default: 'ui-monospace, monospace',
  })!,
} as const;

export interface TextStyleToken {
  fontFamily: string;
  fontSize: number;
  lineHeight: number;
  letterSpacing?: number;
  fontWeight?: '400' | '500' | '600' | '700';
}

export const type = {
  /** Screen-defining moments only: the empty state, the capture prompt. */
  display: {
    fontFamily: fontFamily.serif,
    fontSize: 34,
    lineHeight: 41,
    letterSpacing: -0.5,
    fontWeight: '400',
  },
  /** Note titles in detail view. */
  title: {
    fontFamily: fontFamily.serif,
    fontSize: 26,
    lineHeight: 33,
    letterSpacing: -0.3,
    fontWeight: '400',
  },
  /** Note titles in the list. */
  heading: {
    fontFamily: fontFamily.serif,
    fontSize: 19,
    lineHeight: 25,
    letterSpacing: -0.15,
    fontWeight: '400',
  },
  /** Transcript and long-form reading. */
  body: {
    fontFamily: fontFamily.serif,
    fontSize: 17,
    lineHeight: 28,
    letterSpacing: 0,
    fontWeight: '400',
  },
  /** Everything in the chrome: buttons, rows, form labels. */
  ui: {
    fontFamily: fontFamily.sans,
    fontSize: 16,
    lineHeight: 22,
    letterSpacing: -0.1,
    fontWeight: '500',
  },
  uiSmall: {
    fontFamily: fontFamily.sans,
    fontSize: 14,
    lineHeight: 19,
    letterSpacing: -0.05,
    fontWeight: '500',
  },
  /** Timestamps, counts, secondary metadata. */
  caption: {
    fontFamily: fontFamily.sans,
    fontSize: 13,
    lineHeight: 17,
    letterSpacing: 0,
    fontWeight: '500',
  },
  /** Section headers. Always uppercase where used. */
  overline: {
    fontFamily: fontFamily.sans,
    fontSize: 11,
    lineHeight: 14,
    letterSpacing: 1.1,
    fontWeight: '700',
  },
  /** Durations and timers — tabular so digits don't jitter as they tick. */
  numeric: {
    fontFamily: fontFamily.mono,
    fontSize: 15,
    lineHeight: 20,
    letterSpacing: -0.3,
    fontWeight: '500',
  },
} satisfies Record<string, TextStyleToken>;

/**
 * Motion. Short and eased-out for anything the user triggered (it should feel
 * like a direct response); longer and gentler for anything the system decided
 * to show on its own (it should not startle).
 */
export const motion = {
  instant: 90,
  fast: 160,
  base: 240,
  slow: 380,
  deliberate: 620,
  /** Standard ease-out — decelerating, feels responsive. */
  easeOut: [0.16, 1, 0.3, 1] as const,
  /** Symmetric ease for things that loop, like the recording pulse. */
  easeInOut: [0.65, 0, 0.35, 1] as const,
  /** Spring config for press feedback. */
  press: { damping: 18, stiffness: 320, mass: 0.6 },
  /** Spring config for things entering the screen. */
  enter: { damping: 22, stiffness: 210, mass: 0.9 },
} as const;

export const elevation = {
  none: {},
  /** Cards resting on the page. */
  low: {
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 2,
  },
  /** Sheets and floating controls. */
  mid: {
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.16,
    shadowRadius: 22,
    elevation: 8,
  },
  /** The record button — it should read as the closest thing to the user. */
  high: {
    shadowOffset: { width: 0, height: 14 },
    shadowOpacity: 0.28,
    shadowRadius: 34,
    elevation: 16,
  },
} as const;

/** Minimum touch target. Anything interactive must reach this. */
export const HIT_SLOP_MIN = 44;
