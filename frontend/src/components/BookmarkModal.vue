<template>
  <BaseModal :model-value="modelValue" :title="isEdit ? '编辑书签' : '添加书签'" @update:model-value="close">
    <form @submit.prevent="handleSubmit" class="form">
      <BaseInput label="标题" v-model="form.title" placeholder="网站名称" :error="errors.title" />
      <BaseInput label="网址" v-model="form.url" placeholder="https://example.com" :error="errors.url" />
      <BaseInput label="描述（可选）" v-model="form.description" placeholder="简短描述" />

      <div class="field">
        <label class="field__label">分类</label>
        <select class="field__select" v-model="form.category_id">
          <option :value="null">无分类</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
        </select>
      </div>

      <div class="form__actions">
        <BaseButton variant="secondary" type="button" @click="close">取消</BaseButton>
        <BaseButton type="submit" :loading="loading">{{ isEdit ? '保存' : '添加' }}</BaseButton>
      </div>
    </form>
  </BaseModal>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import BaseModal from './BaseModal.vue'
import BaseInput from './BaseInput.vue'
import BaseButton from './BaseButton.vue'
import type { Bookmark } from '@/api/bookmarks'
import type { Category } from '@/api/categories'

const props = defineProps<{
  modelValue: boolean
  bookmark?: Bookmark | null
  categories: Category[]
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  save: [data: { title: string; url: string; description: string; category_id: number | null }]
}>()

const loading = ref(false)
const isEdit = computed(() => !!props.bookmark)

const form = ref({ title: '', url: '', description: '', category_id: null as number | null })
const errors = ref({ title: '', url: '' })

watch(
  () => props.modelValue,
  (open) => {
    if (open) {
      form.value = {
        title: props.bookmark?.title ?? '',
        url: props.bookmark?.url ?? '',
        description: props.bookmark?.description ?? '',
        category_id: props.bookmark?.category_id ?? null,
      }
      errors.value = { title: '', url: '' }
    }
  }
)

function validate() {
  errors.value = { title: '', url: '' }
  if (!form.value.title.trim()) { errors.value.title = '请输入标题'; return false }
  if (!form.value.url.trim()) { errors.value.url = '请输入网址'; return false }
  try { new URL(form.value.url) } catch { errors.value.url = '请输入有效的网址'; return false }
  return true
}

async function handleSubmit() {
  if (!validate()) return
  loading.value = true
  try {
    emit('save', { ...form.value })
  } finally {
    loading.value = false
  }
}

function close() {
  emit('update:modelValue', false)
}
</script>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.field { display: flex; flex-direction: column; gap: 6px; }
.field__label { font-size: 13px; font-weight: 500; color: var(--color-heading); }
.field__select {
  background: transparent;
  border: none;
  border-bottom: 1px solid var(--color-border-subtle);
  padding: 10px 0;
  font-size: 14px;
  color: var(--color-heading);
  outline: none;
  cursor: pointer;
  transition: border-color var(--transition);
}
.field__select:focus { border-bottom-color: var(--color-primary); }

.form__actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding-top: 8px;
}
</style>
