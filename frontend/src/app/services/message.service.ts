import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class MessageService {
  AUTH_SERVER_ADDRESS: string = environment.apiUrl;

  constructor(private  http: HttpClient) {
  }

  send(formValue: any): Observable<any> {
    return this.http.post(this.AUTH_SERVER_ADDRESS + '/messages/', formValue);
  }

  inbox(url?: string): Observable<any> {
    const apiUrl = url || this.AUTH_SERVER_ADDRESS + '/messages/inbox/';
    return this.http.get(apiUrl);
  }

  outbox(url?: string): Observable<any> {
    const apiUrl = url || this.AUTH_SERVER_ADDRESS + '/messages/outbox/';
    return this.http.get(apiUrl);
  }

  delete(id: number): Observable<any> {
    return this.http.delete(this.AUTH_SERVER_ADDRESS + `/messages/${id}/`);
  }

}
