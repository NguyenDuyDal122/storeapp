import { createDrawerNavigator } from '@react-navigation/drawer';
import { NavigationContainer } from '@react-navigation/native';
import { StyleSheet, Text, View } from 'react-native';
import Login from './components/User/Login';
import Home from './components/Home/Home';
import MyContext from './configs/MyContext';
import { useReducer } from 'react';
import MyUserReducer from './reducers/MyUserReducer';
import Logout from './components/User/Logout';

const Drawer = createDrawerNavigator();

const App = () => {
  const [user, dispatch] = useReducer(MyUserReducer, null);

  return (
    <MyContext.Provider value={[user, dispatch]}>
      <NavigationContainer>
        <Drawer.Navigator
          screenOptions={({ navigation }) => ({
            headerRight: () => <Logout navigation={navigation} />,
          })}
        >
          {user === null ? (
            <Drawer.Screen 
              name="Login" 
              component={Login} 
              options={{ title: 'Đăng Nhập' }} 
            />
          ) : (
            <>
              <Drawer.Screen 
                name="Home" 
                component={Home} 
                options={{ title: 'Trang Chủ' }} 
              />
              <Drawer.Screen 
                name={user.username} 
                component={Home} 
                options={{ title: user.username }} 
              />
            </>
          )}
        </Drawer.Navigator>
      </NavigationContainer>
    </MyContext.Provider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});

export default App;
