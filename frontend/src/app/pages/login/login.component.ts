import {Component, OnInit} from '@angular/core';
import {AbstractControl, FormControl, FormGroup, Validators} from '@angular/forms';
import {AuthService} from '../../services/auth.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  loginFormSubmitted = false;
  error: any;

  loginForm = new FormGroup({
    email: new FormControl('member@messages.com', [Validators.required, Validators.email]),
    password: new FormControl('Password', [Validators.required]),
  });

  constructor(
    private authService: AuthService,
    private router: Router
  ) {
  }

  get lf(): { [key: string]: AbstractControl; } {
    return this.loginForm.controls;
  }


  ngOnInit(): void {
    if (this.authService.isLoggedIn()){
      this.router.navigateByUrl('/inbox');
    }
  }

  onSubmit(): void {
    this.error = undefined;
    this.loginFormSubmitted = true;
    if (this.loginForm.invalid) {
      return;
    }
    console.log(this.loginForm.value);

    this.authService.login(this.loginForm.value).subscribe(data => {
      console.log(data);
      this.router.navigate(['/inbox']);
    }, errorData => {
      this.error = errorData.error;
      console.log(this.error);
    });
  }


  gerErrors(error: any): any {
    if (error) {
      return Object.entries(error);
    }
  }

}
