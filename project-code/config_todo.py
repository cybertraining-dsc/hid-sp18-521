mysql_user = 'IUuser'
mysql_user_password = 'Password123'

'''

maybe also make config a dict e.g. use yaml

so you have

cloudmesh:
   mysql:
      user: 
         name: TBD
         password: TBD
         
config = read in your config yam

password = config['cloudmesh']['mysql']['user']['password'] 
username = config['cloudmesh']['mysql']['user']['name'] 


pseudo code suggested by gregor

if there is no file at ~/.cloudmesh/tbd-config.yaml
   copy the file there from etc
   
read in the yaml
changed = false
if passwd == TBD
   get a new password
   changed = true
if username == TBD 
   get a new username
   changed = true
if changed:
   write the yaml file back to  ~/.cloudmesh/tbd-config.yaml

'''