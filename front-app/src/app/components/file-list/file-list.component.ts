import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-file-list',
  templateUrl: './file-list.component.html',
  styleUrls: ['./file-list.component.css']
})
export class FileListComponent {
  @Input() files: File[] = [];
  @Output() fileRemoved = new EventEmitter<number>(); 
  constructor() { }


  removeFile(index: number): void {
    this.fileRemoved.emit(index); // Émettre l'événement pour supprimer le fichier
  }
}
