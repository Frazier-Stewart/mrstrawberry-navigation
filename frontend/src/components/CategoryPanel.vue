<template>
  <aside :class="['panel', { 'panel--collapsed': collapsed }]">
    <div class="panel__header">
      <span v-if="!collapsed" class="panel__title">分类</span>
      <div class="panel__actions">
        <!-- 展开/收起按钮 -->
        <button
          class="panel__collapse-btn"
          @click="toggleCollapse"
          :title="collapsed ? '展开' : '收起'"
        >
          <svg v-if="!collapsed" width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M11 2L6 8l5 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <svg v-else width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M5 2l5 6-5 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <template v-if="!collapsed">
          <button
            :class="['panel__sort-btn', { 'panel__sort-btn--active': sortMode }]"
            @click="toggleSortMode"
            :title="sortMode ? '完成排序' : '排序分类'"
          >
            <svg v-if="!sortMode" width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M2 4h12M2 7h12M2 10h8" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
              <path d="M11 11l2 2 2-2" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <svg v-else width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M2 4h12M2 7h12M2 10h8" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
              <path d="M11 15l2-2 2 2" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <button class="panel__add" @click="$emit('add')" title="新建分类">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M8 2v12M2 8h12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </button>
        </template>
      </div>
    </div>

    <!-- 收起模式：简洁图标列表 -->
    <ul v-if="collapsed" class="panel__list panel__list--collapsed">
      <li>
        <button
          :class="['panel__item panel__item--icon', { 'panel__item--active': activeId === null }]"
          @click="$emit('select', null)"
          title="全部"
        >
          <svg width="18" height="18" viewBox="0 0 16 16" fill="none">
            <rect x="2" y="2" width="5" height="5" rx="1" stroke="currentColor" stroke-width="1.4"/>
            <rect x="9" y="2" width="5" height="5" rx="1" stroke="currentColor" stroke-width="1.4"/>
            <rect x="2" y="9" width="5" height="5" rx="1" stroke="currentColor" stroke-width="1.4"/>
            <rect x="9" y="9" width="5" height="5" rx="1" stroke="currentColor" stroke-width="1.4"/>
          </svg>
        </button>
      </li>
      <li v-for="cat in categories" :key="cat.id">
        <button
          :class="['panel__item panel__item--icon', { 'panel__item--active': activeId === cat.id }]"
          @click="$emit('select', cat.id)"
          :title="cat.name"
        >
          <span class="panel__initial">{{ cat.name.charAt(0).toUpperCase() }}</span>
        </button>
      </li>
    </ul>

    <!-- 正常模式：简洁列表 -->
    <ul v-else-if="!sortMode" class="panel__list">
      <li>
        <button
          :class="['panel__item', { 'panel__item--active': activeId === null }]"
          @click="$emit('select', null)"
        >
          全部
        </button>
      </li>
      <li v-for="cat in categories" :key="cat.id" class="panel__row">
        <button
          :class="['panel__item', { 'panel__item--active': activeId === cat.id }]"
          @click="$emit('select', cat.id)"
        >
          {{ cat.name }}
        </button>
        <div class="panel__row-actions">
          <button class="panel__icon-btn" @click="$emit('edit', cat)" title="编辑">
            <svg width="13" height="13" viewBox="0 0 16 16" fill="none">
              <path d="M11.5 2.5l2 2-9 9H2.5v-2l9-9z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>
            </svg>
          </button>
          <button class="panel__icon-btn panel__icon-btn--danger" @click="$emit('delete', cat)" title="删除">
            <svg width="13" height="13" viewBox="0 0 16 16" fill="none">
              <path d="M2 4h12M5 4V2h6v2M6 7v5M10 7v5M3 4l1 10h8l1-10" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </li>
    </ul>

    <!-- 排序模式：整个区域可拖拽 -->
    <ul v-else ref="sortListRef" class="panel__list panel__list--sort">
      <li class="panel__tip">拖拽调整顺序</li>
      <li
        v-for="cat in categories"
        :key="cat.id"
        :data-id="cat.id"
        class="panel__sort-item"
        title="拖拽排序"
      >
        <div class="panel__drag-indicator">
          <svg width="12" height="12" viewBox="0 0 16 16" fill="none">
            <circle cx="5" cy="4" r="1.5" fill="currentColor"/>
            <circle cx="11" cy="4" r="1.5" fill="currentColor"/>
            <circle cx="5" cy="8" r="1.5" fill="currentColor"/>
            <circle cx="11" cy="8" r="1.5" fill="currentColor"/>
            <circle cx="5" cy="12" r="1.5" fill="currentColor"/>
            <circle cx="11" cy="12" r="1.5" fill="currentColor"/>
          </svg>
        </div>
        <span class="panel__sort-name">{{ cat.name }}</span>
      </li>
    </ul>
  </aside>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue'
import Sortable from 'sortablejs'
import type { Category } from '@/api/categories'

const props = defineProps<{
  categories: Category[]
  activeId: number | null
}>()

const emit = defineEmits<{
  select: [id: number | null]
  add: []
  edit: [cat: Category]
  delete: [cat: Category]
  sort: [ids: number[]]
}>()

// 展开/收起状态
const collapsed = ref(false)
const sortMode = ref(false)
const sortListRef = ref<HTMLElement | null>(null)
let sortable: Sortable | null = null

function toggleCollapse() {
  collapsed.value = !collapsed.value
  // 收起时退出排序模式
  if (collapsed.value && sortMode.value) {
    sortMode.value = false
    if (sortable) {
      sortable.destroy()
      sortable = null
    }
  }
}

function toggleSortMode() {
  sortMode.value = !sortMode.value
  if (sortMode.value) {
    nextTick(() => initSortable())
  } else if (sortable) {
    sortable.destroy()
    sortable = null
  }
}

function initSortable() {
  if (!sortListRef.value) return

  sortable = new Sortable(sortListRef.value, {
    animation: 150,
    ghostClass: 'panel__sort-item--ghost',
    chosenClass: 'panel__sort-item--chosen',
    dragClass: 'panel__sort-item--drag',
    onEnd: (evt) => {
      if (evt.oldIndex === evt.newIndex) return
      
      const items = sortListRef.value?.querySelectorAll('.panel__sort-item')
      if (items) {
        const ids = Array.from(items).map(el => Number(el.getAttribute('data-id')))
        emit('sort', ids)
      }
    },
  })
}

onMounted(() => {
  if (sortMode.value) {
    initSortable()
  }
})
</script>

<style scoped>
.panel {
  width: 220px;
  flex-shrink: 0;
  padding: 8px 0;
  transition: width 0.2s ease;
}

.panel--collapsed {
  width: 60px;
}

.panel__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 16px 12px;
}

.panel--collapsed .panel__header {
  justify-content: center;
  padding: 8px 8px 12px;
}

.panel__title {
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-placeholder);
}

.panel__actions {
  display: flex;
  align-items: center;
  gap: 4px;
}

.panel--collapsed .panel__actions {
  justify-content: center;
}

.panel__add,
.panel__sort-btn,
.panel__collapse-btn {
  color: var(--color-tertiary);
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all var(--transition);
  display: flex;
}
.panel__add:hover,
.panel__sort-btn:hover,
.panel__collapse-btn:hover {
  color: var(--color-primary);
  background: var(--color-surface-alt);
}

.panel__sort-btn--active {
  color: var(--color-primary) !important;
  background: rgba(62, 106, 225, 0.1) !important;
}

.panel__list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

/* Collapsed mode */
.panel__list--collapsed {
  align-items: center;
  padding: 0 8px;
}

.panel__list--collapsed li {
  width: 100%;
}

.panel__item--icon {
  width: 44px;
  height: 44px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

.panel__initial {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--color-surface-alt);
  color: var(--color-body);
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
}

.panel__item--active .panel__initial {
  background: var(--color-primary);
  color: #fff;
}

.panel__tip {
  padding: 8px 16px;
  font-size: 12px;
  color: var(--color-placeholder);
  text-align: center;
}

.panel__row {
  display: flex;
  align-items: center;
}

.panel__item {
  flex: 1;
  text-align: left;
  padding: 8px 16px;
  font-size: 14px;
  color: var(--color-body);
  background: none;
  border: none;
  cursor: pointer;
  border-radius: var(--radius-btn);
  transition: background-color var(--transition), color var(--transition);
}
.panel__item:hover { background: var(--color-surface-alt); }
.panel__item--active {
  background: var(--color-surface-alt);
  color: var(--color-heading);
  font-weight: 500;
}

.panel__row-actions {
  display: none;
  gap: 2px;
  padding-right: 8px;
}
.panel__row:hover .panel__row-actions { display: flex; }

.panel__icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-placeholder);
  padding: 4px;
  border-radius: 4px;
  display: flex;
  transition: color var(--transition);
}
.panel__icon-btn:hover { color: var(--color-body); }
.panel__icon-btn--danger:hover { color: var(--color-error); }

/* Sort mode styles */
.panel__sort-item {
  display: flex;
  align-items: center;
  padding: 10px 16px;
  background: var(--color-surface);
  border-radius: var(--radius-btn);
  cursor: grab;
  transition: background-color var(--transition);
  margin-bottom: 4px;
}
.panel__sort-item:hover {
  background: var(--color-surface-alt);
}
.panel__sort-item:active {
  cursor: grabbing;
}

.panel__drag-indicator {
  color: var(--color-placeholder);
  margin-right: 10px;
  display: flex;
  align-items: center;
}

.panel__sort-name {
  flex: 1;
  font-size: 14px;
  color: var(--color-body);
}

/* Sortable drag styles */
.panel__sort-item--ghost {
  opacity: 0.4;
  background: var(--color-primary) !important;
}
.panel__sort-item--chosen {
  background: var(--color-surface-alt);
}
.panel__sort-item--drag {
  opacity: 0.9;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
</style>
