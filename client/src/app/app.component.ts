import { Tweet } from './tweet.model';
import { Component , OnInit} from '@angular/core';
import {Http} from '@angular/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  tweetsList: Tweet[] = [];
  constructor(private _http: Http) {}

  ngOnInit() {
    this.gettweets().subscribe(response =>
        JSON.parse(response['_body']).map(tweet => this.tweetsList.push( new Tweet(tweet['text'], tweet['time']))
      )
    );

  }
  gettweets() {
    return this._http.get('/zappy/gettweets');
  }
}

