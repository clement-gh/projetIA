import { Component, ElementRef, EventEmitter, Input, Output, ViewChild } from '@angular/core';
import  { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-drag-and-drop',
  templateUrl: './drag-and-drop.component.html',
  styleUrls: ['./drag-and-drop.component.css']
})
export class DragAndDropComponent {
  selectedFiles: File[] = [];
 @Output() filesChanged = new EventEmitter<File[]>();

  @ViewChild('fileInput') fileInput!: ElementRef;

  constructor(private apiService: ApiService) {}


  
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
    // enveoyer un get à  /hello pour tester
    this.apiService.get('hello').subscribe(res => {
      console.log(res);
    });
    
    
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
