import { NgModule } from '@angular/core';
import { BrowserModule, provideClientHydration } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './pages/home/home.component';
import { SearchComponent } from './pages/search/search.component';
import { UploadComponent } from './pages/upload/upload.component';
import { ConnexionComponent } from './pages/connexion/connexion.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { UploadDirective } from './directives/upload.directive';
import { HttpClientModule } from '@angular/common/http'; // Importez HttpClientModule depuis @angular/common/http
import { ApiService } from './services/api.service';


import {MatIconModule} from '@angular/material/icon';
import {MatInputModule} from '@angular/material/input';
import {MatListModule} from '@angular/material/list';
import {MatButtonModule} from '@angular/material/button';
import {MatGridListModule} from '@angular/material/grid-list';
import {MatSnackBarModule} from '@angular/material/snack-bar';

import { DragAndDropComponent } from './components/drag-and-drop/drag-and-drop.component';
import { FileListComponent } from './components/file-list/file-list.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    SearchComponent,
    UploadComponent,
    ConnexionComponent,
    NavbarComponent,
    UploadDirective,
    DragAndDropComponent,
    FileListComponent,
  
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatIconModule,
    MatInputModule,
    MatListModule,
    MatButtonModule,
    MatGridListModule,
    MatSnackBarModule,
    HttpClientModule

  ],
  providers: [
    provideClientHydration(),
    ApiService

  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
