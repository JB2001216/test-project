import { Component } from '@angular/core';
import {AuthService} from './services/auth.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'frontend';

   constructor(
    private authService: AuthService,
    private router: Router
  ) {
  }

  public loggedIn(): boolean{
     return this.authService.isLoggedIn();
  }

  logout(): void{
    this.authService.logout();
  }
}
