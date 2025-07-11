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
          error: () => {
            this.authService.clearAuthToken();
            this.router.navigate(['/login']);
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
      new_password: ['', [Validators.minLength(10)]],
      confirmPassword: [''],
    });
  }

  onSubmit() {
    if (this.accountForm.invalid) return;
    this.error = null;
    this.success = false;
    if (this.isAuthenticated) {
      this.updateUser();
    } else {
      this.postUser();
    }
  }

  checkPasswordMatch(): void {
    const password = this.accountForm.get('password')?.value;
    const new_password = this.accountForm.get('new_password')?.value;
    const confirmPassword = this.accountForm.get('confirmPassword')?.value;
    this.accountForm.get('confirmPassword')?.setErrors(null);
    switch (this.isAuthenticated) {
      case true:
        if (new_password && confirmPassword)
          this.validatenew_password(new_password, confirmPassword);
        break;
      case false:
        if (password && confirmPassword)
          this.validatenew_password(password, confirmPassword);
        break;
    }
  }

  validatenew_password(password: string, confirmPassword: string): void {
    if (password !== confirmPassword) {
      this.accountForm.get('confirmPassword')?.setErrors({
        notMatching: true,
      });
    } else {
      this.accountForm.get('confirmPassword')?.setErrors(null);
    }
  }

  postUser(): void {
    const { new_password, confirmPassword, ...newUser } =
      this.accountForm.value;
    this.userService.postUser(newUser).subscribe({
      next: () => {
        this.success = true;
        setTimeout(() => this.router.navigate(['/login']), 1500);
      },
      error: (err) => {
        this.error =
          err.error?.error_description || 'Error while creating the account';
      },
    });
  }

  updateUser(): void {
    this.accountForm.value.email = this.user?.email;
    const { confirmPassword, ...updateUser } = this.accountForm.value;
    this.userService
      .putUser(this.authService.getUserId() || -1, updateUser)
      .subscribe({
        next: () => {
          this.success = true;
          setTimeout(() => this.router.navigate(['/']), 1500);
        },
        error: (err) => {
          this.error =
            err.error?.error_description || 'Error while updating the account';
        },
      });
  }
}
