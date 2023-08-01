import mdEmail_pythoncode
import os
import sys
import json


class DataContainer:
    def __init__(self, email="", result_codes=[]):
        self.email = email
        self.result_codes = result_codes

class EmailObject:
    """ Set license string and set path to data files  (.dat, etc) """
    def __init__(self, license, data_path):
        self.md_email_obj = mdEmail_pythoncode.mdEmail()
        self.md_email_obj.SetLicenseString(license)
        self.data_path = data_path

        """
        If you see a different date than expected, check your license string and either download the new data files or use the Melissa Updater program to update your data files.  
        """

        self.md_email_obj.SetPathToEmailFiles(data_path)
        p_status = self.md_email_obj.InitializeDataFiles()
        

        if (p_status != mdEmail_pythoncode.ProgramStatus.ErrorNone):
            print("Failed to Initialize Object.")
            print(p_status)
            return
        
        print(f"                DataBase Date: {self.md_email_obj.GetDatabaseDate()}")
        print(f"              Expiration Date: {self.md_email_obj.GetLicenseStringExpirationDate()}")
      
        """
        This number should match with file properties of the Melissa Object binary file.
        If TEST appears with the build number, there may be a license key issue.
        """
        print(f"               Object Version: {self.md_email_obj.GetBuildNumber()}\n")
    

    def execute_object_and_result_codes(self, data):
        self.md_email_obj.SetCacheUse(1)
        self.md_email_obj.SetCorrectSyntax(True)
        self.md_email_obj.SetDatabaseLookup(True)
        self.md_email_obj.SetFuzzyLookup(True)
        self.md_email_obj.SetMXLookup(True)
        self.md_email_obj.SetStandardizeCasing(True)
        self.md_email_obj.SetWSLookup(False)

        self.md_email_obj.VerifyEmail(data.email)
        result_codes = self.md_email_obj.GetResults()

        """ 
        ResultsCodes explain any issues email object has with the object.
        List of result codes for Email object
        https://wiki.melissadata.com/?title=Result_Code_Details#Email_Object
        """

        return DataContainer(data.email, result_codes)


def parse_arguments():
    license, test_email, data_path = "", "", ""

    args = sys.argv
    index = 0
    for arg in args:
        
        if (arg == "--license") or (arg == "-l"):
            if (args[index+1] != None):
                license = args[index+1]
        if (arg == "--email") or (arg == "-p"):
            if (args[index+1] != None):
                test_email = args[index+1]
        if (arg == "--dataPath") or (arg == "-d"):
            if (args[index+1] != None):
                data_path = args[index+1]
        index += 1

    return (license, test_email, data_path)

def run_as_console(license, test_email, data_path):
    print("\n\n=========== WELCOME TO MELISSA EMAIL OBJECT WINDOWS PYTHON3 ===========\n")

    email_object = EmailObject(license, data_path)

    should_continue_running = True

    if email_object.md_email_obj.GetInitializeErrorString() != "No error.":
      should_continue_running = False
      
    while should_continue_running:
        if test_email == None or test_email == "":        
          print("\nFill in each value to see the Email Object results")
          email = str(input("Email: "))
        else:        
          email = test_email
        
        data = DataContainer(email)

        """ Print user input """
        print("\n================================ INPUTS ===============================\n")
        print(f"\t                Email: {email}")

        """ Execute Email Object """
        data_container = email_object.execute_object_and_result_codes(data)

        """ Print output """
        print("\n================================ OUTPUT ===============================\n")
        print("\n\t    Email Object Information:")

        print(f"\t                       Email: {data_container.email}")
        print(f"\t                Mailbox Name: {email_object.md_email_obj.GetMailBoxName()}")
        print(f"\t                 Domain Name: {email_object.md_email_obj.GetDomainName()}")
        print(f"\t            Top-Level Domain: {email_object.md_email_obj.GetTopLevelDomain()}")
        print(f"\tTop-Level Domain Description: {email_object.md_email_obj.GetTopLevelDomainDescription()}")
        print(f"\t                Result Codes: {data_container.result_codes}")



        rs = data_container.result_codes.split(',')
        for r in rs:
            print(f"        {r}: {email_object.md_email_obj.GetResultCodeDescription(r, mdEmail_pythoncode.ResultCdDescOpt.ResultCodeDescriptionLong)}")


        is_valid = False
        if not (test_email == None or test_email == ""):
            is_valid = True
            should_continue_running = False    
        while not is_valid:
        
            test_another_response = input(str("\nTest another email? (Y/N)\n"))
            

            if not (test_another_response == None or test_another_response == ""):         
                test_another_response = test_another_response.lower()
            if test_another_response == "y":
                is_valid = True
            
            elif test_another_response == "n":
                is_valid = True
                should_continue_running = False            
            else:
            
              print("Invalid Response, please respond 'Y' or 'N'")

    print("\n=============== THANK YOU FOR USING MELISSA PYTHON3 OBJECT ============\n")
    


"""  MAIN STARTS HERE   """

license, test_email, data_path = parse_arguments()

run_as_console(license, test_email, data_path)