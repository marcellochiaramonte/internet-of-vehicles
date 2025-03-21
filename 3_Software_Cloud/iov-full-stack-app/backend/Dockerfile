FROM maven:3.6-jdk-11-slim AS builder
RUN mkdir /app
WORKDIR /app


COPY ./source/pom.xml ./pom.xml
# fetch all dependencies
RUN mvn dependency:go-offline -B

ARG BUILD_PROFILE
ARG MYSQL_USER
ARG MYSQL_PASSWORD
ARG MYSQL_DATABASE_URL

RUN echo ${MYSQL_USER} ${MYSQL_PASSWORD} ${MYSQL_DATABASE_URL} ${BUILD_PROFILE}

COPY ./source .
RUN mvn clean package 
# RUN mvn \
#     -Ddatabase.username=${MYSQL_USER} \
#     -Ddatabase.password=${MYSQL_PASSWORD} \
#     -Ddatabase.url=${MYSQL_DATABASE_URL} \
#     -DskipTests \
#     # -P${BUILD_PROFILE} \
#     clean package

FROM openjdk:11.0-jre-slim
RUN mkdir /app && chmod ugo+rwx /app
COPY --from=builder /app/target/ovms3lite-backend*.jar /app/ovms3lite-backend.jar
WORKDIR /app
ENTRYPOINT [ "java","-jar","/app/ovms3lite-backend.jar"]

