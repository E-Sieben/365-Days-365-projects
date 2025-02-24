def calc_tip(price: float, tip_in_percent: float = 5) -> float:
    try:
        if isinstance(tip_in_percent, str):
            tip_in_percent = tip_in_percent.replace("%", "")
        tip_in_percent = float(tip_in_percent)
    except TypeError:
        print("Please use a proper number")
        return
    
    return round(float(price) * (tip_in_percent * 0.01), 2)

print(calc_tip(input("Please Enter your price to pay: "), input("Now, please enter the Tip you want to give in percent: ")))