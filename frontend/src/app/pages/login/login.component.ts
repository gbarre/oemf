import { Component } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { AuthService } from '../../services/auth.service';
import { Token } from '../../objects/token';

@Component({
  selector: 'app-login',
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    RouterLink,
    TranslateModule,
  ],
  templateUrl: './login.component.html',
})
export class LoginComponent {
  loginForm: FormGroup;
  error: string | null = null;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private authService: AuthService
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required]],
    });
  }

  onSubmit() {
    if (this.loginForm.invalid) return;
    this.error = null;
    const params = new URLSearchParams(window.location.search);
    const redirect = params.get('redirect');

    this.authService.post_auth(this.loginForm.value).subscribe({
      next: (token: Token) => {
        if (!token || !token.jwt) {
          this.error = 'Invalid credentials';
          return;
        }
        this.authService.setAuthToken(token.jwt);
        this.authService.authChangedSubject.next(true);
      },
      error: (err) => {
        this.error = err.error?.error_description || 'Invalid credentials';
      },
      complete: () => this.router.navigate([redirect || '/']),
    });
  }
}
