## Deployment

```bash
docker-compose up --build
```

## Documentation

```bash
http://0.0.0.0:8000/api/schema/swagger/
```

## APi Walkthrough

```
/api/flights/ - flights list with necessaty search and filtering.
/api/airports/ - airports list with nested flights, number of aircraft in flight and time in flight, filtering by time period.
```

## Requirements

```
requirements.txt - minimal set of dependencies to run server.
requirements-dev.txt - extra dependencies for type checking, linting.
```
