import { Component, OnDestroy, OnInit } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import packageInfo from '../../package.json';
import { LINKS } from './app.constants';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { AuthService } from './services/auth.service';
import { CommonModule } from '@angular/common';
import { Token } from './objects/token';

@Component({
  selector: 'app-root',
  imports: [
    CommonModule,
    RouterOutlet,
    RouterLink,
    RouterLinkActive,
    TranslateModule,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'OEMF - Où est ma flèche ?';
  version: string = packageInfo.version;
  githubLink = LINKS.GITHUB.repo;
  isAuthenticated = false;
  tokenExpire = 0;

  private intervalId: any;

  constructor(
    public translate: TranslateService,
    private authService: AuthService
  ) {
    translate.setDefaultLang('fr');
    const browserLang = translate.getBrowserLang() || 'fr';
    translate.use(browserLang.match(/fr|en/) ? browserLang : 'fr');

    this.authService.authChanged$.subscribe((auth) => {
      this.isAuthenticated = auth;
    });
  }

  ngOnInit(): void {
    this.intervalId = setInterval(() => {
      if (this.authService.isValidToken()) {
        if (this.authService.getExpirationTime()) {
          this.tokenExpire = this.authService.getExpirationTime();
          this.authService.refreshTokenIfNecessary().subscribe({
            next: (response: Token) => {
              if (response !== null)
                this.authService.setAuthToken(response.jwt);
            },
          });
        }
      } else {
        this.authService.clearAuthToken();
        this.isAuthenticated = false;
      }
    }, 10000);
  }

  ngOnDestroy(): void {
    if (this.intervalId) clearInterval(this.intervalId);
  }

  logout(): void {
    this.authService.clearAuthToken();
    window.location.href = './';
  }
}
