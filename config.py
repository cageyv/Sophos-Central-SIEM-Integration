#!/usr/bin/env python3

# Copyright 2019-2021 Sophos Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in
# compliance with the License.
# You may obtain a copy of the License at:  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing permissions and limitations under the
# License.
#

import re
import os
import configparser

# Default values for configuration
DEFAULTS = {
    'auth_url': 'https://id.sophos.com/api/v2/oauth2/token',
    'api_host': 'api.central.sophos.com',
    'format': 'json',
    'filename': 'result.txt',
    'endpoint': 'event',
    'address': '/var/run/syslog',
    'facility': 'daemon',
    'socktype': 'udp',
    'append_nul': 'false',
    'append_newline': 'false',
    'state_file_path': 'state/siem_sophos.json',
    'events_from_date_offset_minutes': '0',
    'alerts_from_date_offset_minutes': '0',
    'convert_dhost_field_to_valid_fqdn': 'true',
    'logging_level': 'INFO',
    'syslog_max_retries': '20',
    'token_info': '',
    'client_id': '',
    'client_secret': '',
    'tenant_id': '',
}


class Config:
    """Class providing config values from config.ini or environment variables"""

    def __init__(self, path):
        """Open the config file or use environment variables"""
        self.config = configparser.ConfigParser()
        self.use_env = False
        
        # Try to read config file
        if path and os.path.exists(path):
            self.config.read(path)
        else:
            # Config file doesn't exist, use environment variables
            self.use_env = True
            self._load_from_env()

    def _load_from_env(self):
        """Load configuration from environment variables"""
        self.config.add_section('login')
        
        # Map environment variables to config keys
        for key, default in DEFAULTS.items():
            env_var = f'SOPHOS_SIEM_{key.upper()}'
            value = os.environ.get(env_var, default)
            self.config.set('login', key, value)

    def __getattr__(self, name):
        try:
            return self.config.get("login", name)
        except (configparser.NoOptionError, configparser.NoSectionError):
            # Return default value if available
            return DEFAULTS.get(name, '')


class Token:
    def __init__(self, token_txt):
        """Initialize with the token text"""
        rex_txt = r"url\: (?P<url>https\://.+), x-api-key\: (?P<api_key>.+), Authorization\: (?P<authorization>.+)$"
        rex = re.compile(rex_txt)
        m = rex.search(token_txt)
        self.url = m.group("url")
        self.api_key = m.group("api_key")
        self.authorization = m.group("authorization").strip()
