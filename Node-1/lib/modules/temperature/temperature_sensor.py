import board
import busio as io
import adafruit_mlx90614 as ml

i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
mlx = ml.MLX90614(i2c)

def get_object_temperature():    
    return mlx.object_temperature