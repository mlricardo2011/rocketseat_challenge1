def decodeROT13(text):
    """
    Decodifica texto cifrado com ROT13.
    Mantém caracteres não-alfabéticos inalterados.
    """
    decoded = []
    for char in text:
        if 'a' <= char <= 'z':
            # Para letras minúsculas: desloca 13 posições no alfabeto
            decoded.append(chr((ord(char) - ord('a') + 13) % 26 + ord('a')))
        elif 'A' <= char <= 'Z':
            # Para letras maiúsculas: desloca 13 posições no alfabeto
            decoded.append(chr((ord(char) - ord('A') + 13) % 26 + ord('A')))
        else:
            # Mantém caracteres especiais/numéricos
            decoded.append(char)
    return ''.join(decoded)