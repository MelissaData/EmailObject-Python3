/*
* Melissa Data Email Object for Windows/Linux/Solaris
* Copyright 1999-2006 Melissa Data Corporation.
*
* Public interface
*
* PRELIMINARY VERSION SUBJECT TO CHANGES
*/
#ifndef MDEMAIL_H
#define MDEMAIL_H

#ifndef MDAPI
#if defined(_WIN32) || defined(_WIN64)
#define MDAPI __declspec(dllimport)
#else
#define MDAPI
#endif
#endif

/*
* C++ version of interface
*/
#if defined(__cplusplus) && !defined(MDCFORCE)

//
// Email Interface
//
class MDAPI mdEmail
{
protected:
	struct mdEmail_ *I;
private:	/* disable implicit constructor and assignment */
	mdEmail(mdEmail &x);
	mdEmail& operator=(mdEmail &x);
public:
#undef MDENUMS_H
#include "mdEnums.h"
	mdEmail();
	~mdEmail();

	/* Setup methods */
	bool        SetLicenseString(const char* License);
	void		SetPathToEmailFiles(const char* emailDataFiles);
	enum ProgramStatus InitializeDataFiles();
	const char* GetInitializeErrorString();
	const char* GetBuildNumber();
	const char* GetDatabaseDate();
	const char* GetDatabaseExpirationDate();
	const char* GetLicenseStringExpirationDate();

	/* Processing methods */
	bool		VerifyEmail(const char* email);

	/* Option methods */
	void SetCorrectSyntax(bool);
	void SetUpdateDomain(bool);
	void SetDatabaseLookup(bool);
	void SetFuzzyLookup(bool);
	void SetWSLookup(bool);
	void SetWSMailboxLookup(enum MailboxLookupMode mailboxLookupmode );
	void SetMXLookup(bool);
	void SetStandardizeCasing(bool);

	/* Errors and status */
	const char* GetStatusCode();
	const char* GetErrorCode();
	const char* GetErrorString();
	const unsigned int GetChangeCode();
	const char* GetResults();
	const char* GetResultCodeDescription(const char* resultCode, enum ResultCdDescOpt opt=ResultCodeDescriptionLong);

	/* Output data */
	const char* GetMailBoxName();
	const char* GetDomainName();
	const char* GetTopLevelDomain();
	const char* GetTopLevelDomainDescription();
	const char* GetEmailAddress();
	
	void SetReserved(const char *Property, const char *Value_);
	const char* GetReserved(const char *Property_);

	void SetCachePath(const char* cachePath);
	void SetCacheUse(int cacheUse);
};

#else

/*
* C version of interface
*/
#include "mdEnums.h"

typedef struct mdEmail_ *mdEmail;
MDAPI mdEmail         mdEmailCreate(void);
MDAPI void            mdEmailDestroy(mdEmail);
MDAPI void            mdEmailPlsCompat(int n_mode);


/* Setup methods */
MDAPI int					mdEmailSetLicenseString(mdEmail, const char* License);
MDAPI void					mdEmailSetPathToEmailFiles(mdEmail, const char*);
MDAPI enum mdProgramStatus	mdEmailInitializeDataFiles(mdEmail);
MDAPI const char*			mdEmailGetInitializeErrorString(mdEmail);
MDAPI const char*			mdEmailGetBuildNumber(mdEmail);
MDAPI const char*			mdEmailGetDatabaseDate(mdEmail);
MDAPI const char*			mdEmailGetDatabaseExpirationDate(mdEmail);
MDAPI const char*			mdEmailGetLicenseStringExpirationDate(mdEmail);

/* Processing methods */
MDAPI int					mdEmailVerifyEmail(mdEmail, const char* email);

/* Option methods */ 
MDAPI void					mdEmailSetCorrectSyntax(mdEmail, int);
MDAPI void					mdEmailSetUpdateDomain(mdEmail, int);
MDAPI void					mdEmailSetDatabaseLookup(mdEmail, int);
MDAPI void          mdEmailSetFuzzyLookup(mdEmail, int);
MDAPI void          mdEmailSetWSLookup(mdEmail, int);
MDAPI void          mdEmailSetWSMailboxLookup(mdEmail, enum mdMailboxLookupMode mailboxLookupMode);
MDAPI void					mdEmailSetMXLookup(mdEmail, int);
MDAPI void					mdEmailSetStandardizeCasing(mdEmail, int);

/* Errors and status */
MDAPI const char*			mdEmailGetStatusCode(mdEmail);
MDAPI const char*			mdEmailGetErrorCode(mdEmail);
MDAPI const char*			mdEmailGetErrorString(mdEmail);
MDAPI const unsigned int	mdEmailGetChangeCode(mdEmail);
MDAPI const char*			mdEmailGetResults(mdEmail);
MDAPI const char*			mdEmailGetResultCodeDescription(mdEmail, const char* resultCode, enum mdResultCdDescOpt opt);

/* Output data */
MDAPI const char*			mdEmailGetMailBoxName(mdEmail);	
MDAPI const char*			mdEmailGetDomainName(mdEmail);
MDAPI const char*			mdEmailGetTopLevelDomain(mdEmail);
MDAPI const char*			mdEmailGetTopLevelDomainDescription(mdEmail);
MDAPI const char*			mdEmailGetEmailAddress(mdEmail);	

MDAPI void					mdEmailSetReserved(mdEmail, const char *Property_, const char *Value_);
MDAPI const char*			mdEmailGetReserved(mdEmail I, const char* Property_);

MDAPI	void mdEmailSetCachePath(mdEmail, const char* cachePath);
MDAPI void mdEmailSetCacheUse(mdEmail, int cacheUse);

#endif /* __cplusplus && (!MDCFORCE) */

#endif /* MDEMAIL_H */

