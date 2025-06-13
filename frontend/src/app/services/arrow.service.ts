import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Arrow, ArrowFilters } from '../objects/arrow';

@Injectable({
  providedIn: 'root',
})
export class ArrowService {
  private apiUrl = `${environment.apiBaseUrl}/arrows`;

  constructor(private http: HttpClient) {}

  searchArrows(formValues: ArrowFilters): Observable<Arrow[]> {
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

    return this.http.get<Arrow[]>(`${this.apiUrl}${filters}`);
  }
}
