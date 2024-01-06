// upload.component.ts

import { Component, ViewChild } from '@angular/core';
import { DragAndDropComponent } from '../../components/drag-and-drop/drag-and-drop.component';
import { ApiService } from '../../services/api.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';
import { DialogService } from '../../services/dialog.service';


@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css'],
})
export class UploadComponent {
  @ViewChild(DragAndDropComponent) dragAndDropComponent!: DragAndDropComponent;
  selectedFiles: File[] = [];
  constructor(
    private apiService: ApiService,
    private _snackBar: MatSnackBar,
    private dialogService: DialogService
  ) {}

  openSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 0, // Durée d'affichage du Snackbar en millisecondes
    });
  }

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
    const confirmed = await this.dialogService.openConfirmationDialog('Êtes-vous sûr de vouloir téléverser ces fichiers ?').toPromise();
     

    if (confirmed) {
        const formData = new FormData();
        this.selectedFiles.forEach((file) => {
          formData.append('image', file);
        });

        try {
          const data = await this.apiService.post('upload', formData).toPromise();
          console.log('data', data);
          console.log('Téléversement réussi !');

          this.selectedFiles = [];
          this.updateUploadButtonState();
          this.dragAndDropComponent.clearFiles();
          alert('Téléversement réussi !');
        } catch (error: any) {
          console.error(error);
          if (error.status===0) {
            this._snackBar.open(
              "Le serveur backend n'a pas pu être contacté. Veuillez réessayer plus tard.",
              'Fermer',{ duration: 2000}
            );
            return; 
          }
          if (error.error.message.code === 'ECONNREFUSED') {
            this._snackBar.open(
              "Le serveur n'a pas pu se connecter à l'API Python. Veuillez réessayer plus tard.",
              'Fermer' ,{ duration: 8000}
              
            );
          }
          
        }
      }
      else {
        console.log('Téléversement annulé');
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
