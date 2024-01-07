import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './pages/home/home.component'
import { SearchComponent } from './pages/search/search.component';
import { UploadComponent } from './pages/upload/upload.component';

import { ExternalRedirectComponent } from './pages/external-redirect/external-redirect.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'search', component: SearchComponent },
  { path: 'upload', component: UploadComponent },
  { path: 'pdf', component: ExternalRedirectComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
