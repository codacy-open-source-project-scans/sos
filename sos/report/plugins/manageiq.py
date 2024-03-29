# -*- python -*-
# -*- coding: utf-8 -*-

# Copyright (C) 2015 Red Hat, Inc., Pep Turró Mauri <pep@redhat.com>

# This file is part of the sos project: https://github.com/sosreport/sos
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# version 2 of the GNU General Public License.
#
# See the LICENSE file in the source distribution for further information.

from os import environ
import os.path
from sos.report.plugins import Plugin, RedHatPlugin


class ManageIQ(Plugin, RedHatPlugin):

    short_desc = 'ManageIQ/CloudForms related information'

    plugin_name = 'manageiq'

    miq_dir = '/var/www/miq/vmdb'

    packages = (
        'cfme',
        'cfme-appliance',
        'cfme-gemset',
        'cfme-appliance-tools',
        'cfme-appliance-common'
    )
    files = (
        os.path.join(miq_dir, 'BUILD'),
        os.path.join(miq_dir, 'GUID'),
        os.path.join(miq_dir, 'VERSION'),
        os.path.join(miq_dir, 'REGION')
    )

    # Config files to collect from miq_dir/config/
    miq_conf_dir = os.path.join(miq_dir, "config")
    miq_conf_files = [
        '*.rb',
        '*.yaml',
        '*.yml',
        '*.yml.db',
        '*.yml.sample',
        'settings/*.yml',
        'environments/*.rb',
        'environments/*.yml',
        'environments/patches/*.rb',
        'initializers/*.rb',
        'database.yml.old',
        'brakeman.ignore',
    ]

    # Log files to collect from miq_dir/log/
    miq_log_dir = os.path.join(miq_dir, "log")

    miq_main_logs = [
        'ansible_tower.log',
        'top_output.log',
        'evm.log',
        'production.log',
        'automation.log',
    ]

    miq_log_files = [
        '*.log',
        'apache/*.log',
        '*.txt',
        '*.yml',
    ]

    def setup(self):
        if self.get_option("all_logs"):
            # turn all log files to a glob to include logrotated ones
            self.miq_log_files = map(lambda x: x + '*', self.miq_log_files)

        self.add_copy_spec(list(self.files))

        self.add_copy_spec([
            self.path_join(self.miq_conf_dir, x) for x in self.miq_conf_files
        ])

        # Collect main log files without size limit.
        self.add_copy_spec([
            self.path_join(self.miq_log_dir, x) for x in self.miq_main_logs
        ], sizelimit=0)

        self.add_copy_spec([
            self.path_join(self.miq_log_dir, x) for x in self.miq_log_files
        ])

        self.add_copy_spec([
            "/var/log/tower.log",
            "/etc/manageiq/postgresql.conf.d/*.conf"
        ])

        if environ.get("APPLIANCE_PG_DATA"):
            pg_dir = environ.get("APPLIANCE_PG_DATA")
            self.add_copy_spec([
                    self.path_join(pg_dir, 'pg_log'),
                    self.path_join(pg_dir, 'postgresql.conf')
            ])

# vim: set et ts=4 sw=4 :
