<template>
  <BaseModal :model-value="modelValue" :title="isEdit ? '编辑分类' : '新建分类'" @update:model-value="close">
    <form @submit.prevent="handleSubmit" class="form">
      <BaseInput label="分类名称" v-model="name" placeholder="如：工作、娱乐、工具" :error="error" />
      <div class="form__actions">
        <BaseButton variant="secondary" type="button" @click="close">取消</BaseButton>
        <BaseButton type="submit" :loading="loading">{{ isEdit ? '保存' : '创建' }}</BaseButton>
      </div>
    </form>
  </BaseModal>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import BaseModal from './BaseModal.vue'
import BaseInput from './BaseInput.vue'
import BaseButton from './BaseButton.vue'
import type { Category } from '@/api/categories'

const props = defineProps<{
  modelValue: boolean
  category?: Category | null
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  save: [name: string]
}>()

const loading = ref(false)
const name = ref('')
const error = ref('')
const isEdit = computed(() => !!props.category)

watch(
  () => props.modelValue,
  (open) => {
    if (open) {
      name.value = props.category?.name ?? ''
      error.value = ''
    }
  }
)

async function handleSubmit() {
  if (!name.value.trim()) { error.value = '请输入分类名称'; return }
  loading.value = true
  try {
    emit('save', name.value.trim())
  } finally {
    loading.value = false
  }
}

function close() {
  emit('update:modelValue', false)
}
</script>

<style scoped>
.form { display: flex; flex-direction: column; gap: 20px; }
.form__actions { display: flex; gap: 12px; justify-content: flex-end; padding-top: 8px; }
</style>
