import datetime
import sys

# Definicion de la clase tarifa
# Objeto que tiene una tasa de precio para semana
# y una tasa de precio para fines de semana
class Tarifa:
    def __init__(self):
        self.tasasem = 0
        self.tasafinsem = 0

# Funcion que dado una tarifa y un tiempo de servicio
# Calcula el monto a pagar por un servicio
def calcularPrecio(tarifa, tiempodeServicio: datetime):
    try:
        assert(tarifa.tasasem >= 0 and tarifa.tasafinsem >= 0)
    except:
        print("La tarifa no debe ser negativa")
        return -1
    try:
        assert((tiempodeServicio[1]-tiempodeServicio[0]).days <= 7)
    except:
        print("El servicio dura mas de 7 dias")
        return -2
    try:
        assert((tiempodeServicio[1]-tiempodeServicio[0]).total_seconds() >= 900)
    except:
        print("El servicio dura menos de 15 minutos")
        return -3