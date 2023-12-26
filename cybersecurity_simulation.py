import time

def simulate_phishing_scenario():
    print("You receive an email from your bank asking you to reset your password.")
    time.sleep(1)
    print("What do you want to do?")
    time.sleep(1)
    
    user_choice = input("1. Click on the link in the email\n2. Ignore the email\n3. Report the email as phishing\nYour choice (enter the corresponding number): ")
    time.sleep(0.3)

    if user_choice == "1":
        print("\nYou clicked on the link and entered your credentials. Unfortunately, it was a phishing attempt.")
        time.sleep(0.5)
        print("Result: You fell victim to a phishing attack. Please be cautious and report such incidents.")
    elif user_choice == "2":
        print("\nYou ignored the email. Good decision! Always be cautious with unsolicited emails.")
        
        print("Result: You successfully avoided a potential phishing attack.")
    elif user_choice == "3":
        print("\nYou reported the email as phishing. Excellent! Reporting suspicious emails helps protect others.")
        time.sleep(0.5)
        print("Result: You took the right action to prevent a potential phishing attack.")
    else:
        print("\nInvalid choice. Please enter a valid number.")
        simulate_phishing_scenario()

def simulate_malware_scenario():
    print("You receive a pop-up message claiming your computer is infected. It prompts you to download a file to fix the issue.")
    time.sleep(1)
    print("What do you want to do?")
    time.sleep(1)
    
    user_choice = input("1. Download and run the file\n2. Close the pop-up and run a malware scan\n3. Ignore the message\nYour choice (enter the corresponding number): ")
    time.sleep(0.3)

    if user_choice == "1":
        print("\nYou downloaded and ran the file. Unfortunately, it was malware.")
        time.sleep(0.5)
        print("Result: Your computer is now infected. Always be cautious about unexpected downloads.")
    elif user_choice == "2":
        print("\nYou closed the pop-up and ran a malware scan. Good decision!")
        time.sleep(0.5)
        print("Result: You successfully avoided a malware infection.")
    elif user_choice == "3":
        print("\nYou ignored the message. Wise choice! Don't trust unsolicited pop-ups.")
        time.sleep(0.5)
        print("Result: You successfully avoided a potential malware infection.")
    else:
        print("\nInvalid choice. Please enter a valid number.")
        simulate_malware_scenario()

def simulate_password_scenario():
    print("You are required to setup a password for your account. This account is used in logging into your work office computer. It therefore requires a strong password")
    time.sleep(1)
    print("What measures will you implement to ensure it remains secure?")

    user_choice = input("1. Use personal information as your password e.g your name and date of birth\n2. Using the same password in all accounts you use to avoid forgetting\n3. Use a passsword of 10 characters and above, using alphabets, numbers and symbols.\n Your choice (enter the corresponding number): ")
    time.sleep(0.3)

    if user_choice == "1":
        print("\nYou used personal information as your password. Unfortunately it's not secure. It can be easily guessed. ")
        time.sleep(0.5)
        print("Result: You are at risk of your password to leak. Always use a strong password that is known to you omly.")
    elif user_choice == "2":
        print("\nYou used similar passwords for different accouts. It is not a secure practice if one account is compromised then others are at risk")   
        time.sleep(0.5)
        print("Result: you are at risk if one of the password to the accounts is discovered. Avoid using similar passwords for different accounts")
    elif user_choice == "3":
        print("\n You  used a minimum of 10 characters. Great choice!")
        time.sleep(0.5)
        print("Result: You have chosen a strong password. ") 
    else:
        print("\nInvalid choice. Please enter a valid number.")
        simulate_password_scenario()      

if __name__ == "__main__":
    print("Welcome to the Security Scenario Simulation!")
    time.sleep(1)
    
    print("\nScenario 1: Phishing Simulation")
    simulate_phishing_scenario()

    print("\nScenario 2: Malware Simulation")
    simulate_malware_scenario()

    print("\nScenario 3: Password Simulation")
    simulate_password_scenario()