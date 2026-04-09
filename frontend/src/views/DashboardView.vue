<template>
  <div class="layout">
    <Navbar />

    <div class="content">
      <!-- Sidebar -->
      <CategoryPanel
        :categories="store.categories"
        :active-id="store.activeCategoryId"
        @select="store.setActiveCategory"
        @add="openCategoryModal(null)"
        @edit="openCategoryModal"
        @delete="confirmDeleteCategory"
      />

      <!-- Main area -->
      <main class="main">
        <div class="main__toolbar">
          <h2 class="main__heading">
            {{ activeLabel }}
            <span class="main__count">{{ store.filteredBookmarks.length }}</span>
          </h2>
          <BaseButton @click="openBookmarkModal(null)">
            <svg width="14" height="14" viewBox="0 0 16 16" fill="none" style="margin-right:4px">
              <path d="M8 2v12M2 8h12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            添加书签
          </BaseButton>
        </div>

        <div v-if="store.loading" class="main__loading">
          <span class="spinner" />
        </div>

        <div v-else-if="store.filteredBookmarks.length === 0" class="main__empty">
          <p>暂无书签</p>
          <BaseButton variant="secondary" @click="openBookmarkModal(null)">添加第一个书签</BaseButton>
        </div>

        <!-- 全部书签：按分类分组展示 -->
        <template v-else-if="store.activeCategoryId === null">
          <template v-for="(group, idx) in groupedBookmarks" :key="group.categoryId ?? 'uncategorized'">
            <hr v-if="idx > 0" class="group-divider" />
            <div class="group">
              <h3 class="group__name">{{ group.name }}</h3>
              <div class="bookmark-grid">
                <BookmarkCard
                  v-for="bm in group.bookmarks"
                  :key="bm.id"
                  :bookmark="bm"
                  @edit="openBookmarkModal"
                  @delete="confirmDeleteBookmark"
                />
              </div>
            </div>
          </template>
        </template>

        <!-- 单分类：直接平铺 -->
        <div v-else class="bookmark-grid">
          <BookmarkCard
            v-for="bm in store.filteredBookmarks"
            :key="bm.id"
            :bookmark="bm"
            @edit="openBookmarkModal"
            @delete="confirmDeleteBookmark"
          />
        </div>
      </main>
    </div>

    <!-- Modals -->
    <BookmarkModal
      v-model="bookmarkModalOpen"
      :bookmark="editingBookmark"
      :categories="store.categories"
      @save="handleSaveBookmark"
    />

    <CategoryModal
      v-model="categoryModalOpen"
      :category="editingCategory"
      @save="handleSaveCategory"
    />

    <ConfirmModal
      v-model="confirmOpen"
      :title="confirmTitle"
      :message="confirmMessage"
      :loading="confirmLoading"
      @confirm="handleConfirm"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useBookmarksStore } from '@/stores/bookmarks'
import Navbar from '@/components/Navbar.vue'
import CategoryPanel from '@/components/CategoryPanel.vue'
import BookmarkCard from '@/components/BookmarkCard.vue'
import BookmarkModal from '@/components/BookmarkModal.vue'
import CategoryModal from '@/components/CategoryModal.vue'
import ConfirmModal from '@/components/ConfirmModal.vue'
import BaseButton from '@/components/BaseButton.vue'
import type { Bookmark } from '@/api/bookmarks'
import type { Category } from '@/api/categories'

const store = useBookmarksStore()

onMounted(() => store.fetchAll())

// ── Grouped bookmarks (全部模式下按分类分组) ──────────────────────────────────
const groupedBookmarks = computed(() => {
  const groups: { categoryId: number | null; name: string; bookmarks: typeof store.bookmarks }[] = []

  // 先按已有分类排列
  for (const cat of store.categories) {
    const bms = store.bookmarks.filter((b) => b.category_id === cat.id)
    if (bms.length > 0) groups.push({ categoryId: cat.id, name: cat.name, bookmarks: bms })
  }

  // 最后放无分类
  const uncategorized = store.bookmarks.filter((b) => b.category_id === null)
  if (uncategorized.length > 0) groups.push({ categoryId: null, name: '未分类', bookmarks: uncategorized })

  return groups
})

// ── Labels ────────────────────────────────────────────────────────────────────
const activeLabel = computed(() => {
  if (store.activeCategoryId === null) return '全部书签'
  return store.categories.find((c) => c.id === store.activeCategoryId)?.name ?? '书签'
})

// ── Bookmark modal ────────────────────────────────────────────────────────────
const bookmarkModalOpen = ref(false)
const editingBookmark = ref<Bookmark | null>(null)

function openBookmarkModal(bm: Bookmark | null) {
  editingBookmark.value = bm
  bookmarkModalOpen.value = true
}

async function handleSaveBookmark(data: { title: string; url: string; description: string; category_id: number | null }) {
  if (editingBookmark.value) {
    await store.updateBookmark(editingBookmark.value.id, data)
  } else {
    await store.createBookmark(data)
  }
  bookmarkModalOpen.value = false
}

// ── Category modal ────────────────────────────────────────────────────────────
const categoryModalOpen = ref(false)
const editingCategory = ref<Category | null>(null)

function openCategoryModal(cat: Category | null) {
  editingCategory.value = cat
  categoryModalOpen.value = true
}

async function handleSaveCategory(name: string) {
  if (editingCategory.value) {
    await store.updateCategory(editingCategory.value.id, name)
  } else {
    await store.createCategory(name)
  }
  categoryModalOpen.value = false
}

// ── Confirm delete ────────────────────────────────────────────────────────────
const confirmOpen = ref(false)
const confirmTitle = ref('')
const confirmMessage = ref('')
const confirmLoading = ref(false)
let confirmAction: (() => Promise<void>) | null = null

function confirmDeleteBookmark(bm: Bookmark) {
  confirmTitle.value = '删除书签'
  confirmMessage.value = `确定要删除「${bm.title}」吗？此操作不可撤销。`
  confirmAction = () => store.deleteBookmark(bm.id)
  confirmOpen.value = true
}

function confirmDeleteCategory(cat: Category) {
  confirmTitle.value = '删除分类'
  confirmMessage.value = `确定要删除分类「${cat.name}」吗？该分类下的书签将变为无分类。`
  confirmAction = () => store.deleteCategory(cat.id)
  confirmOpen.value = true
}

async function handleConfirm() {
  if (!confirmAction) return
  confirmLoading.value = true
  try {
    await confirmAction()
    confirmOpen.value = false
  } finally {
    confirmLoading.value = false
    confirmAction = null
  }
}
</script>

<style scoped>
.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-surface-alt);
}

.content {
  display: flex;
  flex: 1;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  padding: 32px 24px;
  gap: 24px;
}

.main {
  flex: 1;
  min-width: 0;
}

.main__toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.main__heading {
  font-size: 20px;
  font-weight: 500;
  color: var(--color-heading);
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.main__count {
  font-size: 13px;
  font-weight: 400;
  color: var(--color-placeholder);
}

.main__loading {
  display: flex;
  justify-content: center;
  padding: 64px 0;
}

.spinner {
  width: 24px;
  height: 24px;
  border: 2px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.main__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 80px 0;
  color: var(--color-placeholder);
  font-size: 14px;
}

.group-divider {
  border: none;
  border-top: 1px solid var(--color-border);
  margin: 16px 0;
}

.group__name {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-placeholder);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-bottom: 12px;
}

.bookmark-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
}

@media (max-width: 768px) {
  .content {
    flex-direction: column;
    padding: 16px;
  }
  .bookmark-grid {
    grid-template-columns: 1fr;
  }
}
</style>
