# main.py
from instascrape import *
import argparse
import os
import csv
import sys


def parse_args():
    parser = argparse.ArgumentParser(description='Instagram Scraper. EX: python main.py --users usernames.txt --save info.csv')
    parser.add_argument('--users', help='Scrape all the users inside the file')
    parser.add_argument('--user', help='Scrape one username only.')
    parser.add_argument('--save', help='Directory to save csv file.')
    parser.add_argument('--debug', default=False , help='Enables printing debug output. True/False Value. Default=False')
    args = parser.parse_args()
    return args

# Remove newlines used mostly for BIO
def removeNewLines(str):
    str = str.replace('\n', " ")
    return str

# Checks if savefile already exists
def checkIfSaveFileExists(saveFile):
    if(os.path.exists(saveFile)):
        user_input = input("File Already Exists, do you want to Overwrite(y) OR Append(a) to it?[y/a/n] ")
        if(user_input.lower() == 'y'):
            print("Will overwrite file.")
            os.remove(saveFile)
            initializeCSV(saveFile)
            return True
        elif(user_input.lower() == 'a'):
            print("Will append to file.")
            return True
        else:
            sys.exit("Please provide an unused filename.")
    else:
        return False

# Initializes the CSV head
def initializeCSV(saveFile):
    with open(saveFile, 'a') as fd:
        initCSV = ["Username", "Followers", "Following",
                        "is_verified", "is_business", "Posts", "BIO"]
        writer=csv.writer(fd)
        writer.writerow(initCSV)
    fd.close()

# Scrapes a single user account
def scrapeUser(user):
    full_username = "https://www.instagram.com/" + user
    user_profile = Profile(full_username)
    user_profile.scrape()
    return user_profile

# Gets the user's account data and places it into an array
def getUserData(user, user_profile):
    user_array = [user, user_profile.followers, user_profile.following, 
                    user_profile.is_verified, user_profile.is_business_account, 
                    user_profile.posts, removeNewLines(user_profile.biography)]
    return user_array

# Reads a username file, returns and array with all user list
def readUsernameFile(usernameFile, debug):
    if(os.path.exists(usernameFile)):
        username_array = []
        count = 1
        fp = open(usernameFile, 'r') 
        Lines = fp.readlines()

        if(debug):
            print("Reading usernames from file:")
        for line in Lines:
            if(debug):
                print(count, "-", line.strip())
            username_array.append(line.strip())
            count = count + 1
        fp.close()
        return username_array

    else:
        sys.exit("{} Not found, please input an existing filename.".format(usernameFile))


def listToString(user_array):
    listToStr = ' '.join([str(elem) for elem in user_array])
    return listToStr


def writeToCSV(saveFile, user_array):
    with open(saveFile, 'a') as fd:
        writer=csv.writer(fd)
        if(debug):
            listToStr = listToString(user_array)
            print(listToStr)
        writer.writerow(user_array)
    fd.close()


def printInfoHeader():
    initCSV = ["Username", "Followers", "Following",
                "is_verified", "is_business", "Posts", "BIO"]
    listToStr = listToString(initCSV)
    print(listToStr)


if __name__ == '__main__':
    args = parse_args()
    if(args.user is not None):
        username = args.user
        user_profile = scrapeUser(username)
        user_array = getUserData(username, user_profile)

        # Print the info headers (Username, followers...)
        printInfoHeader()

        # Print the Account info
        listToStr = listToString(user_array)
        print(listToStr)

    elif(args.users is not None and args.save is not None):
        debug = args.debug
        saveFile = args.save
        usernameFile = args.users

        # Read username files and store usernames inside array.
        username_array = readUsernameFile(usernameFile, debug)

        # Check if filename already exists
        fileExists = checkIfSaveFileExists(saveFile)
        
        # If file does no exist, initialize csv header
        if(not fileExists):
            initializeCSV(saveFile)

        # Iterate through all usernames
        for user in username_array:
            user_profile = scrapeUser(user)
            user_array = getUserData(user, user_profile)

            # Append to CSV file.
            writeToCSV(saveFile, user_array)

    else:
        sys.exit("""Error. Please check -h in order to know how to use the program. \n
                    Either use --user alone Or combine --users and --save""")