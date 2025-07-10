from collections.abc import Generator
from typing import Any
import json

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

# Import logging and custom handler
import logging
from dify_plugin.config.logger_format import plugin_logger_handler

# Set up logging with the custom handler
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(plugin_logger_handler)


from twlib.twsnmpapi import TwsnmpAPI
from twlib.time_util import nanosecond_unix_to_datetime_string

class GetIPAddressListTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        """
        TWSNMP FCからIPアドレスのリストを取得してJSONで返す。

        Args:
            tool_parameters: ツールの入力パラメータを含む辞書:
                - name_filter (str): 名前フィルター
                - ip_filter (str): IPフィルター
                - vendor_filter (str): ベンダー名フィルター

        Yields:
            ToolInvokeMessage: JSON
        """
        logger.info("start get_ip_address_list")
        # 1. ランタイムから認証情報を取得
        try:
            url = self.runtime.credentials["twsnmp_url"]
            user = self.runtime.credentials["twsnmp_user"]
            password = self.runtime.credentials["twsnmp_password"]
        except KeyError:
            logger.error("Credentials not set")
            yield self.create_text_message("Credentials not set")
 
        # 2. ツールの入力パラメータを取得
        name = tool_parameters.get("name_filter", "") 
        ip = tool_parameters.get("ip_filter", "") 
        vendor = tool_parameters.get("vendor_filter", "") 

        # 3. TWSNMP FCからIP addressリストを取得
        api = TwsnmpAPI(url)
        r = api.login(user,password)
        if r:
            logger.error("Can not login to TWSNMP FC")
            yield self.create_text_message(f"Can not login to TWSNMP FC: {r}")
          
        ips = api.get("/api/report/ips")
        if not ips:
            logger.error("Failed to retrieve IP address from TWSNMP FC")
            yield self.create_text_message("Failed to retrieve IP address list from TWSNMP FC")
        
        # 4. 結果を返す
        for i  in ips:
            if name and name not in i.get("Name",""):
                continue
            if ip and ip not in i.get("IP",""):
                continue
            if vendor and vendor not in i.get("Vendor",""):
                continue
            i["FirstTime"] = nanosecond_unix_to_datetime_string(i.get("FirstTime",0))
            i["LastTime"] = nanosecond_unix_to_datetime_string(i.get("LastTime",0))
            i["UpdateTime"] = nanosecond_unix_to_datetime_string(i.get("UpdateTime",0))
            i["Location"] = i.get("Loc","")
            del i["ValidScore"]
            del i["Loc"]
            yield self.create_json_message(i)
        logger.info("end get_ip_address_list")
 