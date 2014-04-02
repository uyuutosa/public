
def prmconv(paralst, tmplst):
    """
    'prmconv' convert a value as decline in 'paralst' 
    to new value baced on the config data as decline in 'tmplst'.
    """
    from numpy import array, where
    if type(paralst) != list:
        paralst = [paralst]
    origlst, convlst = array(tmplst,dtype=float)
    retlst = []
    for para in paralst:
         nummin = where(origlst <= para)[0][-1]
         nummax = where(origlst >= para)[0][0]
         orig_paramin = origlst[nummin]
         orig_paramax = origlst[nummax]
         orig_delta = orig_paramax - orig_paramin
         ratio = (para - orig_paramin) / orig_delta
         conv_paramin = convlst[nummin]
         conv_paramax = convlst[nummax]
         conv_delta = conv_paramax - conv_paramin
         retlst += [conv_delta * ratio + conv_paramin]
    return retlst

a= [[1,3,5],[10,13,15]]
para = 2
print prmconv(para, a)

