import { CommonModule } from '@angular/common';
import { Component, Input, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';

declare let jQuery: any;
@Component({
  selector: 'app-modal',
  templateUrl: './modal.component.html',
  imports: [CommonModule, TranslateModule],
})
export class ModalComponent {
  @ViewChild('modal') modal: any;
  @Input() modalColor = 'default';
  @Input() modalTitle = '';
  @Input() modalContent = '';
  @Input() modalLarge = false;
  @Input() modalRedirectPath = '';
  @Input() modalRedirectQueryParams: object = {};
  public refreshAll = false;

  constructor(private router: Router) {}

  redirect() {
    if (this.refreshAll) {
      window.location.href = this.modalRedirectPath;
      return;
    }
    if (this.modalRedirectPath !== '') {
      this.router.navigate([this.modalRedirectPath], {
        queryParams: this.modalRedirectQueryParams,
      });
    }
  }

  showModal(color: string, title: string, content: string) {
    this.modalColor = color;
    this.modalTitle = title;
    this.modalContent = content;
    jQuery(this.modal.nativeElement).modal('show');
  }

  showErrorModal(err: any) {
    this.showModal(
      'danger',
      `${err.status} - ${err.statusText}`,
      err.error.detail
    );
  }
}
