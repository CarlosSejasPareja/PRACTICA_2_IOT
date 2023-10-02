import math

class CalculateSpeedOfSound:
    def __init__(self, temperature, humidity):
        self.p = 102000 #hectopascales
        self.cramer_coefficients = [331.5024, 0.603055, -0.000528, 51.471935,
                             0.1495874, -0.000782, -1.82e-7, 3.73e-8,
                             -2.93e-10, -85.20931, -0.228525, 5.91e-5,
                             -2.835149, -2.15e-13, 29.179762, 0.000486]
        self.temp = temperature
        self.humidity = humidity

    def calculate_speed_of_sound(self):
        T = self.temp + 273.15
        h = self.humidity / 100.0
        f = 1.00062 + 0.0000000314 * self.p + 0.00000056 * self.temp**2
        Psv = math.exp(0.000012811805 * T**2 - 0.019509874 * T + 34.04926034 - 6353.6311 / T)
        Xw = h * f * Psv / self.p
        c = 331.45 - self.cramer_coefficients[0] - self.p * self.cramer_coefficients[6] - self.cramer_coefficients[13] * self.p**2
        c = math.sqrt(self.cramer_coefficients[9]**2 + 4 * self.cramer_coefficients[14] * c)
        Xc = ((-1) * self.cramer_coefficients[9] - c) / (2 * self.cramer_coefficients[14])
        speed = (self.cramer_coefficients[0] + self.cramer_coefficients[1] * self.temp +
                 self.cramer_coefficients[2] * self.temp**2 +
                 (self.cramer_coefficients[3] + self.cramer_coefficients[4] * self.temp +
                  self.cramer_coefficients[5] * self.temp**2) * Xw +
                 (self.cramer_coefficients[6] + self.cramer_coefficients[7] * self.temp +
                  self.cramer_coefficients[8] * self.temp**2) * self.p +
                 (self.cramer_coefficients[9] + self.cramer_coefficients[10] * self.temp +
                  self.cramer_coefficients[11] * self.temp**2) * Xc +
                 self.cramer_coefficients[12] * Xw**2 + self.cramer_coefficients[13] * self.p**2 +
                 self.cramer_coefficients[14] * Xc**2 + self.cramer_coefficients[15] * Xw * self.p * Xc)
        return speed
