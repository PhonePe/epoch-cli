import configparser
import json
import os
import requests
import urllib3
from pathlib import Path
from requests.adapters import HTTPAdapter, Retry
from types import SimpleNamespace


class TokenAuth(requests.auth.AuthBase):
    def __init__(self, token: str):
        self.token = token
        super().__init__()

    def __call__(self, r):
        r.headers.update({"Authorization": self.token})
        return r


class EpochException(Exception):
    """Exception raised while calling epoch endpoint"""

    def __init__(self, status_code: int, message: str, raw: str = None, api_response: dict = None):
        self.status_code = status_code
        self.raw = raw
        self.api_response = api_response
        super().__init__(message)


class EpochClient:
    def __init__(self):
        self.endpoint: str = None
        self.auth_header: str = None
        self.username = None
        self.password = None
        self.insecure: bool = False
        self.session = requests.session()
        retries = Retry(connect=1,
                        read=1,
                        backoff_factor=0.1)

        self.session.mount('https://', HTTPAdapter(max_retries=retries))
        self.session.mount('http://', HTTPAdapter(max_retries=retries))

    def start(self,
              endpoint: str = None,
              auth_header: str = None,
              username: str = None,
              password: str = None,
              insecure: bool = False):
        self.endpoint = endpoint
        self.auth_header = auth_header
        self.insecure = insecure
        self.session.verify = not insecure
        if insecure:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        if username != None and password != None:
            self.session.auth = requests.auth.HTTPBasicAuth(username, password)
        elif auth_header:
            self.session.auth = TokenAuth(auth_header)

    def get(self, path: str, expected_status=200) -> dict:
        try:
            response = self.session.get(self.endpoint + path)
        except requests.ConnectionError as e:
            raise EpochException(-1, "Error connecting to endpoint " + self.endpoint, raw={})
        return handle_epoch_response(response, expected_status)

    def post(self, path: str, body: dict, expected_status=200) -> dict:
        try:
            response = self.session.post(self.endpoint + path, json=body)
        except requests.ConnectionError as e:
            raise EpochException(-1, "Error connecting to endpoint " + self.endpoint, raw={})
        return handle_epoch_response(response, expected_status)

    def put(self, path: str, body: dict, expected_status=200) -> dict:
        try:
            response = self.session.put(self.endpoint + path, json=body)
        except requests.ConnectionError as e:
            raise EpochException(-1, "Error connecting to endpoint " + self.endpoint, raw={})
        return handle_epoch_response(response, expected_status)

    def delete(self, path: str, body: dict, expected_status=200) -> dict:
        try:
            response = self.session.delete(self.endpoint + path, json=body)
        except requests.ConnectionError as e:
            raise EpochException(-1, "Error connecting to endpoint " + self.endpoint, raw={})
        return handle_epoch_response(response, expected_status)


def handle_epoch_response(response: requests.Response, expected_status: int):
    status_code = response.status_code
    text = response.text
    api_response = None
    try:
        if text != None and response.json() != None:
            api_response = response.json()
    except json.decoder.JSONDecodeError:
        raise EpochException(status_code, text)
    except Exception as e:
        raise EpochException(status_code, str(e))
    if status_code != expected_status:
        raise EpochException(status_code,
                             "Epoch call failed with status code: {code}, error: {message}".format(code=status_code,
                                                                                                   message=text),
                             api_response=api_response)
    if api_response is None:
        raise EpochException(status_code, "Epoch call failed with status code: {code}".format(code=status_code))

    if "status" in api_response:
        if api_response["status"] != "SUCCESS":
            raise EpochException(status_code, message=api_response.get("message", ""), raw=text,
                                 api_response=api_response)
    else:
        raise EpochException(status_code, text)
    return api_response["data"] if "data" in api_response else api_response


def build_epoch_client(epoch_client: EpochClient, args: SimpleNamespace):
    endpoint = args.endpoint
    auth_header = args.auth_header
    insecure = args.insecure
    username = args.username
    password = args.password
    if endpoint is None:
        # If cmdl options are not passed, see if config file is passed
        # If config file path is not passed, see if .epoch exists in home and use that
        config_file = args.file if args.file is not None else str(Path.home()) + "/.epoch"
        # Try to parse config if it exists and is readable
        if os.path.isfile(config_file) and os.access(config_file, os.R_OK):
            config_parser = configparser.ConfigParser()
            try:
                with open(config_file) as stream:
                    config_parser.read_string(stream.read())
                epoch_config = config_parser['DEFAULT']
                if args.cluster is not None:
                    if args.cluster in config_parser:
                        epoch_config = config_parser[args.cluster]
                    else:
                        print("error: No cluster definition found for {cluster} in config {config_file}".format(
                            config_file=config_file, cluster=args.cluster))
                        return None
                endpoint = epoch_config.get("endpoint")
                username = epoch_config.get("username")
                password = epoch_config.get("password")
                auth_header = epoch_config.get("auth_header", None)
                insecure = epoch_config.get("insecure", False)
            except Exception as e:
                # Looks like some random file was passed. Bail out
                print("Error parsing config file " + config_file + ": " + str(e))
                return None
        else:
            print("Error: Config file {config_file} is not present or readable".format(config_file=config_file))
            return None
    # At least endpoint is needed
    if endpoint is None:
        raise Exception("Error: provide config file or required command line params for epoch connectivity\n")
    endpoint = endpoint[:-1] if endpoint.endswith('/') else endpoint
    if args.debug:
        print(
            'Endpoint: {endpoint} Username: {has_username} Password: {has_password} AuthHeader: {has_auth_header} Insecure: {insecure}'
            .format(endpoint=endpoint, has_username=username is not None, has_password=password is not None,
                    has_auth_header=auth_header is not None, insecure=insecure))
    epoch_client.start(endpoint, auth_header, username, password, insecure)
    return epoch_client
