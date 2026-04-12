<template>
  <!-- 简化模式：纯文字链接 -->
  <template v-if="simple">
    <a 
      :href="bookmark.url" 
      target="_blank" 
      rel="noopener noreferrer" 
      class="simple-link"
      :data-id="bookmark.id"
    >
      {{ bookmark.title }}
    </a>
  </template>
  
  <!-- 正常模式：卡片 -->
  <div v-else class="card bookmark-card" :data-id="bookmark.id">
    <a :href="bookmark.url" target="_blank" rel="noopener noreferrer" class="card__link">
      <img
        class="card__favicon"
        :src="faviconUrl"
        :alt="bookmark.title"
        @error="onFaviconError"
      />
      <div class="card__info">
        <span class="card__title">{{ bookmark.title }}</span>
        <span class="card__url">{{ displayUrl }}</span>
      </div>
    </a>
    <div class="card__actions">
      <button class="card__icon-btn" @click="$emit('edit', bookmark)" title="编辑">
        <svg width="13" height="13" viewBox="0 0 16 16" fill="none">
          <path d="M11.5 2.5l2 2-9 9H2.5v-2l9-9z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>
        </svg>
      </button>
      <button class="card__icon-btn card__icon-btn--danger" @click="$emit('delete', bookmark)" title="删除">
        <svg width="13" height="13" viewBox="0 0 16 16" fill="none">
          <path d="M2 4h12M5 4V2h6v2M6 7v5M10 7v5M3 4l1 10h8l1-10" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { Bookmark } from '@/api/bookmarks'

const props = defineProps<{ 
  bookmark: Bookmark
  simple?: boolean
}>()
defineEmits<{ edit: [b: Bookmark]; delete: [b: Bookmark] }>()

const faviconError = ref(false)

const faviconUrl = computed(() => {
  if (faviconError.value) return defaultFavicon
  if (props.bookmark.favicon_url) return props.bookmark.favicon_url
  try {
    const hostname = new URL(props.bookmark.url).hostname
    return `https://www.google.com/s2/favicons?sz=64&domain=${hostname}`
  } catch {
    return defaultFavicon
  }
})

const defaultFavicon = `data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><rect width='16' height='16' rx='3' fill='%23EEEEEE'/><text x='8' y='12' text-anchor='middle' font-size='10' fill='%238E8E8E'>🔗</text></svg>`

const displayUrl = computed(() => {
  try {
    const hostname = new URL(props.bookmark.url).hostname.replace('www.', '')
    return hostname.length > 20 ? hostname.slice(0, 20) + '...' : hostname
  } catch {
    const url = props.bookmark.url
    return url.length > 20 ? url.slice(0, 20) + '...' : url
  }
})

function onFaviconError() {
  faviconError.value = true
}
</script>

<style scoped>
.card {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background: var(--color-surface);
  border-radius: var(--radius-card);
  border: 1px solid var(--color-border);
  transition: border-color var(--transition);
  gap: 12px;
}
.card:hover {
  border-color: var(--color-border-subtle);
}

.card__link {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  min-width: 0;
  text-decoration: none;
}

.card__favicon {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  object-fit: contain;
  flex-shrink: 0;
  background: var(--color-surface-alt);
}

.card__info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.card__title {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-heading);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card__url {
  font-size: 12px;
  color: var(--color-placeholder);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card__actions {
  display: none;
  gap: 4px;
  flex-shrink: 0;
}
.card:hover .card__actions { display: flex; }

.card__icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-placeholder);
  padding: 4px;
  border-radius: 4px;
  display: flex;
  transition: color var(--transition);
}
.card__icon-btn:hover { color: var(--color-body); }
.card__icon-btn--danger:hover { color: var(--color-error); }

/* Sortable drag styles */
.bookmark-card--ghost {
  opacity: 0.4;
  background: var(--color-surface-alt);
}
.bookmark-card--chosen {
  background: var(--color-surface-alt);
}
.bookmark-card--drag {
  opacity: 0.9;
  background: var(--color-surface);
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  cursor: grabbing;
}

/* 简化模式样式 */
.simple-link {
  color: var(--color-primary);
  text-decoration: none;
  font-size: 14px;
  line-height: 1.6;
}

.simple-link:hover {
  text-decoration: underline;
}
</style>
