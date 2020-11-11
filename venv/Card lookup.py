from mtgsdk import Card
from mtgsdk import Set
from mtgsdk import Type
from mtgsdk import Supertype
from mtgsdk import Subtype
from mtgsdk import Changelog
import time as ti
import json

card_name = input("Enter the card you'd like to look up:")
start_time = ti.time()
print("Sent Request!")
cards = Card.where(name=card_name).all()
result = str(cards[0].__dict__)
print(result)
end_time = ti.time()
print("Request Complete! \r"+str(int(end_time-start_time))+" Seconds Elapsed")
