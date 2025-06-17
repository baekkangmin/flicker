from fastapi import FastAPI, Body
from typing import List
from models import SentimentReviewEvent, SentimentResult, ContentMovieRequest, ContentMovieResponse, \
    CollaboMovieRequest, CollaboMovieResponse, ModelUpdateRequest, WordCloudRequest, NewMovieUpdateRequest
from predict import sequential_movie_evaluation
from gensim.models import Word2Vec
from word2vec_model import load_word2vec_model, get_similar_words_with_T
from CollaboModel import updatePcaResultOptimal, recommendMovieByUserTime, load_initial_data
from word2vecUpdate import model_update
from wordcloud import wordcloudUpdate
import sqlite3
import asyncio
from contextlib import asynccontextmanager

BATCH_SIZE = 8192  # 배치 크기 설정


# Lifespan 이벤트 핸들러 정의
@asynccontextmanager
async def lifespan(app: FastAPI):
    global word2vec_model
    print("Loading initial data...")
    await load_initial_data()  #
    word2vec_model = load_word2vec_model()
    print("Initial data loaded.")
    yield  # 애플리케이션이 실행되는 동안 유지
    # 애플리케이션 종료 시 실행될 로직 (필요 시 추가 가능)
    print("Cleaning up resources...")


# FastAPI 애플리케이션 생성
app = FastAPI(lifespan=lifespan)


# FastAPI 엔드포인트 정의
@app.post("/content")
async def get_movie_with_content(request: List[ContentMovieRequest]):
    """입력된 단어 리스트에서 'T'로 끝나는 유사 단어들을 추출하는 API"""
    # 요청에서 words 값을 모두 추출
    all_words = [req.actorName if req.actorName is not None else req.movieTitle + "^" + str(req.year) + "T" for req in
                 request]

    # 유사 단어 추출
    sorted_movies = get_similar_words_with_T(word2vec_model, all_words)
    movie_objects = [ContentMovieResponse(movieTitle=title, movieYear=year) for title, year in sorted_movies]

    return movie_objects


# API 엔드포인트 정의 (배치 처리)
# 1. 추천 관련 API
# 협업 필터링을 활용한 리뷰데이터 기반 추천 API
@app.post("/collabo")
async def get_movie_with_collabo(userSeq: int = Body(...)):
    # 결과 출력
    movies = recommendMovieByUserTime(userSeq)
    collabo_movie_responses = [CollaboMovieResponse(movieTitle=movie[0], movieYear=movie[1]) for movie in movies]
    return collabo_movie_responses


# 2. Kobert 리뷰 감성분석 API
@app.post("/sentiment_score")
async def analyze_sentiment(reviews: List[SentimentReviewEvent]):
    print(f"Received reviews: {reviews}")
    sentiment_scores = sequential_movie_evaluation(reviews, batch_size=BATCH_SIZE)
    return sentiment_scores


# 3. 업데이트 관련 API
# 협업 필터링을 위한 리뷰 데이터 수집 및 수집 된 데이터를 통한 PCA 업데이트
@app.post("/update_model")
async def update_model(reviews: List[ModelUpdateRequest]):
    conn = sqlite3.connect('recommend.db')
    # print(reviews)
    cursor = conn.cursor()

    # SQL INSERT 문 준비
    insert_query = """
    INSERT INTO review_info (review_seq, user_seq, movie_seq, review_rating, sentiment_score) 
    VALUES (?, ?, ?, ?, ?)
    """

    delete_query = """
    DELETE FROM review_info 
    WHERE review_seq = ?
    """

    try:
        # 받은 데이터를 반복하면서 삽입
        for review in reviews:
            if review.action == "CREATE":
                cursor.execute(insert_query, (
                review.reviewSeq, review.userSeq, review.movieSeq, review.rating, review.sentimentScore))
            elif review.action == "DELETE":
                cursor.execute(delete_query, (review.reviewSeq,))

        # 변경 사항 커밋
        conn.commit()

    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()  # 오류 발생 시 롤백

    finally:
        # 연결 종료
        conn.close()

    # await updatePcaResultOptimal()


# word2vec 업데이트 API
@app.post("/word2vec_update")
async def word2vec_update():
    asyncio.create_task(model_update())
    word2vec_model = load_word2vec_model()


# 4. wordCloud 관련 API
# 워드 클라우드를 위한 형태소 분석 데이터 수집
@app.post("/word_cloud")
async def word_cloud_update(reviews: List[WordCloudRequest]):
    conn = sqlite3.connect('recommend.db')
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO wordcloud (movie_seq, content) 
        VALUES (?, ?)
        """
    try:
        for review in reviews:
            if review.content is not None and review.content.strip() != "":
                cursor.execute(insert_query, (review.movieSeq, review.content))

        conn.commit()

    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()  # 오류 발생 시 롤백

    finally:
        # 연결 종료
        conn.close()


# 워드 클라우드 업데이트
@app.post("/wordcloud_update")
async def wordcloud_update():
    return wordcloudUpdate()


# 5. 크롤링 된 새로운 영화 업데이트 (word2vec 업데이트를 위한 수집 API)
@app.post("/movie_update")
async def new_movieUpdate(movies: List[NewMovieUpdateRequest]):
    conn = sqlite3.connect('recommend.db')
    cursor = conn.cursor()
    insert_query = """
        INSERT INTO movie_info (movie_seq, movie_title, movie_year, genre) 
        VALUES (?, ?, ?, ?)
        """
    insert_query2 = """
        INSERT INTO movie_actor (movie_seq, actor_name) 
        VALUES (?, ?)
        """
    try:
        # 받은 데이터를 반복하면서 삽입
        for movie in movies:
            cursor.execute(insert_query, (movie.movieSeq, movie.movieTitle, movie.movieYear, movie.genre))
            for actor in movie.actors:
                cursor.execute(insert_query2, (movie.movieSeq, actor.actorName))

        # 변경 사항 커밋
        conn.commit()

    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()  # 오류 발생 시 롤백

    finally:
        # 연결 종료
        conn.close()


@app.get("/")
async def root():
    return {"message": "Sentiment analysis API is running"}


# 메인 함수 정의
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)