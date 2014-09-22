# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Hewlett-Packard Development Company, L.P.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _  # noqa

from horizon import tables

from monitoring.alarmdefs import constants
from monitoring import api

LOG = logging.getLogger(__name__)


def show_by_dimension(data, dim_name):
    if 'dimensions' in data['expression_data']:
        dimensions = data['expression_data']['dimensions']
        if dim_name in dimensions:
            return str(data['expression_data']['dimensions'][dim_name])
    return ""


class CreateAlarm(tables.LinkAction):
    name = "create_alarm"
    verbose_name = _("Create Alarm Definition")
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = (("alarm", "alarm:create"),)
    ajax = True


    def get_link_url(self):
        return urlresolvers.reverse(constants.URL_PREFIX + 'alarm_create',
                                    args=())

    def allowed(self, request, datum=None):
        return True


class EditAlarm(tables.LinkAction):
    name = "edit_alarm"
    verbose_name = _("Edit Alarm Definition")
    classes = ("ajax-modal", "btn-create")

    def get_link_url(self, datum):
        return urlresolvers.reverse(constants.URL_PREFIX + 'alarm_edit',
                                    args=(
                                          datum['id'], ))

    def allowed(self, request, datum=None):
        return True


class GraphMetric(tables.LinkAction):
    name = "graph_alarm"
    verbose_name = _("Graph Metric")
    icon = "dashboard"

    def render(self):
        self.attrs['target'] = 'newtab'
        return super(self, GraphMetric).render()

    def get_link_url(self, datum):
        name = datum['expression_data']['metric_name']
        threshold = datum['expression_data']['threshold']
        self.attrs['target'] = '_blank'
        return "/static/grafana/index.html#/dashboard/script/detail.js?token=%s&name=%s&threshold=%s" % \
               (self.table.request.user.token.id, name, threshold)

    def allowed(self, request, datum=None):
        return 'metric_name' in datum['expression_data']


class DeleteAlarm(tables.DeleteAction):
    name = "delete_alarm"
    verbose_name = _("Delete Alarm Definition")
    data_type_singular = _("Alarm Definition")
    data_type_plural = _("Alarm Definitions")

    def allowed(self, request, datum=None):
        return True

    def delete(self, request, obj_id):
        api.monitor.alarm_delete(request, obj_id)


class AlarmsFilterAction(tables.FilterAction):
    def filter(self, table, alarms, filter_string):
        """Naive case-insensitive search."""
        q = filter_string.lower()
        return [alarm for alarm in alarms
                if q in alarm.name.lower()]


class AlarmsTable(tables.DataTable):
    target = tables.Column('name', verbose_name=_('Name'),
                           link=constants.URL_PREFIX + 'alarm_detail',
                           )
    description = tables.Column('description', verbose_name=_('Description'))
    enabled = tables.Column('actions_enabled',
                            verbose_name=_('Notifications Enabled'))

    def get_object_id(self, obj):
        return obj['id']

    def get_object_display(self, obj):
        return obj['name']

    class Meta:
        name = "alarms"
        verbose_name = _("Alarm Definitions")
        row_actions = (GraphMetric,
                       EditAlarm,
                       DeleteAlarm,
                       )
        table_actions = (CreateAlarm,
                         AlarmsFilterAction,
                         DeleteAlarm,
                        )