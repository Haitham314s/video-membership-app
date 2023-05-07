# video-membership-app

## To run the video membership project:

Use the code

```commandline
    uvicron app.main:app --reload --port 8000
```

## Env variables requiered to run this project

ASTRADB_KEYSPACE=video_membership_app
ASTRADB_CLIENT_ID=
ASTRADB_CLIENT_SECRET=
SECRET_KEY=
JWT_ALGORITHM=HS256
SESSION_DURATION=86400

ALGOLIA_API_KEY=
ALGOLIA_APP_ID=
ALGOLIA_INDEX_NAME=video_membership_index