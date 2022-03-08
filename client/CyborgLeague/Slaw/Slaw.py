import base64
import json
import os
import re
import tempfile

import requests
from colorama import Fore, Style, init

init()


class SLAW:
    """
    Simple League API Wrapper
    """

    def __throw_error(self, error_code:str):
        print(f"{Fore.RED}{Style.BRIGHT}{error_code}{Style.RESET_ALL}")
        raise Exception(error_code)



    def __get_descriptor(self) -> str:
        """
        #### Returns:
            API Descriptor from the LOL lockfile.
        """
        lockfile = open(fr"{self.lpath}\lockfile","r",encoding="utf-8")
        descriptor = re.search(r"(.*?):(.*?):(.*?):(.*?):(.+)", lockfile.read())
        lockfile.close()
        return descriptor.groups()



    def __init_self_ssl(self):
        req = requests.get(self.__remote_pem_url, allow_redirects=True)
        open(self.__ssl_cert, 'wb').write(req.content)




    def get_live(self,method:str) -> str:
        """
        Query a method supported by the LIVE LoL API.\n

        The difference between `slaw.get_live` and `slaw.get`
        is that `get_live` uses the API endpoint from the LoL
        Client on port `2999`, which only runs during a LoL match.

        #### Args:
          - A Method URL, without a protocol/IP Address, such as: `/api/method/1/value`

        #### Returns:
          - A Valid JSON Response from the client, parsed into a dict.
        """
        port = "2999"
        protocol = self.__get_descriptor()[4]
        url = f"{protocol}://127.0.0.1:{port}{method}"
        auth = {'Authorization': self.authorization}
        try:
            response = requests.get(url,verify=self.__ssl_cert, headers=auth).content.decode()
        except: # pylint: disable=bare-except
            response = '{"status":"error", "message":"client_not_playing"}'
        try:
             return json.loads(response)
        except:
            return response
        #return json.loads(response)



    def get(self,method:str) -> str:
        """
        Query a method supported by the LoL API.

        #### Args:
          - A Method URL, without a protocol/IP Address, such as: `/api/method/1/value`

        #### Returns:
          - A Valid JSON Response from the client, parsed into a dict.
        """
        port = self.__get_descriptor()[2]
        protocol = self.__get_descriptor()[4]
        url = f"{protocol}://127.0.0.1:{port}{method}"
        authorization = {'Authorization': self.authorization}
        response = requests.get(url,verify=self.__ssl_cert, headers=authorization).content.decode()
        return json.loads(response)

    def init(self, lpath):
        self.lpath = lpath
        if not os.path.isfile(fr"{self.lpath}\lockfile"):
            self.__throw_error("League of Legends Lockfile not found. Are you sure LoL is running?")
        self.authorization_clear = f"riot:{self.__get_descriptor()[3]}".encode("ascii")
        self.authorization = f"Basic {base64.b64encode(self.authorization_clear).decode()}"


    def __init__(self):
        self.__ssl_cert = tempfile.gettempdir()+"cert.pem"
        self.__remote_pem_url = "https://static.developer.riotgames.com/docs/lol/riotgames.pem"
        self.__init_self_ssl()
        
        
