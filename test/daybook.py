import json
import requests

data = {
    'dishes': "{'House Salad': 3, 'Classic American Burger': 1}", 
    'num_of_customer': 3, 
    'rival_info': 'Restaurant: The Atlantic Bridge\n Number of customers: 3\n Customer Comments: [{\'day\': 1, \'name\': \'Frank\', \'score\': 6, \'content\': "The fusion cuisine at The Atlantic Bridge was interesting, but the flavors didn\'t quite hit the mark. The \'Shepherd\'s Pie with a Twist\' was unique but lacked depth of flavor, and the \'Fish and Chips Tacos\' were slightly soggy. However, the service was excellent and the 20% discount made the meal affordable. I\'d recommend this place for its novelty, but the execution could be improved."}] Menu: [{\'name\': "Shepherd\'s Pie with a Twist", \'price\': 15, \'description\': \'Traditional shepherd’s pie with a unique American BBQ flavor\'}, {\'name\': \'Bangers and Mash Burger\', \'price\': 14, \'description\': \'Fusion of a classic British dish into a juicy American burger\'}, {\'name\': \'Fish and Chips Tacos\', \'price\': 13, \'description\': \'Crispy fish and chips served in a soft taco shell\'}, {\'name\': \'Atlantic Bridge Special\', \'price\': 20, \'description\': \'Chef’s special dish of the day, a surprise fusion of British and American cuisine\'}]\n '}

data2= {
    'dishes': '{"Shepherd\'s Pie with a Twist": 3, \'Fish and Chips Tacos\': 2}', 
    'num_of_customer': 3, 
    'rival_info': "Restaurant: Stars and Stripes Diner\n Number of customers: 3\n Customer Comments: [] Menu: [{'name': 'Classic American Burger', 'price': 10, 'description': 'A juicy, all-beef patty topped with cheese, lettuce, tomato, and our signature sauce. Served with a side of crispy fries.'}, {'name': 'Steak and Potatoes', 'price': 18, 'description': 'Grilled steak cooked to your liking, served with seasoned potatoes and a side of fresh vegetables.'}, {'name': 'Apple Pie', 'price': 7, 'description': 'A sweet and tangy apple filling encased in a flaky, buttery crust. Served with a scoop of vanilla ice cream.'}, {'name': 'House Salad', 'price': 8, 'description': 'Crisp lettuce, fresh tomatoes, cucumbers, and carrots, topped with your choice of dressing.'}, {'name': 'Chicken Wings', 'price': 9, 'description': 'Crispy chicken wings tossed in our signature sauce. Served with celery and a side of blue cheese dip.'}, {'name': 'Iced Tea', 'price': 4, 'description': 'Refreshing iced tea sweetened just right. The perfect companion to any dish.'}]\n "}

data3 = {
    'dishes': {"Shepherd\'s Pie with a Twist": 3, "Fish and Chips Tacos": 2},
    'num_of_customer': 3,
    'rival_info': "Restaurant: Stars and Stripes Diner\n Number of customers: 3\n Customer Comments: [] Menu: [{'name': 'Classic American Burger', 'price': 10, 'description': 'A juicy, all-beef patty topped with cheese, lettuce, tomato, and our signature sauce. Served with a side of crispy fries.'}, {'name': 'Steak and Potatoes', 'price': 18, 'description': 'Grilled steak cooked to your liking, served with seasoned potatoes and a side of fresh vegetables.'}, {'name': 'Apple Pie', 'price': 7, 'description': 'A sweet and tangy apple filling encased in a flaky, buttery crust. Served with a scoop of vanilla ice cream.'}, {'name': 'House Salad', 'price': 8, 'description': 'Crisp lettuce, fresh tomatoes, cucumbers, and carrots, topped with your choice of dressing.'}, {'name': 'Chicken Wings', 'price': 9, 'description': 'Crispy chicken wings tossed in our signature sauce. Served with celery and a side of blue cheese dip.'}, {'name': 'Iced Tea', 'price': 4, 'description': 'Refreshing iced tea sweetened just right. The perfect companion to any dish.'}]\n "
}

data4 = {'dishes': '{}', 'num_of_customer': 1, 'rival_info': 'Restaurant: American Diner Delight\n Number of customers: 5\n Customer Comments: [{\'day\': 1, \'name\': \'Charlie\', \'score\': 6, \'content\': "The Classic Cheeseburger was satisfactory, but not exceptional. The New York Cheesecake was quite good. Overall, the food is decent but there\'s room for improvement. The prices are reasonable, making it a good option for affordable dining."}, {\'day\': 1, \'name\': \'Alice\', \'score\': 7, \'content\': "The dishes at American Diner Delight were quite good, especially the Southern Fried Chicken and BBQ Baby Back Ribs. However, the Cheeseburger was just average, and the Chocolate Milkshake could have been creamier. The service was decent, but there\'s room for improvement. Overall, a solid dining experience but not exceptional."}] Menu: [{\'name\': \'Classic Cheeseburger\', \'price\': 12, \'description\': \'Juicy beef patty with melted cheese, lettuce, tomato, onions, pickles, and our special sauce. Served with a side of fries.\'}, {\'name\': \'Southern Fried Chicken\', \'price\': 14, \'description\': \'Crispy, golden fried chicken seasoned with a blend of spices. Served with mashed potatoes and coleslaw.\'}, {\'name\': \'BBQ Baby Back Ribs\', \'price\': 18, \'description\': \'Tender baby back ribs smothered in our homemade BBQ sauce. Served with corn on the cob and coleslaw.\'}, {\'name\': \'New York Cheesecake\', \'price\': 8, \'description\': \'Creamy and smooth cheesecake with a graham cracker crust. Served with a side of whipped cream and strawberry sauce.\'}, {\'name\': \'Chocolate Milkshake\', \'price\': 6, \'description\': \'Rich and creamy milkshake made with premium chocolate ice cream.\'}]\n '}

def test(data):
    # data = json.dumps(data)
    response = requests.post("http://localhost:9000/daybook/", json=data)
    print(response.status_code)

    daybook = requests.get("http://localhost:9000/daybook/").json()
    print(daybook[0])

test(data3)