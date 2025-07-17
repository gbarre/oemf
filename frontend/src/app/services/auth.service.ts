import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, catchError, map, Observable, of } from 'rxjs';
import { environment } from '../../environments/environment';
import { Token } from '../objects/token';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private authTokenKey = 'authToken';
  private tokenExpirationThreshold = 100000; // in milliseconds
  private endpoint_auth = `${environment.apiBaseUrl}/auth`;

  public authChangedSubject = new BehaviorSubject<boolean>(
    this.isAuthenticated()
  );
  public authChanged$ = this.authChangedSubject.asObservable();

  private adminStatus$ = new BehaviorSubject<boolean>(false);

  constructor(private http: HttpClient) {}

  post_auth(data: any): Observable<Token> {
    const url = `${this.endpoint_auth}`;
    return this.http.post<Token>(url, data);
  }

  getAuthToken(): string | null {
    return localStorage.getItem(this.authTokenKey);
  }

  setAuthToken(token: string): void {
    localStorage.setItem(this.authTokenKey, token);
  }

  clearAuthToken(): void {
    localStorage.removeItem(this.authTokenKey);
  }

  isAuthenticated(): boolean {
    const token = localStorage.getItem(this.authTokenKey);
    return !!token;
  }

  isValidToken(): boolean {
    const expirationTime = this.getExpirationTime();
    const currentTime = new Date().getTime();
    return expirationTime > currentTime;
  }

  refreshTokenIfNecessary(): Observable<any> {
    const expirationTime = this.getExpirationTime();
    const currentTime = new Date().getTime();

    if (expirationTime - currentTime < this.tokenExpirationThreshold) {
      return this.http.get<Token>(this.endpoint_auth, this.getRequestOptions());
    } else {
      return of(null);
    }
  }

  getExpirationTime(): number {
    const token = this.getAuthToken();
    if (!token) {
      return 0;
    }
    const tokenPayload = JSON.parse(atob(token.split('.')[1]));
    return tokenPayload.exp * 1000; // Expiration time in milliseconds
  }

  getRequestOptions(): { headers: HttpHeaders } {
    const authToken = this.getAuthToken();
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      Accept: 'application/json',
      Authorization: `Bearer ${authToken}`,
    });
    return { headers: headers };
  }

  getUserId(): number | null {
    const token = this.getAuthToken();
    if (!token) {
      return null;
    }
    try {
      const tokenPayload = JSON.parse(atob(token.split('.')[1]));
      return tokenPayload.userid ?? null;
    } catch {
      return null;
    }
  }

  isAdmin(): Observable<boolean> {
    const url = `${this.endpoint_auth}/is-admin`;
    return this.http.get<{ admin: boolean }>(url).pipe(
      map((res) => res.admin),
      catchError(() => of(false))
    );
  }

  loadAdminStatus(): void {
    this.isAdmin().subscribe((isAdmin) => {
      this.adminStatus$.next(isAdmin);
    });
  }

  getAdminStatus(): Observable<boolean> {
    return this.adminStatus$.asObservable();
  }
}
