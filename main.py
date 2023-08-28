# create the Based Item class
class BaseItem:

  def __init__(self, name, price, item_number):
    self.name = name
    self.price = price
    self.item_number = item_number
    self.sold = 0

  def purchase(self):
    self.sold = self.sold + 1

  def restock(self, amount):
    self.stock = self.stock + int(amount)

  def __str__(self):
    return (
        f"{self.item_number}: {self.name} (${self.price}) Sold: {self.sold}")


# DigitalItem inherits from BaseItem
# expanding child class
class DigitalItem(BaseItem):

  def __str__(self):
    output = super().__str__()
    output = f"Digital " + output
    return output


# ShippableItem inherits from BaseItem
# expanding child class
class ShippableItem(BaseItem):

  def __init__(self, name, price, item_number, stock):
    super().__init__(name, price, item_number)
    self.stock = stock

  def purchase(self):
    if self.stock != 0:
      self.sold += 1
      self.stock -= 1
    else:
      raise Exception

  def restock(self, amount):
    self.stock = self.stock + int(amount)

  def __str__(self):
    output = f"Physical " + super().__str__() + f" Qty: {self.stock}"
    return output


# create the Shop class
class Shop:

  def __init__(self, name, address, init_inventory_file):
    self.name = name
    self.address = address
    self.inventory_dictionary = self.load_inventory(init_inventory_file)

  def purchase(self, item_num):
    self.inventory_dictionary[item_num].purchase()

  def restock(self, item_num, quantity):
    self.inventory_dictionary[item_num].restock(quantity)

  # compute the total dollar amount of sales made
  def get_sales(self):
    earned = 0
    for object in self.inventory_dictionary.values():
      earned = earned + object.sold * object.price
    return earned

  # reset the sold number to 0
  def reset(self):
    for i in self.inventory_dictionary.values():
      i.sold = 0

  # load the inventory to a dictionary,
  # key: item number -> value: Item object
  def load_inventory(self, filename):
    dic = {}
    infile = open(filename)
    for item in infile:
      item = item.strip().split('|')
      if item[3] == "-1":
        myItem = DigitalItem(item[0], int(item[1]), item[2])
        dic[myItem.item_number] = myItem
      else:
        myItem = ShippableItem(item[0], int(item[1]), item[2], int(item[3]))
        dic[myItem.item_number] = myItem
    return dic

  # write its current inventory to a file
  def save(self, filename):
    file = open(filename, "w")
    for item in self.inventory_dictionary.values():
      file.write(item.__str__() + "\n")
    file.write("\n\n")
    file.close()

  # process events and print out the updated inventory
  def process_events(self, transaction_log, output_file):
    error = 0
    for daily_events in transaction_log:
      infile = open(daily_events)
      for event in infile:
        event = event.strip().split("|")
        if event[0] == "buy":
          try:
            shop1.inventory_dictionary[event[1]].purchase()
          except:
            error += 1
        else:
          shop1.inventory_dictionary[event[1]].restock(event[2])
      infile.close()

    self.save(output_file)
    outfile = open(output_file, "a")
    outfile.write(f"Total Sale Amounts: ${shop1.get_sales()}\n")
    outfile.write(f"{error} failed purchases\n")
    outfile.close()


# run the program:

# create an init shop object:
shop1 = Shop("Brooklyn", "Brooklyn downtown", "inventory.txt")

# process events happend in Monday and Tuesday for shop1
# and output the updated inventory, total sale amouts, and failed transaction
shop1.process_events(["events_monday.txt", "events_tuesday.txt"],
                     "updated_after_Mon_Tue.txt")
