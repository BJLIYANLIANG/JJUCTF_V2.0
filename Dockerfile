## 进入到mysql数据库下
```
mysql> use mysql
Database changed
```
## 对新用户增删改

### 1.创建用户:
```
# 指定ip：192.118.1.1的jjuctf用户登录
create user 'jjuctf'@'192.118.1.1' identified by '123';
# 指定ip：192.118.1.开头的jjuctf用户登录
create user 'jjuctf'@'192.118.1.%' identified by '123';
# 指定任何ip的jjuctf用户登录
create user 'jjuctf'@'%' identified by '123';
```
### 2.删除用户
```
drop user '用户名'@'IP地址';

```
### 3.修改用户
```
rename user '用户名'@'IP地址' to '新用户名'@'IP地址';
```
### 4.修改密码
```
set password for '用户名'@'IP地址'=Password('新密码');
```

##  对当前的用户授权管理
```
# 查看权限
```
show grants for '用户'@'IP地址'
```
#授权 mjj用户仅对db1.t1文件有查询、插入和更新的操作
```
grant select ,insert,update on db1.t1 to "jjuctf"@'%';

# 表示有所有的权限，除了grant这个命令，这个命令是root才有的。mjj用户对db1下的t1文件有任意操作
grant all privileges  on db1.t1 to "jjuctf"@'%';
#mjj用户对db1数据库中的文件执行任何操作
grant all privileges  on db1.* to "jjuctf"@'%';
#mjj用户对所有数据库中文件有任何操作
grant all privileges  on *.*  to "jjuctf"@'%';
 
#取消权限
 
# 取消mjj用户对db1的t1文件的任意操作
revoke all on db1.t1 from 'jjuctf'@"%";  

# 取消来自远程服务器的mjj用户对数据库db1的所有表的所有权限

revoke all on db1.* from 'jjuctf'@"%";  

取消来自远程服务器的mjj用户所有数据库的所有的表的权限
revoke all privileges on *.* from 'jjuctf'@'%';
```
MySql备份命令行操作
```
# 备份：数据表结构+数据
mysqdump -u root db1 > db1.sql -p


# 备份：数据表结构
mysqdump -u root -d db1 > db1.sql -p

#导入现有的数据到某个数据库
#1.先创建一个新的数据库
create database db10;
# 2.将已有的数据库文件导入到db10数据库中
mysqdump -u root -d db10 < db1.sql -p
```