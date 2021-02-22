async def save_message(conn, key, value):
    '''
    Function creates new record with key and value in the table message
    until key is unique. If key exists, the value is updated.
    '''

    async with conn.execute(
        'SELECT * FROM messages WHERE key = ?', [key]
    ) as cursor:
        message = await cursor.fetchall()
    
    if message:
        await conn.execute(
            'UPDATE messages SET value = ? WHERE id = ?', 
            [value, message[0][0]] 
        )
    else:
        await conn.execute(
            "INSERT INTO messages (key, value) VALUES(?, ?)",
            [key, value]
        )

    await conn.commit()


async def get_message_value(conn, key):
    '''
    Function gets value from the table messages for given key.
    In case of not existing key function returns empty string.
    '''

    value = ''

    async with conn.execute(
        'SELECT * FROM messages WHERE key = ?', [key]
    ) as cursor:
        message = await cursor.fetchall()

    if message:
        value = message[0][2]
    print('get message value: ', value)

    return value