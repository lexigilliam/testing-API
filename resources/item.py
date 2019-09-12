from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store_id."
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}

# import sqlite3
# from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
# from flask import request
# from models.item import ItemModel

# class Item(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument(
#         'price',
#         type=float,
#         required=True,
#         help="This field cannot be left blank"
#     )
        
#     #get
#     @jwt_required() #going to have to authenticate before we call the get method
#     def get(self, name):
#         item = ItemModel.find_by_name(name)
        
#         if item:
#             return item.json() #returns the item itself
#         return {'message':'item does not exist'}, 404
    
#     #post
#     def post(self, name):
#         if ItemModel.find_by_name(name):
#             return {'message': f'an item with name {name} already exists'}, 400

#         data = Item.parser.parse_args()

#         data = request.get_json(silent=True) #no error, just returns none
#         # item = {'name':name, 'price': data['price']} want to return an item model object, not a dictionary
#         item = ItemModel(name, data['price'])

#         try:
#             # ItemModel.insert(item)
#             # item.insert() #doesn't needlessly call the class
#             item.save_to_db()
#         except:
#             return {'message':'an error occured inserting the item'}, 500 #internal server error
#         # items.append(item)

#         return item.json(), 201

#     #delete
#     def delete(self, name):
#         item = Item.find_by_name(name)
#         if item:
#             item.delete_from_db()

#         return {'message':'item deleted'}

#         # #connect, query, close to database
#         # connection = sqlite3.Connection('data.db')
#         # cursor = connection.cursor()
        
#         # query = "DELETE FROM items WHERE name=?"
#         # cursor.execute(query, (name,))

#         # connection.commit()
#         # connection.close()

#         # return {'message': 'item deleted'}

#     #put
#     def put(self, name):
#         data = Item.parser.parse_args()

#         item = ItemModel.find_by_name(name)
#         # updated_item = {name, 'price':data['price']}
#         # updated_item = ItemModel(name, data['price']) # need to make a model object, not dictionary

#         if item is None:
#             item = ItemModel(name, data['price'])
#             # try:
#             #     #updated_item.insert() #saves the item to the database
#             #     # ItemModel.insert(updated_item)
#             #     updated_item.insert()
#             # except:
#             #     return {'message':'an error occured inserting the item'}, 500
#             # # items.append(item)
#         else:
#             item.price = data['price']
        
#         item.save_to_db()
#             # try:
#             #     updated_item.update()
#             #     # ItemModel.update(updated_item)
#             # except:
#             #     return {'message':'an error occured updating the item'}, 500
#             # # item.update(data)
#         return item.json()


# class ItemList(Resource):
#     def get(self):
#         #connect, query, close to database
#         connection = sqlite3.Connection('data.db')
#         cursor = connection.cursor()
        
#         query = "SELECT * FROM items"
#         result = cursor.execute(query)
#         items =[]

#         for row in result:
#             items.append({'name':row[0],'price':row[1]})

#         connection.close() # no need to commit because we didn't change anything
        
#         return {'items':items}