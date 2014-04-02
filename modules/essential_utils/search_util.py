
def find_dec_place(val):
    """Find decimal place.
    
    Arguments
        val -- float value.
    """
    val = str(val)
    try:
        p = val.index(".")
        return len(val) - (p + 1)
    except:
        return 0
