import psycopg2

def create_client(conn):
    cur.execute("""
    create table if not exists client(
    id_client serial primary key,
    first_name varchar(80) not null,
    last_name varchar(80) not null,
    email varchar(80) unique not null
    )
    """);


def create_phone(conn):
    cur.execute("""
    create table if not exists client_phone(    
    id serial primary key,
    id_client integer references Client(id_Client),
    phone varchar(80) unique
    )
    """);

def add_client(first_name_, last_name_, email_, phone=None):
    cur.execute("""
    insert into client(first_name, last_name, email)
    values(%s, %s, %s);
    """, (first_name_, last_name_, email_))


def add_phone(id_client, phone):
    cur.execute("""
    insert into client_phone(id_client, phone)
    values(%s, %s);
    """, (id_client, phone))




def change_client(first_name_, last_name_, email_, id_client_):
    cur.execute("""
    update client 
    set first_name = %s,
        last_name = %s,
        email = %s
    where id_client = %s;
    """, (first_name_, last_name_, email_, id_client_))

           
            
            
def delete_phone_client(id_client,phone):
    cur.execute("""
    delete from client_phone
    where id_client = %s
    """, (id_client,));

            
            
            
def delete_client(id_client):
    cur.execute("""
    delete from client
    where id_client = %s
    """, (id_client,))


def find_client(first_name, last_name, email, phone):
    cur.execute("""
    select * from client
    join client_phone on client.id_client = client_phone.id_client where first_name = %s
                                                                      or last_name = %s    
                                                                      or email = %s       
                                                                      or phone = %s                                                                  
     """, (first_name, last_name, email, phone))
    data_from_table = cur.fetchall()
    for row in data_from_table:
        print('first_name=', row[1])
        print('last_name=', row[2])
        print('email=', row[3])
        print('phone=', row[6])




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with psycopg2.connect(database="client_db", user="postgres", password="27932aliK") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                    DROP TABLE client_phone;
                    DROP TABLE client;
                    """)
            create_client(conn)
            create_phone(conn)
            add_client('Oleg', 'Baronov', 'alik2408@gmail.com')
            add_phone(1, '+79112348488')
            change_client('Slava', 'Baronov', 'baronov2408@gmail.com', 1)
            find_client(None, None, None, '+79112348488')
            delete_phone_client(1, '+79112348488')
            delete_client(1)

            conn.commit







