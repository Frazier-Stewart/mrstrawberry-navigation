<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="modelValue" class="overlay" @click.self="$emit('update:modelValue', false)">
        <div class="panel">
          <div class="panel__header">
            <h3 class="panel__title">{{ title }}</h3>
            <button class="panel__close" @click="$emit('update:modelValue', false)" aria-label="关闭">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M2 2l12 12M14 2L2 14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
          <div class="panel__body">
            <slot />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
defineProps<{ modelValue: boolean; title: string }>()
defineEmits<{ 'update:modelValue': [value: boolean] }>()
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: var(--color-overlay);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 16px;
}

.panel {
  background: var(--color-surface);
  width: 100%;
  max-width: 480px;
  max-height: 90vh;
  overflow-y: auto;
  border-radius: var(--radius-card);
}

.panel__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 24px 0;
}

.panel__title {
  font-size: 17px;
  font-weight: 500;
  color: var(--color-heading);
}

.panel__close {
  color: var(--color-tertiary);
  padding: 4px;
  border-radius: 4px;
  transition: color var(--transition);
  cursor: pointer;
  background: none;
  border: none;
}
.panel__close:hover { color: var(--color-heading); }

.panel__body {
  padding: 24px;
}

/* Transition */
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.2s ease;
}
.modal-enter-from, .modal-leave-to {
  opacity: 0;
}
</style>
