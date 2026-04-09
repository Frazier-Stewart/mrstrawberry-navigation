import client from './client'

export interface UserResponse {
  id: number
  email: string
  is_active: boolean
  created_at: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export const authApi = {
  register(email: string, password: string) {
    return client.post<UserResponse>('/auth/register', { email, password })
  },
  login(email: string, password: string) {
    return client.post<TokenResponse>('/auth/login', { email, password })
  },
  forgotPassword(email: string) {
    return client.post('/auth/forgot-password', { email })
  },
  resetPassword(token: string, new_password: string) {
    return client.post('/auth/reset-password', { token, new_password })
  },
  getMe() {
    return client.get<UserResponse>('/auth/me')
  },
  changePassword(old_password: string, new_password: string) {
    return client.post('/auth/change-password', { old_password, new_password })
  },
}
