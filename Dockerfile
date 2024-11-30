FROM tomcat:10.1.33.0-openjdk:21-jdk

# Jar 파일의 위치

RUN rm -Rf /opt/tomcat/latest/webapps/ROOT
ARG ENVIRONMENT
ENV SPRING_PROFILES_ACTIVE=${ENVIRONMENT}

ARG WAR_FILE=target/*.war

# app.jar는 경우에 따라 이름 변경
COPY ${WAR_FILE} /opt/tomcat/latest/webapps/ROOT.war

# 생략 가능 - 해당 컨테이너는 8080 port 를 사용한다는 의미.
EXPOSE 8903