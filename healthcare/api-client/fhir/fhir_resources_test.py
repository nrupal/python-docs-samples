# Copyright 2018 Google LLC All Rights Reserved.
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

import os
import pytest
import sys
import time

# Add datasets for bootstrapping datasets for testing
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'datasets')) # noqa
import datasets
import fhir_stores
import fhir_resources

cloud_region = 'us-central1'
api_key = os.environ['API_KEY']
base_url = 'https://healthcare.googleapis.com/v1alpha'
project_id = os.environ['GOOGLE_CLOUD_PROJECT']
service_account_json = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

dataset_id = 'test_dataset_{}'.format(int(time.time()))
fhir_store_id = 'test_fhir_store-{}'.format(int(time.time()))
resource_type = 'Patient'


@pytest.fixture(scope='module')
def test_dataset():
    dataset = datasets.create_dataset(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id)

    yield dataset

    # Clean up
    datasets.delete_dataset(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id)


@pytest.fixture(scope='module')
def test_fhir_store():
    fhir_store = fhir_stores.create_fhir_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id)

    yield fhir_store

    fhir_stores.delete_fhir_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id)


@pytest.mark.skip(reason='Disable until API whitelisted.')
def test_CRUD_search_resource(test_dataset, test_fhir_store, capsys):
    fhir_resources.create_resource(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_type)

    resource = fhir_resources.search_resources_get(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_type)

    # Save the resource_id from the object returned by search_resources()
    # because you need to pass it into get_resource() and delete_resource()
    resource_id = resource["entry"][0]["resource"]["id"]

    fhir_resources.get_resource(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_type,
        resource_id)

    fhir_resources.update_resource(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_type,
        resource_id)

    fhir_resources.patch_resource(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_type,
        resource_id)

    fhir_resources.delete_resource(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_type,
        resource_id)

    out, _ = capsys.readouterr()

    # Check that create/search worked
    assert 'Created Resource' in out
    assert 'id' in out
    assert 'search' in out
    assert resource_id in out
    assert 'Deleted Resource' in out


@pytest.mark.skip(reason='Disable until API whitelisted.')
def test_get_patient_everything(test_dataset, test_fhir_store, capsys):
    fhir_resources.create_resource(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_type)

    resource = fhir_resources.search_resources_get(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_type)

    # Save the resource_id from the object returned by search_resources()
    # because you need to pass it into get_resource() and delete_resource()
    resource_id = resource["entry"][0]["resource"]["id"]

    fhir_resources.get_patient_everything(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_id)

    fhir_resources.delete_resource(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_type,
        resource_id)

    out, _ = capsys.readouterr()

    assert 'id' in out


@pytest.mark.skip(reason="no way of currently testing this")
def test_get_metadata(test_dataset, test_fhir_store, capsys):
    fhir_resources.get_metadata(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id)

    out, _ = capsys.readouterr()

    # Check that getMetadata worked
    assert 'fhirVersion' in out
