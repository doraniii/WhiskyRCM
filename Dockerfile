#FROM doraniii/webapp:1.2
# Jar 파일의 위치
#ARG JAR_FILE=target/*.jar
# app.jar는 경우에 따라 이름 변경
#COPY ${JAR_FILE} app.jar
# 생략 가능 - 해당 컨테이너는 8080 port 를 사용한다는 의미.
#EXPOSE 8903
# docker run 시 실행할 필수 명령어
#ENTRYPOINT ["java", "-jar", "/app.jar"]
# 경우에 따라 java 옵션 사용.
# ENTRYPOINT ["java", "-jar", "-Dspring.profiles.active=docker", "/app.jar"]

FROM doraniii/webapp:1.2
ARG WAR_FILE=target/ROOT.war
EXPOSE 8905
COPY ${WAR_FILE} /opt/tomcat/latest/webapps/ROOT.war
CMD ["catalina.sh", "run"]
RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime