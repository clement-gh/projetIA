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
  

  verifyFileIsImage(files: File[]): boolean {
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const fileName = file.name;
      const fileExtension = fileName.split('.').pop();
      if (fileExtension !== 'jpg' && fileExtension !== 'png') {
        return false;
      } else {
        return true;
      }
    }
    return false; // Add a default return statement
  }
  onDragOver(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
  }

  onDragLeave(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
  }

clearFiles() {
  this.selectedFiles = [];
  this.filesChanged.emit(this.selectedFiles);
}

  handleFiles(files: FileList | null) {
    if (files) {
      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        if (this.verifyFileIsImage([file])) {
          this.selectedFiles.push(file);
        }
        else {
          alert('Le fichier ' + file.name + ' n\'est pas une image. \n Veuillez sélectionner uniquement des fichiers .jpg ou .png');
        }
 
      }
      
      this.filesChanged.emit(this.selectedFiles); // Émettre l'événement avec les nouveaux fichiers sélectionnés
    }
  }


  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    const files = input?.files;
    this.handleFiles(files);
  }
}
