// seed.js - generates pets.json with 100+ items
const fs = require('fs');

const petTypes = [
  { type: 'Dog', breeds: [
    'Golden Retriever', 'Labrador', 'Beagle', 'Poodle', 'Bulldog', 'Husky',
    'Dachshund', 'Shih Tzu', 'Pug', 'Boxer', 'Border Collie', 'Chihuahua',
    'German Shepherd', 'Cocker Spaniel', 'Doberman', 'Maltese', 'Dalmatian',
    'Samoyed', 'Corgi', 'Akita'
  ]},
  { type: 'Cat', breeds: [
    'Siamese', 'Persian', 'Maine Coon', 'Ragdoll', 'Bengal', 'Scottish Fold',
    'Sphynx', 'Birman', 'Abyssinian', 'British Shorthair', 'Russian Blue',
    'Norwegian Forest', 'Burmese', 'Tonkinese', 'Manx', 'Ocicat',
    'Turkish Angora', 'Somali', 'Balinese', 'Devon Rex'
  ]},
  { type: 'Rabbit', breeds: [
    'Holland Lop', 'Mini Rex', 'Lionhead', 'Dutch', 'Flemish Giant',
    'Angora', 'Harlequin', 'Himalayan', 'Californian', 'Rex'
  ]},
  { type: 'Bird', breeds: [
    'Cockatiel', 'Parakeet', 'African Grey', 'Macaw', 'Conure',
    'Lovebird', 'Cockatoo', 'Canary', 'Finch', 'Eclectus'
  ]},
  { type: 'Hamster', breeds: [
    'Syrian', 'Dwarf Campbell', 'Roborovski', 'Chinese', 'Winter White'
  ]},
];

// Unsplash search photo URLs by animal type (stable collection URLs)
const imagesByType = {
  Dog: [
    'https://images.unsplash.com/photo-1552053831-71594a27632d?w=600',
    'https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=600',
    'https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=600',
    'https://images.unsplash.com/photo-1518717758536-85ae29035b6d?w=600',
    'https://images.unsplash.com/photo-1561037404-61cd46aa615b?w=600',
    'https://images.unsplash.com/photo-1530281700549-e82e7bf110d6?w=600',
    'https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=600',
    'https://images.unsplash.com/photo-1477884213360-7e9d7dcc1e48?w=600',
    'https://images.unsplash.com/photo-1534361960057-19f4e9c5d8d5?w=600',
    'https://images.unsplash.com/photo-1608096299210-db7e38487075?w=600',
    'https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=600',
    'https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?w=600',
    'https://images.unsplash.com/photo-1596492784531-6e6eb5ea9993?w=600',
    'https://images.unsplash.com/photo-1508532566027-b2032cd8a715?w=600',
    'https://images.unsplash.com/photo-1601979031925-424e53b6caaa?w=600',
    'https://images.unsplash.com/photo-1576201836106-db1758fd1c97?w=600',
    'https://images.unsplash.com/photo-1517849845537-4d257902454a?w=600',
    'https://images.unsplash.com/photo-1568572933382-74d440642117?w=600',
    'https://images.unsplash.com/photo-1592754862816-1a21a4ea2281?w=600',
    'https://images.unsplash.com/photo-1574144611937-0df059b5ef3e?w=600',
  ],
  Cat: [
    'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600',
    'https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=600',
    'https://images.unsplash.com/photo-1592194996308-7b43878e84a6?w=600',
    'https://images.unsplash.com/photo-1495360010541-f48722b34f7d?w=600',
    'https://images.unsplash.com/photo-1518791841217-8f162f1912da?w=600',
    'https://images.unsplash.com/photo-1561948955-570b270e7c36?w=600',
    'https://images.unsplash.com/photo-1526336024174-e58f5cdd8e13?w=600',
    'https://images.unsplash.com/photo-1511044568932-338ceba04645?w=600',
    'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=600',
    'https://images.unsplash.com/photo-1533743983669-94fa5c4338ec?w=600',
    'https://images.unsplash.com/photo-1543852786-1cf6624b9987?w=600',
    'https://images.unsplash.com/photo-1570824104453-508955ab713e?w=600',
    'https://images.unsplash.com/photo-1548802673-380ab8ebc7b7?w=600',
    'https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?w=600',
    'https://images.unsplash.com/photo-1529778873920-4da4926a72c2?w=600',
    'https://images.unsplash.com/photo-1513245543132-31f507417b26?w=600',
    'https://images.unsplash.com/photo-1471286174890-9c112ffca5b4?w=600',
    'https://images.unsplash.com/photo-1501820488136-72669149e0d4?w=600',
    'https://images.unsplash.com/photo-1425082661705-1834bfd09dca?w=600',
    'https://images.unsplash.com/photo-1520315342629-6ea920342047?w=600',
  ],
  Rabbit: [
    'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=600',
    'https://images.unsplash.com/photo-1425082661705-1834bfd09dca?w=600',
    'https://images.unsplash.com/photo-1452857297128-d9c29adba80b?w=600',
    'https://images.unsplash.com/photo-1535241749838-299277b6305f?w=600',
    'https://images.unsplash.com/photo-1549480017-d76466a4b7e8?w=600',
    'https://images.unsplash.com/photo-1580759003043-b678cf5a7b5c?w=600',
    'https://images.unsplash.com/photo-1606425271394-c3ca9aa1fc06?w=600',
    'https://images.unsplash.com/photo-1591488320449-011701bb6704?w=600',
    'https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=600',
    'https://images.unsplash.com/photo-1622018462074-27e4754a1a88?w=600',
  ],
  Bird: [
    'https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=600',
    'https://images.unsplash.com/photo-1522858547137-f1dcec554f55?w=600',
    'https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=600',
    'https://images.unsplash.com/photo-1554456854-55a089fd4cb2?w=600',
    'https://images.unsplash.com/photo-1567306295427-94503f8300d5?w=600',
    'https://images.unsplash.com/photo-1606851091851-e8c8c0fca5ba?w=600',
    'https://images.unsplash.com/photo-1529467713831-a738c1524e5a?w=600',
    'https://images.unsplash.com/photo-1549365067-37d1aacc5e21?w=600',
    'https://images.unsplash.com/photo-1604237834684-d2b72b36c5f2?w=600',
    'https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=600',
  ],
  Hamster: [
    'https://images.unsplash.com/photo-1548767797-d8c844163c4a?w=600',
    'https://images.unsplash.com/photo-1425082661705-1834bfd09dca?w=600',
    'https://images.unsplash.com/photo-1609253437024-b47b37f6e9dd?w=600',
    'https://images.unsplash.com/photo-1518796745738-41048802f99a?w=600',
    'https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=600',
  ],
};

const names = [
  'Buddy','Max','Bella','Luna','Charlie','Lucy','Cooper','Daisy','Rocky','Lola',
  'Oliver','Zoe','Milo','Sadie','Leo','Molly','Jack','Bailey','Duke','Maggie',
  'Toby','Sophie','Teddy','Chloe','Riley','Lily','Bear','Roxy','Tucker','Gracie',
  'Oscar','Coco','Murphy','Stella','Buster','Nala','Bentley','Ellie','Zeus','Penny',
  'Ginger','Rusty','Peanut','Willow','Bruno','Hazel','Shadow','Rosie','Finn','Ruby',
  'Simba','Lulu','Thor','Violet','Jasper','Mia','Atlas','Ivy','Caesar','Nova',
  'Archie','Olive','Louie','Scout','Sam','Amber','Rex','Pepper','Winston','Cleo',
  'Chester','Pearl','Ranger','Abby','Boomer','Elsa','Gus','Athena','Beau','Freya',
  'Jake','Xena','Ace','Poppy','Captain','Millie','Diesel','Aurora','Hunter','Cali',
  'Memphis','Fiona','Dexter','Sasha','Phoenix','Callie','Bruno','Gemma','Diesel','Skye'
];

const descriptions = [
  'Loves cuddles and long naps in the sun.',
  'Energetic and playful, great with kids.',
  'Gentle giant looking for a cozy home.',
  'Super friendly and loves belly rubs.',
  'Shy at first but incredibly loyal once comfortable.',
  'Mischievous and curious — always exploring.',
  'Loves outdoor adventures and fetch.',
  'A total lap pet who adores TV time.',
  'Incredibly gentle with a heart of gold.',
  'Playful and social, gets along with everyone.',
  'Loves treats and showing off tricks.',
  'Calm and patient — the perfect companion.',
  'Bouncy and affectionate, full of personality.',
  'Incredibly smart and learns new tricks fast.',
  'Loves water and outdoor activities.',
  'The calmest soul you will ever meet.',
  'Cheeky and charming — steals your heart instantly.',
  'Snuggly and sweet, loves couch days.',
  'Bold and curious, loves new experiences.',
  'Old soul with puppy energy — best of both worlds.',
];

const items = [];
let id = 1;

for (const { type, breeds } of petTypes) {
  const images = imagesByType[type];
  breeds.forEach((breed, breedIdx) => {
    const name = names[(id - 1) % names.length];
    const description = descriptions[(id - 1) % descriptions.length];
    const image = images[breedIdx % images.length];
    items.push({
      id: String(id),
      name,
      type,
      breed,
      label: `${name} — ${breed}`,
      description,
      age: `${Math.floor(Math.random() * 8) + 1} ${Math.random() > 0.5 ? 'year' : 'months'} old`,
      image,
    });
    id++;
  });
}

fs.writeFileSync('./pets.json', JSON.stringify(items, null, 2));
console.log(`Generated ${items.length} pets.`);
