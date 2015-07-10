#!/usr/bin/python
#Importing modules
import re
import os
import sys

# This was pulled from wikipedia its the luhn checksum algorithm which tells us if the credit card is valid. 
def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10

#Calling function to return true or false if the number is a valid credit card. 
def is_luhn_valid(card_number):
    return luhn_checksum(card_number) == 0
	
#If its actually a valid number return as a num, not a string, else just return the number 1
def num(s):
    try:
        return int(s)
    except ValueError:
        return 1

# Define variables
inputFile = sys.argv[1]

#This Regexps works on the following: 
#^(?:4[0-9]{12}(?:[0-9]{3})?          # Visa
# |  5[1-5][0-9]{14}                  # MasterCard
# |  3[47][0-9]{13}                   # American Express
# |  3(?:0[0-5]|[68][0-9])[0-9]{11}   # Diners Club
# |  6(?:011|5[0-9]{2})[0-9]{12}      # Discover
# |  (?:2131|1800|35\d{3})\d{11}      # JCB
#)$

searchPattern = '(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})'
#We have a lot of false positives on certain log lines that have phone numbers
ignorePattern = '(PhoneNumber|\+61)'

tempinputFile = open(inputFile)
tempLine = tempinputFile.readline()
 
while tempLine:
  #remove spaces and dashes so we don't need to worry about them in the regexps
  cleanLine = tempLine.replace('-', '').replace(' ', '')
  #Do the regexps check for the matching credit card 
  foundContent = re.findall(searchPattern,cleanLine)
  ignoreContent = re.search(ignorePattern,cleanLine)
  
  if not ignoreContent:
    #If we have a matching reg exps
    if foundContent:
      for match in foundContent:
        #Sanitise it, ie convert a string to a number for math calcualtions, if it contains anything that makes it not a number we'll just get the number 1 back which wont pass as a valid credit card. 
        ccAsANumber = num(match)
        if is_luhn_valid(ccAsANumber):
          print("FOUND in: " + inputFile + ": " + match)
          print("Matched Line: " + tempLine)
  tempLine = tempinputFile.readline()
 
tempinputFile.close()


