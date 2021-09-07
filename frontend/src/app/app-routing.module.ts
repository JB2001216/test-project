import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {LoginComponent} from './pages/login/login.component';
import {RegisterComponent} from './pages/register/register.component';
import {InboxComponent} from './pages/inbox/inbox.component';
import {OutboxComponent} from './pages/outbox/outbox.component';
import {CreateComponent} from './pages/create/create.component';
import {AuthGuard} from './services/auth-guard.guard';


const routes: Routes = [
  {
    path: '',
    children: [
      {
        path: '',
        component: LoginComponent,
        data: {
          title: 'Login'
        }
      },
      {
        path: 'register',
        component: RegisterComponent,
        data: {
          title: 'Register'
        }
      },
      {
        path: 'inbox',
        component: InboxComponent,
        data: {
          title: 'Inbox'
        },
        canActivate: [AuthGuard]
      },

      {
        path: 'outbox',
        component: OutboxComponent,
        data: {
          title: 'Outbox'
        },
        canActivate: [AuthGuard]
      },
      {
        path: 'create',
        component: CreateComponent,
        data: {
          title: 'Create'
        },
        canActivate: [AuthGuard]
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
