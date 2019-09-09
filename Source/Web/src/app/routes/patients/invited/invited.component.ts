import { Component, OnDestroy, OnInit } from '@angular/core';
import * as moment from 'moment';
import { filter as _filter, flattenDeep as _flattenDeep, groupBy as _groupBy, map as _map, mean as _mean, uniqBy as _uniqBy } from 'lodash';

import { AppConfig } from '../../../app.config';
import { HttpService, StoreService, AuthService } from '../../../services';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { PatientCreationModalService } from '../../../services/patient-creation-modal.service';
import { ReminderEmailComponent } from './modals/reminder-email/reminder-email.component';

import { IAddPatientToPlanComponentData } from '../../../models/iadd-patient-to-plan-component-data';

@Component({
  selector: 'app-invited',
  templateUrl: './invited.component.html',
  styleUrls: ['./invited.component.scss'],
})
export class InvitedPatientsComponent implements OnDestroy, OnInit {
  public invitedPatients = [];
  public invitedPatientsGrouped = [];
  public serviceAreas = [];
  public serviceAreaSearch: string = '';
  public carePlanSearch: string = '';
  public activeServiceAreas: { [key: string]: boolean } = {};
  public carePlanTemplates = [];
  public activeCarePlans: { [key: string]: boolean } = {};
  public openAlsoTip = {};
  public toolIP1Open;
  public tooltip2Open: { [key: string]: boolean } = {};
  public tooltipPP2Open;
  public accord2Open;
  public multi1Open;
  public multi2Open;
  public multi3Open;
  public multi4Open;
  public totalInvited = 0;
  public facilityAccordOpen: { [key: string]: boolean } = {};
  public facilities = [];
  public employees = [];
  public employeeChecked = {};
  public userSearch: string = '';

  constructor(
    private auth: AuthService,
    private http: HttpService,
    private modals: ModalService,
    private patientCreationModalService: PatientCreationModalService,
    private store: StoreService,
  ) {
    // Nothing yet
  }

  public ngOnInit() {
    this.invitedPatients = [];
    this.invitedPatientsGrouped = [];
    this.store.Facility.readListPaged().subscribe((res: any) => {
      this.facilities = res.filter(f => !f.is_affiliate);
      this.facilities.forEach(f => this.facilityAccordOpen[f.id] = false);
      this.auth.user$.subscribe(user => {
        if (!user) {
          return;
        }

        if (user.facilities.length === 1) {
          this.facilityAccordOpen[user.facilities[0].id] = true;
        }

        this.facilities = this.facilities.filter(f => user.facilities.find(fa => fa.id === f.id));
      });

      this.facilities.forEach(facility => {
        this.getPatients(facility).then((patients: any) => {
          facility.invitedPatients = patients.results;
          facility.invitedPatients.forEach(patient => {
            this.store.CarePlan.readListPaged({ patient: patient.id }).subscribe(plans => {
              patient.carePlans = plans;
              patient.carePlans.forEach(plan => {
                this.store.CareTeamMember.readListPaged({ plan: plan.id }).subscribe(careTeamMembers => {
                  plan.careTeamMembers = careTeamMembers;
                });
              });
            });
          });
        });
      });
    });

    this.store.EmployeeProfile.readListPaged().subscribe((res: any) => {
      this.employees = res;
      this.employees.forEach(e => {
        this.employeeChecked[e.id] = true;
      });
    });

    this.store.ServiceArea.readListPaged().subscribe(res => {
      this.serviceAreas = res;
      this.serviceAreas.forEach(sa => {
        this.activeServiceAreas[sa.id] = true;
      });
    });

    this.store.CarePlanTemplate.readListPaged().subscribe(res => {
      this.carePlanTemplates = res;
      this.carePlanTemplates.forEach(cp => this.activeCarePlans[cp.id] = true);
    });

    this.auth.organization$.subscribe(org => {
      if (!org) {
        return;
      }

      this.store.PatientProfile
        .listRoute('GET', 'overview', {}, { 'facility__organization__id': org.id })
        .subscribe((res: any) => this.totalInvited = res.invited);
    });
  }

  public ngOnDestroy() { }

  public getPatients(facility): Promise<any> {
    const promise = new Promise<any>((resolve, reject) => {
      const patientsSub = this.store.Facility.detailRoute('GET', facility.id, 'patients', {}, { type: 'invited' }).subscribe(
        (patients) => resolve(patients),
        (err) => reject(err),
        () => patientsSub.unsubscribe()
      );
    });

    return promise;
  }

  public getAlsoPlans(i, patient): Array<any> {
    if (patient && patient.carePlans) {
      const plans = patient.carePlans.slice();
      plans.splice(i, 1);

      return _map(plans, p => p.plan_template.name);
    }

    return [];
  }

  public getPatientsForFacility(facility) {
    return this.invitedPatientsGrouped[facility.id];
  }

  public groupPatientsByFacility(patients) {
    const groupedByFacility = _groupBy(patients, (obj) => obj.facility.id);
    return groupedByFacility;
  }

  get allPlans(): Array<any> {
    if (this.invitedPatients) {
      return _flattenDeep(_map(this.invitedPatients, p => p.care_plans));
    }

    return null;
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
    return _uniqBy(this.invitedPatients.map((obj) => obj.facility), 'id');
  }

  public daysSinceEnroll(patient) {
    const dateJoined = moment(patient.user.date_joined);
    const now = moment();
    return now.diff(dateJoined, 'days');
  }

  public toggleAllServiceAreas(status) {
    Object.keys(this.activeServiceAreas).forEach(area => {
      this.activeServiceAreas[area] = status;
    });
  }

  public toggleAllCarePlans(status) {
    Object.keys(this.activeCarePlans).forEach(area => {
      this.activeCarePlans[area] = status;
    });
  }

  public reminderEmail(patient, facility) {
    const modalSub = this.modals.open(ReminderEmailComponent, {
      data: {
        patient,
        facility
      },
      width: '512px',
    }).subscribe(
      (response) => {
        if (!response) {
          return;
        }

        const url = AppConfig.apiUrl + 'reminder_email';
        const reminderData = {
          patient: response.patient.id,
          subject: response.subject,
          message: response.message,
        };
        const postSub = this.http.post(url, reminderData).subscribe(
          (success) => {
            patient.emails_sent++;
          },
          (err) => console.error(err),
          () => postSub.unsubscribe()
        );
      },
      (err) => { },
      () => modalSub.unsubscribe()
    );
  }

  public addPatientToPlan() {
    const data:IAddPatientToPlanComponentData = {
        action: 'add',
        enrollPatientChecked: true
    };

    this.patientCreationModalService.openEnrollment_PotentialPatientDetails(data);
  }

  public confirmRemovePatient(facility, patient, plan) {
    const modalData = {
      data: {
        title: 'Remove Patient?',
        body: 'Are you sure you want to revoke this patient’s invitation? This cannot be undone.',
        cancelText: 'Cancel',
        okText: 'Continue',
      },
      width: '384px'
    };
    this.modals.open(ConfirmModalComponent, modalData).subscribe((res) => {
      if (res !== modalData.data.okText) {
        return;
      }

      this.store.CarePlan.destroy(plan.id).subscribe(res => {
        const targetFacility = this.facilities.find(f => f.id === facility.id);
        const targetPatient = targetFacility.invitedPatients.find(p => p.id === patient.id);
        patient.carePlans = targetPatient.carePlans.filter(p => p.id !== plan.id);
        document.dispatchEvent(new Event('refreshPatientOverview'));

        this.auth.organization$.subscribe(org => {
          if (!org) {
            return;
          }

          this.store.PatientProfile.listRoute('GET', 'overview', {}, { 'facility__organization__id': org.id }).subscribe((res: any) => {
            this.totalInvited = res.invited;
          });
        });
      });
    });
  }

  public hasCheckedCareTeamMember(plan): boolean {
    let result = false;
    if (plan.careTeamMembers) {
      plan.careTeamMembers.forEach(teamMember => {
        if (this.employeeChecked[teamMember.employee_profile.id]) {
          result = true;
        }
      });
    }

    return result;
  }

  public userSearchMatch(user) {
    return `${user.user.first_name} ${user.user.last_name}`.toLowerCase().indexOf(this.userSearch) > -1;
  }

  public toggleAllUsers(status) {
    Object.keys(this.employeeChecked).forEach(id => {
      this.employeeChecked[id] = status;
    });
  }

  public saSearchMatch(sa) {
    return sa.name.toLowerCase().indexOf(this.serviceAreaSearch.toLowerCase()) > -1;
  }

  public cpSearchMatch(cp) {
    return cp.name.toLowerCase().indexOf(this.carePlanSearch.toLowerCase()) > -1;
  }

  public patientsWithPlansCount(patients): number {
    return (patients || []).filter(p => p.carePlans && p.carePlans.length).length;
  }
}
