import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 20000
})

export const analyze = (filename: string, code: string) => api.post('/analyze', { filename, code })
export const getHistory = () => api.get('/history')

export default api
