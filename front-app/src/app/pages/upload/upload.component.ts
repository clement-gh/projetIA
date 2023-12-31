// upload.component.ts

import { Component, ViewChild } from '@angular/core';
import { DragAndDropComponent } from '../../components/drag-and-drop/drag-and-drop.component';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent {


  @ViewChild(DragAndDropComponent) dragAndDropComponent!: DragAndDropComponent;
  selectedFiles: File[] = [];

  constructor(private apiService: ApiService) { }

  
 
  ngAfterViewInit() {
    this.dragAndDropComponent.filesChanged.subscribe((files: File[]) => {
      this.selectedFiles = files; // Mettre à jour selectedFiles lors de l'événement de changement
      console.log('Fichiers sélectionnés : ', this.selectedFiles);

    });
  }

  uploadFile() {
    console.log('uploadFile()');
    this.apiService.get('hello') // enveoyer un get à  /hello pour tester
  
  }
}
