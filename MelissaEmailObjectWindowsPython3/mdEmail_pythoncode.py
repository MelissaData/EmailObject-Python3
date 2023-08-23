from ctypes import *
from enum import Enum
import ctypes
import os
import sys

if (os.name == 'nt' and sys.version_info[:2] >= (3,8)):
  lib = ctypes.CDLL('mdEmail.dll', winmode=0)
elif (os.name == 'nt'):
  lib = ctypes.CDLL('mdEmail.dll')
else:
  lib = ctypes.CDLL('libmdEmail.so')

lib.mdEmailCreate.argtypes = []
lib.mdEmailCreate.restype = c_void_p
lib.mdEmailDestroy.argtypes = [c_void_p]
lib.mdEmailDestroy.restype = None
lib.mdEmailSetLicenseString.argtypes = [c_void_p, c_char_p]
lib.mdEmailSetLicenseString.restype = c_bool
lib.mdEmailSetPathToEmailFiles.argtypes = [c_void_p, c_char_p]
lib.mdEmailSetPathToEmailFiles.restype = None
lib.mdEmailInitializeDataFiles.argtypes = [c_void_p]
lib.mdEmailInitializeDataFiles.restype = c_int
lib.mdEmailGetInitializeErrorString.argtypes = [c_void_p]
lib.mdEmailGetInitializeErrorString.restype = c_char_p
lib.mdEmailGetBuildNumber.argtypes = [c_void_p]
lib.mdEmailGetBuildNumber.restype = c_char_p
lib.mdEmailGetDatabaseDate.argtypes = [c_void_p]
lib.mdEmailGetDatabaseDate.restype = c_char_p
lib.mdEmailGetDatabaseExpirationDate.argtypes = [c_void_p]
lib.mdEmailGetDatabaseExpirationDate.restype = c_char_p
lib.mdEmailGetLicenseStringExpirationDate.argtypes = [c_void_p]
lib.mdEmailGetLicenseStringExpirationDate.restype = c_char_p
lib.mdEmailVerifyEmail.argtypes = [c_void_p, c_char_p]
lib.mdEmailVerifyEmail.restype = c_bool
lib.mdEmailSetCorrectSyntax.argtypes = [c_void_p, c_bool]
lib.mdEmailSetCorrectSyntax.restype = None
lib.mdEmailSetUpdateDomain.argtypes = [c_void_p, c_bool]
lib.mdEmailSetUpdateDomain.restype = None
lib.mdEmailSetDatabaseLookup.argtypes = [c_void_p, c_bool]
lib.mdEmailSetDatabaseLookup.restype = None
lib.mdEmailSetFuzzyLookup.argtypes = [c_void_p, c_bool]
lib.mdEmailSetFuzzyLookup.restype = None
lib.mdEmailSetWSLookup.argtypes = [c_void_p, c_bool]
lib.mdEmailSetWSLookup.restype = None
lib.mdEmailSetWSMailboxLookup.argtypes = [c_void_p, c_int]
lib.mdEmailSetWSMailboxLookup.restype = None
lib.mdEmailSetMXLookup.argtypes = [c_void_p, c_bool]
lib.mdEmailSetMXLookup.restype = None
lib.mdEmailSetStandardizeCasing.argtypes = [c_void_p, c_bool]
lib.mdEmailSetStandardizeCasing.restype = None
lib.mdEmailGetStatusCode.argtypes = [c_void_p]
lib.mdEmailGetStatusCode.restype = c_char_p
lib.mdEmailGetErrorCode.argtypes = [c_void_p]
lib.mdEmailGetErrorCode.restype = c_char_p
lib.mdEmailGetErrorString.argtypes = [c_void_p]
lib.mdEmailGetErrorString.restype = c_char_p
lib.mdEmailGetChangeCode.argtypes = [c_void_p]
lib.mdEmailGetChangeCode.restype = c_uint
lib.mdEmailGetResults.argtypes = [c_void_p]
lib.mdEmailGetResults.restype = c_char_p
lib.mdEmailGetResultCodeDescription.argtypes = [c_void_p, c_char_p, c_int]
lib.mdEmailGetResultCodeDescription.restype = c_char_p
lib.mdEmailGetMailBoxName.argtypes = [c_void_p]
lib.mdEmailGetMailBoxName.restype = c_char_p
lib.mdEmailGetDomainName.argtypes = [c_void_p]
lib.mdEmailGetDomainName.restype = c_char_p
lib.mdEmailGetTopLevelDomain.argtypes = [c_void_p]
lib.mdEmailGetTopLevelDomain.restype = c_char_p
lib.mdEmailGetTopLevelDomainDescription.argtypes = [c_void_p]
lib.mdEmailGetTopLevelDomainDescription.restype = c_char_p
lib.mdEmailGetEmailAddress.argtypes = [c_void_p]
lib.mdEmailGetEmailAddress.restype = c_char_p
lib.mdEmailSetReserved.argtypes = [c_void_p, c_char_p, c_char_p]
lib.mdEmailSetReserved.restype = None
lib.mdEmailGetReserved.argtypes = [c_void_p, c_char_p]
lib.mdEmailGetReserved.restype = c_char_p
lib.mdEmailSetCachePath.argtypes = [c_void_p, c_char_p]
lib.mdEmailSetCachePath.restype = None
lib.mdEmailSetCacheUse.argtypes = [c_void_p, c_int]
lib.mdEmailSetCacheUse.restype = None

# mdEmail Enumerations
class ProgramStatus(Enum):
	ErrorNone = 0
	ErrorOther = 1
	ErrorOutOfMemory = 2
	ErrorRequiredFileNotFound = 3
	ErrorFoundOldFile = 4
	ErrorDatabaseExpired = 5
	ErrorLicenseExpired = 6

class AccessType(Enum):
	Local = 0
	Remote = 1

class DiacriticsMode(Enum):
	Auto = 0
	On = 1
	Off = 2

class StandardizeMode(Enum):
	ShortFormat = 0
	LongFormat = 1
	AutoFormat = 2

class SuiteParseMode(Enum):
	ParseSuite = 0
	CombineSuite = 1

class AliasPreserveMode(Enum):
	ConvertAlias = 0
	PreserveAlias = 1

class AutoCompletionMode(Enum):
	AutoCompleteSingleSuite = 0
	AutoCompleteRangedSuite = 1
	AutoCompletePlaceHolderSuite = 2
	AutoCompleteNoSuite = 3

class ResultCdDescOpt(Enum):
	ResultCodeDescriptionLong = 0
	ResultCodeDescriptionShort = 1

class MailboxLookupMode(Enum):
	MailboxNone = 0
	MailboxExpress = 1
	MailboxPremium = 2

class mdEmail(object):
	def __init__(self):
		self.I = lib.mdEmailCreate()

	def __del__(self):
		lib.mdEmailDestroy(self.I)

	def SetLicenseString(self, License):
		return lib.mdEmailSetLicenseString(self.I, License.encode('utf-8'))

	def SetPathToEmailFiles(self, emailDataFiles):
		lib.mdEmailSetPathToEmailFiles(self.I, emailDataFiles.encode('utf-8'))

	def InitializeDataFiles(self):
		return ProgramStatus(lib.mdEmailInitializeDataFiles(self.I))

	def GetInitializeErrorString(self):
		return lib.mdEmailGetInitializeErrorString(self.I).decode('utf-8')

	def GetBuildNumber(self):
		return lib.mdEmailGetBuildNumber(self.I).decode('utf-8')

	def GetDatabaseDate(self):
		return lib.mdEmailGetDatabaseDate(self.I).decode('utf-8')

	def GetDatabaseExpirationDate(self):
		return lib.mdEmailGetDatabaseExpirationDate(self.I).decode('utf-8')

	def GetLicenseStringExpirationDate(self):
		return lib.mdEmailGetLicenseStringExpirationDate(self.I).decode('utf-8')

	def VerifyEmail(self, email):
		return lib.mdEmailVerifyEmail(self.I, email.encode('utf-8'))

	def SetCorrectSyntax(self, p1):
		lib.mdEmailSetCorrectSyntax(self.I, p1)

	def SetUpdateDomain(self, p1):
		lib.mdEmailSetUpdateDomain(self.I, p1)

	def SetDatabaseLookup(self, p1):
		lib.mdEmailSetDatabaseLookup(self.I, p1)

	def SetFuzzyLookup(self, p1):
		lib.mdEmailSetFuzzyLookup(self.I, p1)

	def SetWSLookup(self, p1):
		lib.mdEmailSetWSLookup(self.I, p1)

	def SetWSMailboxLookup(self, mailboxLookupmode):
		lib.mdEmailSetWSMailboxLookup(self.I, MailboxLookupMode(mailboxLookupmode).value)

	def SetMXLookup(self, p1):
		lib.mdEmailSetMXLookup(self.I, p1)

	def SetStandardizeCasing(self, p1):
		lib.mdEmailSetStandardizeCasing(self.I, p1)

	def GetStatusCode(self):
		return lib.mdEmailGetStatusCode(self.I).decode('utf-8')

	def GetErrorCode(self):
		return lib.mdEmailGetErrorCode(self.I).decode('utf-8')

	def GetErrorString(self):
		return lib.mdEmailGetErrorString(self.I).decode('utf-8')

	def GetChangeCode(self):
		return lib.mdEmailGetChangeCode(self.I)

	def GetResults(self):
		return lib.mdEmailGetResults(self.I).decode('utf-8')

	def GetResultCodeDescription(self, resultCode, opt=0):
		return lib.mdEmailGetResultCodeDescription(self.I, resultCode.encode('utf-8'), ResultCdDescOpt(opt).value).decode('utf-8')

	def GetMailBoxName(self):
		return lib.mdEmailGetMailBoxName(self.I).decode('utf-8')

	def GetDomainName(self):
		return lib.mdEmailGetDomainName(self.I).decode('utf-8')

	def GetTopLevelDomain(self):
		return lib.mdEmailGetTopLevelDomain(self.I).decode('utf-8')

	def GetTopLevelDomainDescription(self):
		return lib.mdEmailGetTopLevelDomainDescription(self.I).decode('utf-8')

	def GetEmailAddress(self):
		return lib.mdEmailGetEmailAddress(self.I).decode('utf-8')

	def SetReserved(self, Property, Value_):
		lib.mdEmailSetReserved(self.I, Property.encode('utf-8'), Value_.encode('utf-8'))

	def GetReserved(self, Property_):
		return lib.mdEmailGetReserved(self.I, Property_.encode('utf-8')).decode('utf-8')

	def SetCachePath(self, cachePath):
		lib.mdEmailSetCachePath(self.I, cachePath.encode('utf-8'))

	def SetCacheUse(self, cacheUse):
		lib.mdEmailSetCacheUse(self.I, cacheUse)
