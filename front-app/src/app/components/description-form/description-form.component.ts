// description-form.component.ts
import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface Description {
  cap: { detected: boolean; color: string };
  t_shirt: { color: string };
  sunglasses: { detected: boolean };
  trousers: { color: string };
  numbers: { number: string };
}

@Component({
  selector: 'app-description-form',
  templateUrl: './description-form.component.html',
  styleUrls: ['./description-form.component.css']
})
export class DescriptionFormComponent {
  description: Description = {
    cap: { detected: false, color: '' },
    t_shirt: { color: '' },
    sunglasses: { detected: false },
    trousers: { color: '' },
    numbers: { number: '' }
  };

  constructor(private apiService: ApiService) {}
  
  colorOptions: string[] = [
    'Red',
    'Orange',
    'Yellow',
    'Yellow green',
    'Green',
    'Blue green',
    'Cyan',
    'Blue',
    'Dark blue',
    'Purple',
    'Magenta',
    'Pink',
    'White',
    'Grey',
    'Black',
    'Any'
  ];


  submitForm() {
    // Convertir l'objet Description en FormData
    const formData = new FormData();
    formData.append('capDetected', this.description.cap.detected.toString());
    formData.append('capColor', this.description.cap.color);
    formData.append('tshirtColor', this.description.t_shirt.color);
    formData.append('sunglassesDetected', this.description.sunglasses.detected.toString());
    formData.append('trousersColor', this.description.trousers.color);
    formData.append('number', this.description.numbers.number);

    console.log('formData', formData);

    // Envoie de l'objet FormData via le service ApiService
    this.apiService.post('search', formData)
      .subscribe(response => {
        // Traitez la réponse ici si nécessaire
        console.log('Response:', response);
      }, error => {
        // Gérez les erreurs ici
        console.error('Error:', error);
      });
  }
}
