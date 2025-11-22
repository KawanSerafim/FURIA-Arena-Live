from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.game_engine import GameEngine
from app.services.connection_manager import ConnectionManager
from app.services.ai_service import AIService
from app.models.schemas import WSPayload, ChatMessageDTO

router = APIRouter()

game_engine = GameEngine()
connection_manager = ConnectionManager()
ai_service = AIService()

game_engine.subscribe(connection_manager.on_game_state_change)

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await connection_manager.connect(websocket)

    user_session = ai_service.create_session()

    initial_state = game_engine.get_state()
    await connection_manager.on_game_state_change(initial_state)

    try:
        while True:
            data = await websocket.receive_text()

            # Identifica um comando de Admin e manda a engine processar.
            if data.startswith("/"):
                cmds = ["/adv", "/mapa", "/jogo", "/reset"]
                if any(cmd in data for cmd in cmds):
                    user_session = ai_service.create_session()

                evento = await game_engine.processar_admin(data)

                if evento:
                    prompt_reacao = ""

                    if evento == "gol_furia":
                        prompt_reacao = (
                            "A FURIA ACABOU DE MARCAR UM PONTO/GOL! COMEMORE "
                            "MUITO, VIBRE, GRITE! USE EMOJIS DE FOGO E TROFÉU!"
                        )
                    elif evento == "ponto_adv":
                        prompt_reacao = (
                            "O ADVERSÁRIO MARCOU PONTO. FIQUE BRAVO, MAS "
                            "INCENTIVE O TIME A VIRAR. PEÇA RAÇA!"
                        )
                    elif evento == "reset":
                        prompt_reacao = (
                            "O JOGO REINICIOU! DIGA QUE AGORA É PRA VALER!"
                        )

                    if evento in ["mudou_adversario", "mudou_mapa",
                                  "mudou_jogo"]:
                        prompt_reacao = (
                            "O Admin atualizou os dados da partida "
                            "(Mapa, Adversário ou jogo). Comente sobre o novo "
                            "desafio de forma empolgada! Se trocar o jogo, não"
                            "deixe de informar.")

                    if prompt_reacao:
                        state = game_engine.get_state()
                        contexto_jogo = (
                            f"Placar: {state.placar_furia} x "
                            f"{state.placar_adversario} {state.nome_adversario}"
                            f". {prompt_reacao}"
                        )

                        await connection_manager.broadcast_json(WSPayload(
                            tipo="digitando", state=state
                        ))

                        resposta_ia = await ai_service.get_response(
                            user_session,
                            "EVENTO SISTEMA",
                            contexto_jogo
                        )

                        bot_msg = ChatMessageDTO(
                            autor="FURIÃO",
                            texto=resposta_ia,
                            is_bot=True
                        )

                        await connection_manager.broadcast_json(
                            WSPayload(
                                tipo="chat",
                                state=state,
                                chat=bot_msg
                            )
                        )
                continue

            # Tenta identificar algum sentimento para manipular o termômetro.
            await game_engine.processar_sentimento(data)

            user_msg = ChatMessageDTO(
                autor=f"Torcedor {client_id}",
                texto=data, is_bot=False
            )
            payload_user = WSPayload(
                tipo="chat",
                state=game_engine.get_state(),
                chat=user_msg
            )
            await connection_manager.broadcast_json(payload_user)

            payload_typing = WSPayload(
                tipo="digitando",
                state=game_engine.get_state()
            )
            await connection_manager.broadcast_json(payload_typing)

            state = game_engine.get_state()

            contexto_jogo = (
                f"Placar: FURIA {state.placar_furia} x "
                f"{state.placar_adversario} {state.nome_adversario}. "
                f"Jogo: {state.nome_jogo}. "
                f"Mapa Atual: {state.mapa_atual}"
                f"Termômetro da Torcida: {state.temperatura}"
            )

            resposta_ia = await ai_service.get_response(
                user_session,
                data,
                contexto_jogo
            )

            await game_engine.processar_sentimento(resposta_ia)

            bot_msg = ChatMessageDTO(
                autor="FURIÃO",
                texto=resposta_ia,
                is_bot=True
            )
            payload_bot = WSPayload(
                tipo="chat",
                state=game_engine.get_state(),
                chat=bot_msg
            )
            await connection_manager.broadcast_json(payload_bot)

    except WebSocketDisconnect:
        await connection_manager.disconnect(websocket)