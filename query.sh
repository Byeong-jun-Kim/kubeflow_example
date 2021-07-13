MODEL_NAME="kfserving-fmnist"
SERVICE_HOSTNAME=$(kubectl -n kubeflow-user-example-com get inferenceservice ${MODEL_NAME} -o jsonpath='{.status.url}' | cut -d "/" -f 3)
INPUT_PATH="@./input.json"
SESSION=""
curl -v -H "Host: ${SERVICE_HOSTNAME}" -H "Cookie: authservice_session=${SESSION}" http://10.100.49.226:80/v1/models/${MODEL_NAME}:predict -d $INPUT_PATH