import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';


@Component({
  selector: 'app-image-list',
  templateUrl: './image-list.component.html',
  styleUrls: ['./image-list.component.css']
})
export class ImageListComponent implements OnInit {
  images: string[] = []; // Tableau pour stocker les données d'images

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    this.apiService.getImages().subscribe(
      (response: any) => {
        this.images = response.images;
      },
      (error) => {
        console.error('Erreur lors de la récupération des images :', error);
        // Gérez l'erreur de récupération des images ici
      }
    );
  }
}
