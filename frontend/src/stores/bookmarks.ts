import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { bookmarksApi, type Bookmark, type BookmarkCreate } from '@/api/bookmarks'
import { categoriesApi, type Category } from '@/api/categories'

export type ViewMode = 'card' | 'simple'

export const useBookmarksStore = defineStore('bookmarks', () => {
  const bookmarks = ref<Bookmark[]>([])
  const categories = ref<Category[]>([])
  const activeCategoryId = ref<number | null>(null)
  const loading = ref(false)
  
  // 视图模式：card = 卡片网格, simple = 简化文字列表
  const viewMode = ref<ViewMode>((localStorage.getItem('view_mode') as ViewMode) || 'card')
  
  const isSimpleMode = computed(() => viewMode.value === 'simple')
  
  function toggleViewMode() {
    viewMode.value = viewMode.value === 'card' ? 'simple' : 'card'
    localStorage.setItem('view_mode', viewMode.value)
  }

  const filteredBookmarks = computed(() => {
    if (activeCategoryId.value === null) return bookmarks.value
    return bookmarks.value.filter((b) => b.category_id === activeCategoryId.value)
  })

  async function fetchAll() {
    loading.value = true
    try {
      const [bRes, cRes] = await Promise.all([bookmarksApi.list(), categoriesApi.list()])
      bookmarks.value = bRes.data
      categories.value = cRes.data
    } finally {
      loading.value = false
    }
  }

  async function fetchCategories() {
    const res = await categoriesApi.list()
    categories.value = res.data
  }

  async function createCategory(name: string) {
    const res = await categoriesApi.create(name)
    categories.value.push(res.data)
    return res.data
  }

  async function updateCategory(id: number, name: string) {
    const res = await categoriesApi.update(id, { name })
    const idx = categories.value.findIndex((c) => c.id === id)
    if (idx !== -1) categories.value[idx] = res.data
    return res.data
  }

  async function deleteCategory(id: number) {
    await categoriesApi.remove(id)
    categories.value = categories.value.filter((c) => c.id !== id)
    bookmarks.value = bookmarks.value.map((b) =>
      b.category_id === id ? { ...b, category_id: null } : b
    )
    if (activeCategoryId.value === id) activeCategoryId.value = null
  }

  async function createBookmark(data: BookmarkCreate) {
    const res = await bookmarksApi.create(data)
    bookmarks.value.unshift(res.data)
    return res.data
  }

  async function updateBookmark(id: number, data: Partial<BookmarkCreate>) {
    const res = await bookmarksApi.update(id, data)
    const idx = bookmarks.value.findIndex((b) => b.id === id)
    if (idx !== -1) bookmarks.value[idx] = res.data
    return res.data
  }

  async function deleteBookmark(id: number) {
    await bookmarksApi.remove(id)
    bookmarks.value = bookmarks.value.filter((b) => b.id !== id)
  }

  function setActiveCategory(id: number | null) {
    activeCategoryId.value = id
  }

  return {
    bookmarks,
    categories,
    activeCategoryId,
    loading,
    viewMode,
    isSimpleMode,
    filteredBookmarks,
    fetchAll,
    fetchCategories,
    createCategory,
    updateCategory,
    deleteCategory,
    createBookmark,
    updateBookmark,
    deleteBookmark,
    setActiveCategory,
    toggleViewMode,
  }
})
