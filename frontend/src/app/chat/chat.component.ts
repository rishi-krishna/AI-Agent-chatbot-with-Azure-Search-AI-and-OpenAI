import { Component, inject, signal, computed } from '@angular/core';
import { NgFor, NgIf } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CoochatService } from './coochat.service';
import type { ChatMessage } from './models';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [NgIf, NgFor, FormsModule],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css'],
})
export class ChatComponent {
  private coochat = inject(CoochatService);
  input = signal('');
  messages = signal<ChatMessage[]>([]);
  loading = signal(false);
  isOpen = signal(false);
  hasMessages = computed(() => this.messages().length > 0);

  toggleWidget(): void {
    this.isOpen.update((open) => !open);
  }

  closeWidget(): void {
    this.isOpen.set(false);
  }

  send(): void {
    const text = this.input().trim();
    if (!text || this.loading()) return;
    this.input.set('');
    this.messages.update((m) => [...m, { role: 'user', content: text }]);
    this.loading.set(true);
    this.messages.update((m) => [...m, { role: 'assistant', content: '', loading: true }]);
    this.coochat.sendMessage(text).subscribe((res) => {
      this.loading.set(false);
      this.messages.update((msgs) => {
        const out = msgs.slice(0, -1);
        out.push({ role: 'assistant', content: res.reply, citations: res.citations });
        return out;
      });
    });
  }

  trackByIndex(i: number): number {
    return i;
  }
}
