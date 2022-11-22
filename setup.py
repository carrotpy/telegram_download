#create the db
#install the requirement.txt file
#make the download path for each channel
#confirm if all the requirements are fullfilled if not dont run the code


import subprocess as sp




def main():
    #run setup checks one by one if its precedder is succesfullly executed
    #else stop there and put false in yaml "SETUP_STATUS"
    try:
        sp.check_call('pip3 install  -r requirements.txt', shell=True,close_fds=True)
    except Exception as e:
        print(e)
    # sp.(args)
    

    from  sqlalchemy import create_engine
    engine=create_engine("postgresql://postgres:Carrotpy123@localhost/postgres")
    try:

        engine.execute('CREATE SCHEMA telegram_loger AUTHORIZATION postgres;')
        engine.execute('''CREATE TABLE telegram_loger.download_audict (
        file_nm varchar NOT NULL,
        channel_id varchar NOT NULL,
        message_id int8 NOT NULL,
        "date" date NULL,
        status varchar NULL,
        channel_nm varchar NULL,
        CONSTRAINT download_audict_pkey PRIMARY KEY (channel_id, message_id)
    );''')
    except Exception as e:
        print(e)
    finally:
        engine.dispose()
    
        
    pass



if __name__ =='__main__':
    main()