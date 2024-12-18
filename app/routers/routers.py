# app/routers.py
from .Computer.createComputer import router as router_create_computer
from .Computer.listComputer import router as router_list_computer
from .Metrics.createMetrics import router as router_create_metrics
from .Metrics.listMetrics import router as router_list_metrics

# Agrupar todas as rotas em uma lista
routers = [
    router_create_computer,
    router_create_metrics,
    router_list_metrics,
    router_list_computer
]
