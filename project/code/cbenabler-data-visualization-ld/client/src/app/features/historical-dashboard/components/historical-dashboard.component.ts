import { Component, OnInit,ElementRef,Renderer2 } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-historical-dashboard',
  templateUrl: './historical-dashboard.component.html',
  styleUrls: ['./historical-dashboard.component.scss'],
})
export class HistoricalDashboardComponent implements OnInit {
  private el: any;
  private renderer: Renderer2;
  private prevHeight: number;
  private sameCount: number;

  public usersDashboard: any = "http://your_ip/app/dashboards#/"; // // Copy here the dashboard URL from your Kibana
  public routesDashboard: any = "http://your_ip/app/dashboards#/"; // // Copy here the dashboard URL from your Kibana
  public beachDashboard: any = "http://your_ip/app/dashboards#/"; // // Copy here the dashboard URL from your Kibana

  public dashboardRef: any;

  constructor(private sanitizer: DomSanitizer) {
    this.dashboardRef = this.sanitizer.bypassSecurityTrustResourceUrl(this.beachDashboard);
   }


  public ngOnInit(): void {
  }
  public changeDashboard(dashboard: string): void {
    switch (dashboard) {
      case 'beach':
        this.dashboardRef = this.sanitizer.bypassSecurityTrustResourceUrl(this.beachDashboard);
        break;
      case 'routes':
        this.dashboardRef = this.sanitizer.bypassSecurityTrustResourceUrl(this.routesDashboard);
        break;
      case 'users':
        this.dashboardRef = this.sanitizer.bypassSecurityTrustResourceUrl(this.usersDashboard);
        break;
      default:
        this.dashboardRef = this.sanitizer.bypassSecurityTrustResourceUrl(this.beachDashboard);
        break;
    }
  }

}

