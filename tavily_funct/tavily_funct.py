#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import humps

__author__ = "bibow"

import logging
import traceback
from typing import Any, Dict, List

from pydantic import BaseModel, Field
from tavily import TavilyClient

from ai_agent_funct_base import AIAgentFunctBase
from silvaengine_utility import Utility


class BaseSearchArgs(BaseModel):
    topic: str = Field(
        ...,
        description="The main subject area or category for the search (e.g., 'technology', 'science', 'general')",
    )
    search_depth: str = Field(
        "basic",
        description="Level of search depth - 'basic' for faster, surface-level results or 'advanced' for more comprehensive search",
    )
    days: int = Field(7, description="Number of days back to search from current date")
    max_results: int = Field(
        5, description="Maximum number of search results to return"
    )
    include_domains: List[str] = Field(
        [],
        description="List of specific website domains to include in the search results",
    )
    exclude_domains: List[str] = Field(
        [], description="List of website domains to exclude from search results"
    )
    timeout: int = Field(
        60, description="Maximum time in seconds to wait for search completion"
    )


class search(BaseModel):
    class FullSearchArgs(BaseSearchArgs):
        time_range: str = Field(
            None,
            description="Specific time period for search results (e.g., 'past_week', 'past_month', 'past_year')",
        )
        include_answer: bool = Field(
            False,
            description="Whether to include an AI-generated summary answer in the search results",
        )
        include_raw_content: bool = Field(
            False,
            description="Whether to include the full unprocessed content of search results",
        )
        include_images: bool = Field(
            False, description="Whether to include image results alongside text results"
        )

    query: str = Field(
        ..., description="The search query text used to find relevant information"
    )
    search_args: FullSearchArgs = Field(
        ..., description="Configuration parameters controlling the full search behavior"
    )


class get_search_context(BaseModel):
    class SearchContextArgs(BaseSearchArgs):
        max_tokens: int = Field(
            4000,
            description="Maximum number of text tokens to include in the returned search context",
        )

    query: str = Field(
        ...,
        description="The search query text used to find relevant contextual information",
    )
    search_args: SearchContextArgs = Field(
        ..., description="Configuration parameters for retrieving search context"
    )


class qna_search(BaseModel):
    query: str = Field(
        ..., description="The question to be answered through the search system"
    )
    search_args: BaseSearchArgs = Field(
        ...,
        description="Configuration parameters for the question-answering search process",
    )


class extract(BaseModel):
    class ExtractArgs(BaseModel):
        extract_depth: str = Field(
            ...,
            description="Level of detail for content extraction - 'basic' for essential information or 'advanced' for comprehensive extraction",
        )

    query: str = Field(
        ..., description="The search query used to identify content for extraction"
    )
    extract_args: ExtractArgs = Field(
        ...,
        description="Configuration parameters controlling the content extraction process",
    )


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
