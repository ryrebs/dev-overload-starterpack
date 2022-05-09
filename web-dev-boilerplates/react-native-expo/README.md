React Native Expo boilerplate

_Expo SDK 39_

Libraries:

1. React navigation

2. Redux, Redux Persist and Redux Saga

3. Using axios

4. Build with turtle-cli

5. Using dotenv for .env files

6. i18n ready

Getting Started

1. Clone the repo

2. Install dependencies: `npm install`

3. Start expo: `npm start` or `yarn start` (Assuming yarn is installed globally.)

4. A browser will open or tab that contains the development server.

5. Download the `Expo` mobile app, then scan the qr code in the terminal or in the development server using `Expo` mobile app.

Setup

A. Update .env file

B. Building standalone apps

Android: `expo build:android -t apk`

IOS: `expo build:ios`

### Android Signing:

#### Option 1:

Let expo generate the keystore for you. It contains the signing key and upload key

On the first build, if you choose "let expo handle it for you", fetch the keystore:

`expo fetch:android:keystore`

Extract your upload cert in to a .pem file:

`expo fetch:android:upload-cert`

_Clearing expo keystore: `expo build:android --clear-credentials`_

#### Option 2:

Create your own keystore.

```keytool -genkey -v -keystore \
   <keystore-name>.keystore \
   -alias <keystore-alias> \
   -keyalg RSA -keysize 2048 -validity 10000
```

Create upload key:

```
keytool -export -rfc \
  -keystore <keystore-name>.keystore \
  -alias <keystore-alias> \
  -file entangle_upload_cert.pem \
```

#### Option 3:

Create your own keystore and your upload key and let google play handle app signing key for you. (Recommended)

---

### Building stand alone app on self hosted server.

A. Android

Setup turtle for the first time:

0. `npm run turtle setup:android --sdk-version 39.0.0`

1. Export credentials:

```
EXPO_ANDROID_KEYSTORE_PASSWORD=
EXPO_ANDROID_KEY_PASSWORD=
EXPO_KEYSTORE_ALIAS=
```

2. Create the js bundles on `dist` folder:

`expo export --dev --force --public-url http://127.0.0.1:8000`

3. Serve the `dist` folder.

`./server`

4. Create the app-bundle|apk/ipa: `npm run build`
