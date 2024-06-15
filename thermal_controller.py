import matplotlib.pyplot as plt
import time, os

class ThermalController:
  def __init__(self, target_temp, initial_temp):
    self.target_temp = target_temp
    self.current_temp = initial_temp
    self.error_previous = None
    self.iteration = 1
    self.error_history = []
    self.temp_history = []

    self.proportional_gain = 0.5  # Proportional control
    self.derivative_gain = 0.05  # Derivative control

  def adjust_temp(self, error_current, error_dot):
    return self.proportional_gain * error_current + self.derivative_gain * error_dot

  def get_rule(self, error_current, error_dot):
    if error_current > 0 and error_dot > 0: # PP
      return "Heater"
    elif error_current == 0 and error_dot > 0: # ZP
      return "Cooler"
    elif error_current < 0 and error_dot > 0: # NP
      return "Cooler"

    elif error_current > 0 and error_dot == 0: # PZ
      return "Heater"
    elif error_current == 0 and error_dot == 0: # ZZ
      return "No Change"
    elif error_current < 0 and error_dot == 0: # NZ
      return "Cooler"
    
    elif error_current > 0 and error_dot < 0: # PN
      return "Heater"
    elif error_current == 0 and error_dot < 0: # ZN
      return "Heater"
    elif error_current < 0 and error_dot < 0: # NN
      return "Cooler"

  def run_controller(self):
    while True:
      error_current = round(self.target_temp - self.current_temp)

      if self.iteration == 1:
          self.error_previous = error_current

      error_dot = round(self.error_previous - error_current)

      os.system("cls")
      print("------------------------------------------------------------------------------------------------------------------------")
      print(f"| {"TIME":<15}| {"TEMP [CMD]":<15}| {"CURRENT TEMP":<15}| {"PREV ERROR":<15}| {"ERROR":<15}| {"ERROR DOT":<15}| {"OUTPUT":<15}|")
      print("------------------------------------------------------------------------------------------------------------------------")
      print(f"| {self.iteration:<15}| {self.target_temp:<15}| {self.current_temp:<15}| {self.error_previous:<15}| {error_current:<15}| {error_dot:<15}| {self.get_rule(error_current, error_dot):<15}|")
      print("------------------------------------------------------------------------------------------------------------------------")

      self.temp_history.append(self.current_temp)
      self.error_history.append(error_current)
      
      temp_adjustment = self.adjust_temp(error_current, error_dot)
      self.current_temp += round(temp_adjustment)

      self.error_previous = error_current
      self.iteration += 1

      # Simulate a delay or time interval
      time.sleep(0.5) 

      # Terminate the loop if the error becomes insignificant
      if abs(error_current) == 0:
        break

  def plot_history(self):
    plt.plot(range(1, len(self.temp_history) + 1), self.temp_history, marker='o', label='TEMP')
    plt.plot(range(1, len(self.error_history) + 1), self.error_history, marker='o', label='Error')
    plt.plot([1, len(self.temp_history)], [self.target_temp, self.target_temp], linestyle='--', color='r', label='Target TEMP')
    plt.title('Error and TEMP History')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.legend()  # Add legend
    plt.grid(True)
    plt.show()

# Input parameters
target_temp = int(input("Enter target TEMP [CMD]: "))
initial_temp = int(input("Enter initial TEMP: "))

# Create and run the controller
controller = ThermalController(target_temp, initial_temp)
controller.run_controller()

# Plot the history
controller.plot_history()