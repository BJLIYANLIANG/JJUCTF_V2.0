class Contain:
    def __init__(self,a):
        self.a =  a
    def printA(self):
        print(self.a)




# create table challenge_list(
#           challenge_id int primary key auto_increment,
#           challenge_type int(2) not null,
#           challenge_name varchar(20) not null,
#           challenge_score int(4) not null,
#           challenge_hint varchar(30),
#           docker_flag int(1) not null,
#           docker_path varchar(30) ,
#           challenge_flag int(1) not null,
#           challenge_file varchar(20));
# type web--0    misc---1 crypto---2  reverse---3
#

# insert into challenge_list
#   (challenge_name,challenge_type,challenge_score,challenge_hint,docker_flag,challenge_flag)
#   values("easyPython",0,50,"SSTI漏洞",0,0),("easymisc",1,100,"简单的misc",0,0);
#
# id dchallengename type challenge  flag dockerpath

#
# insert into challenge_list
#   (challenge_name,challenge_type,challenge_score,challenge_hint,docker_flag,challenge_flag)
#   values("easycrypto",3,50,"简单逆向",0,0),("easypwn",1,100,"简单的PWN",4,0);