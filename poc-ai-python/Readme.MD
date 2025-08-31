pip install psycopg2-binary  -- install postgresql
pip install psycopg2-binary pgvector -- to understand vector

CREATE TABLE images (
id SERIAL PRIMARY KEY,
uuid VARCHAR(255) UNIQUE,
embedding VECTOR(512)
);

pip install PyYAML

pip install requests Pillow sentence-transformers
pip install mysql-connector-python
pip install Flask