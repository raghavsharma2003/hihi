import React, { createContext, useContext, useMemo } from 'react';
import { useColorScheme } from 'react-native';

import {
  type ColorScheme,
  type Palette,
  elevation,
  motion,
  palettes,
  radius,
  space,
  type,
} from './tokens';

export * from './tokens';

export interface Theme {
  scheme: ColorScheme;
  color: Palette;
  space: typeof space;
  radius: typeof radius;
  type: typeof type;
  motion: typeof motion;
  elevation: typeof elevation;
  /** Shadow tokens pre-tinted with the palette's shadow colour. */
  shadow: (level: keyof typeof elevation) => object;
}

const ThemeContext = createContext<Theme | null>(null);

function buildTheme(scheme: ColorScheme): Theme {
  const color = palettes[scheme];
  return {
    scheme,
    color,
    space,
    radius,
    type,
    motion,
    elevation,
    shadow: (level) => {
      const base = elevation[level];
      if (!('shadowOpacity' in base)) return {};
      return { ...base, shadowColor: color.shadow };
    },
  };
}

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const system = useColorScheme();
  const scheme: ColorScheme = system === 'light' ? 'light' : 'dark';
  const theme = useMemo(() => buildTheme(scheme), [scheme]);

  return <ThemeContext.Provider value={theme}>{children}</ThemeContext.Provider>;
}

export function useTheme(): Theme {
  const theme = useContext(ThemeContext);
  if (!theme) throw new Error('useTheme must be used inside <ThemeProvider>');
  return theme;
}

/**
 * Build styles that depend on the theme without re-creating the object on every
 * render. Mirrors the ergonomics of StyleSheet.create but theme-aware.
 */
export function useThemedStyles<T>(factory: (theme: Theme) => T): T {
  const theme = useTheme();
  return useMemo(() => factory(theme), [theme, factory]);
}
