<template>
  <aside class="panel">
    <div class="panel__header">
      <span class="panel__title">分类</span>
      <button class="panel__add" @click="$emit('add')" title="新建分类">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path d="M8 2v12M2 8h12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
      </button>
    </div>

    <ul class="panel__list">
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
  </aside>
</template>

<script setup lang="ts">
import type { Category } from '@/api/categories'

defineProps<{
  categories: Category[]
  activeId: number | null
}>()

defineEmits<{
  select: [id: number | null]
  add: []
  edit: [cat: Category]
  delete: [cat: Category]
}>()
</script>

<style scoped>
.panel {
  width: 220px;
  flex-shrink: 0;
  padding: 8px 0;
}

.panel__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 16px 12px;
}

.panel__title {
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-placeholder);
}

.panel__add {
  color: var(--color-tertiary);
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: color var(--transition);
  display: flex;
}
.panel__add:hover { color: var(--color-primary); }

.panel__list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 2px;
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
</style>
