import psycopg2

def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
        create table if not exists client(
        id_client serial primary key,
        first_name varchar(80) not null,
        last_name varchar(80) not null,
        email varchar(80) unique not null);
        
        
        create table if not exists client_phone(    
        id serial primary key,
        id_client integer references Client(id_Client) on delete cascade,
        phone varchar(80) unique
        )
        ;""")

def add_client(conn, first_name_, last_name_, email_,phone=None):
    with conn.cursor() as cur:
        cur.execute("""
        insert into client(first_name, last_name, email)
        values(%s, %s, %s) returning id_client;
        """, (first_name_, last_name_, email_))
        if not not phone:
            id_number = cur.fetchone()
            adding_a_number = add_phone(conn, id_number, phone)
        conn.commit()
        return "Клиент успешно добавлен"
def add_phone(conn, id_client, phone):
    with conn.cursor() as cur:
        cur.execute("""
        insert into client_phone(id_client, phone)
        values(%s, %s);
        """, (id_client, phone))




def change_client(conn, first_name, last_name, email, id_client):
    with conn.cursor() as cur:
        cur.execute("""
        select first_name, last_name, email, id_client from client
        where id_client = %s
        """, (id_client,))
        user_data = cur.fetchone()
        if not user_data:
            return "Такого пользователя не сущуствует"
        if first_name == None:
            first_name = user_data[0]
        if last_name == None:
            last_name = user_data[1]
        if email == None:
            email = user_data[2]
        cur.execute("""
        update client
        set first_name = %s, last_name = %s, email = %s
        where id_client = %s;
        """, (first_name, last_name, email, id_client)
        )
        conn.commit()
    return "Пользователь успешно изменен"
def delete_phone_client(conn, phone):
    with conn.cursor() as cur:
        cur.execute("""
        delete from client_phone
        where phone = %s;
        """, (phone,))

            
            
            
def delete_client(conn, id_client):
    with conn.cursor() as cur:
        cur.execute("""
        delete from client
        where id_client = %s;
        """, (id_client,))


def find_client(conn, first_name='%', last_name='%', email='%', phone='%'):
    with conn.cursor() as cur:
        request_data = f"""
        SELECT
            email,
            first_name,
            last_name,
            CASE
                WHEN ARRAY_AGG(phone) = '{{Null}}' THEN '{{}}'
                ELSE ARRAY_AGG(phone)
            END phones
        FROM client
        LEFT JOIN client_phone ON client.id_client = client_phone.id_client
        WHERE first_name LIKE %s or last_name LIKE %s or email LIKE %s or phone LIKE %s
        GROUP BY email, first_name, last_name;
        """
        cur.execute(
            request_data,
            (first_name, last_name, email, phone)
        )
        return print(cur.fetchall())
        
        
                                                                     
        


def drop_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE if exists client, client_phone;
       """)








# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with psycopg2.connect(database="client_db", user="postgres", password="27932aliK") as conn:
        drop_table(conn)
        create_table(conn)
        add_client(conn, 'Oleg', 'Baronov', 'alik2408@gmail.com', '+11111111111')
        add_client(conn, 'Slava', 'Baronov', 'baronov2408@gmail.com', '+22222222222')
        add_phone(conn, 1, '+79112348488')

        change_client(conn, 'Slava', None, 'bar2408@gmail.com', 1)
        find_client(conn, None, None, None, '+11111111111')
        delete_phone_client(conn, '+79112348488')
        delete_client(conn, 1)









