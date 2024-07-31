if not __name__ == '__main__':
    from django.conf import settings

    # Chave de criptografia
    encrypt_dict = settings.ENCRYPT_DICT
    '''
    ENCRYPT_DICT = {
        '0': 'aD3$j',
        '1': 'B&5fh',
        '2': 'Cj2!t',
        '3': 'D4s@X',
        '4': 'Ejs*X',
        '5': 'Fj#s5',
        '6': 'Gjs$X',
        '7': 'Hj!sX',
        '8': 'Ijs^X',
        '9': 'Jj^sX',
    }
    '''

    # Função para criptografar uma string
    def encrypt(data: str) -> str:
        '''
        Criptografa uma string.

        Parâmetros:
            - data: A string a ser criptografada.

        Retorna:
            - A string criptografada.
        '''
        encrypted_data = ''
        for char in data:
            encrypted_data += encrypt_dict[char]
        return encrypted_data

    # Função para descriptografar uma string
    def decrypt(data: str) -> str:
        '''
        Descriptografa uma string.

        Parâmetros:
            - data: A string a ser descriptografada.

        Retorna:
            - A string descriptografada.
        '''
        decrypted_data = ''
        key_list = list(encrypt_dict.keys())
        value_list = list(encrypt_dict.values())
        for i in range(0, len(data), 5):
            decrypted_data += key_list[value_list.index(data[i:i + 5])]
        return decrypted_data

else:
    encrypt_dict = {
                    '0': 'aD3$j',
                    '1': 'B&5fh',
                    '2': 'Cj2!t',
                    '3': 'D4s@X',
                    '4': 'Ejs*X',
                    '5': 'Fj#s5',
                    '6': 'Gjs$X',
                    '7': 'Hj!sX',
                    '8': 'Ijs^X',
                    '9': 'Jj^sX',
                }

    # Função para criptografar uma string
    def encrypt(data: str) -> str:
        '''
        Criptografa uma string.

        Parâmetros:
            - data: A string a ser criptografada.

        Retorna:
            - A string criptografada.
        '''
        encrypted_data = ''
        for char in data:
            encrypted_data += encrypt_dict[char]
            print(encrypted_data)
        return encrypted_data

    # Função para descriptografar uma string
    def decrypt(data: str) -> str:
        '''
        Descriptografa uma string.

        Parâmetros:
            - data: A string a ser descriptografada.

        Retorna:
            - A string descriptografada.
        '''
        decrypted_data = ''
        key_list = list(encrypt_dict.keys())
        value_list = list(encrypt_dict.values())
        for i in range(0, len(data), 5):
            print(data[i:i + 5])
            decrypted_data += key_list[value_list.index(data[i:i + 5])]
        return decrypted_data

    # print(encrypt('79999068342'))
    print(decrypt('Hj!sXJj^sXJj^sXJj^sXJj^sXaD3$jGjs$XIjs^XD4s@XEjs*XCj2!t'))
