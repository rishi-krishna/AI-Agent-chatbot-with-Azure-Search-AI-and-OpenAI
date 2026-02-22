import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap, catchError, of } from 'rxjs';
import { environment } from '../../environments/environment';
import type { ChatResponse } from './models';

@Injectable({ providedIn: 'root' })
export class CoochatService {
  private http = inject(HttpClient);
  private baseUrl = this.normalizeBaseUrl(environment.apiBaseUrl);

  private normalizeBaseUrl(value: string): string {
    const trimmed = (value || '').trim();
    if (!trimmed) {
      return '';
    }
    const withProtocol = /^https?:\/\//i.test(trimmed) ? trimmed : `https://${trimmed}`;
    return withProtocol.replace(/\/+$/, '');
  }

  sendMessage(message: string): Observable<ChatResponse> {
    return this.http.post<ChatResponse>(`${this.baseUrl}/chat`, { message }).pipe(
      tap(() => {}),
      catchError((err) => {
        console.error('Chat API error', err);
        return of({
          reply: 'Sorry, the assistant is unavailable. Please check the connection and try again.',
          citations: [],
        });
      })
    );
  }
}
