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
        return abs(tiempodeServicio[1].hour - tiempodeServicio[0].hour)
    
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
    # Casos que involucran fin de semana
    else:
        # Se trabajo el fin de semana completo
        if(tiempodeServicio[0].weekday() < 5 and tiempodeServicio[1].weekday() < 5):
            horasFinSem = 48
            tarifaFinSem = horasFinSem*tarifa.tasafinsem
            horasSem = 24-tiempodeServicio[0].hour
            horasSem += 24*((tiempodeServicio[1].day - tiempodeServicio[0].day)-3)
            if(tiempodeServicio[1].minute != 0):
                horasSem += tiempodeServicio[1].hour + 1
            else:
                horasSem += tiempodeServicio[1].hour
            tarifaSem = horasSem*tarifa.tasasem
            return tarifaSem + tarifaFinSem
        # Se empieza un dia de semana pero se termina un dia de fin de semana
        elif(tiempodeServicio[0].weekday() < 5):
            dias = 4 - tiempodeServicio[0].weekday()
            horasSem = dias*24
            horasSem += 24 - tiempodeServicio[0].hour
            horasFinSem = 0
            if(tiempodeServicio[1].weekday() == 6):
                horasFinSem = 24
            if(tiempodeServicio[1].minute != 0):
                horasFinSem += tiempodeServicio[1].hour + 1
            else:
                horasFinSem += tiempodeServicio[1].hour
            tarifaTotal = horasSem*tarifa.tasasem + horasFinSem*tarifa.tasafinsem 
            return tarifaTotal
        
        # Se empieza un dia del fin de semana y se termina en un dia de la semana
        else:
            diasfinsem = 6 - tiempodeServicio[0].weekday()
            horasFinSem = diasfinsem*24
            horasFinSem += 24-tiempodeServicio[0].hour
            horasSem = tiempodeServicio[1].weekday()*24
            if(tiempodeServicio[1].minute != 0):
                horasSem += tiempodeServicio[1].hour + 1
            else:
                horasSem += tiempodeServicio[1].hour
            tarifaTotal = horasSem*tarifa.tasasem + horasFinSem*tarifa.tasafinsem 
            return tarifaTotal   