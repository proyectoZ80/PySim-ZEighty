class Z80(object):
    # Registros son declarados como cadenas en hexadecimal
    B = "00"
    C = "00"
    D = "00"
    E = "00"
    H = "00"
    L = "00"
    A = "00"
    F = "00"
    SP = "00"
    IX = "00"
    IY = "00"

    """ 
        Para el cambio de banderas pueden realizar lo siguiente
        Z80.F = Z80.F[:indice] + '1' + Z80.F[inidice:]
        cambiando el '1' por el caso que vayan a realizar.
        Antes deben de hacer el cambio del registro F de hexadecimal a binario
        y usar zfill para tener 8 bits al convertir
    """