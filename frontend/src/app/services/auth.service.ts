import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {tap} from 'rxjs/operators';
import {Observable} from 'rxjs';
import {Router} from '@angular/router';
import {JwtHelperService} from '@auth0/angular-jwt';


@Injectable({
  providedIn: 'root'
})
export class AuthService {
  AUTH_SERVER_ADDRESS: string = environment.apiUrl;

  constructor(
    private  http: HttpClient,
    private router: Router
  ) { }

  isLoggedIn(): boolean {
    let isLogged = false;
    const myRawToken = localStorage.getItem('ACCESS_TOKEN');
    if (myRawToken && myRawToken !== 'undefined') {
      const helper = new JwtHelperService();
      const isExpired = helper.isTokenExpired(myRawToken);
      if (!isExpired) {
        isLogged = true;
      }
    }
    return isLogged;
  }

  login(formValue: any): Observable<any> {
     return this.http.post(this.AUTH_SERVER_ADDRESS + '/users/login/', formValue).pipe(
       tap((data: any ) => {
         localStorage.setItem('ACCESS_TOKEN', data.access);
       })
     );
  }

  register(formValue: any): Observable<any> {
     return this.http.post(this.AUTH_SERVER_ADDRESS + '/users/register/', formValue).pipe(
       tap((data: any ) => {
         localStorage.setItem('ACCESS_TOKEN', data.access);
       })
     );
  }

  logout(): void {
    localStorage.clear();
    this.router.navigate(['/']);
  }
}
