import re
import random
import sys
import SQL as reserve
import datetime 
error_counter = 0
positive = ["yes", "y" ,"sure" , "why not" , "yep", "absolutely"]
negative = ["no",  "nope" ,"n" , "no way"]
reports = []

def init():
    print("Hi, welcome to Strawberry Farm, how can I help you? I am UtraHighIntaliganceBot, named Mansikka.")

# Message probability

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Longer responses
    R_WHEATHER = "I would use ilmatieteenlaitos for that. :)"
    R_ADVICE = "If I were you, I would go to Google and type exactly what you wrote there!"
    R_LOVE = "Thank you ! Our strawberries are the best that money can buy."
    R_WRONG = "I am sorry that something is wrong, please contact our cutomer servivices."
    R_URGENT = "If there is urengt situtation, please contact this phone number: 050 000 0000"
    R_CANCEL = "If you want to cancel your order, please submit the request and we will come back to you as soon as possible."
    R_RATE = "Do you want to rate our services?"
    R_PURCHASE = "Do you want to purchase?"
    R_ORDER = "Do you want to order?"
    R_BUY = "Do you want to buy?"
    R_NAME = "My name is Mansikka!"
    R_SCORE = "Do you want to score our services?"
    R_ISSUE = "I am sorry that you have an issue, please contact our cutomer servivices."
    R_RESERVE = "You wish to reserve an amount for picking? Very well, let me bring up the list."
    R_RESERVATION = "You wish to make a reservation for picking? Very well, let me bring up the list."
    R_REVIEW = "Let's see about your reservation"
    R_REVIEW2 = "Let me check your reservation"
    R_REVIEW3 = "Let me check your reservation!"
    R_OPEN = "We are open from Monday to Friday from 9AM to 5PM"
    R_OPEN2 = "Our opening hours are from Monday to Friday between 9AM and 5PM"
    R_KIND = 'We currently offer only strawberries of the Polka kind '
    R_VARIETY = 'We currently offer only strawberries of the Polka variety'


    # Responses -------------------------------------------------------------------------------------------------------
    response("Hello!", ["hello", "hi", "hey", "sup", "heyo"], single_response=True)
    response("That is very nice to hear :)", ["good", "fine", "alright"], single_response=True)
    response("Like I care.", ["bad", "horrible", "shit"], single_response=True)
    response(R_LOVE, ["i", "love", "your","strawberries"], required_words=["love","strawberries"])
    #response("See you!", ["bye", "goodbye"], single_response=True)
    response("I\'m doing fine, and you?", ["how", "are", "you", "doing"], required_words=["how", "you"])
    response("You\'re welcome!", ["thank", "thanks"], single_response=True)
    response(R_ADVICE, ["give", "advice"], required_words=["advice"])
    response(R_WHEATHER, ["what", "wheather", "is", "can", "tell"], required_words=["weather"])
    response(R_WRONG, ["something", "is", "wrong"], required_words=["wrong"])
    response(R_ISSUE, ["there", "is", "issue"], required_words=["issue"])
    response(R_URGENT, ["something", "came", "unplanned", "please", "fast", "quick", "urgent"], required_words= ["urgent"])
    response(R_CANCEL, ["cancel", "stop"], required_words=["cancel"])
    response(R_RATE, ["rate", "rating"], required_words=["rate"])
    response(R_SCORE, ["score"], required_words=["score"])
    response(R_ORDER, ["would", "like","order"], required_words=["order"])
    response(R_BUY, ["would", "like","buy"], required_words=["buy"])
    response(R_PURCHASE, ["would", "like","purchase"], required_words=["purchase"])
    response(R_NAME, ["my","name","what"], required_words=["name"])
    response(R_RESERVE, ['I', 'would', 'like', ' to', 'reserve', 'strawberries', 'pick', 'picking'], required_words=['reserve'])
    response(R_RESERVATION, ['I', 'would', 'like', ' to', 'reservation', 'strawberries', 'pick', 'picking'], required_words=['reservation'])
    response(R_REVIEW, ['I', 'would', 'like', ' to', 'see', 'my', 'reservation', 'order', 'time', 'review'], required_words=['see', 'reservation'])
    response(R_REVIEW2, ['I', 'would', 'like', ' to', 'when', 'my', 'reservation', 'order', 'time', 'review'], required_words=['when', 'reservation'])
    response(R_REVIEW3, ['I', 'would', 'like', ' to', 'show', 'my', 'reservation', 'order', 'time', 'review'], required_words=['show', 'reservation'])
    response(R_OPEN, ['Wha', 'time', 'are', 'you', 'open', 'when'], required_words=['open', 'time'])
    response(R_OPEN2, ['What', 'are', 'your', 'opening', 'hours', 'time'], required_words=['opening'])
    response(R_KIND, ['What', 'kind', 'are', 'your', 'strawberries', 'strawberry'], required_words= ['kind'])
    response(R_VARIETY, ['What', 'variety', 'have', 'offer', 'your', 'strawberries', 'strawberry'], required_words= ['variety'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return unknown() if highest_prob_list[best_match] < 1 else best_match

# In case we do not understand the question

def unknown():
    reports.append(user_input)
    global error_counter
    error_counter = error_counter + 1
    response = ["Could you please re-phrase that? ",
                 "...",
                "Sounds about right.",
                "What does that mean?"][
        random.randrange(4)]
    return response

# Some other functions calling

def get_response(user_input):
    split_message = re.split(r"\s+|[,;?!.-]\s*", user_input.lower())
    if not set(split_message).isdisjoint(["quit", "bye", "goodbye", "q"]):
        print("See you !")
        sys.exit()
    elif not set(split_message).isdisjoint(["much", "cost", "price"]):
        return calculateprice()
    elif not set(split_message).isdisjoint(["offer", "discount", "offers", "discounts"]):
        return discount_list()    
    else:
# Checks if we need to calculate strawberries price
        response = check_all_messages(split_message) 
        if response == "Do you want to buy?" or response == "Do you want to order?" or response == "Do you want to purchase?":
            response = calculateprice()
        elif response == "You wish to reserve an amount for picking? Very well, let me bring up the list." or response == "You wish to make a reservation for picking? Very well, let me bring up the list.":
            response = makeReservation()
        elif response == "Let's see about your reservation" or response == "Let me check your reservation" or response == "Let me check your reservation!":
            response = orderReview()
        return response
    
# Calculate strawberries price 

def calculateprice():
    kgprice = 12
    global resamount    # this needs to be global so makeReservation can use this function
    resamount = ""
    while isFloat(resamount) == False:
        resamount = input("Bot: What is the amount of kg of strawberries you want to know the price of? \nPlease enter amount (number): ")
        if isFloat(resamount) == False:
            print("Please enter a number (e.g 12.3) ")

    amount = float(resamount)
    if amount <= 5 and amount > 0:
        kgprice = 12.0
    elif amount < 0:
        print("Bot: I don't think you'll want to give us starwberries.")
        return 0
    elif amount == 0:
        print("Bot: Please don't waste my time.")
    else:
        print("Because your order is over 5kg, you are eligible for a discount.") 
        while True:
            dislist = input("Bot: Would you like to see our discount list?\nYou: ").lower()
            if dislist in positive:
                discount_list()
                break
            elif dislist in negative:
                print("Bot: Alright then")
                break
            else:
                print("Bot: Sorry I did not get that.... Can you please answer a YES or NO?\nYou:  ")
        if amount > 5 and amount <= 10:
            kgprice = 11.5
        elif amount > 10 and amount <= 15:
            kgprice = 11.0
        elif amount <= 30 and amount > 15:
            kgprice = 10.5
        elif amount <= 50 and amount > 30:
            kgprice = 10.0
        elif amount <= 100 and amount > 50:
            kgprice = 9.5
        else:
            kgprice = 9.0
    kgprice = float(kgprice)        
    price = kgprice * amount
    price = float(price)
    price = round(price, 2)
    return "The price for "+ str(amount) + " Kg is "+ str(kgprice) +" € per kilo. With total of "+ str(price) +" €."

#Reservation system

def makeReservation():
    while True:
        day_inp = input('On which day would you like to make the reservation? Please enter a date in YYYY-MM-DD format between 2021-07-01 and 2021-07-13 \n')
        try:
            day = datetime.datetime.strptime(day_inp, '%Y-%m-%d')
            day = day.strftime('%Y-%m-%d')
            break
        except ValueError as e:
            print("Invalid format")
    year, month, day = map(int, day.split('-'))
    date1 = datetime.date(year, month, day)
    day = date1.strftime('%j')
    day = int(day)
    if isFloat(day) == False:
        return unknown()
    print("Bot: Let's see about the amount and price.\n")
    acceptable_result = False
    while acceptable_result == False:
        cost = calculateprice()
        print(cost)
        answer = input("Bot: Is this acceptable, yes or no? ")
        answer = answer.lower()
        if answer in positive:
            acceptable_result = True
        elif answer in negative:
            print("Bot: Sorry to hear that, let's try again.")
        else:
            unknown()
    amount = float(resamount)
    reservation = reserve.cropamount(day, amount)
    if reservation == "Sorry, we don't have that amount of crop":
        return "Sorry, we don't have that amount of crop"
    else:
        reserve.OrderRecorder(day, amount, reservation)
        return "I have made a reservation for you on that day, on row "+ str(reservation) + ". See you there!"

# Shows last reservation
def orderReview():
    result = reserve.reservationReview()
    row = result[2]
    kg = result[1]
    result = result[0]
    result = str(result)
    result.rjust(3 + len(result), '0')
    year = "2021"
    result = datetime.datetime.strptime(year + "-" + result, "%Y-%j").strftime("%m-%d-%Y")
    print("Reservation date: " + str(result) + ", Reserved amount: " + str(kg) + " kg, reserved row: nr. " + str(row) +". See you there!")
# Showing discount list

def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def discount_list():
    print(
""" Price   for 5 kg or less the price is 12,00 €/kg
           from 5 kg - 10 kg the price is 11,50 €/kg
               10 kg - 15 kg the price is 11,00 €/kg
               15 kg - 30 kg the price is 10,50 €/kg
               30 kg - 50 kg the price is 10,00 €/kg
               50 kg - 100 kg the price is 9,50 €/kg
         over 100 kg - the price is        9,00 €/kg """)

# Send feedback in case of many errors

def send_feedback():
    global error_counter
    error_counter = 0
    print("Bot: I am sorry that I am not smart enough yet to understand you...")
    while True:
        feedback = input("Would you like to send feeback back to us?\nYou: ").lower()
        if feedback in positive:
            file = open("Reports.txt", "a")
            file.write("Report = " + repr(reports) + "\n")
            file.close
            print("We really appreciate it. We will become smarter very soon. Thank you for your feedback!\n")
            break
        elif feedback in negative:
            print("It is alright. Thank you for your honesty!\n")
            break
        else:
            print("Sorry, I did not get that... Can you please answer a yes or no? ")

# Response system
init()
while True:
    user_input = input("You: ")
    if error_counter == 4:
        reports.append(user_input)
        send_feedback()
        continue
    if len(user_input) == 0:
        print("Bot: Please write something!")
        continue
    response = get_response(user_input)
    if response and response != "":
        print("Bot: " + response)
