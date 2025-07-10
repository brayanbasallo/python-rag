# api/routes.py
from fastapi import APIRouter
from pydantic import BaseModel
from src.services.chat_service import ChatService
from src.services.search_service import SearchService

chat_service = ChatService()
search_service = SearchService()

router = APIRouter()


class ChatRequest(BaseModel):
    messages: str


class SearchRequest(BaseModel):
    query: str


@router.get('/chat')
def chat_endpoint(request: ChatRequest):
    return {"response": chat_service.get_response(request.messages)}


@router.get('/search')
def search_endpoint(request: SearchRequest):
    return {"results": search_service.search(request.query)}
