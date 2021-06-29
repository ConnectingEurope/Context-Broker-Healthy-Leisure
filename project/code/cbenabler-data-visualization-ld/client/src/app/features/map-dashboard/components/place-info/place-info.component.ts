import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { takeUntil } from 'rxjs/operators';
import { BaseComponent } from 'src/app/shared/misc/base.component';
import { Entity } from 'src/app/shared/models/entity';
import { ModelDto } from 'src/app/shared/models/model-dto';
import { skyState } from 'src/app/shared/models/sky-state';
import { MapDashboardService } from '../../services/map-dashboard.service';

@Component({
  selector: 'app-place-info',
  templateUrl: './place-info.component.html',
  styleUrls: ['./place-info.component.scss'],
})
export class PlaceInfoComponent  implements OnInit {
  private firstLoad: boolean = false;
  beachEntity: Entity;
  airQualityEntity: Entity;
  skyStateData: skyState;

  constructor( private mapDashBoardService: MapDashboardService) {

    this.mapDashBoardService.getSkyState().toPromise().then(
      (sky:skyState)=>{
        this.skyStateData = sky;
      });
    this.mapDashBoardService.getEntitiesData(!this.firstLoad).toPromise().then(
      (models: ModelDto[]) => {
        models.forEach((model, i) => {
          model.data.forEach(entity =>{
             switch(entity.id){
              case 'urn:ngsi-ld:Beach:Benidorm:Playa-Levante:B001':
                this.beachEntity = entity;
                break;
              case 'urn:ngsi-ld:AirQualityObserved:Benidorm:AQO001':
                this.airQualityEntity = entity;
     
             }
          });
         
      });
      });
   }

  public ngOnInit(): void {

  }

 
}
