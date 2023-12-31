import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:3000'; // Remplacez cette URL par l'URL de votre backend

  constructor() { }

  // Exemple de méthode pour effectuer une requête GET
  get(endpoint: string): Observable<any> {
    const url = `${this.baseUrl}/${endpoint}`;
    console.log('url : ', url);
    return new Observable(observer => {
      fetch(url)
        .then(response => {
          console.log('response : ', response);
          if (!response.ok) {
            throw new Error(`Erreur HTTP, statut : ${response.status}`);
          }
          return response.json();
        })
        .then(data => {
          observer.next(data);
          observer.complete();
        })
        .catch(error => {
          observer.error(error);
        });
    });
  }

  // Exemple de méthode pour effectuer une requête POST
  post(endpoint: string, data: any): Observable<any> {
    const url = `${this.baseUrl}/${endpoint}`;
    return new Observable(observer => {
      fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
        .then(response => {
          if (!response.ok) {
            throw new Error(`Erreur HTTP, statut : ${response.status}`);
          }
          return response.json();
        })
        .then(result => {
          observer.next(result);
          observer.complete();
        })
        .catch(error => {
          observer.error(error);
        });
    });
  }

  // Ajoutez des méthodes PUT, DELETE, etc. selon vos besoins
}
