### Sample calculator app using React Native

Setup:

0. Append this to your bash/zshrc. Make sure android studio is installed or you can just install the sdk and use your own phone for development instead of emulators.

    ```
    export ANDROID_HOME=$HOME/Android/Sdk
    export PATH=$PATH:$ANDROID_HOME/emulator
    export PATH=$PATH:$ANDROID_HOME/tools
    export PATH=$PATH:$ANDROID_HOME/tools/bin
    export PATH=$PATH:$ANDROID_HOME/platform-tools
    export PATH="$HOME/.yarn/bin:$HOME/.config/yarn/global/node_modules/.bin:$PATH"
    ```

1. Install create-react-native-app

    `npm install -g react-native-cli`

2. Create your app 

    `react-native-cli init <app-name>`

3. Install dependencies

    `yarn install`

4. List and run emulator 
    
    `emulator -list-avds`
    
    `emulator -avd  <emulator-name>`

5. Run app on the emulator (android)

    `react-native run-android`

Optional setup (Shake the device to show menu):

    Enable live and hot reloading

    Enable remote debugging
