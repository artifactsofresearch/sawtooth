# Copyright 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------

import hashlib
import json
import logging


LOGGER = logging.getLogger(__name__)


ARTIFACT_NAMESPACE = hashlib.sha512(
    'artifact-chain'.encode('utf-8')).hexdigest()[0:6]


def _get_address(key):
    return hashlib.sha512(key.encode('utf-8')).hexdigest()[:62]


def _get_poe_address(asset_name):
    return ARTIFACT_NAMESPACE + '00' + _get_address(asset_name)


def _get_poa_address(asset_name):
    return ARTIFACT_NAMESPACE + '01' + _get_address(asset_name)


def _deserialize(data):
    return json.loads(data.decode('utf-8'))


def _serialize(data):
    return json.dumps(data, sort_keys=True).encode('utf-8')


class State(object):

    TIMEOUT = 3

    def __init__(self, context):
        self._context = context

    def _get_state(self, address):
        state_entries = self._context.get_state(
            [address], timeout=self.TIMEOUT)
        if state_entries:
            entry = _deserialize(data=state_entries[0].data)
        else:
            entry = None
        return entry

    def get_poe(self, name):
        return self._get_state(_get_poe_address(name))

    def get_poa(self, name):
        return self._get_state(_get_poa_address(name))

    def make_poe(self, asset, owner):
        # generate address
        address = _get_poe_address(asset.get('hash'))
        state_data = _serialize(
            {
                "id": asset.get('id'),
                "hash": asset.get('hash'),
                "entity": asset.get('entity'),
                "owner": owner
            })
        return self._context.set_state(
            {address: state_data}, timeout=self.TIMEOUT)


