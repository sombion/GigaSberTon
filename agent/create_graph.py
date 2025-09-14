from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, END
from state import graph_builder
from node import (
    change_node,
    confirmation_node,
    filter_node,
    check_user_data_node,
    info_agent_node,
    send_applications_node,
    user_templates_node,
    not_fillled_data_user_node,
    humman_check_node,
    invalid_request_node,
    confirmation_final_node,
)
from coordinator import change_router, check_user_data_router, confirmation_router, filter_router


graph_builder.add_node("filter_node", filter_node)
graph_builder.add_node("check_user_data_node", check_user_data_node)
graph_builder.add_node("confirmation_node", confirmation_node)
graph_builder.add_node("confirmation_final_node", confirmation_final_node)
graph_builder.add_node("change_node", change_node)
graph_builder.add_node("send_applications_node", send_applications_node)
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
        "confirmation_node": "confirmation_node"
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

graph_builder.add_edge("humman_check_node", "confirmation_node")
graph_builder.add_conditional_edges(
    "confirmation_node",
    confirmation_router,
    {
        "confirmation_final_node": "confirmation_final_node",
        "send_applications_node": "send_applications_node",
        "change_node": "change_node"
    }
)

graph_builder.add_edge("confirmation_final_node", END)

graph_builder.add_conditional_edges(
    "change_node",
    change_router,
    {
        "filter_node": "filter_node",
        "END": END
    }
)

graph_builder.add_edge("send_applications_node", END)
graph_builder.add_edge("info_agent_node", END)
graph_builder.add_edge("invalid_request_node", END)

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)
