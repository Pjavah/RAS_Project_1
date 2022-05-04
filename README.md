# RAS_Project_1
Our groups repository for the Robotics and Autonomous Systems project 1.

Project by Patrik Vahala, Aleksi Eskola, Helena Lähdesniemi and Kalle Hautamäki.


<div> Important files are under droning_ws/src/droning_pkg/droning_pkg/. It goes a bit deep, but there are the files used in the project and demonstrations.</div>


<div></div>

<div></div>


















GIT CHEATS:
<div> git remote -v (you see what kind of url youre using.) </div>
<div> git remote set-url origin git@github.com:Pjavah/RAS_Project_1.git (adding the ssh path) </div>
<div>git status  </div>
<div>git pull </div>
<div>git commit -m "commit message" </div>
<div>git push </div>

TAKEOFF COMMAND
ros2 topic pub /takeoff std_msgs/Empty --once
ros2 topic pub /land std_msgs/Empty --once
