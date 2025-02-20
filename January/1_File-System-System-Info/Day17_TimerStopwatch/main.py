from time import sleep, time

def timer(time_in_sec: int) -> int:
   '''
   use None or False for Stopwatch
   '''
   start_time = time()
   i = 0
   if time_in_sec:
      while time()-start_time < time_in_sec:
         print(f"Elapsed Time: {i/100:.3} seconds", end="\r")
         i += 1
         sleep(0.01)
      print(" " * 50, end="\r")
      print(f"{time_in_sec} seconds are finished")
      return time_in_sec
   else:
      while True:
         try:
            print(f"Elapsed Time: {i/100:.3} seconds", end="\r")
            i += 1
            sleep(0.01)
         except:
            print("")
            print(f"Elapsed Time: {time()-start_time:.3} seconds")
            return i
timer(6.9)