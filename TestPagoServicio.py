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
    
    #Probar los casos en que el intervalo dura exactamente 15 minutos
    def test_exactoMinTiempo(self):
        self.tiempodeservicio = [datetime.datetime(2018,5,11,13,20),datetime.datetime(2018,5,11,13,36)]
        self.tarifa.tasasem = 20
        self.assertEqual(20, calcularPrecio(self.tarifa, self.tiempodeservicio))

    #Probar los casos en que el intervalo dura exactamente7 dias
    def test_exactoMaxTiempo(self):
        self.tiempodeservicio = [datetime.datetime(2018,5,11,13,15),datetime.datetime(2018,5,18,13,15)]
        self.tarifa.tasasem = 30
        self.tarifa.tasafinsem = 20
        self.sumaTotal = 120*self.tarifa.tasasem + 48*self.tarifa.tasafinsem
        self.assertEqual(self.sumaTotal, calcularPrecio(self.tarifa, self.tiempodeservicio))
        
    #Probar que se redondea a un hora los minutos sobrantes
    def test_RedondearMismoDia(self):
        self.tiempodeservicio = [datetime.datetime(2017,2,3,13,20),datetime.datetime(2017,2,3,15,40)]
        self.tarifa.tasasem = 20
        self.assertEqual(3*self.tarifa.tasasem, calcularPrecio(self.tarifa, self.tiempodeservicio))
        
    #Prueba calculo de la tarifa trabajando solo dias de semana
    def test_SoloSemana(self):
        self.tiempodeservicio = [datetime.datetime(2018,5,9,13,20),datetime.datetime(2018,5,11,15,21)]
        self.tarifa.tasasem = 20
        self.assertEqual(51*self.tarifa.tasasem, calcularPrecio(self.tarifa, self.tiempodeservicio))
    
    #Prueba calculo de la tarifa trabajando solo dias del fin de semana
    def test_FinSemana(self):
        self.tiempodeservicio = [datetime.datetime(2018,5,12,13,20),datetime.datetime(2018,5,13,15,40)]
        self.tarifa.tasafinsem = 20
        self.suma = 27*self.tarifa.tasafinsem
        self.assertEqual(self.suma, calcularPrecio(self.tarifa, self.tiempodeservicio))
    
    #Prueba para calcular la tarifa si se empieza un dia de semana y se termina un dia de semana (completo fin de semana)
    def test_DiaSemyDiaSem(self):
        self.tiempodeservicio = [datetime.datetime(2018,5,10,12,10),datetime.datetime(2018,5,15,12,2)]
        self.tarifa.tasafinsem = 20
        self.tarifa.tasasem = 30
        self.suma = 72*self.tarifa.tasasem + 48*self.tarifa.tasafinsem
        self.assertEqual(self.suma, calcularPrecio(self.tarifa, self.tiempodeservicio))
    
    #Prueba para calcular la tarifa si se empieza un dia de semana y se termina un domingo
    def test_DiaSemyFinSem2(self):
        self.tiempodeservicio = [datetime.datetime(2018,5,9,13,20),datetime.datetime(2018,5,13,12,22)]
        self.tarifa.tasafinsem = 20
        self.tarifa.tasasem = 30
        self.suma = 59*self.tarifa.tasasem + 37*self.tarifa.tasafinsem
        self.assertEqual(self.suma, calcularPrecio(self.tarifa, self.tiempodeservicio))
    
    #Prueba para calcular la tarifa si se empieza un dia del fin de semana y se termina un dia de la semana
    def test_DiaFinSemySem(self):
        self.tiempodeservicio = [datetime.datetime(2018,5,13,12,20),datetime.datetime(2018,5,16,14,2)]
        self.tarifa.tasafinsem = 20
        self.tarifa.tasasem = 30
        self.suma = 62*self.tarifa.tasasem + 12*self.tarifa.tasafinsem
        self.assertEqual(self.suma, calcularPrecio(self.tarifa, self.tiempodeservicio))
        
    def test_FinAnoDiaSem(self):
        self.tiempodeservicio = [datetime.datetime(2018,12,31,12,0),datetime.datetime(2019,1,1,12,0)]
        self.tarifa.tasafinsem = 20
        self.tarifa.tasasem = 30
        self.suma = 24*self.tarifa.tasasem
        self.assertEqual(self.suma, calcularPrecio(self.tarifa, self.tiempodeservicio))
        
    def test_FinAnoFinSem(self):
        self.tiempodeservicio = [datetime.datetime(2018,12,29,12,0),datetime.datetime(2019,1,1,12,0)]
        self.tarifa.tasafinsem = 20
        self.tarifa.tasasem = 30
        self.sumaSem = 36*self.tarifa.tasasem
        self.sumaFinSem = 36*self.tarifa.tasafinsem
        self.suma = self.sumaSem + self.sumaFinSem
        self.assertEqual(self.suma, calcularPrecio(self.tarifa, self.tiempodeservicio))
        
    def test_FinMesDiaSem(self):
        self.tiempodeservicio = [datetime.datetime(2018,5,30,12,0),datetime.datetime(2018,6,1,12,0)]
        self.tarifa.tasasem = 30
        self.sumaSem = 48*self.tarifa.tasasem
        self.assertEqual(self.sumaSem, calcularPrecio(self.tarifa, self.tiempodeservicio))    
        
    def test_FinMesFinSem(self):
        self.tiempodeservicio = [datetime.datetime(2018,5,31,12,0),datetime.datetime(2018,6,3,12,0)]
        self.tarifa.tasafinsem = 20
        self.tarifa.tasasem = 30
        self.sumaSem = 36*self.tarifa.tasasem
        self.sumaFinSem = 36*self.tarifa.tasafinsem
        self.suma = self.sumaSem + self.sumaFinSem
        self.assertEqual(self.suma, calcularPrecio(self.tarifa, self.tiempodeservicio))       
        
    def test_FinMesFinSem2(self):
        self.tiempodeservicio = [datetime.datetime(2018,6,30,12,0),datetime.datetime(2018,7,1,12,0)]
        self.tarifa.tasafinsem = 20
        self.sumaSem = 24*self.tarifa.tasafinsem
        self.assertEqual(self.sumaSem, calcularPrecio(self.tarifa, self.tiempodeservicio))
    
    def test_MaxTiempoFin(self):
        self.tiempodeservicio = [datetime.datetime(2018,5,12,12,0),datetime.datetime(2018,5,19,12,0)]
        self.tarifa.tasasem = 30
        self.tarifa.tasafinsem = 20
        self.sumaTotal = 120*self.tarifa.tasasem + 48*self.tarifa.tasafinsem
        self.assertEqual(self.sumaTotal, calcularPrecio(self.tarifa, self.tiempodeservicio))
        
    def test_MaxTiempoFin2(self):
        self.tiempodeservicio = [datetime.datetime(2018,5,13,12,0),datetime.datetime(2018,5,19,12,0)]
        self.tarifa.tasasem = 30
        self.tarifa.tasafinsem = 20
        self.sumaTotal = 120*self.tarifa.tasasem + 24*self.tarifa.tasafinsem
        self.assertEqual(self.sumaTotal, calcularPrecio(self.tarifa, self.tiempodeservicio))
        
    def test_MaxTiempoFin3(self):
        self.tiempodeservicio = [datetime.datetime(2018,5,13,12,0),datetime.datetime(2018,5,20,12,0)]
        self.tarifa.tasasem = 30
        self.tarifa.tasafinsem = 20
        self.sumaTotal = 120*self.tarifa.tasasem + 48*self.tarifa.tasafinsem
        self.assertEqual(self.sumaTotal, calcularPrecio(self.tarifa, self.tiempodeservicio))     

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()