# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2012 NEC Corporation.  All rights reserved.
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
# @author: Ryota MIBU

from quantum.openstack.common import cfg
# import rpc config options
from quantum.openstack.common import rpc


database_opts = [
    cfg.StrOpt('sql_connection', default='sqlite://'),
    cfg.IntOpt('sql_max_retries', default=-1),
    cfg.IntOpt('reconnect_interval', default=2),
    cfg.IntOpt('sql_min_pool_size',
               default=1,
               help=_("Minimum number of SQL connections to keep open in a "
                      "pool")),
    cfg.IntOpt('sql_max_pool_size',
               default=5,
               help=_("Maximum number of SQL connections to keep open in a "
                      "pool")),
    cfg.IntOpt('sql_idle_timeout',
               default=3600,
               help=_("Timeout in seconds before idle sql connections are "
                      "reaped")),
    cfg.BoolOpt('sql_dbpool_enable',
                default=False,
                help=_("Enable the use of eventlet's db_pool for MySQL")),
]

ovs_opts = [
    cfg.StrOpt('integration_bridge', default='br-int'),
]

agent_opts = [
    cfg.IntOpt('polling_interval', default=2),
    cfg.StrOpt('root_helper', default='sudo'),
]

ofc_opts = [
    cfg.StrOpt('host', default='127.0.0.1'),
    cfg.StrOpt('port', default='8888'),
    cfg.StrOpt('driver', default='trema'),
    cfg.BoolOpt('enable_packet_filter', default=True),
    cfg.BoolOpt('use_ssl', default=False),
    cfg.StrOpt('key_file', default=None),
    cfg.StrOpt('cert_file', default=None),
]


cfg.CONF.register_opts(database_opts, "DATABASE")
cfg.CONF.register_opts(ovs_opts, "OVS")
cfg.CONF.register_opts(agent_opts, "AGENT")
cfg.CONF.register_opts(ofc_opts, "OFC")

# shortcuts
CONF = cfg.CONF
DATABASE = cfg.CONF.DATABASE
OVS = cfg.CONF.OVS
AGENT = cfg.CONF.AGENT
OFC = cfg.CONF.OFC
