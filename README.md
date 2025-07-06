# 🌿 Orbisage

**Orbisage** is a friendly, practical starter template for exploring how you can build a **multi-agent AI router** using [LangChain](https://www.langchain.com/) and [LangGraph](https://github.com/langchain-ai/langgraph).

---

Orbisage lets you experiment with how an AI bot can greet you, guide you around a building, tell you the latest news, share a fun fact, or even make you laugh — all routed through a simple, visual graph. It’s small enough to learn in an afternoon but flexible enough to grow into real-world workflows.

---

## ✨ How It Works

Instead of tangled `if/else` statements, Orbisage uses a **directed graph**:

<img src="https://github.com/semework/OrbiSage/blob/main/asssets/orbisage_router_graph.png" style="display: block;
  margin-left: auto;
  margin-right: auto;
  width: 75%;"/> 

- **Nodes:** Each agent is a Python function.
- **Edges:** Conditional transitions that inspect your input.
- **State:** Keeps your conversation context as you move through nodes.

---
<img src="[assets/orbisage_router_graph.png](https://github.com/semework/OrbiSage/blob/main/asssets/orbisage_router_graph.png)" style="display: block;
  margin-left: auto;
  margin-right: auto;
  width: 75%;" /> 
  
## 📦 Quick Start

### Requirements

- Python 3.9+
- (Optional) OpenAI API Key for real LLM calls

### Install & Setup

```bash
git clone git@github.com:semework/OrbiSage.git
cd OrbiSage

python -m venv .venv && source .venv/bin/activate

pip install -e .[dev]

cp .env.example .env  # Add OPENAI_API_KEY if you want
```

### Verify

```bash
python -c "from orbisage_router.graph import build_router_graph; print(build_router_graph())"
```

---

## 📝 Notebook Demo

```bash
jupyter notebook orbisage_full_demo.ipynb
```

- Visualise the graph (Mermaid).
- Inline Gradio chat.
- External chat served on `0.0.0.0:7860` for Docker/K8s.

---

## 🌐 Web UI

```bash
python web/app.py
```

Open [http://localhost:7860](http://localhost:7860)

---

## 🚢 Deployment

### Docker

```bash
docker build -t orbisage:latest .
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -p 7860:7860 orbisage:latest
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: orbisage }
spec:
  replicas: 2
  selector: { matchLabels: { app: orbisage } }
  template:
    metadata: { labels: { app: orbisage } }
    spec:
      containers:
      - name: orbisage
        image: your-dockerhub/orbisage:latest
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef: { name: openai, key: api_key }
        ports: [ { containerPort: 7860 } ]
---
apiVersion: v1
kind: Service
metadata: { name: orbisage-svc }
spec:
  selector: { app: orbisage }
  type: LoadBalancer
  ports: [ { port: 80, targetPort: 7860 } ]
```

```bash
kubectl apply -f k8s/orbisage.yaml
```

---

## 🔍 Example Queries

| Query                           | Agent     | Response                                   |
|---------------------------------|-----------|--------------------------------------------|
| “Hello!”                        | greet     | “Hello! How can I help you today?”         |
| “How do I get to the gym?”      | Navigator | “Office → Elevator → Gym.”                 |
| “What’s in AI news today?”      | News      | “LLM-based agents are trending.”           |
| “Tell me something about honey.”| Discovery | “Honey from ancient Egypt is edible!”      |
| “Give me a programming joke.”   | Joke      | “Why do programmers prefer dark mode?”     |

---

## 🧩 Orbisage

Orbisage is basically your own friendly playground for trying out multi-agent ideas — you can start really small, test out one thing at a time, and see how they work together.
It’s simple enough that you don’t feel stuck reading a giant manual, but it’s flexible enough to build into something real if you want to.
Think of it as a laid-back lab assistant that never gets tired of your experiments — whether you want to navigate an imaginary building,
share a science fact, or just tinker with different chat responses, you can do all of that here.”


---

## 🧩 Extending Orbisage

- Add new tools or plug in real APIs.
- Add nodes and update the graph.
- Use persistent memory like Redis or a vector store.
- Monitor with LangSmith.

---

## 🤝 Contributing & License

Pull requests and forks are welcome — add tests, lint with `ruff`.

Licensed under **MIT License**.

---

**Happy routing! — The Orbisage Team**
