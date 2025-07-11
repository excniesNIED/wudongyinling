// src/utils/request.js
import axios from 'axios';
import { ElMessage } from 'element-plus';

// 创建 axios 实例
const service = axios.create({
  baseURL: 'http://localhost:8000', // 后端 API 基础 URL
  timeout: 5000 // 请求超时时间
});

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 在发送请求之前做些什么
    const token = localStorage.getItem('user-token');
    if (token) {
      // 让每个请求携带自定义 token 请根据实际情况自行修改
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    // 对请求错误做些什么
    console.error('Request error:', error); // for debug
    return Promise.reject(error);
  }
);

// 响应拦截器
service.interceptors.response.use(
  response => {
    // 对响应数据做点什么
    const res = response.data;
    // 如果自定义代码不是20000，则判断为错误。
    // 这里可以根据你的后端接口规范进行调整
    // if (res.code !== 20000) { 
    //   ElMessage.error(res.message || 'Error');
    //   return Promise.reject(new Error(res.message || 'Error'));
    // }
    return res; // 直接返回 data
  },
  error => {
    // 对响应错误做点什么
    console.error('Response error:', error); // for debug
    let message = error.message;
    if (error.response && error.response.data && error.response.data.detail) {
        message = error.response.data.detail;
    }
    ElMessage.error(message);
    return Promise.reject(error);
  }
);

export default service; 