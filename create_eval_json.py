import json

# define qa_pairs
qa_pairs = [
    {"query_text": "What is the capital of Australia?", "expected_answer": ["Canberra"]},
    {"query_text": "When was the Eiffel Tower built?", "expected_answer": ["1889"]},
    {"query_text": "Who wrote the novel '1984'?", "expected_answer": ["George Orwell"]},
    {"query_text": "What is the tallest mountain in the world?", "expected_answer": ["Mount Everest"]},
    {"query_text": "What is the chemical formula for water?", "expected_answer": ["H2O"]},
    {"query_text": "Who was the first person to walk on the moon?", "expected_answer": ["Neil Armstrong"]},
    {"query_text": "What is the distance between the Earth and the Sun?", "expected_answer": ["Approximately 93 million miles", "About 150 million kilometers"]},
    {"query_text": "What is the largest ocean on Earth?", "expected_answer": ["Pacific Ocean"]},
    {"query_text": "When was the United Nations established?", "expected_answer": ["1945"]}, 
    {"query_text": "Who carried the weight of the world on his shoulders?", "expected_answer": ["Atlas"]}, 
]

qa_pairs.extend([
    {"query_text": "What is the square root of 256?", "expected_answer": ["16"]},
    {"query_text": "Who is the author of 'Pride and Prejudice'?", "expected_answer": ["Jane Austen"]},
    {"query_text": "What is the speed of light?", "expected_answer": ["299,792 kilometers per second", "186,282 miles per second"]},
    {"query_text": "When was the internet invented?", "expected_answer": ["1960s", "1969"]},
    {"query_text": "Who was the 16th President of the United States?", "expected_answer": ["Abraham Lincoln"]},
    {"query_text": "Which country has the largest population?", "expected_answer": ["China"]},
    {"query_text": "What is the main ingredient in chocolate?", "expected_answer": ["Cacao beans", "Cocoa beans"]},
    {"query_text": "Who invented the telephone?", "expected_answer": ["Alexander Graham Bell"]},
    {"query_text": "What is the human body's largest organ?", "expected_answer": ["Skin"]},
    {"query_text": "Who discovered penicillin?", "expected_answer": ["Alexander Fleming"]}
])

qa_pairs.extend([
    {"query_text": "What is the currency of Japan?", "expected_answer": ["Yen"]},
    {"query_text": "Who is the current Secretary-General of the United Nations?", "expected_answer": ["António Guterres"]},
    {"query_text": "What is the theory of relativity?", "expected_answer": ["A theory by Albert Einstein that relates space and time"]},
    {"query_text": "Who wrote 'The Odyssey'?", "expected_answer": ["Homer"]},
    {"query_text": "What is photosynthesis?", "expected_answer": ["The process used by plants to convert light energy, usually from the Sun, into chemical energy"]},
    {"query_text": "What is the holy book of Islam?", "expected_answer": ["Quran", "Koran"]},
    {"query_text": "Who invented the light bulb?", "expected_answer": ["Thomas Edison"]},
    {"query_text": "What is the largest mammal in the world?", "expected_answer": ["Blue whale"]},
    {"query_text": "What is the boiling point of water at sea level?", "expected_answer": ["100 degrees Celsius", "212 degrees Fahrenheit"]},
    {"query_text": "When was the first World War?", "expected_answer": ["1914-1918"]}
])

qa_pairs.extend([
    {"query_text": "What is the national bird of the United States?", "expected_answer": ["Bald Eagle"]},
    {"query_text": "Who wrote the play 'Romeo and Juliet'?", "expected_answer": ["William Shakespeare"]},
    {"query_text": "What is the speed of sound?", "expected_answer": ["Approximately 343 meters per second"]},
    {"query_text": "Who was the first woman to win a Nobel Prize?", "expected_answer": ["Marie Curie"]},
    {"query_text": "What is the capital of Brazil?", "expected_answer": ["Brasília"]},
    {"query_text": "What is the practice of farming both fish and plants together in an integrated system?", "expected_answer": ["Aquaponics"]},
    {"query_text": "Who sang it too late baby now it's too late?", "expected_answer": ["Carole King"]},
    {"query_text": "What is the main ingredient in sushi?", "expected_answer": ["Rice"]},
    {"query_text": "Who were the original members of the beatles", "expected_answer": ["Paul McCartney", "Pete Best", "George Harrison", "Stuart Sutcliffe", "John Lennon"]},
    {"query_text": "Who was the first Prime Minister of India?", "expected_answer": ["Jawaharlal Nehru"]}
])

qa_pairs.extend([
    {"query_text": "Who is the current monarch of the United Kingdom?", "expected_answer": ["Queen Elizabeth II"]},
    {"query_text": "what do the four colours of the uae flag represent?", "expected_answer": ["the Pan-Arab colors"]},
    {"query_text": "What is the smallest planet in our solar system?", "expected_answer": ["Mercury"]},
    {"query_text": "Who is the author of 'To Kill a Mockingbird'?", "expected_answer": ["Harper Lee"]},
    {"query_text": "What is the distance from Earth to Mars?", "expected_answer": ["Approximately 225 million kilometers", "Approximately 140 million miles"]},
    {"query_text": "How many teams are there in the premier league?", "expected_answer": ["20"]},
    {"query_text": "Who discovered gravity?", "expected_answer": ["Isaac Newton"]},
    {"query_text": "Who led the Israelites out of Egypt?", "expected_answer": ["Moses"]},
    {"query_text": "What is the national flower of France?", "expected_answer": ["Lily", "Fleur-de-lis"]},
    {"query_text": "When was the first Olympic Games held?", "expected_answer": ["1896"]}
])

qa_pairs.extend([
    {"query_text": "Which mountain range separates Europe from Asia?", "expected_answer": ["Ural Mountains"]},
    {"query_text": "Which chess piece can only move diagonally?", "expected_answer": ["Bishop"]},
    {"query_text": "What do you call a polygon with eight sides?", "expected_answer": ["Octagon"]},
    {"query_text": "Who is known as the 'Father of Medicine'?", "expected_answer": ["Hippocrates"]},
    {"query_text": "Who was the first female Prime Minister of the United Kingdom?", "expected_answer": ["Margaret Thatcher"]},
    {"query_text": "In which board game can you trade properties and try to bankrupt your opponents?", "expected_answer": ["Monopoly"]},
    {"query_text": "Which sea creature has the largest brain?", "expected_answer": ["Sperm whale"]},
    {"query_text": "Which organ is responsible for producing insulin?", "expected_answer": ["Pancreas"]},
    {"query_text": "In which movie will you hear the line, 'Here's looking at you, kid'?", "expected_answer": ["Casablanca"]},
    {"query_text": "In which country can you visit Machu Picchu?", "expected_answer": ["Peru"]}
])

qa_pairs.extend([
    {"query_text": "What is the Aurora Borealis commonly known as?", "expected_answer": ["Northern Lights"]},
    {"query_text": "Who is credited with proposing the theory of evolution by natural selection?", "expected_answer": ["Charles Darwin"]},
    {"query_text": "Which planet is known as the Red Planet?", "expected_answer": ["Mars"]},
    {"query_text": "What is the world's longest river?", "expected_answer": ["The Nile"]},
    {"query_text": "Who composed the music for the ballet 'Swan Lake'?", "expected_answer": ["Pyotr Ilyich Tchaikovsky"]},
    {"query_text": "Which element is represented by the chemical symbol 'Au'?", "expected_answer": ["Gold"]},
    {"query_text": "What is the primary gas found in Earth's atmosphere?", "expected_answer": ["Nitrogen"]},
    {"query_text": "Who is known for his theory of general relativity in physics?", "expected_answer": ["Albert Einstein"]},
    {"query_text": "What instrument is used to measure atmospheric pressure?", "expected_answer": ["Barometer"]},
    {"query_text": "Which famous play features the quote 'To be or not to be, that is the question'?", "expected_answer": ["Hamlet by William Shakespeare"]}
])

qa_pairs.extend([
    {"query_text": "Which mountain range runs along the eastern border of Chile?", "expected_answer": ["Andes"]},
    {"query_text": "What structure was originally built as a mausoleum for the Mughal emperor Shah Jahan's wife?", "expected_answer": ["Taj Mahal"]},
    {"query_text": "Who won the war of 1812 between russia and france?", "expected_answer": ["Russian victory"]},
    {"query_text": "In which year did the Titanic sink?", "expected_answer": ["1912"]},
    {"query_text": "Who is famous for his Mona Lisa and The Last Supper artworks?", "expected_answer": ["Leonardo da Vinci"]},
    {"query_text": "Who is the supreme leader of north korea", "expected_answer": ["Kim Jong-un"]},
    {"query_text": "Where is the erector spinae located in the body?", "expected_answer": ["the back"]},
    {"query_text": "Which famous physicist wrote the book 'A Brief History of Time'?", "expected_answer": ["Stephen Hawking"]},
    {"query_text": "Which language is primarily spoken in Brazil?", "expected_answer": ["Portuguese"]},
    {"query_text": "What ancient city was famously besieged for 10 years and is the setting for Homer's 'Iliad'?", "expected_answer": ["Troy"]}
])

qa_pairs.extend([
    {"query_text": "What is the largest desert in the world?", "expected_answer": ["Sahara"]},
    {"query_text": "Which ancient civilization is credited with the construction of pyramids?", "expected_answer": ["Ancient Egyptians"]},
    {"query_text": "Who formulated the three laws of motion?", "expected_answer": ["Sir Isaac Newton"]},
    {"query_text": "Which country is known as the Land of the Rising Sun?", "expected_answer": ["Japan"]},
    {"query_text": "What is the study of stars and celestial bodies called?", "expected_answer": ["Astronomy"]},
    {"query_text": "Who was the Greek god of war?", "expected_answer": ["Ares"]},
    {"query_text": "Which body part does an optometrist primarily care for?", "expected_answer": ["Eyes"]},
    {"query_text": "What is the primary ingredient in guacamole?", "expected_answer": ["Avocado"]},
    {"query_text": "In which city is the headquarters of the United Nations located?", "expected_answer": ["New York City"]},
    {"query_text": "Which element is represented by the chemical symbol 'Au'?", "expected_answer": ["Gold"]}
])

qa_pairs.extend([
    {"query_text": "Which animal is known as the 'king of the jungle'?", "expected_answer": ["Lion"]},
    {"query_text": "What is the smallest bone in the human body?", "expected_answer": ["Stapes","Ossicles"]},
    {"query_text": "What is the hardest known natural material on Earth?", "expected_answer": ["Diamond"]},
    {"query_text": "Who composed the 'Moonlight Sonata'?", "expected_answer": ["Ludwig van Beethoven"]},
    {"query_text": "What is the Japanese art of paper folding called?", "expected_answer": ["Origami"]},
    {"query_text": "Which city is famously associated with the legend of Dracula?", "expected_answer": ["Bran, Romania"]},
    {"query_text": "What's the study of insects called?", "expected_answer": ["Entomology"]},
    {"query_text": "Who is known for saying 'I think, therefore I am'?", "expected_answer": ["René Descartes"]},
    {"query_text": "Which Brazilian martial art combines elements of dance, acrobatics, and music?", "expected_answer": ["Capoeira"]},
    {"query_text": "What is the art of growing small trees in called?", "expected_answer": ["Bonsai"]}
])

# Convert qa_pairs to the previous format
qa_data = {
    "questions": []
}

for pair in qa_pairs:
    question_data = {
        "query_text": pair["query_text"],
        "expected_answer": pair["expected_answer"],
        "answer_given": "",
        "answer_correct": False
    }
    qa_data["questions"].append(question_data)


# Specify the data path where JSON gets stored
data_path = "/Users/jakob/Desktop/qa_dataset.json"  

# Save the data to the specified JSON file path
with open(data_path, 'w') as file:
    json.dump(qa_data, file, indent=4)

print(f"JSON file populated successfully at {data_path}!")
