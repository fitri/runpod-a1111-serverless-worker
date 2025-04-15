import time
import runpod
import requests
from requests.adapters import HTTPAdapter, Retry

LOCAL_URL = "http://127.0.0.1:3000/sdapi/v1"

automatic_session = requests.Session()
retries = Retry(total=10, backoff_factor=0.1, status_forcelist=[502, 503, 504])
automatic_session.mount('http://', HTTPAdapter(max_retries=retries))


# ---------------------------------------------------------------------------- #
#                              Automatic Functions                             #
# ---------------------------------------------------------------------------- #
def wait_for_service(url):
    """
    Check if the service is ready to receive requests.
    """
    retries = 0

    while True:
        try:
            requests.get(url, timeout=120)
            return
        except requests.exceptions.RequestException:
            retries += 1

            # Only log every 15 retries so the logs don't get spammed
            if retries % 15 == 0:
                print("Service not ready yet. Retrying...")
        except Exception as err:
            print("Error: ", err)

        time.sleep(0.2)


def run_inference(inference_request):
    """
    Run inference on a request.
    """
    response = automatic_session.post(url=f'{LOCAL_URL}/txt2img',
                                      json=inference_request, timeout=600)
    return response.json()


def get_samplers():
    """
    Get the list of available samplers.
    """
    response = automatic_session.get(url=f'{LOCAL_URL}/samplers', timeout=120)
    return response.json()


# ---------------------------------------------------------------------------- #
#                                RunPod Handler                                #
# ---------------------------------------------------------------------------- #
def handler(event):
    """
    This is the handler function that will be called by the serverless.
    """
    # Check if the request is for samplers list
    # this section check if the request json load of with value 'input' inside it contain key-value type: "get_samplers"
    # example: {"input": "type": "get_samplers"}
    if event.get("input", {}).get("type") == "get_samplers":
        return {
            "endpoint": "samplers",
            "data": get_samplers()
        }
    
    # Default txt2img inference
    return {
        "endpoint": "txt2img",
        "data": run_inference(event["input"])
    }


if __name__ == "__main__":
    wait_for_service(url=f'{LOCAL_URL}/sd-models')
    print("WebUI API Service is ready. Starting RunPod Serverless...")
    runpod.serverless.start({"handler": handler})
