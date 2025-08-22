import { RouteProp } from "@react-navigation/native";
import { useNavigation } from "expo-router";
import { useEffect } from "react";
import { StyleSheet, Text, View } from "react-native";

type SendImageScreenProps = {
  route: RouteProp<Record<string, object | undefined>, string>;
};

export default function SendImageScreen({ route }: SendImageScreenProps) {
    const navigation = useNavigation();
    useEffect(() => {
        navigation.setOptions({ headerShown: true, title: "Send Image" });
    }, [navigation])

    return (
        <View style={styles.container}>
            <Text>Send Image Screen</Text>
            {/* Add image sending functionality here */}
        </View>
    );
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  }});