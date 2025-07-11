import request from '@/utils/request';

export function login(data) {
  return request({
    url: '/auth/login',
    method: 'post',
    data
  });
}

export function getInfo() {
  return request({
    url: '/users/me',
    method: 'get'
  });
}
