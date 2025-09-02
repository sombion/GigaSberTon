from langgraph.graph import START, END
from state import graph_builder
from node import filter_node, user_templates_node, commission_templates_node
from coordinator import coordinator_router


graph_builder.add_node("filter_node", filter_node)
graph_builder.add_node("coordinator_router", coordinator_router)
graph_builder.add_node("user_templates_node", user_templates_node)
graph_builder.add_node("commission_templates_node", commission_templates_node)

graph_builder.add_edge(START, "filter_node")
graph_builder.add_conditional_edges(
    "filter_node",
    filter_node,
    {
        "END": END,
        "coordinator_router": "coordinator_router"
    }
)
graph_builder.add_conditional_edges(
    "coordinator_router",
    coordinator_router,
    {
        "user_templates_node": "user_templates_node",
        "commission_templates_node": "commission_templates_node"
    }
)
graph_builder.add_edge("user_templates_node", END)
graph_builder.add_edge("commission_templates_node", END)

graph = graph_builder.compile()