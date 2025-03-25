## Family Cloud

### Project Destriction

The purpose of this project is to create a server where users can upload their photos and videos.
This would serve as backup space for photos and videos from the users phone.

### Useful commands

- Run redis using docker:

```
$ docker run -d --name redis-server -p 6379:6379 redis
```

- Run celery with eventlet (for Windows)

```
$ celery -A app.celery worker --pool=eventlet --loglevel=info
```

- Run celery task manually

```
$ celery -A app.celery call upload
```