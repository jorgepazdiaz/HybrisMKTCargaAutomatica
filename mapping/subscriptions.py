# -*- coding: utf-8 -*-
O_SUBSCRIPTION_CONTACT_ORIGIN = 'CONTACT_ORIGIN'
O_SUBSCRIPTION_CONTACT_ID = 'CONTACT_ID'
O_SUBSCRIPTION_ID_ORIGIN = 'ID_ORIGIN'
O_SUBSCRIPTION_ID = 'ID'
O_SUBSCRIPTION_MKT_AREA_ID = 'MKT_AREA_ID'
O_SUBSCRIPTION_MKT_PERM_COMM_MEDIUM = 'MKT_PERM_COMM_MEDIUM'
O_SUBSCRIPTION_COMM_MEDIUM = 'COMM_MEDIUM'
O_SUBSCRIPTION_TIMESTAMP = 'TIMESTAMP'
O_SUBSCRIPTION_COMM_CAT_ID = 'COMM_CAT_ID'
O_SUBSCRIPTION_OPT_IN = 'OPT_IN'
O_SUBSCRIPTION_FIELDS = [O_SUBSCRIPTION_CONTACT_ORIGIN, O_SUBSCRIPTION_CONTACT_ID, O_SUBSCRIPTION_ID_ORIGIN, O_SUBSCRIPTION_ID, O_SUBSCRIPTION_MKT_AREA_ID, O_SUBSCRIPTION_MKT_PERM_COMM_MEDIUM, O_SUBSCRIPTION_COMM_MEDIUM, O_SUBSCRIPTION_TIMESTAMP, O_SUBSCRIPTION_COMM_CAT_ID, O_SUBSCRIPTION_OPT_IN]
# SUBSCRIPTIONS: File header needed to import
O_SUBSCRIPTION_FILE_HEADER =\
"""\
* User Instructions
* Enter the data for your upload directly below the header row starting at row 18.
* Do not delete the mandatory header row.
* You can define the order of the columns to meet your requirements.
* Do not enter any data in columns that have no attribute name in the header row.
* The column pair (ID_ORIGIN, ID) describes the contact facet for the permission and subscription
* The column pair (CONTACT_ORIGIN, CONTACT_ID) is needed to identify the contact. You must enter this data when the value in the ID column is shared by more than one contact. But if this value is unique, you can leave columns CONTACT_ORIGIN and CONTACT_ID empty.
* If the column TIMESTAMP is left empty, the current date and time is set by the system. If the timestamp is set to a time in the past, the permission and subscription will not be updated in the system if there is already a permission and subscription for the same facet and communication category with a newer timestamp.
* If the column COMM_CAT_ID is left empty, the system uploads the data as permission. If a value is entered in this column, the data is uploaded as subscription referring to the defined communication category.
* Ensure that there are no empty rows above your data. Delete empty rows or enter an asterisk (*) at the start so that they are ignored for the upload.
* Comment rows are allowed only above the header row. They must start with an asterisk (*).
* As row separators, you can use <CRLF> for Windows systems and <CR> for Unix systems.
* As column separators, you can use a comma, semicolon, or tab.
* However, do not use separators (comma, semicolon, tab) in any text you enter in a cell.
* You can mask values using quotation marks or apostrophes. If you mask values, you must mask them in all columns.
* Save the file as a CSV file.
* For more information, see the application help.
*
* Contact Origin;Contact ID;ID Origin;ID;Marketing Area;Outbound Communication Medium;Communication Medium;Timestamp;Communication Category ID;Opt in (Y/N)
"""
