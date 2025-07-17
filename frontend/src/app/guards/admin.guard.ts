import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { map } from 'rxjs/operators';

export const adminGuard: CanActivateFn = () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (!authService.isValidToken()) {
    router.navigate(['/login'], {
      queryParams: { redirect: location.pathname.slice(1) },
    });
    return false;
  }

  return authService.getAdminStatus().pipe(
    map((isAdmin) => {
      console.log('Admin status:', isAdmin);
      if (!isAdmin) {
        router.navigate(['/']);
        return false;
      }
      return true;
    })
  );
};
