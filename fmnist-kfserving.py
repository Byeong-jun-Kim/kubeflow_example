#!/usr/bin/env python
# coding: utf-8
from kubernetes import client
from kfserving import KFServingClient
from kfserving import constants
from kfserving import utils
from kfserving import V1beta1PredictorSpec
from kfserving import V1beta1TFServingSpec
from kfserving import V1beta1InferenceServiceSpec
from kfserving import V1beta1InferenceService
from kubernetes.client import V1ResourceRequirements
import os
import sys
import argparse
import logging
import time

'''
'''
class KFServing(object):
    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--namespace', required=False, default='kubeflow')
        # pvc://${PVCNAME}/dir
        parser.add_argument('--storage_uri', required=False, default='/pv/saved_model')
        parser.add_argument('--name', required=False, default='kfserving-sample')        
        args = parser.parse_args()
        namespace = args.namespace
        serving_name = args.name
        
        isvc = V1beta1InferenceService(
            api_version=constants.KFSERVING_V1BETA1,
            kind=constants.KFSERVING_KIND,
            metadata=client.V1ObjectMeta(
                name=serving_name,
                namespace=namespace,
                annotations={"sidecar.istio.io/inject": "false"}
            ),
            spec=V1beta1InferenceServiceSpec(
                predictor=V1beta1PredictorSpec(
                    tensorflow=V1beta1TFServingSpec(
                        storage_uri=args.storage_uri,
                        resources=V1ResourceRequirements(
                            requests={'cpu':'100m','memory':'1Gi'},
                            limits={'cpu':'100m', 'memory':'1Gi'}
                        )
                    )
                )
            )
        )
        
        KFServing = KFServingClient()
        KFServing.create(isvc)
        print('waiting 5 sec for Creating InferenceService')
        time.sleep(5)
        
        KFServing.get(serving_name, namespace=namespace, watch=True, timeout_seconds=300)
        
if __name__ == '__main__':
    if os.getenv('FAIRING_RUNTIME', None) is None:
        from kubeflow.fairing.builders.append.append import AppendBuilder
        from kubeflow.fairing.preprocessors.base import BasePreProcessor

        DOCKER_REGISTRY = 'kubeflow-registry.default.svc.cluster.local:30000'
        base_image = 'kbjun/python-kfserving:v1'
        image_name = 'kfserving'

        builder = AppendBuilder(
            registry=DOCKER_REGISTRY,
            image_name=image_name,
            base_image=base_image,
            push=True,
            preprocessor=BasePreProcessor(executable='fmnist-kfserving.py')
        )
        builder.build()
    else:
        serving = KFServing()
        serving.run()        
        

