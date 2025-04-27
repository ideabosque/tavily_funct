#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import humps

__author__ = "bibow"

import logging
import traceback
from typing import Any, Dict, List

from tavily import TavilyClient

from ai_agent_funct_base import AIAgentFunctBase
from silvaengine_utility import Utility


class TavilyFunct(AIAgentFunctBase):

    def __init__(self, logger: logging.Logger, **setting: Dict[str, Any]):
        try:
            self.logger = logger
            AIAgentFunctBase.__init__(self, logger, **setting)

            self.tavily_client = TavilyClient(api_key=setting["tvly_api_key"])

            self.base_search_args = {
                "search_depth": setting.get("search_depth", "basic"),
                "topic": setting.get("topic", "general"),
                "days": setting.get("days", 7),
                "max_results": setting.get("max_results", 5),
                "include_domains": setting.get("include_domains", []),
                "exclude_domains": setting.get("exclude_domains", []),
                "timeout": setting.get("timeout", 60),
            }

            self.search_context_args = {
                "max_tokens": setting.get("max_tokens", 4000),
                **self.base_search_args,
            }

            self.full_search_args = {
                "time_range": setting.get("time_range", None),
                "include_answer": setting.get("include_answer", False),
                "include_raw_content": setting.get("include_raw_content", False),
                "include_images": setting.get("include_images", False),
                **self.base_search_args,
            }

            self.extract_args = {
                "include_images": setting.get("include_images", False),
                "extract_depth": setting.get("extract_depth", "basic"),
                "timeout": setting.get("timeout", 60),
            }

        except Exception as e:
            log = traceback.format_exc()
            self.logger.error(log)
            raise e

    def search(self, **arguments: Dict[str, Any]) -> Dict[str, Any]:
        try:
            self.logger.info(f"Arguments: {arguments}")
            endpoint_id = arguments["endpoint_id"]
            query = arguments["query"]
            search_args = arguments.get("search_args", {})
            self.logger.info(f"Endpoint ID: {endpoint_id}")
            self.logger.info(f"Query: {query}")

            return self.tavily_client.search(
                **{"query": query, **dict(self.full_search_args, **search_args)}
            )
        except Exception as e:
            log = traceback.format_exc()
            self.logger.error(log)
            raise e

    def get_search_context(self, **arguments: Dict[str, Any]) -> Dict[str, Any]:
        try:
            self.logger.info(f"Arguments: {arguments}")
            endpoint_id = arguments["endpoint_id"]
            query = arguments["query"]
            search_args = arguments.get("search_args", {})
            self.logger.info(f"Endpoint ID: {endpoint_id}")
            self.logger.info(f"Query: {query}")

            return self.tavily_client.get_search_context(
                **{"query": query, **dict(self.search_context_args, **search_args)}
            )
        except Exception as e:
            log = traceback.format_exc()
            self.logger.error(log)
            raise e

    def qna_search(self, **arguments: Dict[str, Any]) -> Dict[str, Any]:
        try:
            self.logger.info(f"Arguments: {arguments}")
            endpoint_id = arguments["endpoint_id"]
            query = arguments["query"]
            search_args = arguments.get("search_args", {})
            self.logger.info(f"Endpoint ID: {endpoint_id}")
            self.logger.info(f"Query: {query}")

            return self.tavily_client.qna_search(
                **{"query": query, **dict(self.base_search_args, **search_args)}
            )
        except Exception as e:
            log = traceback.format_exc()
            self.logger.error(log)
            raise e

    def extract(self, **arguments: Dict[str, Any]) -> Dict[str, Any]:
        try:
            self.logger.info(f"Arguments: {arguments}")
            endpoint_id = arguments["endpoint_id"]
            urls = arguments["urls"]
            search_args = arguments.get("search_args", {})
            self.logger.info(f"Endpoint ID: {endpoint_id}")
            self.logger.info(f"URLs: {urls}")

            return self.tavily_client.extract(
                **{"urls": urls, **dict(self.extract_args, **search_args)}
            )
        except Exception as e:
            log = traceback.format_exc()
            self.logger.error(log)
            raise e
