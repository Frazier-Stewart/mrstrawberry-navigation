<template>
  <BaseModal :model-value="modelValue" :title="title" @update:model-value="$emit('update:modelValue', $event)">
    <p class="message">{{ message }}</p>
    <div class="actions">
      <BaseButton variant="secondary" @click="$emit('update:modelValue', false)">取消</BaseButton>
      <BaseButton variant="danger" :loading="loading" @click="$emit('confirm')">确认删除</BaseButton>
    </div>
  </BaseModal>
</template>

<script setup lang="ts">
import BaseModal from './BaseModal.vue'
import BaseButton from './BaseButton.vue'

defineProps<{
  modelValue: boolean
  title: string
  message: string
  loading?: boolean
}>()
defineEmits<{
  'update:modelValue': [value: boolean]
  confirm: []
}>()
</script>

<style scoped>
.message {
  color: var(--color-body);
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 24px;
}
.actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}
</style>
