# 🌙 for you , to you , on you Flicker 🌟

> **영화 추천 플랫폼 Flicker**  
> 고객의 시각을 다각화하여 고객 중심의 영화 컨텐츠를 추천

## ![alt text](exec/img/main.png)

## ✨ 서비스 소개

영화진흥원에 따르면 NetFlix, Watcha등 다양한 영화 플랫폼이 생겨나는 것에 반해, 고객이 직접 영화를 보기 까지 걸리는 시간이 전년도(2023 년 초 기준 현재 2024년 10월)에 비해 4.3일 증가함.

이에 팀 육캔두잇(이하 본팀)은 영화 추천 알고리즘의 고착화와 유저의 시각을 다각화 하였지 못함을 주요 원인으로 파악하고 영화 추천 알고리즘의 구체화, 방식의 다각화를 통해 고객 맞춤형 영화 추천 플랫폼을 계획 하고자 함

---

## ✨ Flicker 페이지 소개

### 1️⃣ HOME

![home](exec/img/flicker_home.gif)

Flicker 웹 페이지에 처음 들어왔을때,

랜딩페이지와 움직이는 카드형식의 홈페이지를 볼 수 있습니다.

### 2️⃣ MOVIES

![movies](exec/img/flicker_movies.gif)

Movies 페이지에 들어오면, 사이트의 Today Top 10과 다양한 장르들의 영화 목록을 볼 수 있습니다.

각 영화의 포스터를 호버시에 해당 영화의 간략한 정보를 확인할 수 있습니다.

또한, 오른쪽 상단의 돋보기 모양을 통해서 원하는 영화를 검색 할 수 있습니다.

### 2️⃣ MOVIES - Detail

![movies](exec/img/moviesDetail.gif)

영화의 기본 정보, 예고편과 리뷰 등을 볼 수 있으며, 찜하기와 관심없음을 통해서 본인의 취향을 반영할 수 있습니다.

해당 페이지의 맨 아래의 해당 영화와 유사한 장르의 장품들을 추천 알고리즘을 통해서 추천해줍니다.

### 3️⃣ FOR YOU

![foryou](exec/img/flicker_foryou.gif)

영화 추천은 크게 2개로 나뉘어서 왼쪽 문은 "리뷰"기반(MOOD), 오른쪽 문은 "행동"기반(ACTION)으로 분리했습니다. 

문을 클릭하면 영화관 UI로 사용자에게 맞는 추천 영화 목록이 나옵니다.


### 4️⃣ PHOTOBOOK

![photobook](exec/img/flicker_photobook.gif)

사용자가 리뷰를 작성하면, 자동으로 본인의 포토북에 포토카드가 추가됩니다.

포토북은 앨범식으로 되어있고, 포토카드를 클릭하면 뒷면에 본인이 적은 리뷰에 대한 상세 내용이 적혀있습니다.

포토북을 통해 사용자들에게 리뷰 작성을 독려하고, 본인의 리뷰를 소장하는 기능을 제공합니다.


## ✨ 주요 기능

#### (1) 평점 + 리뷰 기반 추천

평점 리뷰 기반 근접 이웃 도출, 텍스트 마이닝을 통한 초 근접 이웃 유사 군집군 결정

#### (2) 컨텐츠 기반 추천

영화 줄거리, 리뷰, 배우, 감독을 중심으로 word2vec 모델을 학습하여 영화 추천

#### (3) 로그 기반 추천

유저의 행동 로그에 기반하여 영화 추천

#### (4) 리뷰 크롤링 및 DB 반영 자동화

![alt text](exec/img/schedule.png)

## ✨ 추천 기능

### **리뷰를 기반으로 한 추천(협업필터링)**

![alt text](exec/img/collabo.png)

1. 데이터 수집 : 사용자 영화 리뷰 데이터 (평점, 리뷰 등)을 수집하여 협업 핉터링 모델을 구성
2. 차원 축소 : PCA 기법을 사용하여 고차원의 사용자 영화 평점 행렬을 저차원으로 변환
3. 유사도 계산 : 차원 축소된 데이터를 바탕으로 코사인 유사도를 계산하여 비슷한 영화나 사용자를 추천
4. 추천 : 유사도가 높은 영화를 바탕으로 맟춤형 영화 추천 리스트를 생성하여 제공
5. 모델 업데이트 : 실시간 리뷰 로그 데이터를 수집하여 1시간을 주기로 모델 업데이트 진행

### **Word2Vec 모델을 활용한 컨텐츠 기반 추천**

![alt text](exec/img/word2vec.png)

1. 사용자의 행동(ex. 영화 상세조회, 검색 등) 로그를 수집하여 로그 리스트를 기반으로 영화 추천 리스트를 생성
2. 영화 검색 시 DB에서 일치하는 내용을 가지고 오면서 검색 키워드를 기반으로 한 영화 추천 리스트를 생성하여 추가
3. 영화 상세조회 시 해당 영화와 배우를 기반으로 한 추천 리스트를 생성

## 🛠️ 시스템 아키텍처

![alt text](exec/img/systenarch.png)

## ⭐ 팀원 소개

### **_Meet our highly skilled team members!_** | <img src="https://upload.wikimedia.org/wikipedia/commons/e/e9/Notion-logo.svg" alt="Notion Logo" width="20"/> [팀 노션](https://snowy-lilac-f3b.notion.site/6-5193ecebfd8643ba9d99d29e3bea2482?pvs=4)

|                                     |                                                                                                                                                                   |                                      |                                                                                                                                                                            |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ![HaHyul Kim](exec/img/hyulKim.jpg) | **HaHyul Kim** <br> Frontend <br> UX / UI 개발 <br> 데이터 캐싱 및 서버 비동기 통신 <br> [GitHub](https://github.com/busangangster) <br> gkgbf1034@gmail.com      | ![HyunJeong Cho](exec/img/jeong.jpg) | **HyunJeong Cho** <br> Frontend <br> UX / UI 디자인 및 개발 <br> JWT 및 서버 비동기 통신 <br> [GitHub](https://github.com/hyunjeongg11) <br> guswjd4585@gmail.com          |
| ![jihwan](exec/img/jihwan.jpg)      | **JiHwan Gong** <br> Backend <br> 데이터 수집 <br> 영화 도메인 서버 <br> BFF 서버 설계 및 구현 <br>[GitHub](https://github.com/izgnok) <br> rinch12332@gmail.com  | ![dong](exec/img/dong.png)           | **DongGyu Oh** <br> Backend <br> 유저/리뷰 도메인 개발 <br> 시스템 아키텍처 설계 <br> 부하 테스트 <br> [GitHub](https://github.com/Eastplanet) <br> ehdrb1645@gmail.com    |
| ![chan](exec/img/chan.jpg)          | **JaeChan Lee** <br> Infra <br> 인프라 아키텍처, CI/CD 구축 <br> 추천 모델 훈련 및 서버 구현 <br> [GitHub](https://github.com/jaechanjj) <br> jaechanjj@gmail.com | ![jae](exec/img/jae.jpg)             | **JaeYoung Choi** <br> Backend <br> 배치 서버 구현 및 ERD 설계 <br> 추천 모델 훈련 및 서버 구현 <br> [GitHub](https://github.com/wodyddldl333) <br> wodyddldl333@naver.com |

## 🌐 개발 설정

[포팅메뉴얼](https://lab.ssafy.com/s11-bigdata-recom-sub1/S11P21E206/-/blob/master/exec/%EB%B0%B0%ED%8F%AC%20%EA%B0%80%EC%9D%B4%EB%93%9C%20%EB%AC%B8%EC%84%9C.pdf?ref_type=heads)을 참고하세요.
# flicker
