import { Component, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { UserService } from '../../services/user.service';
import { TranslateModule } from '@ngx-translate/core';
import { AuthService } from '../../services/auth.service';
import { User } from '../../objects/user';

@Component({
  selector: 'app-account',
  imports: [CommonModule, FormsModule, ReactiveFormsModule, TranslateModule],
  templateUrl: './account.component.html',
})
export class AccountComponent implements OnInit {
  accountForm: FormGroup;
  error: string | null = null;
  success: boolean = false;

  isAuthenticated: boolean = false;
  user: User | null = null;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private userService: UserService,
    private authService: AuthService
  ) {
    this.accountForm = this.fb.group({});
    this.loadData();
  }

  ngOnInit(): void {
    this.isAuthenticated = this.authService.isAuthenticated();
    if (this.isAuthenticated) {
      this?.userService
        .getUserById(this.authService.getUserId() || -1)
        .subscribe({
          next: (user) => (this.user = user),
          error: (err) => {
            this.error =
              err.error?.error_description ||
              "Erreur lors de la récupération de l'utilisateur";
          },
          complete: () => this.loadData(),
        });
    }
  }

  loadData(): void {
    this.accountForm = this.fb.group({
      email: [
        { value: this.user?.email || '', disabled: this.isAuthenticated },
        [Validators.required, Validators.email],
      ],
      name: [
        this.user?.name || '',
        [Validators.required, Validators.minLength(3)],
      ],
      club: [
        this.user?.club || '',
        [Validators.required, Validators.minLength(2)],
      ],
      password: ['', [Validators.required, Validators.minLength(10)]],
    });
  }

  onSubmit() {
    if (this.accountForm.invalid) return;
    this.error = null;
    this.success = false;
    console.log(this.accountForm.value);
    if (this.isAuthenticated) {
      this.updateUser();
    } else {
      this.postUser();
    }
  }

  postUser(): void {
    this.userService.postUser(this.accountForm.value).subscribe({
      next: () => {
        this.success = true;
        setTimeout(() => this.router.navigate(['/login']), 1500);
      },
      error: (err) => {
        this.error =
          err.error?.error_description ||
          'Erreur lors de la création du compte';
      },
    });
  }

  updateUser(): void {
    this.accountForm.value.email = this.user?.email;
    console.log(this.accountForm.value);
    this.userService
      .putUser(this.authService.getUserId() || -1, this.accountForm.value)
      .subscribe({
        next: () => {
          this.success = true;
          // TODO : voir la redirection après la mise à jour
        },
        error: (err) => {
          this.error =
            err.error?.error_description || 'Erreur lors de la mise à jour';
        },
      });
  }
}
