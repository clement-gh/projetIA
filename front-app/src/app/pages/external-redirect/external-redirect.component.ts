import { Component, Inject, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DOCUMENT } from '@angular/common';

@Component({
  selector: 'app-external-redirect',
  template: ''
})
export class ExternalRedirectComponent implements OnInit {

  
  constructor(
    private router: Router,
    @Inject(DOCUMENT) private document: Document
  ) { }

  ngOnInit(): void {
    // Redirection vers l'URL externe si window est disponible
    if (this.document.defaultView) {
      this.document.defaultView.location.href = 'http://localhost:3000/getpdf/stage4AIT_2023_GHYS_Clement.pdf';
    } else {
      // Gérer le cas où window/document n'est pas disponible
      console.error('window/document is not available');
    }
  }
}
   