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
  

  colorOptions: { name: string; hexCode: string }[] = [
    { name: 'Red', hexCode: '#FF0000' },
    { name: 'Orange', hexCode: '#FFA500' },
    { name: 'Yellow', hexCode: '#FFFF00' },
    { name: 'Yellow green', hexCode: '#9ACD32' },
    { name: 'Green', hexCode: '#008000' },
    { name: 'Blue green', hexCode: '#00fc9d' },
    { name: 'Cyan', hexCode: '#00FFFF' },
    { name: 'Blue', hexCode: '#0000FF' },
    { name: 'Dark blue', hexCode: '#00008B' },
    { name: 'Purple', hexCode: '#800080' },
    { name: 'Magenta', hexCode: '#FF00FF' },
    { name: 'Pink', hexCode: '#FFC0CB' },
    { name: 'White', hexCode: '#FFFFFF' },
    { name: 'Grey', hexCode: '#808080' },
    { name: 'Black', hexCode: '#000000' },
    { name: 'Any', hexCode: '#FFFFFF' }
  ];


  submitForm() {
    // Convertir l'objet Description en FormData
    const formData = new FormData();
    formData.append('capDetected', this.description.cap.detected.toString());
    formData.append('capColor', this.description.cap.color.toString());
    formData.append('tshirtColor', this.description.t_shirt.color.toString());
    formData.append('sunglassesDetected', this.description.sunglasses.detected.toString());
    formData.append('trousersColor', this.description.trousers.color.toString());
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
