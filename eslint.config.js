const expoConfig = require('eslint-config-expo/flat');

module.exports = [
  ...expoConfig,
  {
    // Edge functions are Deno, not React Native — they have their own runtime
    // and globals, and linting them with this config only produces noise.
    ignores: ['dist/*', 'node_modules/*', '.expo/*', 'supabase/functions/**'],
  },
  {
    rules: {
      // Reanimated's public API *is* assignment to `sharedValue.value`, and the
      // whole point of a shared value is that it is mutable from both runtimes.
      // The rule models plain React state and flags every correct use.
      'react-hooks/immutability': 'off',

      // `useDbQuery` and `useAsync` take a caller-supplied dependency array so
      // one implementation can serve every screen. The rule requires an inline
      // array literal, which a generic hook cannot have.
      'react-hooks/use-memo': 'off',

      // A handful of effects deliberately read a value once at mount (starting
      // the recorder, honouring a one-shot seek). Each is disabled inline with
      // its reason; keeping this at "warn" surfaces new ones without failing
      // the build on the intentional ones.
      'react-hooks/exhaustive-deps': 'warn',
    },
  },
];
