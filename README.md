# Table of Contents
- [Table of Contents](#table-of-contents)
- [개요](#개요)
- [Skills](#skills)
      - [Language and Tool](#language-and-tool)
      - [Database](#database)
- [Directory](#directory)
- [API Reference](#api-reference)
- [ERD](#erd)
- [프로젝트 진행 및 이슈 관리](#프로젝트-진행-및-이슈-관리)
- [구현 설계 및 의도](#구현-설계-및-의도)
- [TIL \& 회고](#til--회고)


# 개요
해당 프로젝트는 '예산 관리 서비스' 를 구현하고 있습니다. 사용자의 개인 재무 관리 및 지출 추적을 토대로 재무 컨설팅 기능을 제공합니다. 사용자는 회원가입을 통해 서비스를 이용하고, 월별 예산 설정, 카테고리별 예산 설계, 지출 기록을 기반으로 개인 맞춤형 컨설팅 제공 및 지출 통계 기능이 포함됩니다.

# Skills
#### Language and Tool

<img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white">
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=white">
<img src="https://img.shields.io/badge/jwt-000000?style=for-the-badge&logo=jwt&logoColor=white">

#### Database

<img src="https://img.shields.io/badge/postgresql-4169E1?style=for-the-badge&logo=postgresql&logoColor=white">

# Directory
<details>
<summary>눌러서 프로젝트 파일 구조 보기</summary>
<pre>
budget-mgt-service
├─ .gitignore
├─ assets
│  └─ images
│     ├─ moneydb.png
│     ├─ moneydb_erd.png
│     └─ swagger.png
├─ budget
│  ├─ admin.py
│  ├─ apps.py
│  ├─ migrations
│  │  ├─ 0001_initial.py
│  │  ├─ 0002_alter_budgetcategory_name.py
│  │  └─ __init__.py
│  ├─ models.py
│  ├─ serializers.py
│  ├─ tests.py
│  ├─ urls.py
│  ├─ views.py
│  └─ __init__.py
├─ core
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
│  └─ __init__.py
├─ dummy.py
├─ LICENSE
├─ manage.py
├─ README.md
├─ requirements.txt
├─ stalker
│  ├─ admin.py
│  ├─ apps.py
│  ├─ migrations
│  │  ├─ 0001_initial.py
│  │  ├─ 0002_userpreferences_income_range_and_more.py
│  │  └─ __init__.py
│  ├─ models.py
│  ├─ serializers.py
│  ├─ tests.py
│  ├─ urls.py
│  ├─ views.py
│  └─ __init__.py
├─ swagger.py
└─ users
   ├─ admin.py
   ├─ apps.py
   ├─ manager.py
   ├─ migrations
   │  ├─ 0001_initial.py
   │  └─ __init__.py
   ├─ models.py
   ├─ serializers.py
   ├─ tests.py
   ├─ urls.py
   ├─ views.py
   └─ __init__.py
</pre>
</details>

# API Reference
Swagger : http://127.0.0.1:8000/

![api](assets/images/swagger.png)

# ERD
![ERD](assets/images/moneydb_erd.png)


# 프로젝트 진행 및 이슈 관리
아래 아이콘을 눌러 이슈 및 일정 관리 페이지 바로가기

<a href="https://github.com/users/mireu-san/projects/5">
    <img src="https://img.shields.io/badge/github-000000?style=for-the-badge&logo=github&logoColor=white">
</a>
<a href="https://github.com/users/mireu-san/projects/5">
    <img src="assets/images/planner.png" alt="프로젝트 관리">
</a>

# 구현 설계 및 의도
작성 및 정리 예정.
<details>
<summary>회원 가입</summary>
<pre>
작성 예정
</pre>
</details>

<details>
<summary>예산 입력</summary>
<pre>
작성 예정
</pre>
</details>

<details>
<summary>지출 트래킹 및 개인 맞춤형 컨설팅</summary>
<pre>
작성 예정
</pre>
</details>

<details>
<summary>Discord Webhook 알림 기능</summary>
<pre>
작성 예정
</pre>
</details>

# TIL & 회고
- [Django — Unit Test 작성에서 겪은 이슈들](https://medium.com/@bellwoan/django-unit-test-%EC%9E%91%EC%84%B1%EC%97%90%EC%84%9C-%EA%B2%AA%EC%9D%80-%EC%9D%B4%EC%8A%88%EB%93%A4-ea4f7da18390)

- [Django — Unit test 작성과 절대경로](https://medium.com/@bellwoan/django-unit-test-%EC%9E%91%EC%84%B1%EA%B3%BC-%EC%A0%88%EB%8C%80%EA%B2%BD%EB%A1%9C-5c7f4d6dfea9)

- [Django에서 효율적인 데이터베이스 업데이트를 위한 패턴 고찰](https://medium.com/@bellwoan/django%EC%97%90%EC%84%9C-%ED%9A%A8%EC%9C%A8%EC%A0%81%EC%9D%B8-%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4-%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8%EB%A5%BC-%EC%9C%84%ED%95%9C-%ED%8C%A8%ED%84%B4-%EA%B3%A0%EC%B0%B0-a3cdc2d22d8a)

- [Django — duplicated data issue 회피에는 get_or_create](https://medium.com/@bellwoan/django-duplicated-data-issue-%ED%9A%8C%ED%94%BC%EC%97%90%EB%8A%94-get-or-create-643a1c8d00c6)

- [Python, Django : dummy data 생성 후, 중복 처리하기](https://medium.com/@bellwoan/python-django-dummy-data-%EC%83%9D%EC%84%B1-%ED%9B%84-%EC%A4%91%EB%B3%B5-%EC%B2%98%EB%A6%AC%ED%95%98%EA%B8%B0-266a3b8fffba)