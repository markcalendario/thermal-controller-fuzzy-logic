import matplotlib.pyplot as plt

class ThermalController:
  def __init__(self, target_temp):
    self.target_temp = target_temp
    self.current_temp = None
    self.error_previous = None
    self.iteration = 1
    self.error_history = []
    self.temp_history = []

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
      self.current_temp = str(input("Enter current temperature: "))

      if self.current_temp == "stop":
        break

      self.current_temp = int(self.current_temp)
      error_current = self.target_temp - self.current_temp

      if self.iteration == 1:
          self.error_previous = error_current

      error_dot = self.error_previous - error_current

      print("------------------------------------------------------------------------------------------------------------------------")
      print(f"| {"TIME":<15}| {"TEMP [CMD]":<15}| {"CURRENT TEMP":<15}| {"PREV ERROR":<15}| {"ERROR":<15}| {"ERROR DOT":<15}| {"OUTPUT":<15}|")
      print("------------------------------------------------------------------------------------------------------------------------")
      print(f"| {self.iteration:<15}| {self.target_temp:<15}| {self.current_temp:<15}| {self.error_previous:<15}| {error_current:<15}| {error_dot:<15}| {self.get_rule(error_current, error_dot):<15}|")
      print("------------------------------------------------------------------------------------------------------------------------")

      self.temp_history.append(self.current_temp)
      self.error_history.append(error_current)

      self.error_previous = error_current
      self.iteration += 1

  def plot_history(self):
    plt.plot(range(1, len(self.temp_history) + 1), self.temp_history, marker='o', label='Temp')
    plt.plot(range(1, len(self.error_history) + 1), self.error_history, marker='o', label='Error')
    plt.plot([1, len(self.temp_history)], [self.target_temp, self.target_temp], linestyle='--', color='r', label='CMD')
    plt.title('Error and TEMP History')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.legend()  # Add legend
    plt.grid(True)
    plt.show()

# Input parameters
target_temp = int(input("Enter target TEMP [CMD]: "))

# Create and run the controller
controller = ThermalController(target_temp)
controller.run_controller()

# Plot the history
controller.plot_history()