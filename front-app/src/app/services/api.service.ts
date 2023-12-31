import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';


export class ApiService {
  private baseUrl = 'http://localhost:3000'; // Remplacez par l'URL de votre backend

  constructor() {}

  async get(endpoint: string): Promise<any> {
    const response = await fetch(`${this.baseUrl}/${endpoint}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        // Autres headers si nécessaire
      }
    });
    return await response.json();
  }

  async post(endpoint: string, formData: FormData): Promise<any> {
    const response = await fetch(`${this.baseUrl}/${endpoint}`, {
      method: 'POST',
      body: formData
    });
    return await response.json();
  }
  // Ajoutez des méthodes PUT, DELETE, etc. selon vos besoins
}
