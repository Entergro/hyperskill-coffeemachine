class __State:
    name = None
    allowed = []
    msg = None

    def switch(self, state):
        if state.name in self.allowed:
            self.__class__ = state
        else:
            print('error')

    def __str__(self):
        return self.name


class MenuState(__State):
    name = "menu"
    allowed = ["buy", "fill_water"]
    msg = "Write action (buy, fill, take, remaining, exit): "


class BuyState(__State):
    name = "buy"
    allowed = ["menu"]
    msg = "What do you want to buy? " \
          "1 - espresso, " \
          "2 - latte, " \
          "3 - cappuccino, " \
          "back - to main menu: "


class FillWaterState(__State):
    name = "fill_water"
    allowed = ["fill_milk"]
    msg = "Write how many %s do you want to add: " % "ml of water"


class FillMilkState(__State):
    name = "fill_milk"
    allowed = ["fill_beans"]
    msg = "Write how many %s do you want to add: " % "ml of milk"


class FillBeansState(__State):
    name = "fill_beans"
    allowed = ["fill_cups"]
    msg = "Write how many %s do you want to add: " % "grams of coffee beans"


class FillCupsState(__State):
    name = "fill_cups"
    allowed = ["menu"]
    msg = "Write how many %s do you want to add: " % "disposable cups of coffee"


class CoffeeMachine:
    class __Coffee:
        def __init__(self, water, milk, beans, money):
            self.water = water
            self.milk = milk
            self.beans = beans
            self.money = money

    coffee_data = [__Coffee(250, 0, 16, 4),
                   __Coffee(350, 75, 20, 7),
                   __Coffee(200, 100, 12, 6)]

    def __init__(self):
        self.milk = 540
        self.water = 400
        self.beans = 120
        self.cups = 9
        self.money = 550
        self.state = MenuState()
        print(self.state.msg)

    def __dispatch_menu(self, req):
        if req == "buy":
            self.state.switch(BuyState)
            print(self.state.msg)
        elif req == "fill":
            self.state.switch(FillWaterState)
            print(self.state.msg)
        elif req == "take":
            print(f"I gave you ${self.money}")
            self.money = 0
            print(self.state.msg)
        elif req == "remaining":
            print(f'The coffee machine has:\n'
                  f'{self.water} of water\n'
                  f'{self.milk} of milk\n'
                  f'{self.beans} of coffee beans\n'
                  f'{self.cups} of disposable cups\n'
                  f'${self.money} of money\n')
            print(self.state.msg)

    def make_coffee(self, coffee):
        self.water -= self.coffee_data[coffee].water
        self.milk -= self.coffee_data[coffee].milk
        self.beans -= self.coffee_data[coffee].beans
        self.money += self.coffee_data[coffee].money
        self.cups -= 1

    def __dispatch_buy(self, req):
        def check_res(coffee):
            if self.water < self.coffee_data[coffee].water:
                return False, "water"
            if self.milk < self.coffee_data[coffee].milk:
                return False, "milk"
            if self.beans < self.coffee_data[coffee].beans:
                return False, "coffee beans"
            if self.cups == 0:
                return False, "disposable cups"

            return True, None

        if req != "back":
            status, not_enough_res = check_res(int(req) - 1)
            if not status:
                print("Sorry, not enough %s!" % not_enough_res)
            else:
                print("I have enough resources, making you a coffee!")
                self.make_coffee(int(req) - 1)
        self.state.switch(MenuState)
        print(self.state.msg)

    def __dispatch_fill(self, req):
        if isinstance(self.state, FillWaterState):
            self.water += int(req)
            self.state.switch(FillMilkState)
            print(self.state.msg)
        elif isinstance(self.state, FillMilkState):
            self.milk += int(req)
            self.state.switch(FillBeansState)
            print(self.state.msg)
        elif isinstance(self.state, FillBeansState):
            self.beans += int(req)
            self.state.switch(FillCupsState)
            print(self.state.msg)
        else:
            self.cups += int(req)
            self.state.switch(MenuState)
            print(self.state.msg)

    def dispatch(self, req):
        if isinstance(self.state, MenuState):
            if req == "exit":
                return 0
            self.__dispatch_menu(req)
        elif isinstance(self.state, BuyState):
            self.__dispatch_buy(req)
        else:
            self.__dispatch_fill(req)
        return 1


machine = CoffeeMachine()
while machine.dispatch(input()):
    pass
