// description-form.component.ts
import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ImageDataService } from '../../services/imageData.service';

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

  constructor(private apiService: ApiService,private imageDataService: ImageDataService) {}
  

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
    const payload = {
      capDetected: this.description.cap.detected,
      capColor: this.description.cap.color,
      tshirtColor: this.description.t_shirt.color,
      sunglassesDetected: this.description.sunglasses.detected,
      trousersColor: this.description.trousers.color,
      number: this.description.numbers.number
    };
  
    console.log('payload', payload);
  
    this.apiService.postPayload('search', payload)
      .subscribe(response => {
        // Traitez la réponse ici si nécessaire
        console.log('Response:', response);
        const imageUrls: string[] = response.images;
        this.imageDataService.setImageData(imageUrls);
      }, error => {
        // Gérez les erreurs ici
        console.error('Error:', error);
      });
  }
  
}
