import {Component, OnInit} from '@angular/core';
import {AbstractControl, FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {AuthService} from '../../services/auth.service';
import {Router} from '@angular/router';


export function MustMatch(controlName: string, matchingControlName: string): any {
  return (formGroup: FormGroup) => {
    const control = formGroup.controls[controlName];
    const matchingControl = formGroup.controls[matchingControlName];

    if (matchingControl.errors && !matchingControl.errors.mustMatch) {
      // return if another validator has already found an error on the matchingControl
      return;
    }

    // set error on matchingControl if validation fails
    if (control.value !== matchingControl.value) {
      matchingControl.setErrors({mustMatch: true});
    } else {
      matchingControl.setErrors(null);
    }
  };
}

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {

  registerFormSubmitted = false;
  isLoginFailed = false;
  error: any;
  registerForm: FormGroup;


  constructor(
    private authService: AuthService,
    private router: Router,
    private formBuilder: FormBuilder
  ) {
    this.registerForm = this.formBuilder.group({
      email: new FormControl('member@messages.com', [Validators.required, Validators.email]),
      username: new FormControl('Username', [Validators.required]),
      password1: new FormControl('Password', [Validators.required, Validators.minLength(6)]),
      password2: new FormControl('Password', [Validators.required, Validators.minLength(6)]),
    }, {
      validator: MustMatch('password1', 'password2')
    });
  }

  ngOnInit(): void {
     if (this.authService.isLoggedIn()){
      this.router.navigateByUrl('/inbox');
    }
  }

  get lf(): { [key: string]: AbstractControl; } {
    return this.registerForm.controls;
  }

  onSubmit(): void {
    this.error = undefined;
    this.registerFormSubmitted = true;
    if (this.registerForm.invalid) {
      return;
    }

    this.authService.register(this.registerForm.value).subscribe(data => {
      console.log(data);
      this.router.navigate(['/inbox']);
    }, errorData => {
      this.error = errorData.error;
      console.log(this.error);
    });
  }

  gerErrors(error: any): any {
    if (error)
      return Object.entries(error);
  }
}
