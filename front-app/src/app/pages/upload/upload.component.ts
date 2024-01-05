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
  uploadButtonDisabled: boolean = true;
  updateUploadButtonState(): void {
    this.uploadButtonDisabled = this.selectedFiles.length === 0;
  }
  
 
  ngAfterViewInit() {
    this.dragAndDropComponent.filesChanged.subscribe((files: File[]) => {
      this.selectedFiles = files; // Mettre à jour selectedFiles lors de l'événement de changement
      this.updateUploadButtonState(); 
      console.log('Fichiers sélectionnés : ', this.selectedFiles);

    });
  }

  async uploadFile() {
    
    const confirmUpload = window.confirm('Êtes-vous sûr de vouloir téléverser ces fichiers ?');
    if (confirmUpload) {
    const formData = new FormData();
    this.selectedFiles.forEach(file => {
      formData.append('image', file); 
    });

    try {
      const data = await this.apiService.post('upload', formData).toPromise();
      console.log(data);
      
      this.selectedFiles = [];
      this.updateUploadButtonState();
      this.dragAndDropComponent.clearFiles();
      alert('Téléversement réussi !');
    } catch (error) {
      console.error(error);
    }
    } else {
      console.log('Téléversement annulé.');
      // Ajoutez ici des actions à effectuer si l'utilisateur annule le téléversement
    }
  
  }



  removeFile(index: number): void {

    this.selectedFiles.splice(index, 1); // Supprimer le fichier de selectedFiles
    console.log('Fichiers sélectionnés : ', this.selectedFiles);
    this.updateUploadButtonState(); 
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