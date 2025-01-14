import React from "react";
import { View, Text, ActivityIndicator } from "react-native";
import API, { endpoints } from "../../configs/API";  // Đảm bảo bạn có API cấu hình đúng

const Home = () => {
  const [danhmuc, setDanhmuc] = React.useState(null);

  React.useEffect(() => {
    const loaddanhmuc = async () => {
      try {
        let res = await API.get(endpoints['danh-muc']);
        setDanhmuc(res.data);
      } catch (ex) {
        // Kiểm tra lỗi trong khi gọi API
        if (ex.response) {
          console.error('Server error:', ex.response.data);  // Lỗi từ server
        } else if (ex.request) {
          console.error('No response received:', ex.request);  // Không nhận được phản hồi
        } else {
          console.error('Axios error:', ex.message);  // Lỗi Axios khác
        }
      }
    };

    loaddanhmuc();
  }, []);

  return (
    <View>
      <Text>CHÀO MỪNG ĐẾN VỚI TRANG THƯƠNG MẠI ĐIỆN TỬ</Text>
      {danhmuc === null ? (
        <ActivityIndicator />
      ) : (
        danhmuc.map((d) => (
          <View key={d.id}>
            <Text>{d.ten}</Text>
          </View>
        ))
      )}
    </View>
  );
};

export default Home;
