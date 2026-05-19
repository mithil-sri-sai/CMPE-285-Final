import json, random

pet_types = [
    ("Dog", [
        "Golden Retriever","Labrador","Beagle","Poodle","Bulldog","Husky",
        "Dachshund","Shih Tzu","Pug","Boxer","Border Collie","Chihuahua",
        "German Shepherd","Cocker Spaniel","Doberman","Maltese","Dalmatian",
        "Samoyed","Corgi","Akita","Rottweiler","Great Dane","Shiba Inu",
        "Australian Shepherd","Basset Hound"
    ]),
    ("Cat", [
        "Siamese","Persian","Maine Coon","Ragdoll","Bengal","Scottish Fold",
        "Sphynx","Birman","Abyssinian","British Shorthair","Russian Blue",
        "Norwegian Forest","Burmese","Tonkinese","Manx","Ocicat",
        "Turkish Angora","Somali","Balinese","Devon Rex","American Shorthair",
        "Exotic Shorthair","Himalayan","Savannah","Selkirk Rex"
    ]),
    ("Rabbit", [
        "Holland Lop","Mini Rex","Lionhead","Dutch","Flemish Giant",
        "Angora","Harlequin","Himalayan","Californian","Rex",
        "New Zealand","Chinchilla","Mini Lop","Polish","Silver Marten"
    ]),
    ("Bird", [
        "Cockatiel","Parakeet","African Grey","Macaw","Conure",
        "Lovebird","Cockatoo","Canary","Finch","Eclectus",
        "Sun Conure","Quaker Parrot","Budgerigar","Indian Ringneck","Caique"
    ]),
    ("Hamster", [
        "Syrian","Dwarf Campbell","Roborovski","Chinese","Winter White",
        "European","Golden","Fancy","Teddy Bear","Black Bear"
    ]),
    ("Guinea Pig", [
        "American","Abyssinian","Peruvian","Silkie","Teddy",
        "Rex","Coronet","White Crested","Merino","Texel"
    ]),
]

# Stable, hotlink-friendly pet photos (Unsplash URLs rot; these use lock=id per pet)
FLICKR_TAG = {
    "Dog": "dog",
    "Cat": "cat",
    "Rabbit": "rabbit",
    "Bird": "bird",
    "Hamster": "hamster",
    "Guinea Pig": "guineapig",
}

def image_url(pet_type: str, pid: int) -> str:
    if pet_type == "Dog":
        return f"https://placedog.net/600/800?id={pid}"
    # IDs 80–100 use dedicated cat photos (clearer than hamster/guinea pig placeholders)
    if 80 <= pid <= 100:
        return f"https://placecats.com/600/800?id={pid}"
    tag = FLICKR_TAG[pet_type]
    return f"https://loremflickr.com/600/800/{tag}?lock={pid}"


names = [
    "Buddy","Max","Bella","Luna","Charlie","Lucy","Cooper","Daisy","Rocky","Lola",
    "Oliver","Zoe","Milo","Sadie","Leo","Molly","Jack","Bailey","Duke","Maggie",
    "Toby","Sophie","Teddy","Chloe","Riley","Lily","Bear","Roxy","Tucker","Gracie",
    "Oscar","Coco","Murphy","Stella","Buster","Nala","Bentley","Ellie","Zeus","Penny",
    "Ginger","Rusty","Peanut","Willow","Bruno","Hazel","Shadow","Rosie","Finn","Ruby",
    "Simba","Lulu","Thor","Violet","Jasper","Mia","Atlas","Ivy","Caesar","Nova",
    "Archie","Olive","Louie","Scout","Sam","Amber","Rex","Pepper","Winston","Cleo",
    "Chester","Pearl","Ranger","Abby","Boomer","Elsa","Gus","Athena","Beau","Freya",
    "Jake","Xena","Ace","Poppy","Captain","Millie","Diesel","Aurora","Hunter","Cali",
    "Memphis","Fiona","Dexter","Sasha","Phoenix","Callie","Titan","Gemma","Duke","Skye"
]

descriptions = [
    "Loves cuddles and long naps in the sun.",
    "Energetic and playful, great with kids.",
    "Gentle giant looking for a cozy home.",
    "Super friendly and loves belly rubs.",
    "Shy at first but incredibly loyal once comfortable.",
    "Mischievous and curious — always exploring.",
    "Loves outdoor adventures and fetch.",
    "A total lap pet who adores TV time.",
    "Incredibly gentle with a heart of gold.",
    "Playful and social, gets along with everyone.",
    "Loves treats and showing off tricks.",
    "Calm and patient — the perfect companion.",
    "Bouncy and affectionate, full of personality.",
    "Incredibly smart and learns new tricks fast.",
    "Loves water and outdoor activities.",
    "The calmest soul you will ever meet.",
    "Cheeky and charming — steals your heart instantly.",
    "Snuggly and sweet, loves couch days.",
    "Bold and curious, loves new experiences.",
    "Old soul with puppy energy — best of both worlds.",
]

ages_months = [2,3,4,5,6,8,10,12]
ages_years = [1,2,3,4,5,6,7,8]

items = []
pid = 1
for (pet_type, breeds) in pet_types:
    for i, breed in enumerate(breeds):
        name = names[(pid - 1) % len(names)]
        desc = descriptions[(pid - 1) % len(descriptions)]
        image = image_url(pet_type, pid)
        if random.random() > 0.5:
            age = f"{random.choice(ages_years)} yr old"
        else:
            age = f"{random.choice(ages_months)} mo old"
        items.append({
            "id": str(pid),
            "name": name,
            "type": pet_type,
            "breed": breed,
            "label": f"{name} · {breed}",
            "description": desc,
            "age": age,
            "image": image,
        })
        pid += 1

with open("pets.json", "w") as f:
    json.dump(items, f, indent=2)

print(f"Generated {len(items)} pets.")
