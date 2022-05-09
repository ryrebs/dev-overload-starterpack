import "dotenv/config";

const extractEnv = () => {
  if (process.env.EXPO_ENV === "dev") {
    return {
      EXPO_API: process.env.EXPO_LOCAL_API,
      EXPO_ENV: process.env.EXPO_ENV,
      EXPO_CLIENT_API: process.env.EXPO_DEV_CLIENT_API,
    };
  } else {
    return {
      EXPO_API: process.env.EXPO_PROD_API,
      EXPO_ENV: process.env.EXPO_ENV,
      EXPO_CLIENT_API: process.env.EXPO_PROD_CLIENT_API,
    };
  }
};

export default ({ config }) => {
  // Set android and ios google map keys from environment
  config.ios.config.googleMapsApiKey = process.env.EXPO_IOS_GOOGLE_MAP_API_KEY;
  config.android.config.googleMaps.apiKey =
    process.env.EXPO_ANDROID_GOOGLE_MAP_API_KEY;
  return {
    ...config,
    ...{
      name: "App",
      version: "1.0.0",
      extra: extractEnv(),
    },
  };
};
