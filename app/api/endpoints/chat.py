from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User, Conversation, ConversationMessage
from app.api.deps import get_current_user
from app.services.ai import process_chat

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: int | None = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: int

@router.post("", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Simple rate limiting or guest limit checks could go here
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    # Validation if continuing conversation
    if request.conversation_id:
        conv = db.query(Conversation).filter(Conversation.id == request.conversation_id, Conversation.user_id == current_user.id).first()
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation not found")
        conv_id = conv.id
    else:
        # Create a new conversation if none provided
        conv = Conversation(user_id=current_user.id, account_id=current_user.account_id)
        db.add(conv)
        db.commit()
        db.refresh(conv)
        conv_id = conv.id

    # Call AI service
    response_content, final_conv_id = process_chat(db, current_user, conv_id, request.message)
    
    return {"response": response_content, "conversation_id": final_conv_id}

@router.get("/history", response_model=list[dict])
def get_conversations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    convs = db.query(Conversation).filter(Conversation.user_id == current_user.id).order_by(Conversation.created_at.desc()).limit(10).all()
    return [{"id": c.id, "created_at": c.created_at} for c in convs]

@router.get("/{conversation_id}", response_model=list[dict])
def get_conversation_messages(conversation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == current_user.id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    msgs = db.query(ConversationMessage).filter(ConversationMessage.conversation_id == conv.id).order_by(ConversationMessage.created_at).all()
    # Filter out tools from user view if desired, or return everything
    display_msgs = []
    for m in msgs:
        if m.role in ["user", "assistant"] and m.content:
            display_msgs.append({
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at
            })
    return display_msgs
