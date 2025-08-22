import { createStackNavigator } from '@react-navigation/stack';
import Home from "./index";
import SendImageScreen from "./src/screens/send_image_screen";

const Stack = createStackNavigator();


export default function AppNavigator() {
  return (
    <Stack.Navigator screenOptions={{
        headerStyle: {
          backgroundColor: '#f4511e',
        },
        headerTintColor: '#fff',
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      }}>
        <Stack.Screen name="Home" component={Home} options={{ headerShown: false }} />
        <Stack.Screen name="SendImageScreen" component={SendImageScreen} options={{ title: 'Send Image' }} />
    </Stack.Navigator>
  );
}
