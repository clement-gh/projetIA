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

    const formData = new FormData();
    this.selectedFiles.forEach(file => {
      formData.append('image', file); // 'image' doit correspondre au nom attendu par votre backend pour recevoir les fichiers
    });

    this.apiService.post('upload', formData)
      .then((data) => {
        // Utilisez les données récupérées ici si nécessaire
        console.log(data);
      })
      .catch((error) => {
        // Gérez les erreurs ici
        console.error(error);
      });
  }
}
/*

    console.log('hello');
    this.apiService.get('hello')
      .then((data) => {
        // Utilisez les données récupérées ici
        console.log(data);
      })
      .catch((error) => {
        // Gérez les erreurs ici
        console.error(error);

      });
  }
  */