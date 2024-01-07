import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ImageDataService {
  private imageData = new BehaviorSubject<string[]>([]);
  imageData$ = this.imageData.asObservable();

  constructor() {}

  setImageData(data: string[]): void {
    this.imageData.next(data);
  }
}
