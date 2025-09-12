from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, END
from state import graph_builder
from node import (
    filter_node,
    check_user_data_node,
    info_agent_node,
    user_templates_node,
    not_fillled_data_user_node,
    humman_check_node,
    invalid_request_node,
)
from coordinator import check_user_data_router, filter_router


graph_builder.add_node("filter_node", filter_node)
graph_builder.add_node("check_user_data_node", check_user_data_node)
graph_builder.add_node("user_templates_node", user_templates_node)
graph_builder.add_node("not_fillled_data_user_node", not_fillled_data_user_node)
graph_builder.add_node("humman_check_node", humman_check_node)
graph_builder.add_node("info_agent_node", info_agent_node)
graph_builder.add_node("invalid_request_node", invalid_request_node)

graph_builder.add_edge(START, "filter_node")
graph_builder.add_conditional_edges(
    "filter_node",
    filter_router,
    {
        "user_templates_node": "user_templates_node",
        "invalid_request_node": "invalid_request_node",
        "info_agent_node": "info_agent_node",
    },
)
graph_builder.add_edge("user_templates_node", "check_user_data_node")
graph_builder.add_conditional_edges(
    "check_user_data_node",
    check_user_data_router,
    {
        "True": "humman_check_node", # Отправка данных на проверку
        "False": "not_fillled_data_user_node", # END Завершение
    },
)

graph_builder.add_edge("not_fillled_data_user_node", END)
graph_builder.add_edge("humman_check_node", END)

graph_builder.add_edge("info_agent_node", END)
graph_builder.add_edge("invalid_request_node", END)

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)
