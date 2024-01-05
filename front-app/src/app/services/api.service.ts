import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:3000'; // Remplacez par l'URL de votre backend

  constructor(private http: HttpClient) {}

  get(endpoint: string): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/${endpoint}`);
  }

  post(endpoint: string, formData: FormData): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/${endpoint}`, formData);
  }

  getPdf(fileName: string): Observable<Blob> {
    return this.http.get(`${this.baseUrl}/get-pdf`, { responseType: 'blob' });
  }

  getImages(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/images`);
  }
}
