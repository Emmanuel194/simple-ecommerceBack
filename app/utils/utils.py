def exibir_payload_sem_crc(payload: str):
    payload_sem_crc = payload[:-4]  
    print(f"Payload sem CRC: '{payload_sem_crc}'")
    return payload_sem_crc


def validar_crc16(payload: str) -> bool:
    polinomio = 0x1021
    resultado = 0xFFFF

    payload_sem_crc = payload[:-4]
    crc_recebido = payload[-4:]

    for byte in bytearray(payload_sem_crc.encode("utf-8")):
        resultado ^= (byte << 8)
        for _ in range(8):
            if (resultado & 0x8000) != 0:
                resultado = (resultado << 1) ^ polinomio
            else:
                resultado = resultado << 1

    crc_calculado = f"{resultado & 0xFFFF:04X}".upper()


    print(f"Payload sem CRC: {payload_sem_crc}")
    print(f"CRC Calculado: {crc_calculado}")
    print(f"CRC Recebido: {crc_recebido}")

    return crc_calculado == crc_recebido

