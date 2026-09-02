import json
import os
from sqlalchemy.orm import Session
from openai import OpenAI
from app.db.models import Conversation, ConversationMessage, User
from app.tools import agent_tools

SYSTEM_PROMPT = """You are the ParcelPilot AI Customer Support Representative.
Your goal is to assist users with shipment tracking, support tickets, and SLA inquiries.
Always act professionally and never hallucinate data.

Guidelines:
1. Always use available tools to look up shipment or ticket details before answering.
2. If the user asks about SLAs or policies, search the knowledge base.
3. If the user asks to perform an action (escalate, cancel), use prepare_escalation or similar tools, and explain that confirmation is required.
4. Do NOT output raw JSON unless specifically requested. Answer in friendly natural language.
5. If the database does not contain the answer, say that the information is unavailable.
"""

def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY", "dummy_key_for_testing")
    return OpenAI(api_key=api_key)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "lookup_shipment",
            "description": "Look up current status and core details of a shipment by its tracking ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tracking_id": {"type": "string", "description": "The shipment tracking ID, e.g., ORD-1001"}
                },
                "required": ["tracking_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_tracking_history",
            "description": "Get chronological tracking events and location history for a shipment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tracking_id": {"type": "string"}
                },
                "required": ["tracking_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_support_ticket",
            "description": "Look up an existing support ticket by its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_id": {"type": "string"}
                },
                "required": ["ticket_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_support_ticket",
            "description": "Create a new support ticket.",
            "parameters": {
                "type": "object",
                "properties": {
                    "subject": {"type": "string"},
                    "description": {"type": "string"},
                    "priority": {"type": "string", "enum": ["P1", "P2", "P3"]}
                },
                "required": ["subject", "description", "priority"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "shipment_sla_status",
            "description": "Look up SLA timing, faults, and delays for a shipment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tracking_id": {"type": "string"}
                },
                "required": ["tracking_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "prepare_escalation",
            "description": "Create a pending action to escalate a support ticket.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_id": {"type": "string"},
                    "reason": {"type": "string"}
                },
                "required": ["ticket_id", "reason"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "confirm_action",
            "description": "Confirm or cancel a pending action (like an escalation).",
            "parameters": {
                "type": "object",
                "properties": {
                    "action_id": {"type": "string", "description": "The action ID, e.g. ACT-123456"},
                    "confirmed": {"type": "boolean", "description": "True to execute, False to cancel"}
                },
                "required": ["action_id", "confirmed"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "knowledge_search",
            "description": "Search the ParcelPilot knowledge base for SLA rules, credits, and policies.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    }
]

def dispatch_tool(tool_call, db: Session, current_user: User):
    name = tool_call.function.name
    try:
        args = json.loads(tool_call.function.arguments)
    except json.JSONDecodeError:
        args = {}
    
    if name == "lookup_shipment":
        return agent_tools.lookup_shipment(db, args.get("tracking_id"), current_user)
    elif name == "get_tracking_history":
        return agent_tools.get_tracking_history(db, args.get("tracking_id"), current_user)
    elif name == "lookup_support_ticket":
        return agent_tools.lookup_support_ticket(db, args.get("ticket_id"), current_user)
    elif name == "create_support_ticket":
        return agent_tools.create_support_ticket(db, args.get("subject"), args.get("description"), args.get("priority", "P2"), current_user)
    elif name == "shipment_sla_status":
        return agent_tools.shipment_sla_status(db, args.get("tracking_id"), current_user)
    elif name == "prepare_escalation":
        return agent_tools.prepare_escalation(db, args.get("ticket_id"), args.get("reason"), current_user)
    elif name == "confirm_action":
        return agent_tools.confirm_action(db, args.get("action_id"), args.get("confirmed"), current_user)
    elif name == "knowledge_search":
        return agent_tools.knowledge_search(db, args.get("query"), current_user)
    else:
        return {"error": f"Unknown function: {name}"}

def process_chat(db: Session, user: User, conversation_id: int, user_message: str):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == user.id).first()
    if not conv:
        conv = Conversation(user_id=user.id, account_id=user.account_id)
        db.add(conv)
        db.commit()
        db.refresh(conv)

    user_msg_db = ConversationMessage(conversation_id=conv.id, role="user", content=user_message)
    db.add(user_msg_db)
    db.commit()

    # Build messages for LLM
    db_messages = db.query(ConversationMessage).filter(ConversationMessage.conversation_id == conv.id).order_by(ConversationMessage.created_at).all()
    
    llm_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in db_messages:
        if msg.tool_calls:
            # Reconstruct tool calls format for OpenAI
            try:
                tc = json.loads(msg.tool_calls)
                llm_messages.append({"role": msg.role, "content": msg.content or "", "tool_calls": tc})
            except:
                llm_messages.append({"role": msg.role, "content": msg.content})
        elif msg.role == "tool":
            llm_messages.append({"role": msg.role, "content": msg.content, "tool_call_id": getattr(msg, "tool_call_id", "")}) # tool_call_id would need db field, keeping simple
        else:
            llm_messages.append({"role": msg.role, "content": msg.content})
            
    # For a real integration, we parse the DB messages precisely. 
    # To keep simple and robust without breaking openAI schema on missing tool_call_ids, we'll just send standard role/content history.
    simplified_history = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in db_messages:
        if msg.role in ["user", "assistant"] and msg.content:
            simplified_history.append({"role": msg.role, "content": msg.content})

    client = get_openai_client()
    
    # Check if we should mock LLM response for local tests missing the API key
    if client.api_key == "dummy_key_for_testing":
        # Mocking for CI/tests
        response_content = "AI assistant is running in demo mode right now — responses are simulated."
        ai_msg = ConversationMessage(conversation_id=conv.id, role="assistant", content=response_content)
        db.add(ai_msg)
        db.commit()
        return response_content, conv.id

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # or gpt-4
            messages=simplified_history,
            tools=TOOLS,
            tool_choice="auto"
        )
    except Exception as e:
        err = f"AI Service Error: {str(e)}"
        err_msg = ConversationMessage(conversation_id=conv.id, role="assistant", content=err)
        db.add(err_msg)
        db.commit()
        return err, conv.id

    choice = response.choices[0]
    
    # Handle Tool calls
    if choice.message.tool_calls:
        # Save assistant message with tool calls
        tc_json = [tc.model_dump() for tc in choice.message.tool_calls]
        ai_msg = ConversationMessage(conversation_id=conv.id, role="assistant", content="", tool_calls=json.dumps(tc_json))
        db.add(ai_msg)
        db.commit()
        
        simplified_history.append(choice.message)
        
        # Execute tools
        for tc in choice.message.tool_calls:
            result = dispatch_tool(tc, db, user)
            
            # Save tool result
            tool_msg = ConversationMessage(conversation_id=conv.id, role="tool", content=json.dumps(result))
            # simplified saving for sqlite, but we inject to history
            db.add(tool_msg)
            
            simplified_history.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "name": tc.function.name,
                "content": json.dumps(result)
            })
        db.commit()
        
        # Call LLM again with tool results
        try:
            second_resp = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=simplified_history
            )
            final_content = second_resp.choices[0].message.content
        except Exception as e:
            final_content = f"Error processing tool results: {str(e)}"
            
        final_msg = ConversationMessage(conversation_id=conv.id, role="assistant", content=final_content)
        db.add(final_msg)
        db.commit()
        return final_content, conv.id
        
    else:
        # Standard text response
        content = choice.message.content
        ai_msg = ConversationMessage(conversation_id=conv.id, role="assistant", content=content)
        db.add(ai_msg)
        db.commit()
        return content, conv.id
