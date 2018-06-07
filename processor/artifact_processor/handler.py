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

import logging

from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction

from artifact_processor.payload import Payload
from artifact_processor.state import State
from artifact_processor.state import ARTIFACT_NAMESPACE


LOGGER = logging.getLogger(__name__)


class ArtifactTransactionHandler(TransactionHandler):

    @property
    def family_name(self):
        return 'artifact-chain'

    @property
    def family_versions(self):
        return ['0.0']

    @property
    def encodings(self):
        return ['application/json']

    @property
    def namespaces(self):
        return [ARTIFACT_NAMESPACE]

    def apply(self, transaction, context):

        header = transaction.header
        signer = header.signer_public_key

        LOGGER.info('transaction.payload: %s', transaction.payload)

        payload = Payload(transaction.payload)
        state = State(context)

        LOGGER.info('Handling transaction: %s > %s :: %s',
                    payload.action,
                    payload.asset,
                    # '> ' + payload.owner[:8] + '... ' if payload.owner else '',
                    signer[:8] + '... ')

        if payload.action == 'poe':
            _make_poe(asset=payload.asset,
                      owner=signer,
                      state=state)

        else:
            raise InvalidTransaction('Unhandled action: {}'.format(
                payload.action))


def _make_poe(asset, owner, state):
    LOGGER.info('Hash: %s', asset.get('hash'))
    if state.get_poe(asset.get('hash')) is not None:
        raise InvalidTransaction(
            'Invalid action: Hash already exists: {}'.format(asset.get('hash')))

    state.make_poe(asset, owner)
