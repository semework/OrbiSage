# orbisage_router/agent.py

import requests
import xml.etree.ElementTree as ET
from collections import deque

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import FileChatMessageHistory


class OrbiAgent:
    """OrbiAgent – direct keyword‐based router with:
       • Persistent JSON memory
       • RSS‐based real‐time news (BBC)
       • Public JokeAPI jokes with retry
       • Science discovery via LLM
       • Hard‐coded indoor navigation
       • Fallback LLM chat
    """

    def __init__(self, memory_path: str = "orbi_memory.json"):
        # ─── Initialize LLM & persistent memory ─────────────────────
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        history = FileChatMessageHistory(memory_path)
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True, chat_memory=history
        )

        # ─── Hard‐coded building graph ───────────────────────────────
        self._graph = {
            "Entrance": ["Corridor"],
            "Corridor": ["Entrance", "Office", "Bathroom", "Cafeteria", "Elevator", "Stairs"],
            "Office": ["Corridor"],
            "Bathroom": ["Corridor"],
            "Cafeteria": ["Corridor"],
            "Elevator": ["Corridor", "Gym", "Doctor's Office"],
            "Stairs": ["Corridor", "Gym"],
            "Gym": ["Elevator", "Stairs", "Doctor's Office"],
            "Doctor's Office": ["Elevator", "Gym"],
        }

        # ─── Keyword buckets for routing ────────────────────────────
        self._news_kw = {"news", "headline", "headlines", "updates", "latest"}
        self._joke_kw = {"joke", "laugh", "funny", "pun", "make me laugh", "another"}
        self._fact_kw = {"fact", "explain", "what", "how", "why", "who", "where", "when"}

    def navigate(self, query: str) -> str:
        """BFS pathfinding between rooms in the hard‐coded map."""
        graph = self._graph
        text = query.lower()
        src, dest = "Entrance", None

        # parse "from X to Y"
        if " to " in text:
            left, right = text.split(" to ", 1)
            if left.strip().startswith("from "):
                src = left.split("from ", 1)[1].title()
            dest = right.strip().title()
        else:
            # fallback: detect any room mention
            for room in graph:
                if room.lower() in text:
                    dest = room
                    break

        if dest not in graph:
            return (
                "I can only navigate between Entrance, Office, Gym, "
                "Bathroom, Cafeteria, and Doctor's Office. "
                "Try 'from office to gym'."
            )

        # BFS shortest path
        queue = deque([src])
        visited = {src}
        parent = {src: None}
        while queue:
            node = queue.popleft()
            if node == dest:
                break
            for nbr in graph[node]:
                if nbr not in visited:
                    visited.add(nbr)
                    parent[nbr] = node
                    queue.append(nbr)

        # reconstruct path
        path = []
        cur = dest
        while cur:
            path.append(cur)
            cur = parent[cur]
        return " → ".join(reversed(path))

    def news(self, query: str) -> str:
        """Fetch BBC RSS top 5 headlines and summarize via LLM."""
        RSS = "http://feeds.bbci.co.uk/news/rss.xml"
        try:
            resp = requests.get(RSS, timeout=5)
            resp.raise_for_status()
            root = ET.fromstring(resp.content)
            items = root.find("channel").findall("item")[:5]
            feed = "\n".join(
                f"- **{it.findtext('title','No title')}**: {it.findtext('description','')}"
                for it in items
            )
        except Exception as e:
            return f"Could not fetch news: {e}"

        prompt = f"Summarize these BBC headlines in 2–3 sentences:\n{feed}"
        llm_resp = self.llm.invoke([HumanMessage(content=prompt)])
        return llm_resp.content

    def discovery(self, query: str) -> str:
        """Answer a science/knowledge query or share a fun fact via LLM."""
        # if query looks like a question/fact request, use it, else default prompt
        if any(kw in query.lower() for kw in ("fact", "explain", "what", "how", "why")):
            prompt = query
        else:
            prompt = "Share an interesting science fact."
        llm_resp = self.llm.invoke([HumanMessage(content=prompt)])
        return llm_resp.content

    def joke(self, query: str) -> str:
        """Fetch a programming joke; retry on complaint."""
        text = query.lower()
        apology = (
            "Sorry, here's another:\n"
            if any(w in text for w in ("not funny", "boring", "again", "lame"))
            else ""
        )
        try:
            res = requests.get(
                "https://v2.jokeapi.dev/joke/Programming?type=single&safe-mode", timeout=5
            ).json()
            joke = res.get("joke") or f"{res.get('setup')} ... {res.get('delivery')}"
        except Exception:
            return "Joke service unavailable. Try again later."
        return apology + joke

    def run(self, user_input: str) -> str:
        """Route to the appropriate tool or fallback to LLM chat."""
        txt = user_input.lower()

        # 1) Navigation if any room mentioned
        for room in self._graph:
            if room.lower() in txt:
                return self.navigate(user_input)

        # 2) News
        if any(kw in txt for kw in self._news_kw):
            return self.news(user_input)

        # 3) Joke
        if any(kw in txt for kw in self._joke_kw):
            return self.joke(user_input)

        # 4) Fact/discovery
        if any(kw in txt for kw in self._fact_kw):
            return self.discovery(user_input)

        # 5) Fallback chat
        llm_resp = self.llm.invoke([HumanMessage(content=user_input)])
        return llm_resp.content
