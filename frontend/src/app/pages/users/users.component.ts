import { Component, OnInit } from '@angular/core';
import { UserService } from '../../services/user.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { User } from '../../objects/user';
import { TranslateModule } from '@ngx-translate/core';

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  imports: [CommonModule, FormsModule, TranslateModule],
})
export class UsersComponent implements OnInit {
  users: any[] = [];
  displayedColumns: string[] = ['firstname', 'lastname', 'email'];
  selectedUserPassword: any;
  selectedUser: User | null = null;

  constructor(private userService: UserService) {}

  ngOnInit(): void {
    this.getUsers();
  }

  openEditPasswordModal(user: any): void {
    this.selectedUser = user;
  }

  updatePassword(): void {
    if (this.selectedUserPassword != null && this.selectedUser != null) {
      const updatedUser = {
        ...this.selectedUser,
        password: 'somethingNotUsedSinceIamAdmin',
        new_password: this.selectedUserPassword,
      };

      this.userService
        .putUser(this.selectedUser.id ?? -1, updatedUser)
        .subscribe({
          next: (response) => {
            this.selectedUserPassword = null;
            this.selectedUser = null;
          },
        });
    }
  }

  deleteUser(userId: number): void {
    this.userService.deleteUser(userId).subscribe({
      next: () => {
        this.getUsers();
      },
      error: (err) => {
        console.error('Error deleting user:', err);
      },
    });
  }

  getUsers(): void {
    this.userService.getUsers().subscribe((users) => {
      this.users = users;
    });
  }
}
