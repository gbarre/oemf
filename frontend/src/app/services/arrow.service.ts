import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { filter, Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Arrow } from '../objects/arrow';

@Injectable({
  providedIn: 'root',
})
export class ArrowService {
  private apiUrl = `${environment.apiBaseUrl}/arrows`;

  constructor(private http: HttpClient) {}

  searchArrows(
    formValues: Arrow,
    offset: number = 0,
    limit: number = 9
  ): Observable<HttpResponse<Arrow[]>> {
    let filters: string = '';

    Object.entries(formValues).forEach(([key, value]) => {
      if (value !== null && value !== '' && value !== undefined) {
        if (!filters) {
          filters = '?';
        } else {
          filters += '&';
        }
        filters += `filters[${key}]=${encodeURIComponent(value)}`;
      }
    });

    filters += filters ? '&' : '?';
    filters += `offset=${offset}&limit=${limit}`;

    return this.http.get<Arrow[]>(`${this.apiUrl}${filters}`, {
      observe: 'response',
    });
  }

  postArrow(arrow: Arrow): Observable<Arrow> {
    return this.http.post<Arrow>(this.apiUrl, arrow);
  }
}
