#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# joeprado, 2020-Mar-09, Began modifying Script
# joeprado, 2020-Mar-10, Added docstrings.
# joeprado, 2020-Mar-10, Finished script modifications
#------------------------------------------#

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    @staticmethod
    def add_cd(cdID, title, artist, row, table):
        """Adding user data for new CD to a table.
        
        Takes user input fed into the function via parameters,formats it as a set key:value pairs in a
        dictionary, and then appends that dictionary as row nested inside a list. 
        
        Args: 
            cdID (string): ID number of CD as entered by the user
            title (string): Title of CD as entered by the user
            artist (string): Artist name for the CD as entered by the user
            row (dictionary): empty data row in the form of dictionary 
            table (list of dict): list of dictionaries that holds our data in volatile memory 
            
        Returns: 
            None.
        """
        intID = int(cdID)
        row = {'ID': intID, 'Title': title, 'Artist': artist}
        table.append(row)
    
    @staticmethod
    def delete_cd(selectID, table):
        """Delete a CD selected by user based on ID.
        
        Takes user input for the ID number of a CD the user would like to delete, searches for the row (dictionary) the ID is in,
        then deletes that row (dictionary) in the table (list).
        
        Args:
            selectID (integer): user selection for CD ID number the user would like to delete.
            table (list of dict): list of dictionaries that holds our data in volatile memory 
            
        Returns:
            None.
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == selectID:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
    
       
class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries.

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        objFile = open(file_name, 'r')
        for line in objFile:
            data = line.strip().split(',')
            dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
            table.append(dicRow)
        objFile.close()

    @staticmethod
    def write_file(file_name, table):
        """Function to save the contents of CD Inventory in volatile memory into a text file.
        
        Takes the list of dictionaries identified by table and saves it into text file 
        identified by file_name.
        
        
         Args:
            file_name (string): name of file used to save data to. 
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            
        Returns:
            None
        """
        objFile = open(file_name, 'w')
        for row in table:
            lstValues = list(row.values())
            lstValues[0] = str(lstValues[0])
            objFile.write(','.join(lstValues) + '\n')
        objFile.close()


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.
        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def input_new_cd():
        """Function that collects user input for a new CD to be added to inventory.
        
        Args: 
            None.
            
        Returns:
            cdID (string): string representing ID number user entered for CD 
            title (string): string representing CD title entered by user
            artist (string): string representing artist name entered by user
        """
        cdID = input('Enter ID: ').strip()
        title = input('What is the CD\'s title? ').strip()
        artist = input('What is the Artist\'s name? ').strip()
        return cdID, title, artist


# 1. When program starts, calls function that reads in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl) #Calls function that loads text file containing CD inventory into runtime. 
            IO.show_inventory(lstTbl) #Calls function that displays inventory to user
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl) #Calls function that displays inventory to user
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Calls function that asks user for new ID, CD Title and Artist
        strID, strTitle, strArtist = IO.input_new_cd()  
        # 3.3.2 Calls the function that adds item to the table
        DataProcessor.add_cd(strID, strTitle, strArtist, dicRow, lstTbl)
        #Calls function that displays inventory with added CD
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl) # Calls function that displays current inventory
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 Calls function that displays inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        intIDDel = int(input('Which ID would you like to delete? ').strip())
        # 3.5.2 Calls function that searches thru table and deletes CD
        DataProcessor.delete_cd(intIDDel, lstTbl)
        IO.show_inventory(lstTbl) #Calls function that displays inventory to user
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Calls function that displays current inventory. 
        IO.show_inventory(lstTbl) 
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower() #asks user for confirmation to save
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 Calls function that saves data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




