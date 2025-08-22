import { RouteProp } from "@react-navigation/native";
import { useNavigation } from "expo-router";
import { useEffect } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";
import styles from "../utils/styles";

type SendImageScreenProps = {
  route: RouteProp<Record<string, object | undefined>, string>;
};

export default function SendImageScreen({ route }: SendImageScreenProps) {
    const navigation = useNavigation();
    useEffect(() => {
        navigation.setOptions({ headerShown: true, title: "Send Image" });
    }, [navigation])

    const OpenCameraButton = () => {
      return (
        <Pressable style={styles.button} onPress={openCamera}>
          <Text style={styles.buttonText}>Open Camera</Text>
        </Pressable>
      )
    }

    return (
        <View style={send_image_screen_styles.container}>
            <OpenCameraButton />
        </View>
    );
}

function openCamera() {
  // TODO: Route to camera screen or open camera modal
  // Placeholder function for opening camera
  console.log("Camera opened!");
}

function sendImage() {
  //TODO: Placeholder function for sending image to backend server for processing
  console.log("Image sent!");
}


const send_image_screen_styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  }});