import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap, catchError, of } from 'rxjs';
import { environment } from '../../environments/environment';
import type { ChatResponse } from './models';

@Injectable({ providedIn: 'root' })
export class CoochatService {
  private http = inject(HttpClient);
  private baseUrl = environment.apiBaseUrl;

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
