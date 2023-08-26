curl -X 'POST' \
  'http://0.0.0.0:4000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "model_key": "Audi",
  "mileage": 25000,
  "engine_power": 130,
  "fuel": "diesel",
  "paint_color": "blue",
  "car_type": "sedan",
  "private_parking_available": true,
  "has_gps": true,
  "has_air_conditioning": true,
  "automatic_car": true,
  "has_getaround_connect": true,
  "has_speed_regulator": true,
  "winter_tires": true
}'