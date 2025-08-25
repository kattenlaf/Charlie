import { RouteProp } from "@react-navigation/native";
import { useNavigation } from "expo-router";
import { Pressable, StyleSheet, Text, View } from "react-native";
import styles from "../utils/styles";

type SendImageScreenProps = {
  route: RouteProp<Record<string, object | undefined>, string>;
};

export default function LandingScreen({ route }: SendImageScreenProps) {
    const navigation = useNavigation();

    const OpenCameraButton = () => {
      return (
        <Pressable style={styles.button} onPress={() => openCamera(navigation)}>
          <Text style={styles.buttonText}>Open Camera</Text>
        </Pressable>
      )
    }

    return (
        <View style={landing_screen_styles.container}>
            <OpenCameraButton />
        </View>
    );
}

function openCamera(navigation: any) {
  // TODO: Route to camera screen or open camera modal
  // Placeholder function for opening camera
  // check permissions first and then open camera
  var parentStackName = 'AppNavigator'; // Example parent stack name
  var targetScreenName = 'TakePictureScreen'; // Example target screen name
  navigation.navigate('LandingStack', {screen: 'TakePictureScreen'}); // Navigate to parent stack
}

const landing_screen_styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  }
});