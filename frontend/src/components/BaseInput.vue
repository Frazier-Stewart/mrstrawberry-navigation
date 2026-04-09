<template>
  <div class="field">
    <label v-if="label" class="field__label">{{ label }}</label>
    <input
      v-bind="$attrs"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :class="['field__input', { 'field__input--error': error }]"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
    <span v-if="error" class="field__error">{{ error }}</span>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  label?: string
  modelValue: string
  type?: string
  placeholder?: string
  error?: string
}>()
defineEmits<{ 'update:modelValue': [value: string] }>()
</script>

<style scoped>
.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field__label {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-heading);
}

.field__input {
  background: transparent;
  border: none;
  border-bottom: 1px solid var(--color-border-subtle);
  padding: 10px 0;
  font-size: 14px;
  color: var(--color-heading);
  outline: none;
  transition: border-color var(--transition);
  width: 100%;
}

.field__input::placeholder {
  color: var(--color-placeholder);
}

.field__input:focus {
  border-bottom-color: var(--color-primary);
}

.field__input--error {
  border-bottom-color: var(--color-error);
}

.field__error {
  font-size: 12px;
  color: var(--color-error);
}
</style>
