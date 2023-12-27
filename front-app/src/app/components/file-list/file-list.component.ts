import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-file-list',
  templateUrl: './file-list.component.html',
  styleUrls: ['./file-list.component.css']
})
export class FileListComponent {
  @Input() files: File[] = [];

  constructor() { }

  getFileSize(size: number): string {
    const fileSizeInBytes = size;
    const fileSizeInKB = fileSizeInBytes / 1024;
    return fileSizeInKB.toFixed(2) + ' KB';
  }
}
