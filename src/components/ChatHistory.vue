<template>
  <!-- Komponen Chat History untuk Bimbingan -->
  <div class="chat-container">
    <div class="chat-header">
      <div class="chat-header-info">
        <h4>💬 Riwayat Diskusi Bimbingan</h4>
        <span class="chat-count">{{ messages.length }} pesan</span>
      </div>
    </div>

    <!-- Area Pesan -->
    <div class="chat-messages" ref="chatArea">
      <div v-if="loading" class="chat-loading">
        <div class="skeleton" style="height: 48px; width: 60%; margin-bottom: 12px;"></div>
        <div class="skeleton" style="height: 48px; width: 50%; margin-left: auto; margin-bottom: 12px;"></div>
        <div class="skeleton" style="height: 48px; width: 65%;"></div>
      </div>

      <template v-else>
        <div v-if="messages.length === 0" class="chat-empty">
          <p>Belum ada pesan dalam sesi bimbingan ini.</p>
        </div>

        <div
          v-for="msg in messages"
          :key="msg.id"
          class="chat-bubble"
          :class="msg.sender === 'mahasiswa' ? 'bubble-sent' : 'bubble-received'"
        >
          <div class="bubble-sender">
            {{ msg.sender === 'mahasiswa' ? '👤 Anda' : '👨‍🏫 Dosen' }}
          </div>
          <div class="bubble-text">{{ msg.pesan }}</div>
          <div class="bubble-time">{{ formatWaktu(msg.waktu) }}</div>
        </div>
      </template>
    </div>

    <!-- Input Pesan -->
    <div class="chat-input-area">
      <input
        v-model="newMessage"
        type="text"
        class="chat-input"
        placeholder="Ketik pesan..."
        @keyup.enter="kirimPesan"
      />
      <button class="chat-send-btn" @click="kirimPesan" :disabled="!newMessage.trim()">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="22" y1="2" x2="11" y2="13"/>
          <polygon points="22 2 15 22 11 13 2 9 22 2"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'

const props = defineProps({
  messages: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
})

const emit = defineEmits(['send'])

const newMessage = ref('')
const chatArea = ref(null)

// Format waktu pesan
function formatWaktu(waktu) {
  if (!waktu) return ''
  const date = new Date(waktu.replace(' ', 'T'))
  return date.toLocaleString('id-ID', {
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// Kirim pesan
function kirimPesan() {
  if (!newMessage.value.trim()) return
  emit('send', newMessage.value.trim())
  newMessage.value = ''
}

// Auto-scroll ke bawah saat pesan baru
watch(
  () => props.messages.length,
  async () => {
    await nextTick()
    if (chatArea.value) {
      chatArea.value.scrollTop = chatArea.value.scrollHeight
    }
  }
)
</script>

<style scoped>
.chat-container {
  background: linear-gradient(135deg, #1e293b, #1a2332);
  border: 1px solid #334155;
  border-radius: 16px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 500px;
}
.chat-header {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #334155;
  background: rgba(15, 23, 42, 0.5);
}
.chat-header-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.chat-header-info h4 {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #e2e8f0;
}
.chat-count {
  font-size: 0.75rem;
  color: #64748b;
}

/* Area pesan */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.chat-loading, .chat-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #64748b;
  font-size: 0.875rem;
}

/* Bubble */
.chat-bubble {
  max-width: 75%;
  padding: 0.75rem 1rem;
  border-radius: 16px;
  font-size: 0.875rem;
  line-height: 1.5;
}
.bubble-sent {
  align-self: flex-end;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: #f1f5f9;
  border-bottom-right-radius: 4px;
}
.bubble-received {
  align-self: flex-start;
  background: #0f172a;
  color: #e2e8f0;
  border: 1px solid #334155;
  border-bottom-left-radius: 4px;
}
.bubble-sender {
  font-size: 0.6875rem;
  font-weight: 600;
  margin-bottom: 4px;
  opacity: 0.8;
}
.bubble-text {
  word-wrap: break-word;
}
.bubble-time {
  font-size: 0.625rem;
  opacity: 0.6;
  margin-top: 4px;
  text-align: right;
}

/* Input */
.chat-input-area {
  padding: 1rem 1.25rem;
  border-top: 1px solid #334155;
  display: flex;
  gap: 0.75rem;
  background: rgba(15, 23, 42, 0.5);
}
.chat-input {
  flex: 1;
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 0.75rem 1rem;
  color: #e2e8f0;
  font-size: 0.875rem;
  outline: none;
  transition: border-color 0.2s;
}
.chat-input:focus {
  border-color: #3b82f6;
}
.chat-input::placeholder {
  color: #475569;
}
.chat-send-btn {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border: none;
  border-radius: 12px;
  padding: 0.75rem;
  color: white;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}
.chat-send-btn:hover:not(:disabled) {
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
  transform: translateY(-1px);
}
.chat-send-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
