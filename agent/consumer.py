from pydantic import BaseModel
from create_graph import graph
from producer import send_output_agent
from pydantic import BaseModel
from config import router


class AgentData(BaseModel):
    tg_id: int
    text: str


@router.subscriber("input_agent")
async def consumer_text(data: AgentData):
    print("-> input_agent")
    responce = graph.ainvoke(
        {"input_messages": data.text, "tg_id": data.tg_id},
        config={"configurable": {"thread_id": str(data.tg_id)}},
    )
    responce = await responce  # дожидаемся выполнения
    data.text = responce["output_messages"]
    await send_output_agent(data)