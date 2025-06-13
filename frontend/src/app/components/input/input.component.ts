import { Component, Input } from '@angular/core';
import { ReactiveFormsModule, UntypedFormGroup } from '@angular/forms';

@Component({
  selector: 'app-input',
  imports: [ReactiveFormsModule],
  templateUrl: './input.component.html',
  styleUrl: './input.component.scss',
})
export class InputComponent {
  @Input() formGroup: UntypedFormGroup = new UntypedFormGroup({});
  @Input() label: string = '';
  @Input() inputType: string | undefined = 'text';
  @Input() inputName: string = '';
  @Input() inputPlaceholder: string | undefined = '';
  @Input() min: number | undefined = undefined;
  @Input() max: number | undefined = undefined;
}
