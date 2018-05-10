import datetime
import sys

# Definicion de la clase tarifa
# Objeto que tiene una tasa de precio para semana
# y una tasa de precio para fines de semana
class Tarifa:
    def __init__(self):
        self.tasasem = 0
        self.tasafinsem = 0

#Funcion que dado un tiempo de servicio redondea las horas
def cantidadhoras(tiempodeServicio):
    if((tiempodeServicio[1].minute - tiempodeServicio[0].minute) > 0):
        return tiempodeServicio[1].hour - tiempodeServicio[0].hour + 1
    else:
        return tiempodeServicio[1].hour - tiempodeServicio[0].hour
    
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
    
    #Caso en el que el dia de inicio y el final son el mismo
    if(tiempodeServicio[1].day == tiempodeServicio[0].day):
        if (cantidadhoras(tiempodeServicio)):
            horas = (tiempodeServicio[1].hour-tiempodeServicio[0].hour)+1
        else:
            horas = tiempodeServicio[1].hour-tiempodeServicio[0].hour
        if(tiempodeServicio[0].weekday() < 5):
            return horas*tarifa.tasasem
        else:
            return horas*tarifa.tasafinsem
        
    #Caso en el que el dia de inicio y final son ditintos
    if (((tiempodeServicio[0].weekday() <= 4 and tiempodeServicio[1].weekday() <= 4) or 
        ((tiempodeServicio[0].weekday() > 4 and tiempodeServicio[1].weekday() > 4)))
        and (tiempodeServicio[1].weekday() >= tiempodeServicio[0].weekday())):
            horas = 24 - tiempodeServicio[0].hour
            horas += 24*((tiempodeServicio[1].day - tiempodeServicio[0].day)-1)
            if(tiempodeServicio[1].minute != 0):
                horas += tiempodeServicio[1].hour + 1
            else:
                horas += tiempodeServicio[1].hour
            # Trabajo durante la semana
            if(tiempodeServicio[0].weekday() < 5):
                return horas*tarifa.tasasem
            # Trabajo solo el fin de semana
            else:
                return horas*tarifa.tasafinsem   