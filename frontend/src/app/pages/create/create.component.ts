import { Component, OnInit } from '@angular/core';
import {AbstractControl, FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {Router} from '@angular/router';
import {MessageService} from '../../services/message.service';

@Component({
  selector: 'app-create',
  templateUrl: './create.component.html',
  styleUrls: ['./create.component.scss']
})
export class CreateComponent implements OnInit {

  messageFormSubmitted = false;
  error: any;
  messageForm: FormGroup;
  successMessage: any;

  constructor(
    private router: Router,
    private formBuilder: FormBuilder,
    private messageService: MessageService
  ) {
     this.messageForm = this.formBuilder.group({
      to_user: new FormControl('member@messages.com', [Validators.required, Validators.email]),
      title: new FormControl('Title', [Validators.required]),
      text: new FormControl('Text', [Validators.required])
    });
  }

  ngOnInit(): void {
  }

  get lf(): { [key: string]: AbstractControl; } {
    return this.messageForm.controls;
  }

  onSubmit(): void {
    this.error = undefined;
    this.successMessage = undefined;
    this.messageFormSubmitted = true;
    if (this.messageForm.invalid) {
      return;
    }

    this.messageService.send(this.messageForm.value).subscribe(m => {
      this.successMessage = m;
    }, errorData => {
      this.error = errorData.error;
      console.log(this.error);
    });
  }

  getMessages(res: any): any {
    if (res) {
      return Object.entries(res);
    }
  }

}
