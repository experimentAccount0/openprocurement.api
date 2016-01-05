# -*- coding: utf-8 -*-
from logging import getLogger
from openprocurement.api.models import STAND_STILL_TIME, get_now
from openprocurement.api.utils import (
    add_next_award,
    apply_patch,
    check_tender_status,
    context_unpack,
    json_view,
    opresource,
    save_tender,
    set_ownership,
)
from openprocurement.api.validation import (
    validate_complaint_data,
    validate_patch_complaint_data,
)


LOGGER = getLogger(__name__)


@opresource(name='Tender Award Complaints',
            collection_path='/tenders/{tender_id}/awards/{award_id}/complaints',
            path='/tenders/{tender_id}/awards/{award_id}/complaints/{complaint_id}',
            procurementMethodType='belowThreshold',
            description="Tender award complaints")
class TenderAwardComplaintResource(object):

    def __init__(self, request, context):
        self.context = context
        self.request = request
        self.db = request.registry.db

    @json_view(content_type="application/json", permission='create_award_complaint', validators=(validate_complaint_data,))
    def collection_post(self):
        """Post a complaint for award
        """
        tender = self.request.validated['tender']
        if tender.status not in ['active.qualification', 'active.awarded']:
            self.request.errors.add('body', 'data', 'Can\'t add complaint in current ({}) tender status'.format(tender.status))
            self.request.errors.status = 403
            return
        if any([i.status != 'active' for i in tender.lots if i.id == self.context.lotID]):
            self.request.errors.add('body', 'data', 'Can add complaint only in active lot status')
            self.request.errors.status = 403
            return
        if self.context.complaintPeriod and \
           (self.context.complaintPeriod.startDate and self.context.complaintPeriod.startDate > get_now() or
                self.context.complaintPeriod.endDate and self.context.complaintPeriod.endDate < get_now()):
            self.request.errors.add('body', 'data', 'Can add complaint only in complaintPeriod')
            self.request.errors.status = 403
            return
        complaint = self.request.validated['complaint']
        if complaint.status == 'claim':
            complaint.dateSubmitted = get_now()
        else:
            complaint.status == 'draft'
        set_ownership(complaint, self.request)
        self.context.complaints.append(complaint)
        if save_tender(self.request):
            LOGGER.info('Created tender award complaint {}'.format(complaint.id),
                        extra=context_unpack(self.request, {'MESSAGE_ID': 'tender_award_complaint_create'}, {'complaint_id': complaint.id}))
            self.request.response.status = 201
            self.request.response.headers['Location'] = self.request.route_url('Tender Award Complaints', tender_id=tender.id, award_id=self.request.validated['award_id'], complaint_id=complaint['id'])
            return {
                'data': complaint.serialize("view"),
                'access': {
                    'token': complaint.owner_token
                }
            }

    @json_view(permission='view_tender')
    def collection_get(self):
        """List complaints for award
        """
        return {'data': [i.serialize("view") for i in self.context.complaints]}

    @json_view(permission='view_tender')
    def get(self):
        """Retrieving the complaint for award
        """
        return {'data': self.context.serialize("view")}

    @json_view(content_type="application/json", permission='edit_complaint', validators=(validate_patch_complaint_data,))
    def patch(self):
        """Post a complaint resolution for award
        """
        tender = self.request.validated['tender']
        if tender.status not in ['active.qualification', 'active.awarded']:
            self.request.errors.add('body', 'data', 'Can\'t update complaint in current ({}) tender status'.format(tender.status))
            self.request.errors.status = 403
            return
        if any([i.status != 'active' for i in tender.lots if i.id == self.request.validated['award'].lotID]):
            self.request.errors.add('body', 'data', 'Can update complaint only in active lot status')
            self.request.errors.status = 403
            return
        if self.context.status not in ['draft', 'claim', 'answered', 'pending']:
            self.request.errors.add('body', 'data', 'Can\'t update complaint in current ({}) status'.format(self.context.status))
            self.request.errors.status = 403
            return
        data = self.request.validated['data']
        complaintPeriod = self.request.validated['award'].complaintPeriod
        is_complaintPeriod = complaintPeriod and complaintPeriod.startDate and complaintPeriod.startDate < get_now()
        is_complaintPeriod = is_complaintPeriod and complaintPeriod.endDate and complaintPeriod.endDate > get_now()
        # complaint_owner
        if self.request.authenticated_role == 'complaint_owner' and self.context.status in ['draft', 'claim', 'answered', 'pending'] and data.get('status', self.context.status) == 'cancelled':
            apply_patch(self.request, save=False, src=self.context.serialize())
            self.context.dateCanceled = get_now()
        elif self.request.authenticated_role == 'complaint_owner' and is_complaintPeriod and self.context.status == 'draft' and data.get('status', self.context.status) == self.context.status:
            apply_patch(self.request, save=False, src=self.context.serialize())
        elif self.request.authenticated_role == 'complaint_owner' and is_complaintPeriod and self.context.status == 'draft' and data.get('status', self.context.status) == 'claim':
            apply_patch(self.request, save=False, src=self.context.serialize())
            self.context.dateSubmitted = get_now()
        elif self.request.authenticated_role == 'complaint_owner' and self.context.status == 'answered' and data.get('status', self.context.status) == self.context.status:
            apply_patch(self.request, save=False, src=self.context.serialize())
        elif self.request.authenticated_role == 'complaint_owner' and self.context.status == 'answered' and data.get('satisfied', self.context.satisfied) is True and data.get('status', self.context.status) == 'resolved':
            apply_patch(self.request, save=False, src=self.context.serialize())
        elif self.request.authenticated_role == 'complaint_owner' and self.context.status == 'answered' and data.get('satisfied', self.context.satisfied) is False and data.get('status', self.context.status) == 'pending':
            apply_patch(self.request, save=False, src=self.context.serialize())
            self.context.dateEscalated = get_now()
        # tender_owner
        elif self.request.authenticated_role == 'tender_owner' and self.context.status == 'claim' and data.get('status', self.context.status) == self.context.status:
            apply_patch(self.request, save=False, src=self.context.serialize())
        elif self.request.authenticated_role == 'tender_owner' and self.context.status == 'claim' and data.get('resolutionType', self.context.resolutionType) and data.get('status', self.context.status) == 'answered':
            apply_patch(self.request, save=False, src=self.context.serialize())
            self.context.dateAnswered = get_now()
        # reviewers
        elif self.request.authenticated_role == 'reviewers' and self.context.status == 'pending' and data.get('status', self.context.status) == self.context.status:
            apply_patch(self.request, save=False, src=self.context.serialize())
        elif self.request.authenticated_role == 'reviewers' and self.context.status == 'pending' and data.get('status', self.context.status) in ['pending', 'resolved', 'invalid', 'declined']:
            apply_patch(self.request, save=False, src=self.context.serialize())
            self.context.dateDecision = get_now()
        else:
            self.request.errors.add('body', 'data', 'Can\'t update complaint')
            self.request.errors.status = 403
            return
        if self.context.status not in ['draft', 'claim', 'answered', 'pending'] and tender.status == 'active.awarded':
            check_tender_status(self.request)
        if save_tender(self.request):
            LOGGER.info('Updated tender award complaint {}'.format(self.context.id),
                        extra=context_unpack(self.request, {'MESSAGE_ID': 'tender_award_complaint_patch'}))
            return {'data': self.context.serialize("view")}
