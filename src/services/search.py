"""Search dispatch helpers leveraging HelloAgents SearchTool."""

from __future__ import annotations

import logging
import os
from typing import Any, Optional, Tuple

from hello_agents.tools import SearchTool

from config import Configuration
from utils import (
    deduplicate_and_format_sources,
    format_sources,
    get_config_value,
)

logger = logging.getLogger(__name__)

_GLOBAL_SEARCH_TOOL = SearchTool(backend="hybrid")


def dispatch_search(
    query: str,
    config: Configuration,
    loop_count: int,
) -> Tuple[dict[str, Any] | None, list[str], Optional[str], str]:
    """Execute configured search backend and normalise response payload."""

    max_results = max(1, min(int(config.search_max_results), 8))
    max_tokens_per_source = max(200, min(int(config.max_tokens_per_source), 2000))
    configured_backend = get_config_value(config.search_api)
    fallback_backends: list[str] = [configured_backend]
    if configured_backend != "tavily" and os.getenv("TAVILY_API_KEY"):
        fallback_backends.append("tavily")
    if configured_backend != "duckduckgo":
        fallback_backends.append("duckduckgo")
    fallback_backends = list(dict.fromkeys(fallback_backends))

    notices: list[str] = []
    raw_response: Any | None = None
    resolved_backend = configured_backend

    for backend in fallback_backends:
        try:
            raw_response = _GLOBAL_SEARCH_TOOL.run(
                {
                    "input": query,
                    "backend": backend,
                    "mode": "structured",
                    "fetch_full_page": config.fetch_full_page,
                    "max_results": max_results,
                    "max_tokens_per_source": max_tokens_per_source,
                    "loop_count": loop_count,
                }
            )
            resolved_backend = backend
            if backend != configured_backend:
                switch_notice = (
                    f"搜索后端 {configured_backend} 不可用，已自动切换到 {backend}"
                )
                notices.append(switch_notice)
                logger.warning(switch_notice)
            break
        except Exception as exc:  # pragma: no cover - defensive logging
            fail_notice = f"搜索后端 {backend} 调用失败: {exc}"
            notices.append(fail_notice)
            logger.exception("Search backend %s failed: %s", backend, exc)

    if raw_response is None:
        payload = {
            "results": [],
            "backend": configured_backend,
            "answer": None,
            "notices": notices,
        }
        logger.error(
            "All search backends failed: configured=%s attempted=%s",
            configured_backend,
            fallback_backends,
        )
        return payload, notices, None, configured_backend

    if isinstance(raw_response, str):
        notices.append(raw_response)
        logger.warning(
            "Search backend %s returned text notice: %s",
            resolved_backend,
            raw_response,
        )
        payload: dict[str, Any] = {
            "results": [],
            "backend": resolved_backend,
            "answer": None,
            "notices": notices,
        }
    else:
        payload = raw_response
        payload_notices = list(payload.get("notices") or [])
        if payload_notices:
            notices.extend(payload_notices)
        payload["notices"] = notices

    backend_label = str(payload.get("backend") or resolved_backend)
    answer_text = payload.get("answer")
    results = payload.get("results", [])

    if notices:
        for notice in notices:
            logger.info("Search notice (%s): %s", backend_label, notice)

    logger.info(
        "Search backend=%s resolved_backend=%s answer=%s results=%s",
        configured_backend,
        backend_label,
        bool(answer_text),
        len(results),
    )

    return payload, notices, answer_text, backend_label


def prepare_research_context(
    search_result: dict[str, Any] | None,
    answer_text: Optional[str],
    config: Configuration,
) -> tuple[str, str]:
    """Build structured context and source summary for downstream agents."""

    max_results = max(1, min(int(config.search_max_results), 8))
    max_tokens_per_source = max(200, min(int(config.max_tokens_per_source), 2000))
    max_context_chars = max(4000, int(config.max_summary_context_chars))
    answer_char_limit = max(1000, max_context_chars // 3)

    sources_summary = format_sources(search_result)
    context = deduplicate_and_format_sources(
        search_result or {"results": []},
        max_tokens_per_source=max_tokens_per_source,
        fetch_full_page=config.fetch_full_page,
        max_sources=max_results,
    )

    if answer_text:
        trimmed_answer = (
            f"{answer_text[:answer_char_limit]}... [truncated]"
            if len(answer_text) > answer_char_limit
            else answer_text
        )
        context = f"AI直接答案：\n{trimmed_answer}\n\n{context}"

    if len(context) > max_context_chars:
        context = f"{context[:max_context_chars]}... [context truncated]"

    return sources_summary, context
