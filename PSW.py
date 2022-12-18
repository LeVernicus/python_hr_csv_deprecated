import datetime
import requests
import csv
import keyring

# Below is the python program for getting training data online from CSV reports generated
# and outputting them into an easy-to-ready format
# None of the code posts any data to any website with the exception of the login payload which is needed to first pull the reports.

# No entries or data are posted to any forms.
# This is meant as a read-only tool to help format
# and consolidate the info into an easy-to-ready format. 5/28/2021

#attributes of Csvline match the header columns for the CSV, which means that in the future, a programmer could perform additional operations on the attributes
class Csvline:
    def __init__(self, resource_id, transcript_record_id, last_name, first_name, user_name, resource_email, entered_date, training_start_date, transcript_date, site, occupation_1, occupation_2, department, transcript_date_range_start, transcript_date_rage_end, course_no, course_title, pretest_score, posttest_score, record_time, full_grade_time, grade, notes, due_date, due_date_sort, grade_date, grade_time_passed_only, time_spent, rated_min, reqd, type, cert_option, course_duration, cert_up, letter_grade, cert_link, enrolled, resource_password):
        self.resource_id = resource_id
        self.transcript_record_id = transcript_record_id
        self.last_name = last_name
        self.first_name = first_name
        self.user_name = user_name
        self.resource_email = resource_email
        self.entered_date = entered_date
        self.training_start_date = training_start_date
        self.transcript_date = transcript_date
        self.site = site
        self.occupation_1 = occupation_1
        self.occupation_2 = occupation_2
        self.department = department
        self.transcript_date_range_start = transcript_date_range_start
        self.transcript_date_range_end = transcript_date_rage_end
        self.course_no = course_no
        self.course_title = course_title
        self.pretest_score = pretest_score
        self.posttest_score = posttest_score
        self.record_time = record_time
        self.full_grade_time = full_grade_time
        self.grade = grade
        self.notes = notes
        self.due_date = due_date
        self.due_date_sort = due_date_sort
        self.grade_date = grade_date
        self.grade_time_passed_only = grade_time_passed_only
        self.time_spent = time_spent
        self.rated_min = rated_min
        self.reqd = reqd
        self.type = type
        self.cert_option = cert_option
        self.course_duration = course_duration
        self.cert_up = cert_up
        self.letter_grade = letter_grade
        self.cert_link = cert_link
        self.enrolled = enrolled
        self.resource_password = resource_password

def get_csv():
    todaysdate = datetime.date.today()
    #username and password payload, encrypted with keyring module
    data1 = {'username': 'username', 'password': keyring.get_password("key", "username")}
    #calculate start of fiscal year
    if todaysdate.month >= 7:
        s_year = todaysdate.year
    else:
        s_year = todaysdate.year-1
    
    s_date = '07/01/' + str(s_year)
    e_date = str(todaysdate.month) +'/'+ str(todaysdate.day) +'/'+ str(todaysdate.year)
    todays_f_date = str(todaysdate.year) +'-'+ str(todaysdate.month) +'-'+ str(todaysdate.day)
    #define URLs to get the CSV report using a definition based on todays date from datetime module
    loginpage = 'DEPRECATED_LOGIN_PAGE'
    reports_urls = [ 
    'DEPRECATED_URL'+ s_date +'&e_date='+ e_date +'URL_CONTD',
    'DEPRECATED_URL'+ s_date +'&e_date='+ e_date +'URL_CONTD',
    'DEPRECATED_URL'+ s_date +'&e_date='+ e_date +'URL_CONTD',
    ]
    with requests.Session() as s:
        #post the login payload to the loginpage URL
        response = s.post(loginpage, data1)
        if response.status_code == 200:
            my_list = []
            #Loops through the reports_URLs list in order to get the CSV reports, cuts off the CSV header, and then appends those CSV lines to a new list called my_list, returns my_list as output
            for report in reports_urls:
                response = s.get(report)
                if response.status_code == 200:
                    unicode_content = response.content.decode('utf-8')
                    csv_iterator = csv.reader(unicode_content.splitlines(), delimiter=',')
                    next(csv_iterator)
                    my_list.extend(list(csv_iterator))
                else:
                    print("Public Schoolworks web response returned an error code other than 200. The site may not be responding.")
                    raise SystemExit

            return my_list
        else:
            print("Public Schoolworks web response returned an error code other than 200. The site may not be responding.")
            raise SystemExit


#Determines amount of days passed based on user input and prints entries based on the difference of days from datetime module
def delta_days():
    todaysdate = datetime.datetime.today()
    sum_of_rows = 0
    user_get = input("Days past to check for new entries: ")
    my_list = get_csv()
    linefound = False
    num_found = 0
    #uses my_list as input and assigns those lines to attributes of a class named Csvline, where the attributes are then operated on to determine days passed, name of the nonemployee, training date, etc.
    for row in my_list:
        sum_of_rows+=1
        Currentline=Csvline(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29], row[30], row[31], row[32], row[33], row[34], row[35], row[36], row[37])
        record_time_obj = datetime.datetime.strptime(Currentline.record_time, '%m-%d-%y')
        deltadays = todaysdate - record_time_obj
        if deltadays.days < int(user_get) and (Currentline.course_title == "Acceptable Use Policy" or Currentline.course_title == "Student Privacy Rights (FERPA)" or Currentline.course_title == "Protecting Student Data"):
            print("Row {: <10}{: <10} {: <25} {: <30} {: <40} {: >8}".format(sum_of_rows, Currentline.first_name, Currentline.last_name, Currentline.occupation_1, Currentline.course_title, Currentline.record_time))
            linefound = True
            num_found += 1
    if not linefound:
        print("No entries were found within the specified number of days.")
    else:
        print("\n" + str(num_found) + " completed nonemployee training entries were found for the past " + str(user_get) + " days.")

#Gets user input and searches csv for matches in First Name OR Last Name OR Last Name + First Name
def nonemployee_find():
    sum_of_rows = 0
    user_get = input("Enter an employee name to search for (case sensitive): ")
    if user_get.isalpha():
        my_list = get_csv()
        linefound = False
        num_found = 0
        #uses my_list as input and assigns those lines to attributes of a class named Csvline, where the attributes are then operated on to determine days passed, name of the nonemployee, training date, etc.
        for row in my_list:
            sum_of_rows+=1
            Currentline=Csvline(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29], row[30], row[31], row[32], row[33], row[34], row[35], row[36], row[37])
            if (Currentline.first_name == user_get or Currentline.last_name == user_get or Currentline.first_name + " " + Currentline.last_name == user_get) and (Currentline.course_title == "Acceptable Use Policy" or Currentline.course_title == "Student Privacy Rights (FERPA)" or Currentline.course_title == "Protecting Student Data"):
                print("Row {: <10}{: <10} {: <25} {: <30} {: <40} {: >8}".format(sum_of_rows, Currentline.first_name, Currentline.last_name, Currentline.occupation_1, Currentline.course_title, Currentline.record_time))
                linefound = True
                num_found += 1
        if not linefound:
            print("No entries were found for the name provided. Try adjusting spelling, punctuation, or case.")
        else:
            print("\n" + str(num_found) + " completed nonemployee training entries were found for \"" + user_get + "\".")
    else:
        print("Name provided: \"" + user_get + "\" is not a valid search query. Please remove symbols or punctuation.")
        nonemployee_find()

#User menu function
def print_menu():
    print("Welcome to the Nonemployee Training Search Tool.\n")
    print("Select an option:")
    print("1. Search for training entries by nonemployee name")
    print("2. Search for training entries by days lapsed since entry")
    print("3. Exit")



#While loop continuously prompts user for new inputs and passes the user through the selected menu options unless they choose option 3
while True:
    print_menu()
    user_menu_get = input()
    if int(user_menu_get) == 1 or int(user_menu_get) == 2 or int(user_menu_get) == 3:
        if int(user_menu_get) == 1:
            nonemployee_find()
            print("\n")
            input("Press any key to continue...")
            print("\n")
        elif int(user_menu_get) == 2:
            delta_days()
            print("\n")
            input("Press any key to continue...")
            print("\n")
        elif int(user_menu_get) == 3:
            print("\nExiting...")
            raise SystemExit
        else:
            print("An invalid option was selected...\n \n")
    else:
        print("An invalid option was selected...\n \n")
