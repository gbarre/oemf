import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  {
    path: 'changelog',
    loadComponent: () =>
      import('./pages/changelog/changelog.component').then(
        (m) => m.ChangelogComponent
      ),
  },
  {
    path: 'register',
    loadComponent: () =>
      import('./pages/register/register.component').then(
        (m) => m.RegisterComponent
      ),
  },
];
