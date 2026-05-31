import os

os.environ.setdefault("POSTGRES_DSN", "postgresql://nc:nc-dev-password@localhost:5432/nc")
os.environ.setdefault("MINIO_ACCESS_KEY", "ncadmin")
os.environ.setdefault("MINIO_SECRET_KEY", "ncadminpassword")
os.environ.setdefault("NC_SECRET_KEY", "test-secret")
