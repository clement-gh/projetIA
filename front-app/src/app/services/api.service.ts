import { HttpClient, HttpHeaders  } from '@angular/common/http';
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

  getPdfUrl(pdfFilename: string): Observable<Blob> {
    const url = `${this.baseUrl}/getpdf/${pdfFilename}`;
    return this.http.get<Blob>(url);
  }
  getImages(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/images`);
  }
}
