import AntDesign from "@expo/vector-icons/AntDesign";
import Feather from "@expo/vector-icons/Feather";
import FontAwesome6 from "@expo/vector-icons/FontAwesome6";
import { CameraMode, CameraType, CameraView, useCameraPermissions } from 'expo-camera';
import * as FileSystem from 'expo-file-system';
import { Image } from 'expo-image';
import { useNavigation } from "expo-router";
import { useRef, useState } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";
import * as AppConstants from '../utils/constants/constants';

// Taken from https://github.com/expo/examples/blob/master/with-camera/App.tsx
export default function TakePictureScreen() {
    const navigation = useNavigation();

    const [permission, requestPermission] = useCameraPermissions();
    const ref = useRef<CameraView>(null);
    const [uri, setUri] = useState<string | null>(null);
    const [mode, setMode] = useState<CameraMode>("picture");
    const [facing, setFacing] = useState<CameraType>("back");
    const [recording, setRecording] = useState(false);

    if (!permission) {
      return null;
    }

    if (!permission.granted) {
      return (
        <View style={take_picture_screen_styles.container}>
          <Text style={{ textAlign: "center" }}>
            We need your permission to show the camera
          </Text>
          <Pressable style={take_picture_screen_styles.permissionBtn} onPress={requestPermission}>
            <Text style={{ color: "white" }}>Grant permission</Text>
          </Pressable>
        </View>
      );
    }

    const takePicture = async () => {
    const photo = await ref.current?.takePictureAsync({shutterSound: false});
    const fileInfo = await FileSystem.getInfoAsync(photo?.uri ?? "");
    if (fileInfo.exists && 'size' in fileInfo) {
      console.log('File size:', (fileInfo as any).size);
    } else {
      console.log('File does not exist or size is unavailable');
    }
    setUri(photo?.uri ?? null);
    console.log({ photo });
    };

    const sendPictureToServer = async (imageUri: string) => {
      if (imageUri == null) {
        // TODO: Handle this error properly
        console.error('No image URI provided');
        return;
      }
      console.log('Preparing to upload image:', imageUri);
      const formData = new FormData();
      formData.append('image', {
        uri: imageUri,
        name: 'image.jpg',
        type: 'image/jpeg',
      } as any, 'photo.jpg');
      const headers = {
        'Content-Type': 'multipart/form-data',
        'Accept': 'application/json'
      };
      
      try {
        let route = '/upload_image';
        let upload_image_url = AppConstants.SCHEMA + AppConstants.HOST + ':' + AppConstants.PORT + route;
        const response = await fetch(upload_image_url, 
          {
          method: 'POST',
          headers,
          body: formData
          }
        )
        if (response.ok) {
          const data = response.json();
          console.log('uploading image was successful', data);
          // TODO: Probably respond with item details and then request confirmation from user, then prompt backend again for the next details
        } else {
          const errorText = await response.text();
          console.error('uploading image failed', errorText);
          // TODO: Attempt reupload? not sure how to render that
        }
      } catch (error) {
        console.error('Error uploading image:', error);
        // Handle error gracefully, potentially retrying based on error type
      }
    }


    const recordVideo = async () => {
        if (recording) {
        setRecording(false);
        ref.current?.stopRecording();
        return;
        }
        setRecording(true);
        const video = await ref.current?.recordAsync();
        console.log({ video });
    };

    const toggleMode = () => {
        setMode((prev) => (prev === "picture" ? "video" : "picture"));
    };

    const toggleFacing = () => {
        setFacing((prev) => (prev === "back" ? "front" : "back"));
    };

    const renderPicture = () => {
        return (
        <View>
            <Image
            source={uri ? { uri } : undefined}
            contentFit="contain"
            style={{ width: 300, aspectRatio: 1 }}
            />
            <Pressable style={[take_picture_screen_styles.permissionBtn, take_picture_screen_styles.takeAnotherPictureBtn]} onPress={() => setUri(null)}>
              <Text style={{ color: "white" }}>Take another Picture</Text>
            </Pressable>
            <Pressable
              style={[take_picture_screen_styles.permissionBtn, take_picture_screen_styles.uploadPictureBtn]} onPress={() => { if (uri) sendPictureToServer(uri); }}>
              <Text style={{ color: "white" }}>Upload Picture</Text>
            </Pressable>
        </View>
        );
    };

    const renderCamera = () => {
        return (
        <CameraView
            style={take_picture_screen_styles.camera}
            ref={ref}
            mode={mode}
            facing={facing}
            mute={false}
            responsiveOrientationWhenOrientationLocked
        >
            <View style={take_picture_screen_styles.shutterContainer}>
            <Pressable onPress={toggleMode}>
                {mode === "picture" ? (
                <AntDesign name="picture" size={32} color="white" />
                ) : (
                <Feather name="video" size={32} color="white" />
                )}
            </Pressable>
            <Pressable onPress={mode === "picture" ? takePicture : recordVideo}>
                {({ pressed }) => (
                <View
                    style={[
                    take_picture_screen_styles.shutterBtn,
                    {
                        opacity: pressed ? 0.5 : 1,
                    },
                    ]}
                >
                    <View
                    style={[
                        take_picture_screen_styles.shutterBtnInner,
                        {
                        backgroundColor: mode === "picture" ? "white" : "red",
                        },
                    ]}
                    />
                </View>
                )}
            </Pressable>
            <Pressable onPress={toggleFacing}>
                <FontAwesome6 name="rotate-left" size={32} color="white" />
            </Pressable>
            </View>
        </CameraView>
        );
    };


    return (
        <View style={take_picture_screen_styles.container}>
        {uri ? renderPicture() : renderCamera()}
        </View>
    );
}

const take_picture_screen_styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
  camera: {
    flex: 1,
    width: "100%",
  },
  shutterContainer: {
    position: "absolute",
    bottom: 44,
    left: 0,
    width: "100%",
    alignItems: "center",
    flexDirection: "row",
    justifyContent: "space-between",
    paddingHorizontal: 30,
  },
  shutterBtn: {
    backgroundColor: "transparent",
    borderWidth: 5,
    borderColor: "white",
    width: 85,
    height: 85,
    borderRadius: 45,
    alignItems: "center",
    justifyContent: "center",
  },
  shutterBtnInner: {
    width: 70,
    height: 70,
    borderRadius: 50,
  },
  permissionBtn: {
    alignItems: "center",
    padding: 8,
    backgroundColor: "blue",
    borderRadius: 5,
    marginTop: 35,
  },
  takeAnotherPictureBtn: {
    backgroundColor: "green",
  },
  uploadPictureBtn: {
    backgroundColor: "orange",
  }
});