# coding=utf-8
#
#  Copyright 2016 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Directory: cm module: sync-status.

REST URI
    ``https://localhost/mgmt/tm/cm/sync-status?ver=11.6.0``

GUI Path
    ``XXX``

REST Kind
    ``tm:cm:sync-status:*``
"""

from f5.bigip.resource import UnnamedResource


class Sync_Status(UnnamedResource):
    """BIG-IP® cluster resource"""
    def __init__(self, cm):
        super(Sync_Status, self).__init__(cm)
        self._meta_data['required_json_kind'] =\
            "tm:cm:sync-status:sync-statusstats"