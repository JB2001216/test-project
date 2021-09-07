import {Component, OnInit} from '@angular/core';
import {MessageService} from '../../services/message.service';

@Component({
  selector: 'app-inbox',
  templateUrl: './inbox.component.html',
  styleUrls: ['./inbox.component.scss']
})
export class InboxComponent implements OnInit {

  messages: any;
  next: any;
  prev: any;

  constructor(private messagesService: MessageService) {
  }

  ngOnInit(): void {
    this.getMessages();
  }

  getMessages(): void {
    this.messagesService.inbox().subscribe(data => {
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
     this.messagesService.inbox(url).subscribe(data => {
      this.prev = data.previous;
      this.next = data.next;
      this.messages = data.results;
    });
  }
}
