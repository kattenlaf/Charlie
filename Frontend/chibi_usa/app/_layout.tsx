import { createStackNavigator } from '@react-navigation/stack';
import Home from "./index";
import LandingStack from "./src/screens/_layout";

const IndexStack = createStackNavigator();

export default function AppNavigator() {
  return (
    <IndexStack.Navigator screenOptions={{
        headerStyle: {
          backgroundColor: '#f4511e',
        },
        headerTintColor: '#fff',
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      }}>
        <IndexStack.Screen name="Home" component={Home} options={{ headerShown: false }} />
        <IndexStack.Screen name="LandingStack" component={LandingStack} options={{ headerShown: false }} />
    </IndexStack.Navigator>
  );
}
