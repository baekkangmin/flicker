from fastapi import FastAPI, Body
from typing import List
from .models import SentimentReviewEvent, SentimentResult, ContentMovieRequest, ContentMovieResponse, \
    CollaboMovieRequest, CollaboMovieResponse, ModelUpdateRequest, WordCloudRequest, NewMovieUpdateRequest
from .predict import sequential_movie_evaluation
from gensim.models import Word2Vec
from .word2vec_model import load_word2vec_model, get_similar_words_with_T
from .CollaboModel import updatePcaResultOptimal, recommendMovieByUserTime, load_initial_data
from .word2vecUpdate import model_update
from .wordcloud import wordcloudUpdate
import sqlite3
import asyncio
from contextlib import asynccontextmanager

BATCH_SIZE = 8192  # 배치 크기 설정

@asynccontextmanager
async def lifespan(app: FastAPI):
    global word2vec_model
    print("Loading initial data...")
    await load_initial_data()
    word2vec_model = load_word2vec_model()
    print("Initial data loaded.")
    yield
    print("Cleaning up resources...")

app = FastAPI(lifespan=lifespan)

@app.post("/content")
async def get_movie_with_content(request: List[ContentMovieRequest]):
    all_words = [req.actorName if req.actorName is not None else req.movieTitle + "^" + str(req.year) + "T" for req in request]
    sorted_movies = get_similar_words_with_T(word2vec_model, all_words)
    movie_objects = [ContentMovieResponse(movieTitle=title, movieYear=year) for title, year in sorted_movies]
    return movie_objects

@app.post("/collabo")
async def get_movie_with_collabo(userSeq: int = Body(...)):
    movies = recommendMovieByUserTime(userSeq)
    collabo_movie_responses = [CollaboMovieResponse(movieTitle=movie[0], movieYear=movie[1]) for movie in movies]
    return collabo_movie_responses

@app.post("/sentiment_score")
async def analyze_sentiment(reviews: List[SentimentReviewEvent]):
    print(f"Received reviews: {reviews}")
    sentiment_scores = sequential_movie_evaluation(reviews, batch_size=BATCH_SIZE)
    return sentiment_scores

@app.post("/update_model")
async def update_model(reviews: List[ModelUpdateRequest]):
    conn = sqlite3.connect('recommend.db')
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO review_info (review_seq, user_seq, movie_seq, review_rating, sentiment_score)
    VALUES (?, ?, ?, ?, ?)
    """
    delete_query = "DELETE FROM review_info WHERE review_seq = ?"
    try:
        for review in reviews:
            if review.action == "CREATE":
                cursor.execute(insert_query, (review.reviewSeq, review.userSeq, review.movieSeq, review.rating, review.sentimentScore))
            elif review.action == "DELETE":
                cursor.execute(delete_query, (review.reviewSeq,))
        conn.commit()
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()
    finally:
        conn.close()

@app.post("/word2vec_update")
async def word2vec_update():
    asyncio.create_task(model_update())
    global word2vec_model
    word2vec_model = load_word2vec_model()

@app.post("/word_cloud")
async def word_cloud_update(reviews: List[WordCloudRequest]):
    conn = sqlite3.connect('recommend.db')
    cursor = conn.cursor()
    insert_query = "INSERT INTO wordcloud (movie_seq, content) VALUES (?, ?)"
    try:
        for review in reviews:
            if review.content is not None and review.content.strip() != "":
                cursor.execute(insert_query, (review.movieSeq, review.content))
        conn.commit()
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()
    finally:
        conn.close()

@app.post("/wordcloud_update")
async def wordcloud_update():
    return wordcloudUpdate()

@app.post("/movie_update")
async def new_movieUpdate(movies: List[NewMovieUpdateRequest]):
    conn = sqlite3.connect('recommend.db')
    cursor = conn.cursor()
    insert_query = "INSERT INTO movie_info (movie_seq, movie_title, movie_year, genre) VALUES (?, ?, ?, ?)"
    insert_query2 = "INSERT INTO movie_actor (movie_seq, actor_name) VALUES (?, ?)"
    try:
        for movie in movies:
            cursor.execute(insert_query, (movie.movieSeq, movie.movieTitle, movie.movieYear, movie.genre))
            for actor in movie.actors:
                cursor.execute(insert_query2, (movie.movieSeq, actor.actorName))
        conn.commit()
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()
    finally:
        conn.close()

@app.get("/")
async def root():
    return {"message": "Sentiment analysis API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

