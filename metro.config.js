const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

// `@supabase/supabase-js` ships browser-targeted ESM that expects these
// conditions; without them Metro resolves the Node build and websockets break.
config.resolver.unstable_enablePackageExports = true;
config.resolver.unstable_conditionNames = ['react-native', 'browser', 'require'];

module.exports = config;
