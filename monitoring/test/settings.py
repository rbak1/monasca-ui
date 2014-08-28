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

import os

from django.utils.translation import ugettext_lazy as _  # noqa

from horizon.test.settings import *  # noqa
from horizon.utils import secret_key as secret_key_utils


DEBUG = True
TEMPLATE_DEBUG = DEBUG

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.abspath(os.path.join(TEST_DIR, ".."))

MEDIA_ROOT = os.path.abspath(os.path.join(ROOT_PATH, '..', 'media'))
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.abspath(os.path.join(ROOT_PATH, '..', 'static'))
STATIC_URL = '/static/'

SECRET_KEY = secret_key_utils.generate_or_read_from_file(
    os.path.join(TEST_DIR, '.secret_key_store'))
ROOT_URLCONF = 'monitoring.test.urls'
TEMPLATE_DIRS = (
    os.path.join(TEST_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'openstack_dashboard.context_processors.openstack',
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django_nose',
    'openstack_auth',
    'compressor',
    'horizon',
    'openstack_dashboard',
    'openstack_dashboard.dashboards.project',
    'openstack_dashboard.dashboards.admin',
    'monitoring',
    'openstack_dashboard.dashboards.settings',
)

AUTHENTICATION_BACKENDS = ('openstack_auth.backend.KeystoneBackend',)

SITE_BRANDING = 'OpenStack'

HORIZON_CONFIG = {
    'dashboards': ('project',),
    'default_dashboard': 'project',
    "password_validator": {
        "regex": '^.{8,18}$',
        "help_text": _("Password must be between 8 and 18 characters.")
    },
    'user_home': None,
    'help_url': "http://docs.openstack.org",
}

# Set to True to allow users to upload images to glance via Horizon server.
# When enabled, a file form field will appear on the create image form.
# See documentation for deployment considerations.
HORIZON_IMAGES_ALLOW_UPLOAD = True

AVAILABLE_REGIONS = [
    ('http://localhost:5000/v2.0', 'local'),
    ('http://remote:5000/v2.0', 'remote'),
]

OPENSTACK_KEYSTONE_URL = "http://localhost:5000/v2.0"
OPENSTACK_KEYSTONE_DEFAULT_ROLE = "Member"

OPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = True
OPENSTACK_KEYSTONE_DEFAULT_DOMAIN = 'test_domain'

OPENSTACK_KEYSTONE_BACKEND = {
    'name': 'native',
    'can_edit_user': True,
    'can_edit_group': True,
    'can_edit_project': True,
    'can_edit_domain': True,
    'can_edit_role': True
}

OPENSTACK_NEUTRON_NETWORK = {
    'enable_lb': False,
    'enable_firewall': False,
    'enable_vpn': False,
    'profile_support': None,
    'enable_distributed_router': False,
}

OPENSTACK_HYPERVISOR_FEATURES = {
    'can_set_mount_point': False,
    'can_encrypt_volumes': False,
}

LOGGING['loggers']['openstack_dashboard'] = {
    'handlers': ['test'],
    'propagate': False,
}

LOGGING['loggers']['selenium'] = {
    'handlers': ['test'],
    'propagate': False,
}

SECURITY_GROUP_RULES = {
    'all_tcp': {
        'name': 'ALL TCP',
        'ip_protocol': 'tcp',
        'from_port': '1',
        'to_port': '65535',
    },
    'http': {
        'name': 'HTTP',
        'ip_protocol': 'tcp',
        'from_port': '80',
        'to_port': '80',
    },
}

NOSE_ARGS = ['--nocapture',
             '--nologcapture',
             '--cover-package=openstack_dashboard',
             '--cover-inclusive',
             '--all-modules']

TUSKAR_ENDPOINT_URL = "http://127.0.0.1:8585"

OVERCLOUD_CREDS = {
    'enabled': True,
    'user': 'admin',
    'password': 'password',
    'tenant': 'admin',
    'auth_url': 'http://localhost:5000/v2.0/',
}
