import { useContext, useState } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { TextInput } from 'react-native-gesture-handler';
import MyContext from '../../configs/MyContext';

const Login = ({ navigation }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [user, dispatch] = useContext(MyContext);

  const login = () => {
    if (username === 'admin' && password === '123') {
      dispatch({
        type: "login",
        payload: {
          username: "admin"
        }
      });

      navigation.navigate("Home");
    } else {
      alert("Sai tên đăng nhập hoặc mật khẩu!");
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <Text>Đăng Nhập</Text>
      <TextInput 
        value={username} 
        onChangeText={t => setUsername(t)} 
        placeholder="Tên Đăng Nhập..." 
        style={{ borderWidth: 1, marginVertical: 10, padding: 8 }} 
      />
      <TextInput 
        value={password} 
        onChangeText={t => setPassword(t)} 
        secureTextEntry={true} 
        placeholder="Mật Khẩu..." 
        style={{ borderWidth: 1, marginVertical: 10, padding: 8 }} 
      />
      <TouchableOpacity onPress={login} style={{ backgroundColor: 'blue', padding: 10 }}>
        <Text style={{ color: 'white', textAlign: 'center' }}>Đăng Nhập</Text>
      </TouchableOpacity>
    </View>
  );
};

export default Login;
