receive_data_1 = "jedi,250,250,3.51324,255.0.0,20,10;champ,500,250,4.3,0.255.0,20,10/50,60;120,300;530,90".encode()

data = receive_data_1.decode("utf-8")
player_string = data.split("/")[0]
food_string = data.split("/")[1]

player_list = player_string.split(";")
for player in player_list:
    name, x, y, d, c, r, score = player.split(",")
    c = tuple(map(int,c.split(".")))
    print(f"Player: name: {name}, x_position: {x}, y_position: {y}, direction_radian: {d}, color: {c}, radius: {r}, score: {score}")
    

food_list = food_string.split(";")
for food in food_list:
    x, y = food.split(",")
    print(f"Food: x: {x}, y: {y}")