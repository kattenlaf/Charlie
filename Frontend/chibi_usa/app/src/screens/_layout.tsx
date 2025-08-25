import { createStackNavigator } from "@react-navigation/stack";
import LandingScreen from "./landing_screen";
import TakePictureScreen from "./take_picture_screen";

const LandingStack = createStackNavigator();

// https://reactnavigation.org/docs/screen-options/?config=static

export default function ScreenNavigator() {
    return (
        <LandingStack.Navigator screenOptions={{
            headerStyle: {
                backgroundColor: '#f4511e',
            },
            headerTintColor: '#fff',
            headerTitleStyle: {
                fontWeight: 'bold',
            },
        }}>
            <LandingStack.Screen name="SendImageScreen" component={LandingScreen} options={{ title: 'Main Menu' }} />
            <LandingStack.Screen name="TakePictureScreen" component={TakePictureScreen} options={{ title: 'Take Picture' }} />
        </LandingStack.Navigator>
    );
}