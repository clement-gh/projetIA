import { Component, ElementRef, AfterViewInit, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements AfterViewInit {
  constructor(private elRef: ElementRef, @Inject(PLATFORM_ID) private platformId: object) { }

  ngAfterViewInit() {
    if (isPlatformBrowser(this.platformId)) {
      const navbarHeight = this.elRef.nativeElement.offsetHeight;
      document.body.style.paddingTop = navbarHeight + 'px';
    }
  }
}
export default NavbarComponent;