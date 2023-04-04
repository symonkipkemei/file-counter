from pprint import pprint
import sqlalchemy as s
import os
import refilecounter
from datetime import datetime, date


#path to desktop
path_to_desktop = "/mnt/d/New folder"
desktop_path = refilecounter.get_path(path_to_desktop)

# connecting to the database
database_password = os.environ["pw_mysql"]
database_name = "file_counter"


#get connections
engine = s.create_engine(f"mysql+pymysql://root:{database_password}@localhost/{database_name}")
connection = engine.connect()
metadata = s.MetaData()

def get_table(table_name):
    table = s.Table(table_name,metadata,autoload=True,autoload_with=engine)
    return table


#get file tables
file_type = get_table("file_type")
file = get_table("file")
desktop_session = get_table("desktop_session")
desktop_session_file = get_table("desktop_session_file")


#get file ids
    
def get_file_type_id(name_file_type:str):
    query = s.select(file_type.columns.file_type_id).where(file_type.columns.file_type_name ==name_file_type)
    result_proxy = connection.execute(query)
    result_set = result_proxy.fetchall()
    result_set = [ suffix[0] for suffix in result_set]
    
    return result_set[0]

def get_file_id():
    query = s.select(file.columns.file_id).order_by(s.desc(file.columns.file_id))
    result_proxy = connection.execute(query)
    result_set = result_proxy.fetchall()
    result_set = [ suffix[0] for suffix in result_set]
    last_item = result_set[0]

    return last_item

def get_desktop_session_id():
    query = s.select(desktop_session.columns.desktop_session_id).order_by(s.desc(desktop_session.columns.desktop_session_id))
    result_proxy = connection.execute(query)
    result_set = result_proxy.fetchall()
    result_set = [ suffix[0] for suffix in result_set]
    last_item = result_set[0]

    return last_item


 # insert data into tables
 
def insert_file_type_table():

    #get the suffixes from the desktop

    data =refilecounter.file_type_count(desktop_path)
    suffixes = data.keys()


    #query existing suffixes
    query = s.select([file_type.columns.file_type_name])
    result_proxy = connection.execute(query)
    result_set = result_proxy.fetchall()
    result_set = [ suffix[0] for suffix in result_set]
    

    #check if suffix in desktop already exists in database
    for suffix in suffixes:
        if suffix not in result_set:
            #insert the suffix to the database
            insert = s.insert(file_type).values(
                file_type_name=suffix)
            proxy = connection.execute(insert)

def insert_file_table(FILE_NAME,FILE_PATH,FILE_TYPE_ID):
        #insert values into the database
        insert = s.insert(file).values(
            file_name = FILE_NAME,
            file_path = FILE_PATH,
            file_type_id = FILE_TYPE_ID
            )
        proxy = connection.execute(insert)

def insert_desktop_session():

    #get desktop session values

    DESKTOP_SESSION_DATE = date.today()
    DESKTOP_SESSION_TIME = datetime.now().strftime("%H:%M:%S")
    DESKTOP_SESSION_PATH = path_to_desktop

    #insert values into the database

    insert = s.insert(desktop_session).values(
        desktop_session_date = DESKTOP_SESSION_DATE,
        desktop_session_time = DESKTOP_SESSION_TIME,
        desktop_session_path = DESKTOP_SESSION_PATH
        )
    proxy = connection.execute(insert)
  
def insert_desktop_session_file_table(DESKTOP_SESSION_ID,FILE_ID):
   
    #insert values into the database

    insert = s.insert(desktop_session_file).values(
        desktop_session_id = DESKTOP_SESSION_ID,
        file_id = FILE_ID
        )
    proxy = connection.execute(insert)

def main():
    # After inserting 
    #insert desktop session
    insert_desktop_session()

    #insert file type
    insert_file_type_table()

    #insert file data
    #___________________
    #abstract values from the desktop files
    data = refilecounter.get_file_data(desktop_path)
    for file in data:
        FILE_NAME = file["file_name"]
        FILE_PATH = file["file_path"]
        FILE_TYPE = file["file_type"]
        FILE_TYPE_ID = get_file_type_id(FILE_TYPE)

        insert_file_table(FILE_NAME,FILE_PATH,FILE_TYPE_ID)


        #insert desktop session file table concurrently

        FILE_ID = get_file_id()
        DESKTOP_SESSION_ID = get_desktop_session_id()

        insert_desktop_session_file_table(DESKTOP_SESSION_ID,FILE_ID)

    #after recording the files present, it's time to clean it up
    file_type = refilecounter.file_type_count(desktop_path)
    refilecounter.clean_directory(desktop_path,file_type,1)


    #display a report of ;
    # total number of files
    # on what day was the most files
    # the most common filre type to clutter desktop



if __name__ == "__main__":
    main()






    



