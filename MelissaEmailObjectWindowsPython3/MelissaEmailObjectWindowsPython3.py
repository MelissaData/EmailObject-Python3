"""
Email Object allows your websites and custom applications to update email addresses
in your database files while verifying and correcting misspelled domain names.

High-level flow of this sample:
  1. SETUP     - create an mdEmail instance, hand it the license string and the path to
                 the data files, then InitializeDataFiles() (one time).
  2. INPUT     - feed an email address in.
  3. PROCESS   - configure the lookup options, then VerifyEmail() checks and corrects
                 the address.
  4. READ      - pull the parsed pieces back out with the Get* getters
                 (GetMailBoxName, GetDomainName, GetTopLevelDomain, ...).
  5. INTERPRET - GetResults() returns comma-separated result codes describing what the
                 object did/found; each code has a human description.

The pieces in this file map onto that flow:
  - run_as_console / parse_arguments : console harness (argument parsing + the interactive loop).
  - EmailObject                      : thin wrapper around mdEmail that owns setup + the call sequence.
  - DataContainer                    : plain holder for one record's input and output.

Where mdEmail comes from:
  The mdEmail class lives in mdEmail_pythoncode.py, a generated Python wrapper over
  mdEmail.dll that the accompanying MelissaEmailObjectWindowsPython3.ps1 script
  downloads on every run.

Reference:
  Quickstart    : https://docs.melissa.com/on-premise-api/email-object/email-object-quickstart.html
  Release notes : https://releasenotes.melissa.com/on-premise-api/email-object/
  Result codes  : https://docs.melissa.com/on-premise-api/email-object/result-codes.html
"""

import mdEmail_pythoncode
import os
import sys
import json


class DataContainer:
    """Data holder for a single record: carries the input email in and the result codes out."""
    def __init__(self, email="", result_codes=[]):

        # Input: the email address to process.
        self.email = email

        # Output: comma-separated result codes from GetResults().
        self.result_codes = result_codes

class EmailObject:
    """
    Wrapper that owns a single Melissa Email Object instance and encapsulates the two
    things every Melissa object needs: one-time setup (license + data files) and the
    per-record processing sequence. Reuse one instance across many emails; do NOT
    re-initialize per email.
    """
    def __init__(self, license, data_path):
        """
        Perform the mandatory one-time setup, in this required order:
          1. SetLicenseString     - authorize the object.
          2. SetPathToEmailFiles  - tell it where the data files live.
          3. InitializeDataFiles  - load the data into memory.

        Args:
            license: The Melissa license string used to authorize the object.
            data_path: Path to the folder containing the Email Object data files.
        """
        # Set license string and set path to data files
        # The underlying Melissa Email Object instance.
        self.md_email_obj = mdEmail_pythoncode.mdEmail()
        self.md_email_obj.SetLicenseString(license)

        # Path to the Email Object data files.
        self.data_path = data_path

        # Point the object at the Email Object data files.
        self.md_email_obj.SetPathToEmailFiles(data_path)

        # Load the data files. The returned ProgramStatus reports whether initialization succeeded.
        # If you see a different date than expected, check your license string and either download the new data files
        # or use the Melissa Updater program to update your data files.
        p_status = self.md_email_obj.InitializeDataFiles()

        # If an issue occurred, please investigate the common causes.
        # Common causes: an invalid/expired license, or missing/wrong-path data files.
        if (p_status != mdEmail_pythoncode.ProgramStatus.ErrorNone):
            print("Failed to Initialize Object.")
            print(p_status)
            return

        # Diagnostic information, handy for confirming the object loaded the data you expect:

        # Build date of the data files
        print(f"                DataBase Date: {self.md_email_obj.GetDatabaseDate()}")

        # When the license stops working
        print(f"              Expiration Date: {self.md_email_obj.GetLicenseStringExpirationDate()}")

        # This number should match with the file properties of the Melissa Object binary file.
        # If TEST appears with the build number, there may be a license key issue.
        print(f"               Object Version: {self.md_email_obj.GetBuildNumber()}\n")


    def execute_object_and_result_codes(self, data):
        """
        Run the full Email Object processing sequence for one email and capture its
        result codes. This is the canonical per-record call pattern to copy into your
        own application:
          configure lookup options -> VerifyEmail -> GetResults

        Args:
            data: The record to process; its email is read as input.

        Returns:
            A DataContainer carrying the same input plus this run's result codes.
        """
        # These are the configurable pieces of the Email Object - they control which checks
        # VerifyEmail performs (syntax correction, database & MX lookups, fuzzy matching, ...).
        self.md_email_obj.SetCacheUse(1)
        self.md_email_obj.SetCorrectSyntax(True)
        self.md_email_obj.SetDatabaseLookup(True)
        self.md_email_obj.SetFuzzyLookup(True)
        self.md_email_obj.SetMXLookup(True)
        self.md_email_obj.SetStandardizeCasing(True)
        self.md_email_obj.SetWSLookup(False)

        # Validate and correct the email per the options above
        self.md_email_obj.VerifyEmail(data.email)

        # Collect the result codes for this run
        # ResultsCodes explain any issues Email Object has with the object.
        # List of result codes for Email Object
        # https://docs.melissa.com/on-premise-api/email-object/result-codes.html
        result_codes = self.md_email_obj.GetResults()

        return DataContainer(data.email, result_codes)


def parse_arguments():
    """
    Read the supported command-line options and return them as a (license, test_email,
    data_path) tuple.

    Recognized flags (each followed by its value, e.g. "--email name@example.com"):
      --license / -l   : the Melissa license string
      --email / -p     : an email address to test in one-shot mode
      --dataPath / -d  : path to the Email Object data files

    Returns:
        A (license, test_email, data_path) tuple, each entry empty when its flag
        was not supplied.
    """
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
    """
    Set up the Email Object once, then drive the input -> process -> output cycle.

    In interactive mode (no --email) it loops, asking for a new email each pass until the
    user answers "N". In one-shot mode (--email supplied) it runs a single pass and exits.

    Args:
        license: The Melissa license string used to initialize the object.
        test_email: An email address to process in one-shot mode; if empty, the program
            prompts interactively.
        data_path: Path to the Email Object data files.
    """
    print("\n\n=========== WELCOME TO MELISSA EMAIL OBJECT WINDOWS PYTHON3 ===========\n")

    # Construct the wrapper. This is where the object is licensed, pointed at the data
    # files, and initialized (see the EmailObject constructor above).
    email_object = EmailObject(license, data_path)

    should_continue_running = True

    # Gate the program on a successful initialization. If the data files could not be
    # loaded (bad/expired license, missing or wrong-path data files, ...),
    # GetInitializeErrorString() returns the reason instead of "No error." and we skip
    # the processing loop entirely.
    if email_object.md_email_obj.GetInitializeErrorString() != "No error.":
      should_continue_running = False

    while should_continue_running:
        if test_email == None or test_email == "":
          # Interactive mode: prompt the user for an email address.
          print("\nFill in each value to see the Email Object results")
          email = str(input("Email: "))
        else:
          # One-shot mode: use the email passed on the command line.
          email = test_email

        # Holder for this pass's input and result codes.
        data = DataContainer(email)

        # Print user input
        print("\n================================ INPUTS ===============================\n")
        print(f"\t                Email: {email}")

        # Execute Email Object
        # Runs the configure + verify sequence and returns the result codes.
        data_container = email_object.execute_object_and_result_codes(data)

        # Print output
        # Each Get* getter below returns one component the object produced for the most
        # recently processed email. These read directly from the mdEmail instance, which
        # still holds the results from the Execute call above.
        print("\n================================ OUTPUT ===============================\n")
        print("\n\t    Email Object Information:")

        print(f"\t                       Email: {data_container.email}")
        print(f"\t                Mailbox Name: {email_object.md_email_obj.GetMailBoxName()}")
        print(f"\t                 Domain Name: {email_object.md_email_obj.GetDomainName()}")
        print(f"\t            Top-Level Domain: {email_object.md_email_obj.GetTopLevelDomain()}")
        print(f"\tTop-Level Domain Description: {email_object.md_email_obj.GetTopLevelDomainDescription()}")
        print(f"\t                Result Codes: {data_container.result_codes}")

        # Result codes come back as a single comma-separated string (e.g. "ES01,ES21").
        # Split it and ask the object for a readable description of each code.
        # ResultCodeDescriptionLong requests the long-form text; a short form is also
        # available via ResultCodeDescriptionShort
        rs = data_container.result_codes.split(',')
        for r in rs:
            print(f"        {r}: {email_object.md_email_obj.GetResultCodeDescription(r, mdEmail_pythoncode.ResultCdDescOpt.ResultCodeDescriptionLong)}")


        is_valid = False

        # In one-shot mode there is nothing more to do after a single pass: mark the
        # input handled and stop the outer loop.
        if not (test_email == None or test_email == ""):
            is_valid = True
            should_continue_running = False
        # Interactive mode: ask whether to process another email. Keep prompting until we
        # get a valid Y/N. "N" ends the program; "Y" falls through to another pass.
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



# ---------------------------- MAIN STARTS HERE ----------------------------

# Read the optional command-line arguments, then hand control to run_as_console, which
# performs the actual Email Object setup and processing.
license, test_email, data_path = parse_arguments()

run_as_console(license, test_email, data_path)