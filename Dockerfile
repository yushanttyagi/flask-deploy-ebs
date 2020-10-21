from alpine:latest
RUN apk add py3-pip		#apk is apache package and means we are using our base image to run some commands
RUN apk add --no-cache python3-dev && pip3 install --upgrade pip
WORKDIR /app
COPY . /app
RUN pip3 --no-cache-dir install -r requirements.txt
EXPOSE 5001
ENTRYPOINT [ "python3" ]
CMD [ "empl.py" ]


#this will terminate all the previous FROMs which means that they are done
FROM nginx
EXPOSE 80
#we dump everything else, since dependecies are not required again
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=0 /app /usr/share/nginx/html		

#starting nginx container will automatically run it 