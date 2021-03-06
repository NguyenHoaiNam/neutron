# Copyright 2013 IBM Corp.
# All Rights Reserved.
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

"""
IPv6-related utilities and helper functions.
"""
import os

from debtcollector import moves
from debtcollector import removals
import netaddr
from neutron_lib import constants as const
from oslo_log import log

from neutron._i18n import _, _LI


LOG = log.getLogger(__name__)
_IS_IPV6_ENABLED = None


@removals.remove(
    message="use get_ipv6_addr_by_EUI64 from oslo_utils.netutils",
    version="Newton",
    removal_version="Ocata")
def get_ipv6_addr_by_EUI64(prefix, mac):
    # Check if the prefix is IPv4 address
    isIPv4 = netaddr.valid_ipv4(prefix)
    if isIPv4:
        msg = _("Unable to generate IP address by EUI64 for IPv4 prefix")
        raise TypeError(msg)
    try:
        eui64 = int(netaddr.EUI(mac).eui64())
        prefix = netaddr.IPNetwork(prefix)
        return netaddr.IPAddress(prefix.first + eui64 ^ (1 << 57))
    except (ValueError, netaddr.AddrFormatError):
        raise TypeError(_('Bad prefix or mac format for generating IPv6 '
                          'address by EUI-64: %(prefix)s, %(mac)s:')
                        % {'prefix': prefix, 'mac': mac})
    except TypeError:
        raise TypeError(_('Bad prefix type for generate IPv6 address by '
                          'EUI-64: %s') % prefix)


def is_enabled_and_bind_by_default():
    """Check if host has the IPv6 support and is configured to bind IPv6
    address to new interfaces by default.
    """
    global _IS_IPV6_ENABLED

    if _IS_IPV6_ENABLED is None:
        disabled_ipv6_path = "/proc/sys/net/ipv6/conf/default/disable_ipv6"
        if os.path.exists(disabled_ipv6_path):
            with open(disabled_ipv6_path, 'r') as f:
                disabled = f.read().strip()
            _IS_IPV6_ENABLED = disabled == "0"
        else:
            _IS_IPV6_ENABLED = False
        if not _IS_IPV6_ENABLED:
            LOG.info(_LI("IPv6 not present or configured not to bind to new "
                         "interfaces on this system. Please ensure IPv6 is "
                         "enabled and /proc/sys/net/ipv6/conf/default/"
                         "disable_ipv6 is set to 1 to enable IPv6."))
    return _IS_IPV6_ENABLED


is_enabled = moves.moved_function(is_enabled_and_bind_by_default,
                                  'is_enabled', __name__, version='Ocata',
                                  removal_version='Pike')


def is_auto_address_subnet(subnet):
    """Check if subnet is an auto address subnet."""
    modes = [const.IPV6_SLAAC, const.DHCPV6_STATELESS]
    return (subnet['ipv6_address_mode'] in modes
            or subnet['ipv6_ra_mode'] in modes)


def is_eui64_address(ip_address):
    """Check if ip address is EUI64."""
    ip = netaddr.IPAddress(ip_address)
    # '0xfffe' addition is used to build EUI-64 from MAC (RFC4291)
    # Look for it in the middle of the EUI-64 part of address
    return ip.version == 6 and not ((ip & 0xffff000000) ^ 0xfffe000000)


def is_ipv6_pd_enabled(subnet):
    """Returns True if the subnetpool_id of the given subnet is equal to
       constants.IPV6_PD_POOL_ID
    """
    return subnet.get('subnetpool_id') == const.IPV6_PD_POOL_ID
