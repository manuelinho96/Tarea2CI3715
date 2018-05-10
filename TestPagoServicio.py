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
    
    #Probar que se redondea a un hora los minutos sobrantes
    def test_RedondearMismoDia(self):
        self.tiempodeservicio = [datetime.datetime(2017,2,3,13,20),datetime.datetime(2017,2,3,15,40)]
        self.tarifa.tasasem = 20
        self.assertEqual(3*self.tarifa.tasasem, calcularPrecio(self.tarifa, self.tiempodeservicio))
        
    #Prueba calculo de la tarifa trabajando solo dias de semana
    def test_SoloSemana(self):
        self.tiempodeservicio = [datetime.datetime(2018,5,9,13,20),datetime.datetime(2018,5,11,15,0)]
        self.tarifa.tasasem = 20
        self.assertEqual(50*self.tarifa.tasasem, calcularPrecio(self.tarifa, self.tiempodeservicio))
    
    #Prueba calculo de la tarifa trabajando solo dias de semana
    def test_SoloSemana2(self):
        self.tiempodeservicio = [datetime.datetime(2018,5,9,13,20),datetime.datetime(2018,5,11,9,15)]
        self.tarifa.tasasem = 20
        self.assertEqual(45*self.tarifa.tasasem, calcularPrecio(self.tarifa, self.tiempodeservicio))
    
    #Prueba calculo de la tarifa trabajando solo dias del fin de semana
    def test_FinSemana(self):
        self.tiempodeservicio = [datetime.datetime(2018,5,12,13,20),datetime.datetime(2018,5,13,15,40)]
        self.tarifa.tasafinsem = 20
        self.suma = 27*self.tarifa.tasafinsem
        self.assertEqual(self.suma, calcularPrecio(self.tarifa, self.tiempodeservicio))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()