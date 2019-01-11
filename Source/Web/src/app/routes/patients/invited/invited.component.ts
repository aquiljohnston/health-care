import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { StoreService } from '../../../services';
import { ReminderEmailComponent } from './modals/reminder-email/reminder-email.component';
import {
  uniqBy as _uniqBy,
  groupBy as _groupBy,
  filter as _filter,
  map as _map,
  flattenDeep as _flattenDeep,
  mean as _mean
} from 'lodash';
import * as moment from 'moment';
import patientsData from './../active/patients-data.js';

@Component({
  selector: 'app-invited',
  templateUrl: './invited.component.html',
  styleUrls: ['./invited.component.scss'],
})
export class InvitedPatientsComponent implements OnDestroy, OnInit {

  public invitedPatients = [];
  public invitedPatientsGrouped = [];
  public activeServiceAreas = {};
  public activeCarePlans = {};
  public openAlsoTip = {};
  public toolIP1Open;
  public accord1Open;
  public tooltip2Open;
  public tooltipPP2Open;
  public accord2Open;
  public multi1Open;
  public multi2Open;
  public multi3Open;
  public multi4Open;

  constructor(
    private router: Router,
    private modals: ModalService,
    private store: StoreService,

  ) { }

  public ngOnInit() {
    this.invitedPatients = [];
    this.invitedPatientsGrouped = [];
    this.getPatients().then((patients: any) => {
      patients = patientsData.results; // TODO: remove
      this.invitedPatients = _filter(patients, p => p.is_invited);
      this.invitedPatientsGrouped = this.groupPatientsByFacility(patients);

      this.allServiceAreas.forEach(serviceArea => {
        this.activeServiceAreas[serviceArea] = true;
      });

      this.allCarePlans.forEach(carePlan => {
        this.activeCarePlans[carePlan] = true;
      });

      console.log(this.uniqueFacilities());
      console.log(this.invitedPatientsGrouped);
    });
  }

  public ngOnDestroy() { }

  public getPatients() {
    let promise = new Promise((resolve, reject) => {
      let patientsSub = this.store.PatientProfile.readListPaged().subscribe(
        (patients) => {
          resolve(patients);
        },
        (err) => {
          reject(err);
        },
        () => {
          patientsSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public getAlsoPlans(i, patient) {
    if (patient && patient.care_plans) {
      const plans = patient.care_plans.slice();
      plans.splice(i, 1);
      return _map(plans, p => p.name);
    }
    return [];
  }

  public getPatientsForFacility(facility) {
    return this.invitedPatientsGrouped[facility.id];
  }

  public groupPatientsByFacility(patients) {
    let groupedByFacility = _groupBy(patients, (obj) => {
      return obj.facility.id;
    });
    return groupedByFacility;
  }

  get allPlans() {
    if (this.invitedPatients) {
      return _flattenDeep(_map(this.invitedPatients, p => p.care_plans));
    }
  }

  get allServiceAreas() {
    const plans = this.allPlans;
    return _uniqBy(_map(plans, p => p.service_area));
  }

  get allCarePlans() {
    const plans = _filter(this.allPlans, p => this.activeServiceAreas[p.service_area]);
    return _uniqBy(_map(plans, p => p.name));
  }


  public uniqueFacilities() {
    return _uniqBy(this.invitedPatients.map((obj) => { return obj.facility; }), 'id');
  }

  public daysSinceEnroll(patient) {
    const dateJoined = moment(patient.user.date_joined);
    const now = moment();
    return now.diff(dateJoined, 'days');
  }

  public toggleAllServiceAreas(status) {
    Object.keys(this.activeServiceAreas).forEach(area => {
      this.activeServiceAreas[area] = status;
    })
  }

  public toggleAllCarePlans(status) {
    Object.keys(this.activeServiceAreas).forEach(area => {
      this.activeServiceAreas[area] = status;
    })
  }

  public reminderEmail() {
    this.modals.open(ReminderEmailComponent, {
      closeDisabled: true,
      width: '512px',
    }).subscribe(() => {});
  }

  public confirmRemovePatient() {
    this.modals.open(ConfirmModalComponent, {
     'closeDisabled': true,
     data: {
       title: 'Remove Patient?',
       body: 'Are you sure you want to revoke this patient’s invitation? This cannot be undone.',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {
    // do something with result
    });
  }
}
