import { Component, OnInit } from '@angular/core';
import {MessageService} from '../../services/message.service';

@Component({
  selector: 'app-outbox',
  templateUrl: './outbox.component.html',
  styleUrls: ['./outbox.component.scss']
})
export class OutboxComponent implements OnInit {

  messages: any;
  next: any;
  prev: any;


  constructor(private messagesService: MessageService) { }

  ngOnInit(): void {
    this.getMessages();
  }

  getMessages(): void {
    this.messagesService.outbox().subscribe(data => {
      this.prev = data.previous;
      this.next = data.next;
      this.messages = data.results;
    });
  }

  delete(id: number): void {
    this.messagesService.delete(id).subscribe(() => {
      this.getMessages();
    });
  }

  prevNext(url: any): void {
     this.messagesService.outbox(url).subscribe(data => {
      this.prev = data.previous;
      this.next = data.next;
      this.messages = data.results;
    });
  }

}
