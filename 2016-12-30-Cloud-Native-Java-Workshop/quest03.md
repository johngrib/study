# Quest 03. [Config Server](https://github.com/joshlong/cloud-native-workshop#3-the-config-server)

이번 퀘스트는 Config Server를 구성해보는 모양이다.

* 스터디 안내 [README](https://github.com/joshlong/cloud-native-workshop#3-the-config-server)를 읽어보니 다음과 같은 소개글이 나와 있다.

> The [12 Factor](https://12factor.net/config) manifesto talks about externalizing that which changes from one environment to another - hosts, locators, passwords, etc. - from the application itself. Spring Boot readily supports this pattern, but it's not enough. In this lab, we'll look at how to centralize, externalize, and dynamically update application configuration with the Spring Cloud Config Server.

* 구글 번역으로 돌려 보았더니 다음과 같이 출력되었다. 놀라운 번역 품질 오오.

> 12 Factor 선언문은 응용 프로그램 자체에서 호스트, 로케이터, 암호 등 한 환경에서 다른 환경으로 변경되는 것을 외부화하는 것에 대해 이야기합니다. Spring Boot는이 패턴을 쉽게 지원하지만 충분하지 않습니다. 이 실습에서는 Spring Cloud Config Server를 사용하여 애플리케이션 구성을 중앙화하고 외부화하며 동적으로 업데이트하는 방법을 살펴 보겠습니다.

자신을 믿고 한 걸음씩 나아가자.

## 3.1. 12 Factor 간단 요약

12 Factor 선언문은 예전에 읽어본 바 있지만, 꽤 오래 전에 읽었었기 때문에 이번 기회에 다시 읽어보게 되었다.

> Twelve-Factor App은 아래 특징을 가진 SaaS(Software As A Service) 앱을 만들기 위한 방법론이다.
    * 설정 자동화를 위한 절차(declarative) 를 체계화 하여 새로운 개발자가 프로젝트에 참여하는데 드는 시간과 비용을 최소화한다.
    * OS에 따라 달라지는 부분을 명확히하고, 실행 환경 사이의 이식성을 극대화 한다.
    * 최근 등장한 클라우드 플랫폼 배포에 적합하고, 서버와 시스템의 관리가 필요없게 된다.
    * 개발 환경과 운영 환경의 차이를 최소화하고 민첩성을 극대화하기 위해 지속적인 배포가 가능하다.
    * 툴, 아키텍처, 개발 방식을 크게 바꾸지 않고 확장(scale up) 할 수 있다.

### 3.1.1. 코드 베이스

* 12 Factor App은 버전 컨트롤 시스템을 사용한다.
* 코드 베이스와 앱은 1대 1 관계여야 한다.
* 여러 앱이 동일한 코드를 쓰면 안 된다. 그런 코드가 있다면 라이브러리로 만들고, 종속성 매니저로 관리할 것.

### 3.1.2. 종속성(Dependencies)

* 요즘은 상식인 이야기들이다.
* 의존성 관리 도구를 사용할 것. Java라면 Maven, Gradle 등을 사용하면 된다.
* 새로 join한 개발자가 개발 환경 설정을 쉽게 할 수 있다는 장점이 있다.
* 의존하고 있는 시스템 도구가 있다면 그 도구를 앱과 통합한다.

### 3.1.3. 설정

* 설정을 코드에서 분리한다.
* 인증 키나 DB 접속 정보 등을 코드에 저장하지 말 것!
* 12 Factor 앱은 설정을 환경 변수에 저장한다.
    * 코드 변경 없이 배포 때 쉽게 변경 가능하기 때문이다.
    * 파일이 아니기 때문에 실수로 코드 저장소에 업로드할 가능성도 없기 때문이다.

### 3.1.4. 백엔드 서비스

* DB나 SMTP 서비스와 같은 백엔드 서비스는 리소스로 간주한다.
* 백엔드 서비스들과 앱은 느슨하게 결합시켜야 한다.
* 코드를 수정하지 않고도 다른 DB에 연결할 수 있어야 한다.

### 3.1.5. 빌드, 릴리즈, 실행

* 빌드, 릴리즈, 실행 단계를 엄격히 분리할 것.

### 3.1.6. 프로세스

* 앱은 stateless 프로세스로 실행한다.
* 유지될 필요가 있는 모든 데이터는 DB에 저장할 것.

### 3.1.7. 포트 바인딩

* 12 Factor 웹 앱은 포트를 바인딩하여 HTTP 서비스로 공개한다.
* 포트 바인딩을 사용함으로써, 다른 앱을 위한 백엔드 서비스로 사용할 수도 있게 된다.

### 3.1.8. 동시성(Concurrency)

* 애플리케이션은 여러개의 물리적인 머신에서 돌아가는 여러개의 프로세스로 넓게 퍼질 수 있어야 한다(수평 확장).
* 12 Factor 앱은 어차피 아무것도 공유하지 않게 만들테니까, 하나의 프로세스에서 여러 작업을 개별 스레드로 돌리는 것(수직 확장)보다 각각의 역할을 하는 여러 프로세스를 구동하는 쪽(수평 확장)이 더 간단하고 안정적이다.
* 말이 좀 어렵지만, Docker나 마이크로 서비스 구조를 생각해보면 간단하다.

### 3.1.9. 폐기 가능(Disposability)

* 프로세스의 시작과 종료가 빠르고 간단해야 한다.
* 확장이나 변화가 있을 때 빠르게 배포할 수 있게 된다.
* 하드웨어 에러 등에 의한 예상치 못한 종료에도 대응할 수 있어야 한다.
    * 문제가 생겼을 경우 작업을 큐로 되돌릴 수 있도록 한다.
    * Beanstalkd와 같은 견고한 큐잉 백엔드를 사용할 것.

### 3.1.10. dev/prod 일치

* development, staging, production 환경을 최대한 비슷하게 유지할 것.
* 환경의 차이를 적게 하여 지속적인 배포가 가능하게 해야 한다.

> * 시간의 차이를 최소화: 개발자가 작성한 코드는 몇 시간, 심지어 몇 분 후에 배포됩니다.
> * 담당자의 차이를 최소화: 코드를 작성한 개발자들이 배포와 production에서의 모니터링에 깊게 관여합니다.
> * 툴의 차이를 최소화: 개발과 production 환경을 최대한 비슷하게 유지합니다.

### 3.1.11. 로그

* 12 Factor 앱이 로그 파일의 저장이나 관리에 관여하면 안된다.

### 3.1.12. Admin 프로세스

* admin 코드는 동기화 문제를 피하기 위해 애플리케이션 코드와 함께 배포되어야 한다.
    * DB 마이그레이션이나 일회성 관리 등의 문제 때문에 해당 릴리즈 기반으로 돌아가는 경우가 많기 때문이다.

## 3.2. Config Server

이제 Config Server를 구성해 보자.

### 3.2.1. 초기화

> Go to the Spring Initializr, choose the latest milestone of Spring Boot 1.3.x, specify an `artifactId` of `config-service` and add `Config Server` from the list of dependencies.

* 일단 config server를 관리하기 위해 [Github repository](https://github.com/johngrib/test_config_server) 하나를 새로 만들었다.
* [start.spring.io](http://start.spring.io)에서 `config server`를 선택하고 다운로드 하였다.
* 만들어 놓은 repository에 [푸시](https://github.com/johngrib/test_config_server/commit/0ed09d5b8b49e785ee6329f414ee08706d933c90).

### 3.2.2. `bootiful-microservices-config` 클론

> You should `git clone` the Git repository for this workshop - [https://github.com/joshlong/bootiful-microservices-config](https://github.com/joshlong/bootiful-microservices-config)

* 앞날은 아무도 모른다. 일단 [fork](https://github.com/johngrib/bootiful-microservices-config).
* `$ git clone git@github.com:johngrib/bootiful-microservices-config.git`으로 클론.
* 내용을 보니 다양한 `properties`파일들이 옹기종기 모여 있다. 목록은 다음과 같다.

```
application-cloud.properties
eureka-service.properties
reservation-service.properties
application.properties
hystrix-dashboard.properties
zipkin-service.properties
auth-service.properties
reservation-client-github.properties
dataflow-service.properties
reservation-client.properties
```

### 3.2.3. 설정

> In the Config Server's `application.properties`, specify that it should run on port 8888 (`server.port=8888`) and that it should manage the Git repository of configuration that lives in the root directory of the `git clone`'d configuration. (`spring.cloud.config.server.git.uri=...`).

* `application.properties`파일을 수정하라고 하니 `3.2.2.절`에서 클론한 디렉토리에 들어 있던 같은 이름의 파일을 복사해 config 서버의 `application.properties`파일에 덮어씌웠다.
* `application.properties`파일의 server.port 부분을 다음과 같이 수정해 주었다.

```
server.port=8888
```

* 이번엔 configuration repository를 클론한 경로를 명시해 주어야 한다... 라는 것은 설정 파일을 config server 경로에 복사하지 않고 외부에 두어도 된다는 말 같다. 그렇다면 바로 위에서 `application.properties`파일을 덮어씌운 것은 쓸데없는 일이었던 모양이다.
* 따라서 최종적으로 `application.properties`파일은 다음과 같이 작성되었다.

```
spring.cloud.config.server.git.uri=${HOME}/git/bootiful-microservices-config
server.port=8888
```

### 3.2.4. `@EnableConfigServer` 어노테이션 추가

> Add `@EnableConfigServer` to the `config-service`'s root application

다음과 같이 root application에 `@EnableConfigServer`를 추가해 주었다.

```java
package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.config.server.EnableConfigServer;

@EnableConfigServer     // 추가해 준 어노테이션
@SpringBootApplication
public class DemoConfigServerApplication {

    public static void main(String[] args) {
        SpringApplication.run(DemoConfigServerApplication.class, args);
    }
}
```

이후 Run해주긴 했는데,

#### 3.2.4.1. 어떻게 테스트를 한다?

* 어느 url로 접속해야 할 지 모르겠다.
* `localhost:8888`에 접속해 보니 `Whitelabel Error Page`만 나타난다.
* 쉽게 생각하자. [Josh Long 동영상](https://www.youtube.com/watch?v=fxB0tVnAi0I)을 찾아본다.
    * Josh Long은 `localhost:8888/reservation-service/default`라는 url로 접속해 결과를 확인하고 있다.
    * 앗 어디서 본 주소명인데?
* 클론해 두었던 `bootiful-microservices-config`내에 `reservation-service.properties`라는 파일이 있었다.
    * 나도 똑같은 주소로 확인해 보자.

```sh
$ curl http://localhost:8888/reservation-service/default | jq
```

위와 같이 입력하였더니 다음과 같은 결과가 출력되었다.

```json
{
  "name": "reservation-service",
  "profiles": [
    "default"
  ],
  "label": "master",
  "version": "1760a7d552617e57bb946356d8b434349f31a92d",
  "propertySources": [
    {
      "name": "/Users/johngrib/git/bootiful-microservices-config/reservation-service.properties",
      "source": {
        "server.port": "${PORT:8000}",
        "spring.cloud.stream.bindings.input.destination": "reservations",
        "spring.cloud.stream.bindings.input.group": "reservations-group",
        "message": "Hello World!",
        "spring.cloud.stream.bindings.input.durableSubscription": "true"
      }
    },
    {
      "name": "/Users/johngrib/git/bootiful-microservices-config/application.properties",
      "source": {
        "logging.level.com.netflix.discovery": "OFF",
        "debug": "true",
        "logging.level.org.springframework.security": "DEBUG",
        "spring.sleuth.sampler.percentage": "1.0",
        "logging.level.com.netflix.eureka": "OFF",
        "endpoints.shutdown.enabled": "true",
        "spring.jmx.enabled": "false",
        "endpoints.jmx.enabled": "false",
        "info.id": "${spring.application.name}",
        "spring.jpa.generate-ddl": "true",
        "spring.sleuth.log.json.enabled": "true"
      }
    }
  ]
}
```

`propertySources[0].name`을 보니 `bootiful-microservices-config`의 하위 파일이 맞는 것 같다.
`reservation-service.properties`파일 내용을 확인해보니 다음과 같았다.

```
server.port=${PORT:8000}
message = Hello World!

# define the destination to which the input MessageChannel should be bound
spring.cloud.stream.bindings.input.destination = reservations

# ensures 1 node in a group gets message (point-to-point, not a broadcast)
spring.cloud.stream.bindings.input.group = reservations-group

# ensure that the Q is durable
spring.cloud.stream.bindings.input.durableSubscription = true
```

아무래도 이 내용을 보여주는 것 같다.

오케이. 알 것 같다.  
그래서 다른 파일들 중 아무거나 하나를 골라 이름(`application-cloud.properties`)을 확인해 보고 다음과 같이 시도해 보았다.

```sh
$ curl http://localhost:8888/application-cloud/default | jq
```

그랬더니 다음과 같이 나왔다.

```json
{
  "name": "application-cloud",
  "profiles": [
    "default"
  ],
  "label": "master",
  "version": "1760a7d552617e57bb946356d8b434349f31a92d",
  "propertySources": [
    {
      "name": "/Users/johngrib/git/bootiful-microservices-config/application-cloud.properties",
      "source": {
        "eureka.client.serviceUrl.defaultZone": "${vcap.services.eureka-service.credentials.uri}/eureka/",
        "eureka.client.registryFetchIntervalSeconds": "5",
        "eureka.client.region": "default",
        "spring.rabbitmq.addresses": "${vcap.services.reservations-rabbitmq.credentials.uri}",
        "eureka.instance.metadataMap.instanceId": "${vcap.application.instance_id:${spring.application.name}:${spring.application.instance_id:${server.port}}}",
        "eureka.instance.leaseRenewalIntervalInSeconds": "5",
        "eureka.instance.nonSecurePort": "80",
        "eureka.instance.hostname": "${vcap.application.uris[0]:localhost}"
      }
    }
  ]
}
```

`application-cloud.properties`파일을 확인해보니 역시 `propertySources[0].source`와 같은 내용을 갖고 있었다.

json 출력 결과의 `propertySources[0].source`와 내용이 일치한다는 결론.  
(공식 문서를 찾아보면 바로 알 수 있겠지만)  
좀 더 확실하게 확인해보고 싶어서 `reservation-service.properties`파일의 message를 바꿔보기로 했다.

```
# message = Hello World!
mesage = All your base are belong to us
```

이후 다음 명령어로 내가 수정한 메시지가 출력되는지 확인해 보았다.

```sh
$ curl http://localhost:8888/reservation-service/default | jq .propertySources[0].source.message
```

그런데 결과가 바뀌지 않았다.  
* `All your base are belong to us`가 아니라 `Hello World!` 그대로 나온다.
* 빌드 과정에서 복사해 놓은걸까? 싶어서 찾아봤지만 따로 복사해 놓은 파일도 존재하지 않았다.
* 그러다가 config-server의 `application-properties`파일 내부에 다음과 같이 설정했던 것이 기억났다.

```properties
spring.cloud.config.server.git.uri=${HOME}/git/bootiful-microservices-config
```

key 이름에 `git`이 들어가고 있다.  
* 혹시 파일을 그대로 읽어오는 것이 아니라 git HEAD commit을 읽어오는 것이 아닐까?

그래서 commit을 한 다음 다시 확인해 보았다.

```
$ curl http://localhost:8888/reservation-service/default | jq .propertySources[0].source.message
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1008    0  1008    0     0   6878      0 --:--:-- --:--:-- --:--:--  6904
"All your base are belong to us"
```

`All your base are belong to us`가 잘 출력된다. 오케이.

좀 더 자세히 알아보기 위해 공식 문서를 찾아볼 시간이다.

[spring-cloud-config의 environment_repository](https://cloud.spring.io/spring-cloud-config/spring-cloud-config.html#_environment_repository)를 읽어보았다.

다음과 같은 구절들이 눈에 띈다.

> The default implementation of EnvironmentRepository uses a Git backend, which is very convenient for managing upgrades and physical environments, and also for auditing changes.

대강 읽어보니 Git backend를 사용하므로 변경 관리가 편리하다는 말이다. 좋은 생각 같다.
Git으로 관리하면 설정 셋을 여러 가지로 관리하기 편할 것 같다. 시간 여행도 가능하고, 쓸데없이 날려먹는 일도 피할 수 있다.

> To change the location of the repository you can set the "spring.cloud.config.server.git.uri" configuration property in the Config Server (e.g. in application.yml). If you set it with a file: prefix it should work from a local repository so you can get started quickly and easily without a server, but in that case the server operates directly on the local repository without cloning it (it doesn’t matter if it’s not bare because the Config Server never makes changes to the "remote" repository).

내가 궁금했던 내용이다. `spring.cloud.config.server.git.uri`를 사용해 설정을 분리하는 방법이다. 로컬에서 작동하니 빠르게 돌아가며, 서버는 설정을 복사하지 않고 로컬 저장소의 내용을 바라보게 된다. 어쨌든 다 로컬에서 돌아가니 노출될 걱정도 없고 속도 문제도 해결된다는 내용으로 이해하면 될 것 같다.

> This repository implementation maps the {label} parameter of the HTTP resource to a git label (commit id, branch name or tag). If the git branch or tag name contains a slash ("/") then the label in the HTTP URL should be specified with the special string "(_)" instead (to avoid ambiguity with other URL paths). Be careful with the brackets in the URL if you are using a command line client like curl (e.g. escape them from the shell with quotes '').

tag, commit id, branch name 등을 사용할 수 있다고 한다.  
소문으로 전해들은 golang의 *끔찍한* `import` 생각이 문득 떠올랐지만, 이건 괜찮은 아이디어 같다.

이번엔 커스텀 properties 파일을 만들어 보고 그것도 나타나는지 시험해 보자.

일단 다음과 같이 `johngrib.properties`라는 파일을 새로 추가하고, `commit` 했다.  

```
message = There is always one more bugs.
```

그리고 아래와 같이 확인해 보았다.


```sh
$ curl localhost:8888/johngrib/default | jq .propertySources[0]
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   765    0   765    0     0   3710      0 --:--:-- --:--:-- --:--:--  3713
{
  "name": "/Users/johngrib/git/bootiful-microservices-config/johngrib.properties",
  "source": {
    "message": "There is always one more bugs."
  }
}
```

잘 나온다!

### 3.2.5. `application.properties`에 `server.port=8888`을 추가할 것.

> Add `server.port=8888` to the `application.properties` to ensure that the Config Server is running on the right port for service to find it.

결과적으로 `application.properties`파일의 내용은 다음과 같이 되었다.

```
spring.cloud.config.server.git.uri=${HOME}/git/bootiful-microservices-config
server.port=8888
```

구동한 결과 이상 없이 잘 나온다. (8889로 바꾸고 해 보아도 잘 된다)

### 3.2.6. Add the Spring Cloud BOM

> Add the Spring Cloud BOM (you can copy it from the Config Server) to the `reservation-service`.

`reservation-service`에 지금까지 작업한 내용들을 연결하라는 의도 같은데 정확히 구체적으로 무엇을 하라는 것인지는 잘 모르겠다. `application-cloud.properties`파일을 복사해서 `reservation-service`의 `resource`디렉토리로 복사하면 된다는 걸까? 그것이 아니라면 어느 파일을? 혹은 `git.url`을 설정한 것처럼 경로만 명시해주면 되는 건가?

글쎄. 잘 모르겠다.  
일단 건너 뛰기로 하고 조금 더 아래를 읽어 보았다.

### 3.2.7. `reservation-service`의 `pom.xml` 수정

> We will need to modify the `reservation-service`'s `pom.xml` in order to make it a config client. To do this, add the following to your `pom.xml` of the `reservation-service` from step #1.

step #1에서 만든 `reservation-service`의 `pom.xml`에 다음 내용을 추가하라고 한다.  
좋아. 지금까지 해온 일들 중 가장 쉬운 일이다.

예전에 만들었던 `reservation`프로젝트의 `pom.xml`파일을 수정하기만 하면 된다.

```xml
<dependencyManagement>
    <dependencies>
      ...
      <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-parent</artifactId>
        <version>Brixton.RELEASE</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
</dependencyManagement>
```

이 때, 위의 내용을 `<dependencies>`가 아니라 `<dependencyManagement>`내에 넣어야 한다는 점에 주의해야 한다.

그리고 다음 내용을 `<dependencies>`내에 입력한다.

```xml
<dependencies>
  <dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-config</artifactId>
  </dependency>
..
</dependencies>
```

### 3.2.8. `bootstrap.properties` 파일 추가

> Create a `boostrap.properties` that lives in the same place as `application.properties` and discard the `application.properties` file. Now we need only to tell the Spring application where to find the Config Server, with the property `spring.cloud.config.uri=${config.server:http://localhost:8888}`, and how to identify itself to the Config Server and other services, later, with `spring.application.name`.

* `application.properties`와 같은 경로에 `bootstrap.properties`파일을 추가한다.
* `application.properties` 파일을 삭제한다.
* `spring.cloud.config.uri=${config.server:http://localhost:8888}`를 설정해 스프링 어플리케이션에 Config Server를 어떻게 찾아야 할 지 알려준다.

```
# bootstrap.properties
spring.cloud.config.uri=http://localhost:8888
spring.application.name=reservation-service
```

이후 Config Server를 구동한다.

### 3.2.9. `reservation-service`에 `MessageRestController`를 추가해준다.

> In the `reservation-service`, create a `MessageRestController` and annotate it with `@RefreshScope`. Inject the `${message}` key and expose it as a REST endpoint, `/message`.

이건 Josh Long의 동영상을 보고 따라했다.

```java
package com.reservation.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RefreshScope
@RestController
public class MessageRestController {

    @Value("${message}")
    private String message;

    @RequestMapping(method = RequestMethod.GET, value = "/message")
    String msg() {
        return this.message;
    }
}
```

자 이제 확인해보자.

```sh
$ curl http://localhost:8000/message
All your base are belong to us2017-02-05 일 17:00:09 johngrib Johnui-MacBook-Pro ~
```

이제 일요일을 즐길 시간이다.
