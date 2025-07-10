import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { LINKS } from '../../app.constants';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { NewlinePipe } from '../../pipes/newline.pipe';

@Component({
  selector: 'app-changelog',
  imports: [CommonModule, TranslateModule, NewlinePipe],
  templateUrl: './changelog.component.html',
  styleUrl: './changelog.component.scss',
})
export class ChangelogComponent implements OnInit {
  commits: any[] = [];
  loading = true;
  error: boolean = false;

  constructor(private http: HttpClient, private translate: TranslateService) {}

  ngOnInit(): void {
    this.http.get<any[]>(LINKS.GITHUB.commits).subscribe({
      next: (data) => {
        this.commits = data;
        this.error = false;
      },
      error: () => {
        this.error = true;
      },
      complete: () => {
        this.loading = false;
      },
    });
  }

  getRelativeDate(dateString: string): string {
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);

    let key = '';
    let count = 0;
    let plural = '';

    if (seconds < 60) {
      key = 'CHANGELOG.SECONDS';
      count = seconds;
      plural = seconds > 1 ? 's' : '';
    } else {
      const minutes = Math.floor(seconds / 60);
      if (minutes < 60) {
        key = 'CHANGELOG.MINUTES';
        count = minutes;
        plural = minutes > 1 ? 's' : '';
      } else {
        const hours = Math.floor(minutes / 60);
        if (hours < 24) {
          key = 'CHANGELOG.HOURS';
          count = hours;
          plural = hours > 1 ? 's' : '';
        } else {
          const days = Math.floor(hours / 24);
          if (days < 30) {
            key = 'CHANGELOG.DAYS';
            count = days;
            plural = days > 1 ? 's' : '';
          } else {
            const months = Math.floor(days / 30);
            if (months < 12) {
              key = 'CHANGELOG.MONTHS';
              count = months;
              plural = ''; // "mois" est invariable
            } else {
              const years = Math.floor(months / 12);
              key = 'CHANGELOG.YEARS';
              count = years;
              plural = years > 1 ? 's' : '';
            }
          }
        }
      }
    }

    let translated = '';
    this.translate
      .get(key, { count, plural })
      .subscribe((res) => (translated = res));
    return translated;
  }
}
