from .Computer.createComputer import create_computador
from .Computer.listComputer import list_computador
from .Metrics.createMetrics import create_monitoramento
from .createDisks import create_disco

routers = [create_monitoramento, create_computador, create_disco, list_computador]