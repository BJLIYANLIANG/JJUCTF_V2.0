from jjuctf.SqlServer import *
def ctf_search_rank(group_name):
    mysql = Mysqld()
    a = mysql.selectUserChallengeListDesc()
    j = 1
    print(a)
    for i in a:
        if i[0] == group_name:
            return j
        else:
            j += 1
    return j
#
# b = ctf_search_rank('juu')
# print(b)
