# app/routers.py
from .Computer.createComputer import router as router_create_computer
from .Computer.listComputer import router as router_list_computer
from .Metrics.createMetrics import router as router_create_metrics
from .Metrics.listMetrics import router as router_list_metrics
from .Metrics.updateMetrics import router as router_update_metrics
from .Disks.createDisks import router as router_create_disks
from .Disks.listDisks import router as router_list_disks
from .Disks.updateDisks import router as router_update_disks

# Agrupar todas as rotas em uma lista
routers = [
    router_create_computer,
    router_create_metrics,
    router_list_metrics,
    router_list_computer,
    router_create_disks,
    router_list_disks,
    router_update_metrics,
    router_update_disks
]
