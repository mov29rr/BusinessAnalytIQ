<<<<<<< Updated upstream
from pymongo import MongoClient

#Database client url
uri = "mongodb+srv://rwomack3:nQ1MHyOiXxcQq9LT@test.0tujk.mongodb.net/?retryWrites=true&w=majority&appName=Test"
client = MongoClient(uri)

try:
    #Database being searched
    database = client.get_database("BusinessAnalytiq")

    #Collection(s)/table(s) being searched
    assetsCollection = database.get_collection("Assets")
    usersCollection = database.get_collection("Users")

    assetEntries = ""
    userEntries = ""

    #Fetching data
    query = assetsCollection.find({ "asset" : "Asset Name"}, {"_id" : 0, "expectedReturn": 1, "risk": 1})
    for assetEntries in query:
        print(assetEntries)

    #Making a new user
    #User data
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    email = input("Enter your email address: ")
    
    #Create document with user data
    usersCollection.insert_one({"username" : username, "password" : password, "email" : email})

    #Checking login details
    loginSuccess = False

    while loginSuccess == False:
        #Login Details to check
        usernameToCheck = input("Enter your username: ")
        passwordToCheck = input("Enter your password: ")

        #Search for users with inputted username, password
        account = usersCollection.find({ "username" : usernameToCheck, "password" : passwordToCheck})

        #Place users found into userEntries
        for userEntries in account:
            break

        #If any users have been found, login is success full
        if userEntries:
            print("Login Successful") 
            loginSuccess = True 
        else:
            print("Invalid Login")

    
    client.close()

except Exception as e:
    raise Exception("Error: Unable to find document.", e)
=======
from pymongo import MongoClient

#Database client url
uri = "mongodb+srv://rwomack3:nQ1MHyOiXxcQq9LT@test.0tujk.mongodb.net/?retryWrites=true&w=majority&appName=Test"
client = MongoClient(uri)

try:
    #Database being searched
    database = client.get_database("BusinessAnalytiq")

    #Collection(s)/table(s) being searched
    assetsCollection = database.get_collection("Assets")
    usersCollection = database.get_collection("Users")

    assetEntries = ""
    userEntries = ""

    #Fetching data
    query = assetsCollection.find({ "asset" : "Asset Name"}, {"_id" : 0, "expectedReturn": 1, "risk": 1})
    for assetEntries in query:
        print(assetEntries)

    #Making a new user
    #User data
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    email = input("Enter your email address: ")
    
    #Create document with user data
    usersCollection.insert_one({"username" : username, "password" : password, "email" : email})

    #Checking login details
    loginSuccess = False

    while loginSuccess == False:
        #Login Details to check
        usernameToCheck = input("Enter your username: ")
        passwordToCheck = input("Enter your password: ")

        #Search for users with inputted username, password
        account = usersCollection.find({ "username" : usernameToCheck, "password" : passwordToCheck})

        #Place users found into userEntries
        for userEntries in account:
            break

        #If any users have been found, login is success full
        if userEntries:
            print("Login Successful") 
            loginSuccess = True 
        else:
            print("Invalid Login")

    
    client.close()

except Exception as e:
    raise Exception("Error: Unable to find document.", e)
>>>>>>> Stashed changes
