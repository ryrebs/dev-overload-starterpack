import React from "react";
// import { Provider } from "react-redux";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
// import { PersistGate } from "redux-persist/integration/react";
import "./utils/i18n";
import { enableScreens } from "react-native-screens";
import { SafeAreaView, SafeAreaProvider } from "react-native-safe-area-context";
// import createStore from "./store";
import { Text } from "react-native";

// *Note: uncomment store related elements if you have atleast 1 reducer.

enableScreens();
// const {store, persistor} = createStore();

const Stack = createStackNavigator();

const MainScreen = () => (
  <SafeAreaView>
    <Text>Hello Main</Text>
  </SafeAreaView>
);
const App = () => (
  //   <Provider store={store}>
  //   <PersistGate loading={null} persistor={persistor}>
  <SafeAreaProvider>
    <NavigationContainer>
      <Stack.Navigator headerMode="none">
        <Stack.Screen name="MainScreen" component={MainScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  </SafeAreaProvider>
  //   </PersistGate>
  //   </Provider>
);

export default App;
