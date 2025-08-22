import { useNavigation } from "expo-router";
import { useEffect } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";


const Home = () => {
  const navigation = useNavigation();

  const SendImageScreenButton = () => {
  return(
    <Pressable style={styles.button} onPress={() => navigation.navigate('send_image_screen' as never)}>
      <Text style={styles.buttonText}>Go to Send Image Screen</Text>
    </Pressable>
    );
  };

  useEffect(() => {
    navigation.setOptions({ headerShown: true, title: "Home" });
  }, [navigation]);

  return (
    <View style={styles.container}>
      <Text>Login screen here or something</Text>
      <SendImageScreenButton />
    </View>
  );
}


export default Home;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  image: {
    width: 100,
    height: 100,
    marginBottom: 20,
  },
  button: {
    backgroundColor: "#1ef44cff",
    padding: 5,
    borderRadius: 10,
    alignContent: "center",
    alignItems: "center",
  },
  buttonText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "bold",
    textAlign: "center",
    textTransform: "uppercase",
    letterSpacing: 1,
    padding: 10,
  }
});