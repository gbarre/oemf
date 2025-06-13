import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';
import { translateConfig } from './app/app.translate';

bootstrapApplication(AppComponent,  {
  providers: [...appConfig.providers, ...translateConfig.providers],
})
  .catch((err) => console.error(err));
