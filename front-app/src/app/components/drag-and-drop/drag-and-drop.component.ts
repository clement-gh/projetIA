import { Component, ElementRef, EventEmitter, Input, Output, ViewChild } from '@angular/core';

@Component({
  selector: 'app-drag-and-drop',
  templateUrl: './drag-and-drop.component.html',
  styleUrls: ['./drag-and-drop.component.css']
})
export class DragAndDropComponent {
  selectedFiles: File[] = [];
 @Output() filesChanged = new EventEmitter<File[]>();

  @ViewChild('fileInput') fileInput!: ElementRef;

  constructor() { }


  
  onFileDropped(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    const files = event.dataTransfer?.files;
  
    if (files) {
      this.handleFiles(files);
      console.log('Fichiers déposés : ', this.selectedFiles);
    }
  }
  

  onDragOver(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
  }

  onDragLeave(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
  }

  uploadFiles() {
    if (this.selectedFiles.length > 0) {
      // Ajoutez ici votre logique pour envoyer les fichiers au serveur
      console.log('Fichiers à uploader : ', this.selectedFiles);
      // Réinitialiser les fichiers sélectionnés après l'upload
      this.selectedFiles = [];
      // Réinitialiser également le champ de fichier pour permettre un nouvel upload
      this.fileInput.nativeElement.value = '';
    }
  }

  handleFiles(files: FileList | null) {
    if (files) {
      for (let i = 0; i < files.length; i++) {
        this.selectedFiles.push(files[i]);
      }
      this.filesChanged.emit(this.selectedFiles); // Émettre l'événement avec les nouveaux fichiers sélectionnés
    }
  }

  

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    const files = input?.files;
    this.handleFiles(files);
    console.log('Fichiers sélectionnés : ', this.selectedFiles);
  }
}
