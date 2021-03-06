import simplejson
from numpy import genfromtxt
import csv
from CompanyData import CompanyTwitterAccount, CompanyName

json_file = open("chase_search_results.json", 'r')
jsonResponse = simplejson.load(json_file)

for user in jsonResponse:
    data = {'default_profile': user['default_profile'], 'id': user['id'],  'name': user['name'], 'screen_name': user['screen_name'] }
    print data
    print

def matchUserToCompany(company, user):
    listOfAttributesToCheck = ['screen_name', 'name']
    for attribute in listOfAttributesToCheck:
        if matchNameToCompany(company, user[attribute]):
            return True
    return False

def matchNameToCompany(company, name):
    if name.lower() == company.getExecutiveName().lower():
        return True
    elif name.lower() == company.getCompanyName().lower():
        return True
    else: # need some slightly looser definition of matching
        return False

def findAndBuildTwitterCompnayAccount(companyName, userList):
    for user in userList:
            if matchUserToCompany(companyName, user):
                return CompanyTwitterAccount(companyName, user)

csvFileName = 'test.csv'
print "Reading in CSV from " + csvFileName
with open(csvFileName, 'r') as csvfile:
    # build header info
    data = genfromtxt(csvfile, delimiter=',', dtype=None)
    headerMap = dict(zip(data[0], xrange(0,len(data[0]))))

    foundCompanies = []
    for row in data[1:]:
        # read in data about each company
        companyName = CompanyName(row, headerMap)
        print companyName

        requestList = None
        companyTwitterAccount = findAndBuildTwitterCompnayAccount(companyName, jsonResponse)
        if companyTwitterAccount:
            foundCompanies.append(companyTwitterAccount)

print
print "num companies found " + str(len(foundCompanies))
destinationCsvFileName = 'output.csv'
print "Writing results to " + destinationCsvFileName
with open(destinationCsvFileName, 'w') as fp:
    writer = csv.writer(fp, delimiter=',')
    if len(foundCompanies) > 0:
        writer.writerows([foundCompanies[0].getHeader()])
    data = [twitterAccount.asList() for twitterAccount in foundCompanies]
    writer.writerows(data)
