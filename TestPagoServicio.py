import unittest
from PagoServicio import *

class Test(unittest.TestCase):

    def setUp(self):
        self.tarifa = Tarifa()
        pass

    def tearDown(self):
        self.tarifa = None
        pass

    # Probar si insertar una tarifa negativa genera un error
    def test_TarifaNegativa(self):
        self.tiempodeservicio = [datetime.datetime(2017,2,3,13,15),datetime.datetime(2017,2,3,13,15)]
        self.tarifa.tasasem = -30
        self.tarifa.tasafinsem = -20
        self.assertTrue(calcularPrecio(self.tarifa, self.tiempodeservicio) == -1, "La tarifa debe dar error")
    
    #Probar si la duracion de un servicio es mayor a 7 dias
    def test_MaxDias(self):
        self.tiempodeservicio = [datetime.datetime(2017,2,3,13,15),datetime.datetime(2017,2,14,13,15)]
        self.tarifa.tasasem = 20
        self.assertTrue(calcularPrecio(self.tarifa, self.tiempodeservicio) == -2, "El maximo de dias debe dar error")

    #Probar si la duracion de un servicio es menor a 15 minutos
    def test_MinTiempo(self):
        self.tiempodeservicio = [datetime.datetime(2017,2,3,13,15),datetime.datetime(2017,2,3,13,20)]
        self.tarifa.tasasem = 20
        self.assertTrue(calcularPrecio(self.tarifa, self.tiempodeservicio) == -3, "El minimo de tiempo debe dar error")
    
    
    #Probar si la fecha inicio de servicio es posterior a la de inicio
    def test_OrdenFecha(self):
        self.tiempodeservicio = [datetime.datetime(2018,2,3,13,20),datetime.datetime(2017,2,3,13,15)]
        self.tarifa.tasafinsem = 20
        self.assertTrue(calcularPrecio(self.tarifa, self.tiempodeservicio) == -3, "Fecha final posterior a la inicial")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()