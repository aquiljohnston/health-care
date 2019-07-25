import { Component, OnDestroy, OnInit } from '@angular/core';
import * as moment from 'moment';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import { AddPatientToPlanComponent, EnrollmentComponent } from '../../../components/';
import { AuthService, StoreService } from '../../../services';
import {
  uniq as _uniq,
  map as _map,
  find as _find,
  flattenDeep as _flattenDeep,
  compact as _compact,
  uniqBy as _uniqBy
} from 'lodash';

@Component({
  selector: 'app-potential',
  templateUrl: './potential.component.html',
  styleUrls: ['./potential.component.scss'],
})
export class PotentialPatientsComponent implements OnDestroy, OnInit {
  public facilities = [];
  public potentialPatients = [];
  public activeCarePlans = {};
  public users = null;
  public activeServiceAreas = {};
  public activePatients = [];
  public employee = null;
  public serviceAreas;
  public carePlanTemplates;
  public carePlanSearch: string = '';
  public serviceAreaSearch: string = '';
  public facilitySortDirection = {};
  public accordOpen = {};
  public accord1Open;
  public tooltip2Open;
  public tooltipPP2Open;
  public accord2Open;
  public toolPP1Open;
  public multi1Open;
  public multi2Open;
  public multi3Open;
  public multi4Open;
  private orgSub = null;
  private facilitiesSub = null;

  constructor(
    private modals: ModalService,
    private auth: AuthService,
    private store: StoreService,
  ) {
    // Nothing yet
  }

  public ngOnInit() {
    this.orgSub = this.auth.organization$.subscribe(org => {
      if (!org) {
        return;
      }

      this.facilitiesSub = this.store.Organization.detailRoute('GET', org.id, 'facilities').subscribe((facilities: any) => {
        if (facilities === null) {
          return;
        }

        this.facilities = facilities.results;
        this.facilities.forEach(f => {
          this.accordOpen[f.id] = this.accordOpen[f.id] || false;
          this.facilitySortDirection[f.id] = true;
        });

        this.auth.user$.subscribe(user => {
          if (!user) {
            return;
          }

          if (user.facilities.length === 1) {
            this.accordOpen[user.facilities[0].id] = true;
          }
        });

        const potentialPatientsSub = this.store.PotentialPatient.readListPaged().subscribe(
          (potentialPatients) => {
            this.potentialPatients = potentialPatients;
            this.potentialPatients.forEach(p => {
              p.facility && p.facility.forEach(f => {
                const facility = _find(this.facilities, fac => fac.id === f);
                if (facility) {
                  if (facility.potentialPatients && !_find(facility.potentialPatients, x => x.id === p.id)) {
                    facility.potentialPatients.push(p);
                  } else {
                    facility.potentialPatients = [p];
                  }
                }
              });
            });

            this.carePlans.forEach((p) => this.activeCarePlans[p] = true);
          },
          (err) => { },
          () => potentialPatientsSub.unsubscribe()
        );
      });
    });

    const employeesSub = this.store.EmployeeProfile.readListPaged().subscribe(
      (employees) => this.users = employees,
      (err) => { },
      () => employeesSub.unsubscribe()
    );

    this.auth.user$.subscribe(user => {
      if (!user) {
        return;
      }

      this.employee = user;
      if (this.employee.facilities.length === 1) {
        this.accordOpen[this.employee.facilities[0].id];
      }
    });

    this.store.ServiceArea.readListPaged().subscribe(res => {
      this.serviceAreas = res;
      this.serviceAreas.forEach(s => this.activeServiceAreas[s.id] = true);
    });

    this.store.CarePlanTemplate.readListPaged().subscribe(res => {
      this.carePlanTemplates = res;
      this.carePlanTemplates.forEach(c => this.activeCarePlans[c.id] = true);
    });
  }

  public ngOnDestroy() {
    this.facilitiesSub.unsubscribe();
  }

  public addPatientToPlan(facility = null) {
    const modalData = {
      data: {
        action: 'add',
        patientKnown: false,
        patientInSystem: false,
        planKnown: false,
        facility: facility,
      },
      width: '576px',
    };

    this.modals.open(AddPatientToPlanComponent, modalData).subscribe((data) => {
      if (!data) {
        return;
      }

      document.dispatchEvent(new Event('refreshPatientOverview'));
      this.potentialPatients.push(data);
      const facility = _find(this.facilities, f => f.id === data.facility[0]);
      if (facility.potentialPatients) {
        facility.potentialPatients.push(data);
      } else {
        facility.potentialPatients = [data];
      }
    });
  }

  public enrollPotentialPatient(potentialPatient) {
    const modalData = {
      width: '608px',
      data: { patient: potentialPatient }
    };

    this.modals.open(EnrollmentComponent, modalData).subscribe((res) => {
      if (!res) {
        return;
      }

      const facility = this.facilities.find(f => f.id === res.facility);
      facility.potentialPatients = facility.potentialPatients.filter(p => p.id !== res.patient);
    });
  }

  public editPotentialPatient(potentialPatient) {
    const modalData = {
      data: {
        action: 'edit',
        planKnown: potentialPatient.care_plan ? true : false,
        potentialPatient,
      },
      width: '576px',
    };

    this.modals.open(AddPatientToPlanComponent, modalData).subscribe((res) => {
      if (!res) {
        return;
      }

      let patient = this.potentialPatients.find(p => p.id === res.id);
      patient = Object.assign(patient, res);
    });
  }

  public removePotentialPatient(potentialPatient) {
    const modalData = {
      data: {
        title: 'Remove Patient?',
        body: 'Are you sure you want remove this patient from the list? This cannot be undone.',
        cancelText: 'Cancel',
        okText: 'Continue'
      },
      width: '384px',
    };

    this.modals.open(ConfirmModalComponent, modalData).subscribe((res) => {
      if (res !== modalData.data.okText) {
        return;
      }

      this.store.PotentialPatient.destroy(potentialPatient.id).subscribe(res => {
        this.potentialPatients = this.potentialPatients.filter(p => p.id !== potentialPatient.id);
        potentialPatient.facility.forEach(f => {
          const facility = this.facilities.find(fac => fac.id === f);
          facility.potentialPatients = facility.potentialPatients.filter(p => p.id !== potentialPatient.id);
        });
      });
    });
  }

  public formatTimeAdded(time) {
    return moment(time).fromNow();
  }

  get carePlans() {
    if (this.potentialPatients && this.potentialPatients.length) {
      return _uniq(_map(this.potentialPatients, p => p.care_plan));
    }

    return [];
  }

  get allPlans(): Array<any> {
    if (this.activePatients) {
      return _compact(_flattenDeep(_map(this.activePatients, p => p.care_plans)));
    }

    return null;
  }

  get allServiceAreas() {
    const plans = this.allPlans;
    return _uniqBy(_map(plans, p => p.service_area));
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

  public userInFacility(facility: { id: string }): boolean {
    return this.employee && !!(this.employee.facilities || []).find(f => f.id === facility.id);
  }

  public toggleFacilitySort(id) {
    const facility = this.facilities.find(f => f.id === id);
    facility.potentialPatients = facility.potentialPatients.reverse();
    this.facilitySortDirection[id] = !this.facilitySortDirection[id];
  }

  public saSearchMatch(sa) {
    return sa.name.indexOf(this.serviceAreaSearch) > -1;
  }

  public cpSearchMatch(cp) {
    return cp.name.indexOf(this.carePlanSearch) > -1;
  }
}
