def save_checkpoint(filename, year, month, day):
   f = open(filename, "w")
   f.write("{0},{1},{2}".format(year, month, day)) 
   f.close()
      

def load_checkpoint(filename):
   try:
      f = open(filename, "r")
      date = f.read().split(",")
      f.close()

      # Year, Month, Day
      return (int(date[0]), int(date[1]), int(date[2]))
   except IOError:
      print("IOError")
      return (2012, 3, 28)
