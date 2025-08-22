import { useNavigation } from "expo-router";
import { useEffect } from "react";
import { Pressable, Text, View } from "react-native";
import styles from "./src/utils/styles";


const Home = () => {
  const navigation = useNavigation();

  const SendImageScreenButton = () => {
  return(
    <Pressable style={styles.button} onPress={() => navigation.navigate('SendImageScreen' as never)}>
      <Text style={styles.buttonText}>Go to Send Image Screen</Text>
    </Pressable>
    );
  };

  useEffect(() => {
    navigation.setOptions({ headerShown: false, title: "Home" });
  }, [navigation]);

  return (
    <View style={styles.container}>
      <Text>Login screen here or something</Text>
      <SendImageScreenButton />
    </View>
  );
}


export default Home;