from microbit import *
import utime

x = float(2.0)
y = float(1.5)

loop = 1e6

#start_time = utime.ticks_ms()
start_time = utime.ticks_us()

for n in range(loop):#10*=10の計算を1000回繰り返す。
    x=x*y+x/y

#end_time = utime.ticks_ms()
end_time = utime.ticks_us()

diff_time = utime.ticks_diff(end_time, start_time)/1000000 #msの時：1000、usの時：1000000
flo = float(loop*3)

flops = flo / diff_time /1000 #flopsの単位をK(キロ)にするため

while True:
    display.scroll("flops = {0} K, diff: {1}".format(float(flops),diff_time))

    ####
    #・.formatのコマンドが使えるかわからない。
    #何回か検証して、平均値を使う。
    #1.5*5LEDで検証  2.LCDスクリーンで検証  3.for n in range(1000)をもっと大きくして検証
