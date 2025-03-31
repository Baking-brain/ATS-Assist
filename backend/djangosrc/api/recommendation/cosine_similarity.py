import math

def cos_sim(vec1, vec2):

    vector1 = vec1
    vector2 = vec2

    vec1_mag = math.sqrt(sum(i**2 for i in vector1))
    vec2_mag = math.sqrt(sum(i**2 for i in vector2))

    dot_prod = sum(i*j for i,j in zip(vector1, vector2))

    cosx = dot_prod/((vec1_mag*vec2_mag) or 1)

    return round(cosx, 5)

# test1 = [0, 1, 0, 1]
# test2 = [1, 1, 0, 1]
# print(cos_sim(test1, test2))