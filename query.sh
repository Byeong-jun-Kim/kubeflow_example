MODEL_NAME="kfserving-fmnist"
SERVICE_HOSTNAME=$(kubectl -n kubeflow-user-example-com get inferenceservice ${MODEL_NAME} -o jsonpath='{.status.url}' | cut -d "/" -f 3)
INPUT_PATH="@./input.json"
SESSION="MTYyNTk4NjU0OHxOd3dBTkVOYVdUTlhXVmRNUTBFelMxQk1OVW96VlZRMVRFVk1SbGxSV1RKSk5VaFdNMGd5TTBaSE5FUTFVa0ZPU0RaU1V6WklXRkU9fPTx256KgLZiKVd-rv2-nXWcva8iac9QSGRG_2KPywAV"
curl -v -H "Host: ${SERVICE_HOSTNAME}" -H "Cookie: authservice_session=${SESSION}" http://10.100.49.226:80/v1/models/${MODEL_NAME}:predict -d $INPUT_PATH