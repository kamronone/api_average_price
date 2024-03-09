import mysql.connector
from loguru import logger
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from db_connect.db_connect import db_config
from starlette.responses import JSONResponse
from Models.Commercia import CommerciaDataAverage, CommerciaDataPercent
from Models.Property import PropertyDataAverage, PropertyDataPercent

app = FastAPI()


# Property average price
@app.post("/property_average_price")
def get_property_info(data: PropertyDataAverage):
    with mysql.connector.connect(**db_config) as connection:
        try:
            cursor = connection.cursor()

            query = (
                "SELECT price FROM average_price WHERE district = %s AND rooms = %s AND floor = %s AND floors = %s AND area BETWEEN %s AND %s AND type_flat = %s AND type_build = %s AND (repair = %s OR layout = %s OR bathroom = %s OR furniture = %s)"
            )
            cursor.execute(query, (
                data.district, data.rooms, data.floor, data.floors, data.area, data.max_area, data.type_flat,
                data.type_build, data.repair, data.layout, data.bathroom, data.furniture
            ))

            result = cursor.fetchall()
            logger.success(result)

            if result:
                average_price = sum(price[0] for price in result) / len(result)
                formatted_average_price = "{:,.0f}".format(average_price)

            if not result:
                raise HTTPException(status_code=404, detail="Данные с такими параметрами не найдены")

            property_info = {
                "price": formatted_average_price
            }
            return property_info

        except ValidationError as e:
            return JSONResponse(content={"detail": str(e)}, status_code=422)


# Property percent different
@app.post("/property_price_percent")
def get_property_percent_info(data: PropertyDataPercent):
    with mysql.connector.connect(**db_config) as connection:
        try:
            cursor = connection.cursor()

            query = (
                "SELECT price FROM average_price WHERE district = %s AND rooms = %s AND floor = %s AND floors = %s AND area BETWEEN %s AND %s AND type_flat = %s AND type_build = %s AND (repair = %s OR layout = %s OR bathroom = %s OR furniture = %s)"
            )
            cursor.execute(query, (
                data.district, data.rooms, data.floor, data.floors, data.area, data.max_area, data.type_flat,
                data.type_build, data.repair, data.layout, data.bathroom, data.furniture
            ))

            prices = cursor.fetchall()
            logger.success(prices)

            if prices:
                average_price = sum(price[0] for price in prices) / len(prices)
                formatted_average_price = "{:,.0f}".format(average_price)

                price = float(data.price)

                price_difference = price - average_price

                percent_difference = (price_difference / average_price) * 100 if average_price != 0 else 0
                percent_difference_price = "{:,.0f}".format(percent_difference)

                property_info_percent = {
                    "price": formatted_average_price,
                    "percent": percent_difference_price
                }
                return property_info_percent
            else:
                raise HTTPException(status_code=404, detail="Данные с такими параметрами не найдены")

        except ValidationError as e:
            return JSONResponse(content={"detail": str(e)}, status_code=422)


########################################################################################################################
# Commercia

# Commercia average price
@app.post("/commercia_average_price")
def get_property_info(data: CommerciaDataAverage):
    with mysql.connector.connect(**db_config) as connection:
        try:
            cursor = connection.cursor()

            query = (
                "SELECT price FROM average_price.commercia_price WHERE district = %s AND location = %s AND floor = %s AND floors = %s AND area BETWEEN %s AND %s AND type_flat = %s  AND (repair = %s OR parking = %s)"
            )
            cursor.execute(query, (
                data.district, data.location, data.floor, data.floors, data.area, data.max_area, data.type_build,
                data.repair, data.parking))

            result = cursor.fetchall()
            if result:
                average_price = sum(price[0] for price in result) / len(result)
                formatted_average_price = "{:,.0f}".format(average_price)

            if not result:
                raise HTTPException(status_code=404, detail="Данные с такими параметрами не найдены")
            logger.success(result)

            property_info = {
                "price": formatted_average_price
            }
            return property_info

        except ValidationError as e:
            return JSONResponse(content={"detail": str(e)}, status_code=422)


# Commercia percent different
@app.post("/commercia_price_percent")
def get_property_percent_info(data: CommerciaDataPercent):
    with mysql.connector.connect(**db_config) as connection:
        try:
            cursor = connection.cursor()

            query = (
                "SELECT price FROM average_price.commercia_price WHERE district = %s AND location = %s AND floor = %s AND floors = %s AND area BETWEEN %s AND %s AND type_flat = %s  AND (repair = %s OR parking = %s)"
            )
            cursor.execute(query, (
                data.district, data.location, data.floor, data.floors, data.area, data.max_area, data.type_build,
                data.repair, data.parking))

            prices = cursor.fetchall()
            logger.success(prices)

            if prices:
                average_price = sum(price[0] for price in prices) / len(prices)
                formatted_average_price = "{:,.0f}".format(average_price)

                price = float(data.price)

                price_difference = price - average_price

                percent_difference = (price_difference / average_price) * 100 if average_price != 0 else 0
                percent_difference_price = "{:,.0f}".format(percent_difference)

                property_info_percent = {
                    "price": formatted_average_price,
                    "percent": percent_difference_price
                }
                return property_info_percent
            else:
                raise HTTPException(status_code=404, detail="Данные с такими параметрами не найдены")

        except ValidationError as e:
            return JSONResponse(content={"detail": str(e)}, status_code=422)


@app.get("/")
def read_root():
    return {"message": "Привет хочешь узнать среднюю цену недвижимости"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)

