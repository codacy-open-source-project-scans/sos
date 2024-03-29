# This file is part of the sos project: https://github.com/sosreport/sos
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# version 2 of the GNU General Public License.
#
# See the LICENSE file in the source distribution for further information.

from sos.report.plugins import Plugin, RedHatPlugin


class Convert2RHEL(Plugin, RedHatPlugin):
    """This plugin collects data generated by Convert2RHEL."""

    short_desc = 'Convert2RHEL'
    plugin_name = 'convert2rhel'
    profiles = ('system',)
    packages = ('convert2rhel',)
    verify_packages = ('convert2rhel$',)

    def setup(self):

        self.add_copy_spec([
            "/var/log/convert2rhel/convert2rhel.log",
            "/var/log/convert2rhel/archive/convert2rhel-*.log",
            "/var/log/convert2rhel/rpm_va.log",
            # Convert2RHEL generates a {pre,post}-conversion report.
            "/var/log/convert2rhel/convert2rhel-*-conversion.*",
        ])


# vim: set et ts=4 sw=4 :
