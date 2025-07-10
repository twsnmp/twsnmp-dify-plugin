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
from twlib.time_util import unix_to_datetime_string

class SnmpWalkTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        """
        TWSNMP FCからsnmpwalkを実施して結果をJSONで返す。

        Args:
            tool_parameters: ツールの入力パラメータを含む辞書:
                - target (str): 対象ノード
                - mib (str): 取得するMIBのオブジェクト名
 
        Yields:
            ToolInvokeMessage: JSON
        """
        logger.info("start snmpwalk")
        # 1. ランタイムから認証情報を取得
        try:
            url = self.runtime.credentials["twsnmp_url"]
            user = self.runtime.credentials["twsnmp_user"]
            password = self.runtime.credentials["twsnmp_password"]
        except KeyError:
            logger.error("Credentials not set")
            yield self.create_text_message("Credentials not set")
 
        # 2. ツールの入力パラメータを取得
        target = tool_parameters.get("target", "") 
        mib = tool_parameters.get("mib", "") 
 
        # 3. TWSNMP FCでsnmpwalkを実施
        # 3.1 Login
        api = TwsnmpAPI(url)
        r = api.login(user,password)
        if r:
            logger.error("Can not login to TWSNMP FC")
            yield self.create_text_message(f"Can not login to TWSNMP FC: {r}")
        # 3.2 NodeIDを取得する
        nodes = api.get("/api/nodes")
        if not nodes:
            logger.error("Failed to retrieve nodes from TWSNMP FC")
            yield self.create_text_message("Failed to retrieve nodes from TWSNMP FC")
       
        node_id = ""
        for node  in nodes:
            if node.get("Name","") == target:
                node_id = node.get("ID","")
                break
            if node.get("IP","") == target:
                node_id = node.get("ID","")
                break
        if not node_id:
            logger.error("node not found")
            yield self.create_text_message("node not found")        
        # 3.3 snmpwalkを実行する   
        mibs = api.post("/api/mibbr",{"NodeID":node_id,"Name": mib,"Raw": False})
        if not mibs:
            logger.error("Failed to execute snmpwalk TWSNMP FC")
            yield self.create_text_message("Failed to execute snmpwalk from TWSNMP FC")
        
        # 4. 結果を返す
        for m in mibs:
           yield self.create_json_message(m)
        logger.info("end snmpwalk")
 