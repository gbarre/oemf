import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormsModule,
  ReactiveFormsModule,
  FormBuilder,
  FormGroup,
} from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';
import { InputComponent } from '../components/input/input.component';
import { InputField } from '../objects/inputFields';
import { TranslateService } from '@ngx-translate/core';
import { ArrowService } from '../services/arrow.service';
import { ArrowFilters } from '../objects/arrow';

@Component({
  selector: 'app-home',
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    TranslateModule,
    InputComponent,
  ],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent {
  searchForm: FormGroup;
  isSubmitted = false;
  results: any[] = [];

  showModal: boolean = false;
  selectedResult: any = null;

  inputList: InputField[] = [
    { name: 'dateLost', type: 'date' },
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
    private arrowService: ArrowService
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
    const formGroupConfig: { [key in keyof ArrowFilters]?: any } = {};
    this.inputList.forEach((field) => {
      formGroupConfig[field.name as keyof ArrowFilters] =
        field.type === 'date'
          ? [new Date().toISOString().substring(0, 10)]
          : [''];
    });
    this.searchForm = this.fb.group(formGroupConfig);
  }

  onSubmit(): void {
    this.isSubmitted = true;
    const filters: ArrowFilters = this.searchForm.value;
    filters.action = 'found';
    this.arrowService.searchArrows(filters).subscribe({
      next: (data) => {
        this.results = data;
      },
      error: (err) => {
        this.results = [];
        console.log(err);
      },
    });
  }

  resetForm(): void {
    this.initForm();
    this.results = [];
    this.selectedResult = null;
  }

  openModal(result: any): void {
    this.selectedResult = result;
    this.showModal = true;
  }
  closeModal(): void {
    this.showModal = false;
    this.selectedResult = null;
  }
}
