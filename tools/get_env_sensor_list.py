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

class GetEnvSensorListTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        """
        TWSNMP FCから環境センサーのリストを取得してJSONで返す。

        Args:
            tool_parameters: ツールの入力パラメータを含む辞書:
   
        Yields:
            ToolInvokeMessage: JSON
        """
        logger.info("start get_env_sensor_list")
        # 1. ランタイムから認証情報を取得
        try:
            url = self.runtime.credentials["twsnmp_url"]
            user = self.runtime.credentials["twsnmp_user"]
            password = self.runtime.credentials["twsnmp_password"]
        except KeyError:
            logger.error("Credentials not set")
            yield self.create_text_message("Credentials not set")
 
        # 2. ツールの入力パラメータを取得
 
        # 3. TWSNMP FCから環境センサーのリストを取得
        api = TwsnmpAPI(url)
        r = api.login(user,password)
        if r:
            logger.error("Can not login to TWSNMP FC")
            yield self.create_text_message(f"Can not login to TWSNMP FC: {r}")
          
        envs = api.get("/api/report/EnvMonitor")
        if not envs:
            logger.error("Failed to retrieve env sensor list from TWSNMP FC")
            yield self.create_text_message("Failed to retrieve env sensor list from TWSNMP FC")
        
        # 4. 結果を返す
        for e  in envs:
            ed = e.get("EnvData",[])
            e["EnvData"] = ed[-1] if ed and len(ed) > 0  else ""
            e["FirstTime"] = nanosecond_unix_to_datetime_string(e.get("FirstTime",0))
            e["LastTime"] = nanosecond_unix_to_datetime_string(e.get("LastTime",0))
            yield self.create_json_message(e)
        logger.info("end get_env_sensor_list")
 