import { StyleSheet } from 'react-native';

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

export default styles;