import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup } from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';
import { InputField } from '../objects/inputFields';
import { TranslateService } from '@ngx-translate/core';
import { ArrowService } from '../services/arrow.service';
import { Arrow } from '../objects/arrow';

@Component({
  selector: 'app-home',
  imports: [CommonModule, TranslateModule],
  templateUrl: './home.component.html',
})
export class HomeComponent {
  constructor() {}
}
