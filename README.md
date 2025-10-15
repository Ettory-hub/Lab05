# Lab05
## Run
pip install flask
python flaskHttpServer.py


## Example
curl -X POST -H "Content-Type: application/json" -d '{"name":"Alice","url":"http://good.site.com"}' http://localhost:5000/add-subscriber
curl http://localhost:5000/list-subscribers
curl -X POST -H "Content-Type: application/json" -d '{"subject":"New Post","payload":{"id":1}}' http://localhost:5000/publish
curl -X DELETE http://localhost:5000/delete-subscriber/Alice

## Tests
pip install pytest
pytest -q
