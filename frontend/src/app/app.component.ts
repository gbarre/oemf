import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import packageInfo from '../../package.json';
import { LINKS } from './app.constants';
import { TranslateModule, TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink, RouterLinkActive, TranslateModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'OEMF - Où est ma flèche ?';
  version: string = packageInfo.version;
  githubLink = LINKS.GITHUB.repo;

  constructor(public translate: TranslateService) {
    translate.setDefaultLang('fr');
    const browserLang = translate.getBrowserLang() || 'fr';
    translate.use(browserLang.match(/fr|en/) ? browserLang : 'fr');
  }

}
