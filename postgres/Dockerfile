
# FROM openjdk11:alpine-jre
FROM amd64/openjdk:11
WORKDIR /app
VOLUME ["/app"]
COPY ./app.jar app.jar
#COPY ~/Source/CashflowLambda/Services/build/libs/Services.jar app.jar
ENTRYPOINT ["java","-cp","app.jar","com.wuxwesty.services.Main"]
