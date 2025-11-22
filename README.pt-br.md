# 🐾 FURIA Arena Live - AI Second Screen Experience

> **Versão:** 1.0.1 (Stable)  
> **Deploy:** [Acesse Live no Render](https://furia-arena-live.onrender.com)

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![AI](https://img.shields.io/badge/AI-Google_Gemini-orange?style=for-the-badge&logo=google&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

## 🎯 Sobre o Projeto

O **FURIA Arena Live** é uma aplicação de "Segunda Tela" (Second Screen) projetada para engajar a torcida durante partidas de CS2. O sistema cria uma sala de bate-papo em tempo real onde um **Bot com Inteligência Artificial ("Furião")** interage com os fãs, comemora pontos e responde dúvidas sobre o time, tudo contextualizado com o estado atual da partida.

Este projeto foi desenvolvido como submissão para um **Desafio Técnico de Desenvolvimento de Software**.

---

## ⚠️ Nota sobre a Arquitetura de Dados (Visão vs. Protótipo)

Para fins deste MVP (Produto Mínimo Viável) e demonstração técnica, o sistema utiliza um **"Modo Sandbox"**.

* **A Visão Ideal:** Em um cenário de produção, a aplicação consumiria webhooks ou APIs oficiais de e-sports (como HLTV, Pandascore ou Grid) para atualizar o placar e eventos do jogo automaticamente.
* **A Implementação Atual:** Para garantir testabilidade e controle total durante a apresentação, foi implementado um **Sistema de Comandos de Admin**. Isso permite que o operador simule eventos (gols, troca de mapas, fim de jogo) manualmente, disparando as reações da IA e do Frontend via WebSockets instantaneamente.

---

## 🚀 Funcionalidades (Features)

### 📡 Real-Time & Conectividade
* **WebSockets (Full-Duplex):** Comunicação instantânea bidirecional entre servidor e clientes. Latência mínima para chat e atualizações de placar.
* **HUD Dinâmico:** O placar, nome do torneio e mapa atualizam na tela de todos os usuários sem necessidade de refresh (SPA feel).

### 🧠 Inteligência Artificial (Powered by Gemini 2.0 Flash)
* **Bot "Furião":** Uma persona configurada para agir como um torcedor fanático.
* **Consciência de Contexto:** O bot "sabe" quanto está o jogo. Se você perguntar "Estamos ganhando?", ele analisa o placar atual antes de responder.
* **Gestão de Memória:** O sistema reseta automaticamente a memória de curto prazo da IA quando o contexto crítico muda (ex: troca de adversário) para evitar alucinações.

### ❤️ Análise de Sentimento (Termômetro)
* **Engajamento Visual:** Um algoritmo analisa as mensagens enviadas pelos torcedores. Palavras de apoio ("Vamos", "Ganhamos") aquecem o termômetro; reclamações esfriam.

### 📱 UX/UI Responsiva
* **Mobile First:** Interface adaptada para celulares, com tratamento específico para teclados virtuais e áreas seguras (Safe Area) de iPhones.
* **Dark Mode:** Identidade visual alinhada com a marca FURIA.

---

## 🛠️ Engenharia & Design Patterns

O código foi estruturado seguindo **Clean Architecture** para garantir escalabilidade e testabilidade.

### 1. Observer Pattern (Backend)
Utilizado para desacoplar a Regra de Negócio (`GameEngine`) da Camada de Transporte (`ConnectionManager`).
> *Quando o placar muda, a Engine apenas "notifica". O Gerenciador de Conexões escuta e faz o broadcast para os milhares de fãs conectados.*

### 2. Clean Architecture & SOLID
* `app/models`: **DTOs (Pydantic)** para validação rigorosa de dados.
* `app/services`: Lógica pura (IA, Regras do Jogo), sem dependência de HTTP.
* `app/routers`: Controladores que gerenciam apenas a entrada/saída de dados.

### 3. Singleton
Gerenciamento de estado único para a partida, garantindo que todos os usuários vejam o mesmo placar sincronizado.

---

## 🎮 Guia de Comandos (Admin Sandbox)

Como não estamos conectados a uma API real de CS2, utilize estes comandos no chat para **simular** o andamento da partida:

| Comando | Ação | Reação do Sistema |
| :--- | :--- | :--- |
| `/gol` | Adiciona 1 ponto p/ FURIA | Placar atualiza, Termômetro sobe, IA comemora. |
| `/perdeu` | Adiciona 1 ponto p/ Adversário | Placar atualiza, Termômetro desce, IA lamenta. |
| `/adv [NOME]` | Muda o time inimigo | HUD atualiza, IA reseta memória para novo contexto. |
| `/mapa [NOME]` | Muda o mapa (ex: Mirage) | HUD atualiza, IA comenta sobre o mapa. |
| `/jogo [NOME]` | Muda nome do torneio | HUD atualiza (ex: "Major Shanghai"). |
| `/reset` | Zera tudo | Placar 0-0, IA reiniciada. |

---

## 💻 Instalação e Execução Local

### Pré-requisitos
* Python 3.10+
* Chave de API do Google Gemini (Google AI Studio)

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/FURIA-Arena-Live.git](https://github.com/seu-usuario/FURIA-Arena-Live.git)
    cd FURIA-Arena-Live
    ```

2.  **Crie o ambiente virtual:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/Mac
    # ou
    .\.venv\Scripts\activate   # Windows
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as Variáveis de Ambiente:**
    Crie um arquivo `.env` na raiz do projeto:
    ```env
    GEMINI_API_KEY=SuaChaveAqui
    ```

5.  **Execute o servidor:**
    ```bash
    python -m app.main
    ```

6.  **Acesse:** Abra `http://localhost:8000` no navegador.

---

## 📂 Estrutura do Projeto

```text
├── app/
│   ├── core/           # Configurações (Env vars)
│   ├── models/         # Schemas Pydantic (DTOs)
│   ├── routers/        # Endpoints WebSocket
│   ├── services/       # Lógica de Negócio (AI, Engine, Socket Manager)
│   └── main.py         # Entrypoint da Aplicação
├── static/             # Frontend (HTML, CSS, JS separados)
├── .env                # (Não versionado)
└── requirements.txt    # Dependências
```

---

## 📄 Disclaimer

Este é um projeto educacional e não-oficial, desenvolvido como parte de um portfólio técnico. Não possui vínculo comercial com a organização FURIA Esports, Valve ou Google. Todas as marcas registradas pertencem aos seus respectivos proprietários.

Desenvolvido com 🖤 e ☕ por Kawan Serafim de Souza.