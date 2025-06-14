import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { LINKS } from '../../app.constants';
import { TranslateModule } from '@ngx-translate/core';
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

  constructor(private http: HttpClient) {}

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
    if (seconds < 60)
      return `il y a ${seconds} seconde${seconds > 1 ? 's' : ''}`;
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60)
      return `il y a ${minutes} minute${minutes > 1 ? 's' : ''}`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `il y a ${hours} heure${hours > 1 ? 's' : ''}`;
    const days = Math.floor(hours / 24);
    if (days < 30) return `il y a ${days} jour${days > 1 ? 's' : ''}`;
    const months = Math.floor(days / 30);
    if (months < 12) return `il y a ${months} mois`;
    const years = Math.floor(months / 12);
    return `il y a ${years} an${years > 1 ? 's' : ''}`;
  }
}
