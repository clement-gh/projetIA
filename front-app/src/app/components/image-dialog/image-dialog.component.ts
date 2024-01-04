import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-image-dialog',
  templateUrl: './image-dialog.component.html',
  styleUrls: ['./image-dialog.component.css']
})
export class ImageDialogComponent {
  constructor(@Inject(MAT_DIALOG_DATA) public data: { imageData: string }) { }
  
  downloadImage(): void {
    const link = document.createElement('a');
    link.href = 'data:image/jpeg;base64,' + this.data.imageData;
    link.download = 'image.jpg';
    link.click();
  }
  
}
