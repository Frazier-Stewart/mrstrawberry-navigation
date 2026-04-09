import client from './client'

export interface Category {
  id: number
  name: string
  sort_order: number
  owner_id: number
  created_at: string
}

export const categoriesApi = {
  list() {
    return client.get<Category[]>('/categories')
  },
  create(name: string, sort_order = 0) {
    return client.post<Category>('/categories', { name, sort_order })
  },
  update(id: number, data: Partial<{ name: string; sort_order: number }>) {
    return client.put<Category>(`/categories/${id}`, data)
  },
  remove(id: number) {
    return client.delete(`/categories/${id}`)
  },
}
