# Melissa Data Email Object Windows Python3 Sample

## Purpose

This is an sample of the Melissa Data Email Object using Python3

The console will ask the user for:

- Email Address

And return 

- Mail Box Name
- Domain Name
- Top-Level Domain Name
- Top-Level Domain Description
- ResultCodes

## Tested Environments

- Windows 64-bit Python 3.8.7
- Powershell 5.1
- Melissa data files for 2022-12

## Required File(s) and Programs

#### mdEmail.dll

This is the c++ code of the Melissa Data Object.

#### Data File(s)
- mdEmail.cfg
- mdEmail.db3

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

This project is compatible with Python3

#### Install the Python3
Before starting, make sure that Python3 has been correctly installed on your machine and your environment paths are configured. 
If you are unsure, you can check by opening a command prompt window and typing the following:
`python3 --version`

 ![alt text](/screenshots/python_version.PNG)

If you see the version number then you have installed Python3 and set up your environment paths correctly!


#### Set up Powershell settings

If running Powershell for the first time, you will need to run this command in the Powershell console: `Set-ExecutionPolicy RemoteSigned`.
The console will then prompt you with the following warning shown in the image below. 
 - Enter `'A'`. 
 	- If successful, the console will not output any messages. (You may need to run Powershell as administrator to enforce this setting).
	
 ![alt text](/screenshots/powershell_executionpolicy.png)

----------------------------------------

#### Download this project
```
$ git clone https://github.com/MelissaData/EmailObject-Python3.git
$ cd EmailObject-Python3
```

#### Set up Melissa Updater 

Melissa Updater is a CLI application allowing the user to update their Melissa applications/data. 

- Download Melissa Updater here: <https://releases.melissadata.net/Download/Library/WINDOWS/NET/ANY/latest/MelissaUpdater.exe>
- Create a folder within the cloned repo called `MelissaUpdater`.
- Put `MelissaUpdater.exe` in `MelissaUpdater` folder you just created.

----------------------------------------

#### Different ways to get data file(s)
1.  Using Melissa Updater
	- It will handle all of the data download/path and dll(s) for you. 
2.  If you already have the latest DQS Release (ZIP), you can find the data file(s) and dll(s) in there
	- Use the location of where you copied/installed the data and update the "$DataPath" variable in the powershell script.
	- Copy all the dll(s) mentioned above into the `MelissaDataEmailObjectWindowsPython3Sample` project folder.
	
----------------------------------------

## Run Powershell Script
Parameters:
- -email: a test email address
 	
  This is convenient when you want to get results for a specific email address in one run instead of testing multiple email addresses in interactive mode.  

- -license (optional): a license string to test the email object
- -quiet (optional): add to the command if you do not want to get any console output from the Melissa Updater

When you have modified the script to match your data location, let's run the script. There are two modes:
- Interactive 

	The script will prompt the user for an email address, then use the provided email to test Email object. For example:
	```
	$ .\MelissaDataEmailObjectWindowsPython3Sample.ps1
	```
    For quiet mode:
    ```
    $ .\MelissaDataEmailObjectWindowsPython3Sample.ps1 -quiet
    ```
- Command Line 

	You can pass an email in ```-email``` parameter and a license string in ```-license``` parameter to test Email object. For example:
	```
    $ .\MelissaDataEmailObjectWindowsPython3Sample.ps1 -email "info@melissa.com" 
    $ .\MelissaDataEmailObjectWindowsPython3Sample.ps1 -email "info@melissa.com" -license "<your_license_string>"
    ```
	For quiet mode:
    ```
    $ .\MelissaDataEmailObjectWindowsPython3Sample.ps1 -email "info@melissa.com" -quiet
    $ .\MelissaDataEmailObjectWindowsPython3Sample.ps1 -email "info@melissa.com" -license "<your_license_string>" -quiet
    ```
This is the expected output from a successful setup for interactive mode:

![alt text](/screenshots/output.png)

    
## Troubleshooting

Troubleshooting for errors found while running your sample program.

### Errors:

| Error      | Description |
| ----------- | ----------- |
| ErrorRequiredFileNotFound      | Program is missing a required file. Please check your Data folder and refer to the list of required files above. If you are unable to obtain all required files through the Melissa Updater, please contact technical support below. |
| ErrorDatabaseExpired   | .db file(s) are expired. Please make sure you are downloading and using the latest release version. (If using the Melissa Updater, check powershell script for '$RELEASE_VERSION = {version}'  and change the release version if you are using an out of date release).     |
| ErrorFoundOldFile   | File(s) are out of date. Please make sure you are downloading and using the latest release version. (If using the Melissa Updater, check powershell script for '$RELEASE_VERSION = {version}'  and change the release version if you are using an out of date release).    |
| ErrorLicenseExpired   | Expired license string. Please contact technical support below. |


## Contact Us

For free technical support, please call us at 800-MELISSA ext. 4
(800-635-4772 ext. 4) or email us at tech@MelissaData.com.

To purchase this product, contact Melissa Data sales department at
800-MELISSA ext. 3 (800-635-4772 ext. 3).
