import { Component } from '@angular/core';
import { ChatComponent } from './chat/chat.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ChatComponent],
  template: '<app-chat />',
  styles: [':host { display: block; min-height: 100vh; }'],
})
export class AppComponent {}
