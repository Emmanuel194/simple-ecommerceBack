import qrcode
from io import BytesIO
from base64 import b64encode


PIX_KEY = "emanuel_lima2011@hotmail.com"  
RECEIVER_NAME = "Loja Virtual Simples"  
CITY = "Caruaru"  

def montar_payload_pix(chave_pix, valor, descricao):

    payload = [
        "000201",  
        f"26{len('0014BR.GOV.BCB.PIX') + len(chave_pix) + 4:02d}",  
        "0014BR.GOV.BCB.PIX",
        f"01{len(chave_pix):02d}{chave_pix}",  
        "52040000",  
        "5303986",  
        f"54{len(f'{valor:.2f}'):02d}{valor:.2f}".replace(".", ""),  
        f"5802{len(CITY):02d}{CITY}",  
        f"5902{len(RECEIVER_NAME):02d}{RECEIVER_NAME}",  
        f"6007{len(descricao):02d}{descricao.upper()[:25]}",  
        "6304"  
    ]

    
    payload_str = "".join(payload)
    payload_str += calcular_crc16(payload_str)  
    return payload_str

def calcular_crc16(payload):

    polinomio = 0x1021
    crc = 0xFFFF

    for byte in bytearray(payload, "utf-8"):
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ polinomio
            else:
                crc <<= 1
        crc &= 0xFFFF

    return f"{crc:04X}"

def gerar_qr_code_pix(payload):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=4,
    )
    qr.add_data(payload)
    qr.make(fit=True)

    buffer = BytesIO()
    qr.make_image(fill_color="black", back_color="white").save(buffer)
    base64_img = b64encode(buffer.getvalue()).decode("utf-8")
    buffer.close()

    return base64_img
