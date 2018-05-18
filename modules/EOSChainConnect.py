#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This Class creates connection to EOS nodeos API RPC and the Wallet API RPC.
Only to methods are implemented GET and POST.
"""

import requests

__version: 0.1


class RequestHandlerAPI:
    """ a class to handle the http connection with the EOS node."""
    def __init__(self, base_url,  verify=False, **kwargs):
        self.base_url = base_url
        self.session = requests.Session()
        self.ssl_verify = verify

        for arg in kwargs:
            if isinstance(kwargs[arg], dict):
                kwargs[arg] = self.__set_session_attr(getattr(self.session, arg), kwargs[arg])
            setattr(self.session, arg, kwargs[arg])

    def get(self, path, **kwargs):
        """
        A GET Http method
        :param path: str: path to  api endpoint
        :param kwargs: json: arguments auth, headers, data ..etc.
        :return: response object
        """
        return self.session.get(self.base_url + path, verify=self.ssl_verify, **kwargs)

    def post(self, path, **kwargs):
        """
        A POST Http method
        :param path: str: path to  api endpoint
        :param kwargs: json: arguments auth, headers, data ..etc.
        :return: response object
        """
        return self.session.post(self.base_url + path, verify=self.ssl_verify, **kwargs)

    @staticmethod
    def __set_session_attr(source, destination):
        """
        set session attributes
        :param source: the default attributes when starting the session
        :param destination: json: target attributes to be set
        :return:json: session attributes
        """
        for key, value in source.items():
            if isinstance(value, dict):
                node = destination.setdefault(key, {})
                RequestHandlerAPI.__set_session_attr(value, node)
            else:
                destination[key] = value
        return destination



# test Connection Calss
if __name__ == '__main__':

    my_EOSNodeserver = RequestHandlerAPI("http://167.99.15.249:8888", verify=False, headers={"Accept": "application/json"})
    r = my_EOSNodeserver.post("/v1/chain/get_account", data='{"account_name": "rakoonrakoon"}')
    print(r.text)