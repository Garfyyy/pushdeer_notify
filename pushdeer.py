from typing import Optional, Union
import requests

class PushDeer:
    server = "https://api2.pushdeer.com"
    endpoint = "/message/push"
    pushkey = None

    def __init__(
            self, 
            server: Optional[str] = None, 
            pushkey: Optional[str] = None
    ) -> None:
        if server:
            self.server = server
        if pushkey:
            self.pushkey = pushkey

    def _push(
            self, 
            title: Optional[str], 
            desp: Optional[str] = None,
            server: Optional[str] = None,
            pushkey: Optional[str] = None,
            text_type: Optional[str] = None,
            **kwargs,
    ):
        if not pushkey and not self.pushkey:
            raise ValueError("pushkey is required")
        
        resp = self._send_push_request(title, desp, pushkey or self.pushkey, server or self.server, text_type, **kwargs)

        if resp is None:
            return False
        if resp["code"] == 0:
            return True
        else:
            print(f'push error: {resp["error"]}')
            return False
            
    def _send_push_request(self, title, desp, key, server, type, **kwargs):
        try:
            resp = requests.get(server + self.endpoint, params={
                "pushkey": key,
                "text": title,
                "type": type,
                "desp": desp,
            }, **kwargs)
        except Exception as e:
            print(f'Send push request error: {e}')
            return None
        return resp.json()

    def send_text(
            self,
            title: Optional[str],
            desp: Optional[str] = None,
            server: Optional[str] = None,
            pushkey: Union[str, list, None] = None,
            **kwargs
    ):
        return self._push(title=title, desp=desp, server=server, pushkey=pushkey, text_type="text", **kwargs)
    
    def send_markdown(
            self,
            title: Optional[str],
            desp: Optional[str] = None,
            server: Optional[str] = None,
            pushkey: Union[str, list, None] = None,
            **kwargs
    ):
        return self._push(title=title, desp=desp, server=server, pushkey=pushkey, text_type="markdown", **kwargs)
    
