def compareEmbeddedArrays(a, b):
    if(a==None or b==None):
        return False
    
    if len(a) != len(b):
        return False

    for i in range(len(a)):
        if isinstance(a[i], list) and isinstance(b[i], list):
            if not compareEmbeddedArrays(a[i], b[i]):
                return False
        elif a[i] != b[i]:
            return False

    return True