import { useContext } from "react";
import { Button } from "react-native";
import MyContext from "../../configs/MyContext";

const Logout = ({ navigation }) => {
    const [user, dispatch] = useContext(MyContext);

    const handleLogout = () => {
        dispatch({
            type: "logout",
        });
        navigation.navigate("Login");
    };

    if (user === null) {
        return <Button title="Đăng Nhập" onPress={() => navigation.navigate("Login")} />;
    }

    return <Button title="Đăng Xuất" onPress={handleLogout} />;
};

export default Logout;
