import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';

import { MatDialog } from '@angular/material/dialog';
import { ImageDialogComponent } from '../image-dialog/image-dialog.component';

@Component({
  selector: 'app-image-list',
  templateUrl: './image-list.component.html',
  styleUrls: ['./image-list.component.css']
})
export class ImageListComponent implements OnInit {
  images: string[] = []; // Tableau pour stocker les données d'images

  constructor(private apiService: ApiService, private dialog: MatDialog) { }

  ngOnInit(): void {
    this.apiService.getImages().subscribe(
      (response: any) => {
        this.images = response.images;
      },
      (error: any) => {
        console.error('Erreur lors de la récupération des images :', error);
        // Gérez l'erreur de récupération des images ici
      }
    );
  }

  openImageDialog(imageData: string): void {
    const dialogRef = this.dialog.open(ImageDialogComponent, {
      data: { imageData },
      maxWidth: '90vw',
      maxHeight: '90vh'
    });
  }
}
