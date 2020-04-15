#de la product la dict
import numpy as np

timeLengths = {"DAY" : 1, "WEEK" : 7, "MONTH": 28}
absoluteTime = 1


def updateTime(type=timeLengths["DAY"]):
    global absoluteTime
    value = 0

    for key in timeLengths:
        if type == key:
            value = timeLengths[key]

    absoluteTime += value

    return absoluteTime


class Product:
    def __init__(self, name = '',price = 0.0, quantity = 0, time = 0):
        self.updateCounter = 1

        self.name = name

        self.totalQuantity = quantity
        self.totalPrices = price

        self.quantity = [quantity]
        self.timeStamp = [time]
        self.prices = [price]

    def set_product(self, price, quantity, time):

        self.quantity += [quantity]

        self.totalQuantity += quantity
        self.totalPrices += price

        self.prices += [price]
        self.timeStamp += [time]

    def update_product(self, price=None, quantity=None, time=None):

        if price is None:
            price = self.prices[self.updateCounter - 1]
        if quantity is None:
            quantity = self.quantity[self.updateCounter  - 1]
        if time is None:
            time = self.timeStamp[self.updateCounter  - 1]
        self.updateCounter += 1
        self.set_product(price, quantity, time)

    def get_average_price(self):

        return self.totalPrices / self.updateCounter
        #Avp = average_price = sum of prices / # prices
        #se face dupa set_products

    def average_price_change(self):
        if self.timeStamp[self.updateCounter  - 1] == self.timeStamp[0]:
            return 0
        return (self.prices[self.updateCounter  - 1] - self.prices[0]) / \
               (self.timeStamp[self.updateCounter  - 1] - self.timeStamp[0])
        #ACP = average price change = (price[i] - price[0]) / (t[i] - t[0])
        # se face dupa set_product

    def get_average_daily_distribution(self):
        if absoluteTime == self.timeStamp[0]:
            return -1
        return (self.totalQuantity - self.quantity[self.updateCounter - 1]) / \
               (absoluteTime - self.timeStamp[0])
        #D = Average daily_Distribution = total_quantity without the last buy / (time passed from the first buy)
        #se face dupa set_product

    def get_future_price(self, time):

        #returneaza coeficientii polinomului de interpolare
        def coeficiente(x,y):

            x = np.array(x, dtype=np.float32)
            y = np.array(y, dtype=np.float32)
            n = len(x)
            F = np.zeros((n,n), dtype=float)
            b = np.zeros(n)
            for i in range(0,n):
                F[i,0]=y[i]
            for j in range(1, n):
                for i in range(j,n):
                    F[i,j] = float(F[i,j-1]-F[i-1,j-1])/float(x[i]-x[i-j])
            for i in range(0,n):
                b[i] = F[i,i]
            return np.array(b) # return an array of coefficient
        
        #returneaza valoarea polinomului de interpolare in punctul r
        def eval(x, y, r):
            a = coeficiente(x, y)
            a.astype(float)
            n = len(a) - 1
            temp = a[n]
            for i in range( n - 1, -1, -1 ):
                temp = temp * ( r - x[i] ) + a[i]
            return abs(temp) # return the y_value interpolation
        return eval(self.timeStamp, self.prices, time)
        #returneaza pretul unui obiect la momentul de timp time 

    def get_expense_over_a_week(self):
        avgDailyDistr = self.get_average_daily_distribution()
        ans = 0.0
        for index in range(1, 8):
            ans += avgDailyDistr * self.get_future_price(absoluteTime + index)
        return ans
        # e(x) = Expense of product x over a week = FP(T+1) * D + FP(T + 2) * D +... + FP(T+7) * D

    def to_dict(self):
        ans = dict()
        ans['updateCounter'] = self.updateCounter
        ans['totalQuantity'] = self.totalQuantity
        ans['totalPrices'] = self.totalPrices
        ans['quantity'] = self.quantity
        ans['timeStamp'] = self.timeStamp
        ans['prices'] = self.prices
        ans['name'] = self.name
        return ans


class ProductList:
    def __init__(self):
        self.productList = {}

    def add_product(self, name, price, quantity, time):

        if self.productList.get(name) is None:
            self.productList[name] = Product(name, price, quantity, time)
        else:
            self.productList[name].update_product(price, quantity, time)

    def get_product(self, name):
        if self.productList.get(name) is not None:
            return self.productList[name]
        else:
            return None

    def get_forecast_budget(self):
        sum = 0

        for key in self.productList:
            sum += self.productList[key].get_expense_over_a_week()

        return sum

    def filter(self, type="None"):

        value = 0

        for key in timeLengths:
            if type == key:
                value = timeLengths[key]

        if value == 0:
            return self.productList
        else:
            newList = {}

            for key in self.productList:
                if self.productList[key].get_daily_distribution() >= value:
                    newList[key] = self.productList[key]

            return newList