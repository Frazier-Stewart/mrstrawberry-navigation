import client from './client'

export interface Bookmark {
  id: number
  title: string
  url: string
  description: string | null
  favicon_url: string | null
  sort_order: number
  category_id: number | null
  owner_id: number
  created_at: string
  updated_at: string
}

export interface BookmarkCreate {
  title: string
  url: string
  description?: string
  favicon_url?: string
  category_id?: number | null
  sort_order?: number
}

export const bookmarksApi = {
  list(category_id?: number | null) {
    const params = category_id != null ? { category_id } : {}
    return client.get<Bookmark[]>('/bookmarks', { params })
  },
  create(data: BookmarkCreate) {
    return client.post<Bookmark>('/bookmarks', data)
  },
  update(id: number, data: Partial<BookmarkCreate>) {
    return client.put<Bookmark>(`/bookmarks/${id}`, data)
  },
  remove(id: number) {
    return client.delete(`/bookmarks/${id}`)
  },
  updateSortOrder(items: { id: number; sort_order: number }[]) {
    return client.post('/bookmarks/sort/batch', items)
  },
}
