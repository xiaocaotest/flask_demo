### **1.生成requirements**

pip install pipreqs

pipreqs .  or  pipreqs . --force


### **2.生成docker image**
docker build -t flask .


### **3.运行镜像**
docker run -d -p 80:80 --name flask flask 