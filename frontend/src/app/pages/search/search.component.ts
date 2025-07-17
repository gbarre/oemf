import { Component, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormsModule,
  ReactiveFormsModule,
  FormBuilder,
  FormGroup,
} from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';
import { InputComponent } from '../../components/input/input.component';
import { InputField } from '../../objects/inputFields';
import { TranslateService } from '@ngx-translate/core';
import { ArrowService } from '../../services/arrow.service';
import { Arrow } from '../../objects/arrow';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { ModalComponent } from '../../components/modal/modal.component';

@Component({
  selector: 'app-search',
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    TranslateModule,
    InputComponent,
    ModalComponent,
  ],
  templateUrl: './search.component.html',
})
export class SearchComponent {
  @ViewChild(ModalComponent) modalComponent!: ModalComponent;

  searchForm: FormGroup;
  isSubmitted = false;
  results: any[] = [];

  showModal: boolean = false;
  selectedResult: any = null;

  action: 'found' | 'lost' | null = null;
  totalResults: number = 0;
  limit: number = 3;
  offset: number = 0;

  inputList: InputField[] = [
    { name: 'date', type: 'date' },
    { name: 'location' },
    { name: 'nock' },
    { name: 'point' },
    { name: 'shaft_color' },
    { name: 'shaft_length', type: 'number', min: 0 },
    { name: 'shaft_manufacturer' },
    { name: 'shaft_material' },
    { name: 'shaft_model' },
    { name: 'vanes_color' },
    { name: 'vanes_count', type: 'number', min: 0 },
  ];

  constructor(
    private fb: FormBuilder,
    private translate: TranslateService,
    private arrowService: ArrowService,
    private authService: AuthService,
    private router: Router
  ) {
    this.searchForm = this.fb.group({});
    this.initForm();

    this.inputList.forEach((field) => {
      const placeholderKey = `HOME.${field.name}_placeholder`;
      this.translate.get(placeholderKey).subscribe((res: string) => {
        if (res !== placeholderKey) {
          field.placeholder = res;
        }
      });
    });
  }

  initForm(): void {
    this.isSubmitted = false;
    const formGroupConfig: { [key in keyof Arrow]?: any } = {};
    this.inputList.forEach((field) => {
      formGroupConfig[field.name as keyof Arrow] =
        field.type === 'date'
          ? [new Date().toISOString().substring(0, 10)]
          : [''];
    });
    this.searchForm = this.fb.group(formGroupConfig);
  }

  setAction(action: 'found' | 'lost'): void {
    this.action = this.action === action ? null : action;
  }

  loadResults(): void {
    this.isSubmitted = true;
    const rawFormValues = { ...this.searchForm.value };
    const filters: Arrow = { ...rawFormValues };
    switch (this.action) {
      case 'found':
        filters.action = 'found';
        filters.dateLost = filters.date;
        delete filters.dateFound;
        delete filters.date;
        break;
      case 'lost':
        filters.action = 'lost';
        filters.dateFound = filters.date;
        delete filters.dateLost;
        delete filters.date;
        break;
    }

    this.arrowService.searchArrows(filters, this.offset, this.limit).subscribe({
      next: (response) => {
        this.results = response.body || [];

        const total = response.headers.get('X-Total-Count');
        const limit = response.headers.get('X-Limit');
        const offset = response.headers.get('X-Offset');

        this.totalResults = total ? parseInt(total, 10) : 0;
        this.limit = limit ? parseInt(limit, 10) : 10;
        this.offset = offset ? parseInt(offset, 10) : 0;
      },
      error: () => (this.results = []),
    });
  }

  onSubmit(): void {
    this.offset = 0;
    this.loadResults();
  }

  resetForm(): void {
    this.initForm();
    this.results = [];
    this.selectedResult = null;
  }

  goToPage(page: number): void {
    const newOffset = (page - 1) * this.limit;
    if (newOffset >= 0 && newOffset < this.totalResults) {
      this.offset = newOffset;
      this.loadResults();
    }
  }

  get currentPage(): number {
    return Math.floor(this.offset / this.limit) + 1;
  }

  get pages(): number[] {
    const totalPages = Math.ceil(this.totalResults / this.limit);
    const pagesArray: number[] = [];

    const maxPagesToShow = 7;
    let startPage = Math.max(
      1,
      this.currentPage - Math.floor(maxPagesToShow / 2)
    );
    let endPage = Math.min(totalPages, startPage + maxPagesToShow - 1);

    startPage = Math.max(1, endPage - maxPagesToShow + 1);

    for (let i = startPage; i <= endPage; i++) {
      pagesArray.push(i);
    }
    return pagesArray;
  }

  openModal(result: any): void {
    this.selectedResult = result;
    this.showModal = true;
  }
  closeModal(): void {
    this.showModal = false;
    this.selectedResult = null;
  }

  addArrow(): void {
    const rawFormValues = { ...this.searchForm.value };
    const convertedValues: Record<string, any> = {};

    this.inputList.forEach((field) => {
      const rawValue = rawFormValues[field.name];

      if (rawValue == null || rawValue === '' || rawValue === undefined) {
        delete convertedValues[field.name];
      } else if (field.type === 'number') {
        convertedValues[field.name] = Number(rawValue);
      } else {
        convertedValues[field.name] = rawValue;
      }
    });

    const newArrow: Arrow = {
      ...convertedValues,
      ...(this.action !== null ? { action: this.action } : {}),
    } as Arrow;
    this.arrowService.postArrow(newArrow).subscribe({
      next: (response) => {
        this.resetForm();
      },
      error: (err) => this.modalComponent.showErrorModal(err),
    });
  }
}
