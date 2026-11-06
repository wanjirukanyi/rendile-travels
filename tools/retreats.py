#!/usr/bin/env python3
"""Generate the 2027 retreat pages (March to December) from one data list.

Run from the rendile-travels folder:   python3 tools/retreats.py
Writes src/pages/<slug>.astro for every retreat below. January and February
are hand written pages (new-year-new-you, self-love-retreat) and are not touched.

House rules for copy: no hyphens or dashes, never state a group size or how
often retreats run, women only, aspirational.
"""
import html, json, os

R = [
 dict(slug="womens-month-safari", code="mar", month="March", mon="Mar", region="Africa",
  title="Women's Month Safari", sub="Celebrate International Women's Day in the Maasai Mara",
  dates="4 to 9 Mar 2027", days=6, place="Maasai Mara, Kenya", price="5,400",
  seo="women's safari Kenya, Maasai Mara women's retreat, International Women's Day trip, women only safari, luxury safari for women",
  lead="Spend International Women's Day where the plains run to the horizon. Six days in a luxury tented camp in the Maasai Mara, with women guides, Maasai women's collectives and a celebration dinner under the stars.",
  body=["Days follow the rhythm of the bush: early game drives when the big cats are moving, long lunches in camp, golden hour sundowners. Along the way you'll meet the women who make this land work, from guides and rangers to the beadwork artists of the Mara.",
        "Come to see lions and leopards. Leave with a deeper sense of what women can build, together."],
  theme="Celebrate. Witness. Connect.",
  pillars=[("Celebrate women","An International Women's Day dinner in the bush, toasts to the women who shaped you, and time with women guides and rangers leading conservation in the Mara."),
           ("Witness the wild","Twice daily game drives in big cat country, a dawn hot air balloon over the plains and a champagne breakfast where you land."),
           ("Connect deeply","A morning with a Maasai women's beadwork collective, evening circles by the fire and the kind of conversations that only happen far from home.")],
  gallery=[("A Maasai woman in traditional beadwork, smiling"),("Hot air balloons over the savanna at sunrise"),("A woman relaxing in a luxury safari tent"),("A woman in a safari hat on the plains")],
  daylist=[
   ("Karibu to the Mara","Fly from Nairobi to the Maasai Mara in the morning. Settle into your tent, enjoy lunch overlooking the plains, then head out on your first afternoon game drive and a sundowner on a hill.","Luxury tented camp, Maasai Mara","Lunch, dinner"),
   ("Big cat country","A full day on the plains with your guide, tracking lions, cheetahs and leopards, with a picnic lunch under an acacia. Evening circle by the fire: what does being a woman mean to you right now?","Luxury tented camp","All"),
   ("Women of the Mara","Spend the morning with a Maasai women's beadwork collective, learning their craft and their stories. Afternoon at leisure, then an evening game drive.","Luxury tented camp","All"),
   ("Above the plains","Rise before dawn for an optional hot air balloon flight over the Mara, landing to a champagne bush breakfast. A slow afternoon in camp with a massage or a book.","Luxury tented camp","All"),
   ("International Women's Day","A celebration day: a game drive with women rangers, a talk on women in conservation and a candlelit bush dinner with toasts to the women who brought you here.","Luxury tented camp","All"),
   ("Kwaheri","A final sunrise game drive and breakfast in camp, then fly back to Nairobi for your onward journey.","","Breakfast")],
  incl=["5 nights in a luxury tented camp, all meals","Return flights Nairobi to the Maasai Mara","Twice daily game drives with expert guides","Park and conservancy fees","Visit to a Maasai women's beadwork collective","International Women's Day bush dinner","Evening sharing circles","Female Rendile host throughout &amp; all gratuities"],
  extra="Hot air balloon flight available as an add on.",
  cta=("Celebrate her, celebrate you.","Spend International Women's Day in the wild. Tell us a little about you and we'll hold your place.")),

 dict(slug="spiritual-reset-bali", code="apr", month="April", mon="Apr", region="Asia",
  title="The Spiritual Reset", sub="Yoga, temple blessings and renewal in Bali",
  dates="12 to 19 Apr 2027", days=8, place="Ubud &amp; Uluwatu, Bali", price="4,600",
  seo="Bali retreat for women, women's yoga retreat Bali, spiritual retreat Ubud, wellness retreat Bali, women only retreat Asia",
  lead="A week to reset body and soul on the Island of the Gods. Start in the jungle around Ubud with daily yoga, a sacred water blessing and a visit to a traditional healer, then finish on the cliffs of Uluwatu with the ocean at your feet.",
  body=["Bali has been drawing seekers for centuries, and it's easy to see why. Rice terraces glow green at sunrise, temples fill with offerings of frangipani and incense, and every day seems to slow down a little more.",
        "This is a gentle week. Come as you are, practise as much or as little as you like, and leave lighter than you arrived."],
  theme="Cleanse. Bless. Open.",
  pillars=[("Cleanse","Daily yoga and meditation in an open air shala, nourishing plant based food and a traditional water purification ceremony at Tirta Empul temple."),
           ("Bless","A private session with a Balinese healer, an offering making class with local women and a sound healing ceremony in the jungle."),
           ("Open","Sunrise among the rice terraces, sunset at Uluwatu temple and slow afternoons by an infinity pool overlooking the Indian Ocean.")],
  gallery=["A woman at the Tirta Empul water purification ceremony","A woman sitting at a Balinese temple","A woman meditating in a tropical garden","A hand holding a frangipani flower offering"],
  daylist=[
   ("Selamat datang","Met at Denpasar airport and driven into the hills around Ubud. Settle into your jungle villa, then gather for a welcome dinner and an evening intention setting circle.","Jungle villa, Ubud","Dinner"),
   ("Rice terraces &amp; first practice","Sunrise yoga, then a walk through the Tegallalang rice terraces before the crowds. Afternoon at the spa with a traditional Balinese massage.","Jungle villa, Ubud","All"),
   ("Sacred water","Dress in a sarong for a water purification blessing at Tirta Empul temple, guided by a local priest. In the afternoon, learn to make canang sari offerings with Balinese women.","Jungle villa, Ubud","All"),
   ("The healer","A private session with a traditional Balinese healer, then a free afternoon to rest, swim or explore Ubud's markets and cafes. Evening sound healing ceremony.","Jungle villa, Ubud","All"),
   ("Ubud to the coast","Morning yoga, then transfer south to the cliffs of Uluwatu. Settle into your clifftop villa and watch the sun set over the ocean.","Clifftop villa, Uluwatu","All"),
   ("Ocean days","Slow mornings, beach clubs and secret coves. An optional surf lesson for beginners, or simply the pool and a book.","Clifftop villa, Uluwatu","All"),
   ("Sunset at the temple","A final yoga practice and closing circle, then sunset at Uluwatu temple with the Kecak fire dance, followed by a farewell seafood dinner on the sand.","Clifftop villa, Uluwatu","All"),
   ("Go gently","A last swim and breakfast, then transfer to the airport for your onward flight.","","Breakfast")],
  incl=["7 nights in boutique villas in Ubud and Uluwatu","All transfers in Bali","Daily yoga and meditation","Water purification blessing at Tirta Empul","Private session with a Balinese healer","Offering making class and sound healing ceremony","One Balinese massage per guest","Most meals as shown","Female Rendile host throughout &amp; all gratuities"],
  extra="",
  cta=("Come home to yourself.","Eight days of yoga, blessings and ocean light. Tell us a little about you and we'll hold your place.")),

 dict(slug="la-dolce-vita-amalfi", code="may", month="May", mon="May", region="Europe",
  title="La Dolce Vita", sub="Food, wine and slow living on the Amalfi Coast",
  dates="17 to 23 May 2027", days=7, place="Amalfi Coast, Italy", price="6,800",
  seo="Amalfi Coast women's retreat, Italy retreat for women, women's trip Positano, food and wine retreat Italy, women only travel Europe",
  lead="Lemon groves, long lunches and the bluest water you've ever seen. Seven days on the Amalfi Coast learning the Italian art of living well: cooking with a local nonna, sailing to Capri and toasting the sunset from a cliffside terrace.",
  body=["May is the sweet spot on the coast: warm days, wildflowers on the hillsides and the summer crowds still to come. We stay in a family run boutique hotel above Positano, with the sea glittering below your balcony.",
        "There's nothing to prove here. Just good food, good wine and good company, the way the Italians intended."],
  theme="Savour. Sail. Celebrate.",
  pillars=[("Savour","A hands on cooking class with a local nonna in a lemon grove, a private wine tasting in the hills and lunches that last all afternoon."),
           ("Sail","A private boat day to Capri, swimming in hidden coves and the Blue Grotto, with prosecco on deck as the sun goes down."),
           ("Celebrate","Gardens and music in Ravello, the Path of the Gods walk and a farewell dinner on a terrace above the sea.")],
  gallery=["The colourful houses of Positano tumbling to the sea","Women learning to make fresh pasta","A boat on the turquoise water of the Amalfi Coast","A woman looking out over the Mediterranean"],
  daylist=[
   ("Benvenute","Met in Naples and driven along the coast road to Positano. Settle into your boutique hotel, then a welcome aperitivo on the terrace as the lights come on.","Boutique hotel, Positano","Dinner"),
   ("The lemon grove","A morning cooking class with a local nonna in her family lemon grove, making pasta and limoncello, then a long lunch under the pergola.","Boutique hotel, Positano","All"),
   ("Capri by sea","A private boat day: swim in hidden coves, visit the Blue Grotto and wander Capri's piazzetta before sailing home at sunset.","Boutique hotel, Positano","Breakfast, lunch"),
   ("Ravello","Drive up to Ravello for the gardens of Villa Rufolo and Villa Cimbrone, then a private wine tasting in the hills.","Boutique hotel, Positano","All"),
   ("The Path of the Gods","An optional morning walk on the Path of the Gods with views down the whole coast, or a slow morning at the beach club. Free afternoon.","Boutique hotel, Positano","Breakfast, dinner"),
   ("Dolce far niente","The sweetness of doing nothing: a spa morning, a closing circle and a farewell dinner on a cliffside terrace.","Boutique hotel, Positano","All"),
   ("Arrivederci","Breakfast with a view, then transfer to Naples for your onward flight.","","Breakfast")],
  incl=["6 nights in a boutique hotel in Positano","All transfers from Naples and along the coast","Cooking class with a local nonna in a lemon grove","Private boat day to Capri with lunch","Ravello gardens visit and private wine tasting","Spa morning","Most meals as shown","Female Rendile host throughout &amp; all gratuities"],
  extra="",
  cta=("Life is sweet. Taste it.","Seven days of sun, sea and Italian living. Tell us a little about you and we'll hold your place.")),

 dict(slug="desert-and-hammam-morocco", code="jun", month="June", mon="Jun", region="Middle East &amp; North Africa",
  title="Desert &amp; Hammam", sub="Riads, beauty rituals and a night in the Sahara",
  dates="7 to 13 Jun 2027", days=7, place="Marrakech &amp; Sahara, Morocco", price="4,900",
  seo="Morocco women's retreat, Marrakech retreat for women, Sahara desert trip women, hammam retreat, women only travel North Africa",
  lead="From the rose scented courtyards of Marrakech to the silence of the Sahara. Seven days of riad living, hammam and argan rituals, souk treasure hunting and a night in a luxury desert camp under more stars than you've ever seen.",
  body=["Morocco is a feast for every sense: spice stalls and lantern light, tiled courtyards and mint tea, then the sudden, enormous quiet of the dunes.",
        "We travel in comfort with a trusted local guide, and every night ends somewhere beautiful."],
  theme="Indulge. Discover. Breathe.",
  pillars=[("Indulge","A traditional hammam and argan oil ritual, a rooftop cooking class and evenings in a beautiful riad in the heart of the medina."),
           ("Discover","The souks with a local stylist, the Jardin Majorelle and the Atlas Mountains, with tea in a Berber family home along the way."),
           ("Breathe","A camel ride at sunset into the Merzouga dunes, a night in a luxury desert camp and sunrise over the Sahara.")],
  gallery=["A woman framed by a carved Moroccan archway","A woman relaxing in a tiled hammam","A woman in the colourful souks of Marrakech","Camels crossing the Sahara dunes"],
  daylist=[
   ("Marhaba, Marrakech","Met at the airport and taken to your riad in the medina. Mint tea in the courtyard, then a welcome dinner on the rooftop.","Boutique riad, Marrakech","Dinner"),
   ("Hammam &amp; souks","A traditional hammam with black soap, rhassoul clay and argan oil, then an afternoon in the souks with a local stylist to find your treasures.","Boutique riad, Marrakech","Breakfast, dinner"),
   ("Gardens &amp; spice","The Jardin Majorelle in the morning, then a rooftop cooking class making tagine and Moroccan pastries.","Boutique riad, Marrakech","All"),
   ("Over the Atlas","Cross the High Atlas Mountains, stopping for tea with a Berber family and the ancient kasbah of Ait Benhaddou. Overnight in the Dades Valley.","Boutique kasbah hotel, Dades","All"),
   ("Into the Sahara","Drive through palm oases to Merzouga, then ride camels into the dunes at sunset to your luxury desert camp. Dinner and music under the stars.","Luxury desert camp, Merzouga","All"),
   ("Sunrise in the dunes","Wake for sunrise over the Sahara, breakfast in camp, then travel back toward Ouarzazate for your flight to Marrakech and a farewell dinner.","Boutique riad, Marrakech","All"),
   ("Beslama","A last breakfast in the riad courtyard, then transfer to the airport.","","Breakfast")],
  incl=["4 nights in a boutique riad, 1 night in a kasbah hotel, 1 night in a luxury desert camp","All transfers and private driving with a local guide","Flight Ouarzazate to Marrakech","Traditional hammam and argan oil ritual","Souk visit with a local stylist","Rooftop cooking class","Camel ride into the Merzouga dunes","Most meals as shown","Female Rendile host throughout &amp; all gratuities"],
  extra="",
  cta=("Lose yourself, beautifully.","Seven days from the medina to the Sahara. Tell us a little about you and we'll hold your place.")),

 dict(slug="great-migration-retreat", code="jul", month="July", mon="Jul", region="Africa",
  title="The Great Migration", sub="Wildlife and wonder at the height of the season",
  dates="19 to 24 Jul 2027", days=6, place="Maasai Mara, Kenya", price="6,200",
  seo="Great Migration women's safari, Maasai Mara July, women only safari Kenya, luxury safari for women, river crossing safari",
  lead="The greatest wildlife show on earth, at its peak. Six days in the Maasai Mara as more than a million wildebeest and zebra pour across the plains and plunge through the Mara River, with lions never far behind.",
  body=["July in the Mara is pure drama: dust clouds on the horizon, herds stretching as far as you can see and the heart stopping moment a river crossing begins.",
        "Our camp sits right on the migration's path, so the action often comes to you. Evenings are for the fire, the stars and the women you came with."],
  theme="Wonder. Witness. Wind down.",
  pillars=[("Wonder","Full days following the herds with an expert guide, waiting by the Mara River for the crossings and tracking the big cats that follow."),
           ("Witness","A dawn hot air balloon over the moving herds and a champagne breakfast on the plains."),
           ("Wind down","Massages in camp, bush dinners by lantern light and evening circles around the fire.")],
  gallery=["Wildebeest crossing the Mara River","The great herds on the move","A lantern lit bush dinner","A lion on the savanna"],
  daylist=[
   ("Into the Mara","Fly from Nairobi to the Mara. Lunch in camp, then your first game drive among the herds and a sundowner on the plains.","Luxury tented camp, Maasai Mara","Lunch, dinner"),
   ("Following the herds","A full day with your guide following the migration, with a picnic lunch out on the plains.","Luxury tented camp","All"),
   ("The river","Head to the Mara River for the chance of a crossing, one of nature's most dramatic sights. Patience is rewarded here.","Luxury tented camp","All"),
   ("Above it all","Dawn hot air balloon flight over the herds and a champagne breakfast. Afternoon massage in camp and an evening game drive.","Luxury tented camp","All"),
   ("Bush dinner","A last full day on the plains, ending with a lantern lit bush dinner and a closing circle under the stars.","Luxury tented camp","All"),
   ("Farewell","A final sunrise drive and breakfast, then fly back to Nairobi.","","Breakfast")],
  incl=["5 nights in a luxury tented camp on the migration route, all meals","Return flights Nairobi to the Maasai Mara","Twice daily game drives with expert guides","Park and conservancy fees","Hot air balloon flight with champagne breakfast","One massage per guest","Lantern lit bush dinner","Female Rendile host throughout &amp; all gratuities"],
  extra="",
  cta=("See it once. Feel it forever.","Six days at the height of the migration. Tell us a little about you and we'll hold your place.")),

 dict(slug="sun-and-soul-greece", code="aug", month="August", mon="Aug", region="Europe",
  title="Sun &amp; Soul", sub="Island living between Santorini and Naxos",
  dates="23 to 29 Aug 2027", days=7, place="Santorini &amp; Naxos, Greece", price="6,500",
  seo="Greece women's retreat, Santorini retreat for women, Greek islands trip women, sailing retreat Greece, women only travel Europe",
  lead="Whitewashed villages, caldera sunsets and long Greek lunches by the sea. Seven days island living, from the cliffs of Santorini to the golden beaches of Naxos, with a day under sail in between.",
  body=["Late August brings warm water, clear skies and the gentle meltemi breeze. We start high above the caldera in Santorini, then sail to Naxos, the island the Greeks keep for themselves.",
        "Expect yoga at sunrise, swims at noon and dinners that stretch into the night."],
  theme="Shine. Sail. Savour.",
  pillars=[("Shine","Sunrise yoga on a caldera terrace, a sunset in Oia and a photo shoot in Santorini's white lanes with a female photographer."),
           ("Sail","A private catamaran from Santorini to the hot springs and on to Naxos, with swimming stops and lunch on board."),
           ("Savour","Wine tasting in Santorini's volcanic vineyards, a Naxian cooking class and long dinners by the water.")],
  gallery=["The whitewashed village of Oia in Santorini","A woman by the sea on a Greek island","A seaside dinner on a Greek island at night","Friends laughing together on the beach"],
  daylist=[
   ("Kalos irthate","Arrive in Santorini and settle into your cave suite above the caldera. Welcome dinner on the terrace as the sun goes down.","Cave suite hotel, Santorini","Dinner"),
   ("The caldera","Sunrise yoga, a lazy morning by the pool, then a photo shoot in the lanes of Oia and the famous sunset.","Cave suite hotel, Santorini","Breakfast, dinner"),
   ("Volcanic vines","A wine tasting in Santorini's ancient vineyards and a free afternoon on the black sand beaches.","Cave suite hotel, Santorini","All"),
   ("Under sail","Board a private catamaran: swim in the hot springs, lunch on deck and sail on to Naxos for the evening.","Boutique hotel, Naxos","All"),
   ("Naxos days","Golden beaches, the old town and a Naxian cooking class in a village kitchen.","Boutique hotel, Naxos","All"),
   ("Soul time","A spa morning, a closing circle and a farewell dinner on the beach.","Boutique hotel, Naxos","All"),
   ("Antio","Breakfast by the sea, then transfer to the airport or ferry for your onward journey.","","Breakfast")],
  incl=["3 nights in a cave suite hotel in Santorini, 3 nights in a boutique hotel in Naxos","All transfers","Private catamaran day with lunch","Wine tasting in Santorini","Photo shoot with a female photographer","Naxian cooking class","Sunrise yoga and a spa morning","Most meals as shown","Female Rendile host throughout &amp; all gratuities"],
  extra="",
  cta=("Golden days are waiting.","Seven days of island light and slow living. Tell us a little about you and we'll hold your place.")),

 dict(slug="wild-wellness-rwanda", code="sep", month="September", mon="Sep", region="Africa",
  title="Wild Wellness", sub="Gorillas, forest bathing and mindfulness in Rwanda",
  dates="13 to 18 Sep 2027", days=6, place="Volcanoes &amp; Kigali, Rwanda", price="6,900",
  seo="Rwanda women's retreat, gorilla trekking for women, wellness retreat Rwanda, women only travel Africa, Volcanoes National Park retreat",
  lead="An hour face to face with mountain gorillas, misty volcano mornings and the creative energy of Kigali. Six days where wildness and wellness meet, in one of Africa's most beautiful and welcoming countries.",
  body=["Rwanda is the land of a thousand hills, and every one of them is green. We stay in a luxury lodge with volcano views, trek to the gorillas with expert trackers and slow down with forest bathing and spa time.",
        "Then we finish in Kigali, a city led by women in business, art and design."],
  theme="Trek. Breathe. Create.",
  pillars=[("Trek","A permitted gorilla trek in Volcanoes National Park for an unforgettable hour with a mountain gorilla family, plus a golden monkey trek."),
           ("Breathe","Guided forest bathing, yoga with volcano views and a spa ritual at the lodge."),
           ("Create","Kigali's women led art studios, fashion designers and cafes, and a visit to a women's weaving cooperative.")],
  gallery=["A mountain gorilla in the forest","Rwanda's green hills in the mist","Rwandan women dancing together","A woman resting in a quiet forest"],
  daylist=[
   ("Murakaza neza","Met in Kigali and driven north to the Volcanoes. Settle into your lodge and gather by the fire for a welcome dinner.","Luxury lodge, Volcanoes","Dinner"),
   ("Golden monkeys &amp; forest","A gentle golden monkey trek in the bamboo forest, then guided forest bathing and a spa afternoon.","Luxury lodge, Volcanoes","All"),
   ("The gorillas","The big day: trek with expert trackers to spend an hour with a mountain gorilla family. Celebrate with a sundowner and a quiet evening.","Luxury lodge, Volcanoes","All"),
   ("Lake Kivu or rest","Yoga with volcano views, then choose a day at the lodge or a drive to the twin lakes. Evening sharing circle.","Luxury lodge, Volcanoes","All"),
   ("Kigali, by women","Drive to Kigali for women led art studios, designers and a weaving cooperative, then a farewell dinner in the city.","Boutique hotel, Kigali","All"),
   ("Urabeho","Breakfast and a visit to the Kigali Genocide Memorial for those who wish, then transfer to the airport.","","Breakfast")],
  incl=["4 nights in a luxury lodge near Volcanoes National Park, 1 night in a boutique hotel in Kigali","Gorilla trekking permit (worth $1,500)","Golden monkey trek","All transfers with a private driver guide","Forest bathing, yoga and a spa ritual","Kigali art and design tour","Most meals as shown","Female Rendile host throughout &amp; all gratuities"],
  extra="Gorilla treks are moderately challenging; porters are included to help with your bag.",
  cta=("Meet the wild. Meet yourself.","Six days with the gorillas and the green hills of Rwanda. Tell us a little about you and we'll hold your place.")),

 dict(slug="mindful-asia-thailand", code="oct", month="October", mon="Oct", region="Asia",
  title="Mindful Asia", sub="Thai wellness traditions and island days in Krabi",
  dates="24 to 31 Oct 2027", days=8, place="Krabi, Thailand", price="4,400",
  seo="Thailand women's retreat, Krabi wellness retreat, women's yoga retreat Thailand, Thai massage retreat, women only travel Asia",
  lead="Limestone cliffs, emerald water and the healing traditions of Thailand. Eight days on the Andaman coast with meditation, Thai massage, island hopping by longtail boat and slow days on white sand beaches.",
  body=["Late October is when the Andaman coast wakes up after the rains: lush, green and calm. We stay in a beautiful beachfront resort in Krabi, with Railay and the islands a short boat ride away.",
        "Learn the art of Thai massage, sit with a meditation teacher and let the sea do the rest."],
  theme="Still. Restore. Explore.",
  pillars=[("Still","Daily meditation and yoga with a local teacher, and a morning of chanting and quiet at a Buddhist temple."),
           ("Restore","Traditional Thai massage, a herbal compress ritual and a hands on class to learn Thai massage yourself."),
           ("Explore","Longtail boats to Railay and the Hong islands, kayaking through mangroves and sunset on the beach.")],
  gallery=["Longtail boats on turquoise water in Krabi","A woman receiving a traditional Thai massage","A longtail boat in an emerald lagoon","A woman on the beach below limestone cliffs"],
  daylist=[
   ("Sawasdee","Arrive in Krabi and transfer to your beachfront resort. Welcome dinner and an evening intention circle.","Beachfront resort, Krabi","Dinner"),
   ("Settle in","Morning meditation and yoga, a traditional Thai massage and a free afternoon by the sea.","Beachfront resort, Krabi","All"),
   ("Railay","A longtail boat to Railay's dramatic beaches and cliffs, with swimming and lunch on the sand.","Beachfront resort, Krabi","All"),
   ("Temple morning","A morning of meditation and chanting with monks at a forest temple, then a herbal compress ritual at the spa.","Beachfront resort, Krabi","All"),
   ("The Hong islands","Island hopping to the hidden lagoons of the Hong islands by speedboat and kayak.","Beachfront resort, Krabi","All"),
   ("Learn Thai massage","A hands on class with a master teacher, then a cooking class making Thai curries and mango sticky rice.","Beachfront resort, Krabi","All"),
   ("Mangroves &amp; sunset","Kayak through the mangroves in the morning, closing circle in the afternoon and a farewell dinner on the beach.","Beachfront resort, Krabi","All"),
   ("La gon","A last swim and breakfast, then transfer to Krabi airport.","","Breakfast")],
  incl=["7 nights in a beachfront resort in Krabi","Airport transfers","Daily meditation and yoga","Temple meditation morning","Thai massage, herbal compress ritual and a Thai massage class","Longtail boat to Railay and Hong islands day trip","Mangrove kayaking and a Thai cooking class","Most meals as shown","Female Rendile host throughout &amp; all gratuities"],
  extra="",
  cta=("Breathe in the Andaman.","Eight days of stillness and sea. Tell us a little about you and we'll hold your place.")),

 dict(slug="lamu-yoga-retreat", code="nov", month="November", mon="Nov", region="Africa",
  title="Lamu Yoga Retreat", sub="Yoga, dhows and Swahili soul on the Kenyan coast",
  dates="8 to 12 Nov 2027", days=5, place="Lamu, Kenya", price="5,600",
  seo="Lamu yoga retreat, women's yoga retreat Kenya, Lamu Yoga Festival, Swahili coast retreat, women only retreat Africa",
  lead="Five days on the island of Lamu, where there are no cars, only donkeys, dhows and narrow stone streets. Join Kenya's beloved Lamu Yoga &amp; Wellbeing Festival with your own women's circle, beachfront yoga and Swahili feasts.",
  body=["Lamu Old Town is a UNESCO World Heritage Site and one of the oldest Swahili settlements in East Africa. Each year yoga teachers from around the world gather here for the festival, and the whole island seems to breathe more slowly.",
        "We stay in a beautiful Swahili house in Shela, a short walk from twelve kilometres of empty beach. Dates are timed to the festival and confirmed when it announces its programme."],
  theme="Flow. Sail. Belong.",
  pillars=[("Flow","Festival classes from yoga and meditation to dance and breathwork, plus our own private sunrise practice on the beach."),
           ("Sail","A sunset dhow cruise through the mangroves and a day sailing to the island of Manda with a seafood lunch on the sand."),
           ("Belong","Lamu Old Town with a Swahili guide, henna with local women and Swahili feasts in a beautiful old house.")],
  gallery=["A traditional dhow sailing at sunset","The Lamu waterfront","A dhow anchored in calm water","Women practising yoga together on the beach"],
  daylist=[
   ("Karibu Lamu","Fly from Nairobi to Lamu and cross by boat to Shela. Settle into your Swahili house and gather for a welcome dinner on the rooftop.","Swahili house, Shela","Lunch, dinner"),
   ("Festival day","Sunrise yoga on the beach, then festival classes of your choice. Evening sunset dhow cruise.","Swahili house, Shela","All"),
   ("Old Town","Morning festival classes, then a walk through Lamu Old Town with a Swahili guide and henna with local women.","Swahili house, Shela","All"),
   ("Manda by dhow","Sail to Manda island for swimming and a seafood lunch on the sand. Closing circle and farewell Swahili feast.","Swahili house, Shela","All"),
   ("Kwaheri","A final sunrise practice and breakfast, then boat and fly back to Nairobi.","","Breakfast")],
  incl=["4 nights in a Swahili house in Shela","Return flights Nairobi to Lamu and boat transfers","Lamu Yoga Festival pass","Private sunrise yoga on the beach","Sunset dhow cruise and Manda island sailing day","Old Town walk with a Swahili guide and henna","Most meals as shown","Female Rendile host throughout &amp; all gratuities"],
  extra="Dates are confirmed once the festival announces its programme.",
  cta=("Slow down to island time.","Five days of yoga, dhows and Swahili soul. Tell us a little about you and we'll hold your place.")),

 dict(slug="glow-and-celebrate-dubai", code="dec", month="December", mon="Dec", region="Middle East &amp; North Africa",
  title="Glow &amp; Celebrate", sub="A year end celebration in Dubai",
  dates="1 to 5 Dec 2027", days=5, place="Dubai, UAE", price="5,800",
  seo="Dubai women's retreat, girls trip Dubai, year end celebration trip women, luxury women's travel Middle East, women only retreat Dubai",
  lead="Close the year in style. Five days of desert sunsets, spa days, rooftop evenings and a farewell gala, to celebrate everything you did this year and everything you're becoming.",
  body=["December is Dubai at its best: sunny days, cool evenings and a city sparkling for the season. We stay in a luxury beachfront resort, with the desert and the old souks never far away.",
        "This is the retreat for raising a glass to yourself. You've earned it."],
  theme="Glow. Reflect. Celebrate.",
  pillars=[("Glow","A full spa day with a hammam ritual and facial, mornings by the pool and a styling session before the gala."),
           ("Reflect","A year end reflection circle in the desert at sunset, with journaling and intentions for the year ahead."),
           ("Celebrate","A desert dinner under the stars, a sunset yacht cruise past the skyline and a farewell gala dinner.")],
  gallery=["A woman in an evening gown by a luxury resort pool","A woman on a yacht in Dubai","Women laughing together over a candlelit dinner","A woman on the desert dunes at sunset"],
  daylist=[
   ("Welcome to Dubai","Arrive and check into your beachfront resort. Welcome cocktails and dinner overlooking the sea.","Luxury beach resort, Dubai","Dinner"),
   ("Spa &amp; souks","A full spa morning with a hammam ritual and facial, then the old town, spice souk and an abra ride across the creek.","Luxury beach resort, Dubai","Breakfast, dinner"),
   ("Desert at sunset","A slow morning, then into the desert for a reflection circle at sunset, journaling and a dinner under the stars.","Luxury beach resort, Dubai","All"),
   ("Yacht &amp; gala","A sunset yacht cruise past the skyline, then dress up for the farewell gala dinner.","Luxury beach resort, Dubai","All"),
   ("Until next year","A last breakfast by the sea, then transfer to the airport.","","Breakfast")],
  incl=["4 nights in a luxury beachfront resort","Airport transfers","Full spa day with hammam ritual and facial","Old town, souk and abra tour","Desert reflection circle and dinner under the stars","Sunset yacht cruise","Farewell gala dinner","Female Rendile host throughout &amp; all gratuities"],
  extra="",
  cta=("You did that. Now celebrate it.","Five days to close the year in style. Tell us a little about you and we'll hold your place.")),
]

DAYS = {
 "mar": ["Thu 4","Fri 5","Sat 6","Sun 7","Mon 8","Tue 9"],
 "apr": ["Mon 12","Tue 13","Wed 14","Thu 15","Fri 16","Sat 17","Sun 18","Mon 19"],
 "may": ["Mon 17","Tue 18","Wed 19","Thu 20","Fri 21","Sat 22","Sun 23"],
 "jun": ["Mon 7","Tue 8","Wed 9","Thu 10","Fri 11","Sat 12","Sun 13"],
 "jul": ["Mon 19","Tue 20","Wed 21","Thu 22","Fri 23","Sat 24"],
 "aug": ["Mon 23","Tue 24","Wed 25","Thu 26","Fri 27","Sat 28","Sun 29"],
 "sep": ["Mon 13","Tue 14","Wed 15","Thu 16","Fri 17","Sat 18"],
 "oct": ["Sun 24","Mon 25","Tue 26","Wed 27","Thu 28","Fri 29","Sat 30","Sun 31"],
 "nov": ["Mon 8","Tue 9","Wed 10","Thu 11","Fri 12"],
 "dec": ["Wed 1","Thu 2","Fri 3","Sat 4","Sun 5"],
}
POS = {"may":"18%","jun":"45%","dec":"55%","sep":"70%","jul":"30%","mar":"46%"}
NUM = {5:"Five",6:"Six",7:"Seven",8:"Eight"}
V = "?v=3"

def plain(s): return html.unescape(s)

# Calendar neighbours for the "More 2027 retreats" cards (Jan/Feb are hand written pages)
CAL = [("new-year-new-you","cal-jan","January","New Year, New You","Plan your year under Mount Kenya.")] + \
      [("self-love-retreat","cal-feb","February","The Self Love Retreat","Rest and self care on Zanzibar.")] + \
      [(r["slug"], ("trip-lamu" if r["code"]=="nov" else "cal-"+r["code"]), r["month"], plain(r["title"]), plain(r["sub"])+".") for r in R]

def page(r, idx):
    nights = r["days"] - 1
    trip = f'{plain(r["title"])} ({r["month"]} 2027)'
    days_html = []
    for i,(h,txt,stay,meals) in enumerate(r["daylist"]):
        stay_html = (f'<b>Stay:</b> {stay} · ' if stay else '') + f'<b>Meals:</b> {meals}'
        days_html.append(f'        <div class="day reveal"><div class="day__num">Day {i+1}<br/>{DAYS[r["code"]][i]}</div><div class="day__body"><h3>{h}</h3><p>{txt}</p><p class="day__stay">{stay_html}</p></div></div>')
    pillars = "\n".join(f'''        <article class="pillar reveal">
          <span class="pillar__num">0{i+1}</span>
          <h3>{t}</h3>
          <p>{p}</p>
        </article>''' for i,(t,p) in enumerate(r["pillars"]))
    gallery = "\n".join(f'        <img src="assets/img/{r["code"]}-{i+1}.jpg{V}" alt="{a}" loading="lazy" />' for i,a in enumerate(r["gallery"]))
    incl = "\n".join(f"          <li>{x}</li>" for x in r["incl"])
    body = "\n".join(f"        <p>{p}</p>" for p in r["body"])
    # related: next two retreats in the calendar, then the full calendar
    ci = idx + 2
    nxt = [CAL[(ci+1) % len(CAL)], CAL[(ci+2) % len(CAL)]]
    rel = "\n".join(f'''        <a class="feat" href="{s}.html"><div class="feat__img" style="background-image:url('assets/img/{img}.jpg{V}')"></div><div class="feat__body"><h3>{m} · {html.escape(t)}</h3><p>{html.escape(d)}</p></div></a>''' for s,img,m,t,d in nxt)
    desc = f'{plain(r["title"])}: a {r["days"]} day luxury retreat for women in {plain(r["place"])}, {r["dates"].replace("Mar","March").replace("Apr","April").replace("Jun","June").replace("Jul","July").replace("Aug","August").replace("Sep","September").replace("Oct","October").replace("Nov","November").replace("Dec","December")}. {plain(r["sub"])}. From ${r["price"]} per person.'
    jsonld = json.dumps({"@context":"https://schema.org","@type":"TouristTrip","name":f'{plain(r["title"])}, a women\'s retreat in {plain(r["place"])}',"description":plain(r["lead"]),"image":f'https://rendiletravels.com/assets/img/{r["code"]}-hero.jpg',"touristType":"Women","provider":{"@type":"Organization","name":"Rendile Travels"},"offers":{"@type":"Offer","price":r["price"].replace(",",""),"priceCurrency":"USD","availability":"https://schema.org/LimitedAvailability"}}, ensure_ascii=False)
    extra = f' {r["extra"]}' if r["extra"] else ""
    return f'''---
// Generated by tools/retreats.py. Edit the data there and re-run, or edit this file by hand.
import Base from '../layouts/BaseLayout.astro';
const trip = {json.dumps(trip)};
const enquire = `contact.html?trip=${{encodeURIComponent(trip)}}`;
---
<Base
  title={{`{plain(r["title"])} | Women's Retreat, {plain(r["place"])} | Rendile Travels`}}
  description={{`{desc}`}}
  ogTitle={{`{plain(r["title"])} | {plain(r["sub"])} | Rendile Travels`}}
  ogDescription={{`{plain(r["lead"])}`}}
  ogType={{`website`}}
  ogImage={{`https://rendiletravels.com/assets/img/{r["code"]}-hero.jpg`}}
  canonical={{`https://rendiletravels.com/{r["slug"]}.html`}}
  keywords={{`{r["seo"]}`}}
  jsonld={{`{jsonld}`}}
  credit={{`Photography via Pexels.`}}
>

  <section class="page-hero">
    <div class="page-hero__media" style="background-image:url('assets/img/{r["code"]}-hero.jpg{V}');background-position:center {POS.get(r["code"],"center")}"></div>
    <div class="page-hero__scrim"></div>
    <div class="container page-hero__content">
      <p class="eyebrow eyebrow--light reveal">{r["month"]} 2027 · {r["region"]} retreat</p>
      <h1 class="reveal">{r["title"]}</h1>
      <p class="page-hero__sub reveal">{r["sub"]}</p>
      <div class="itin-meta reveal">
        <span><b>{r["dates"]}</b></span>
        <span>{r["days"]} days</span>
        <span>{r["place"]}</span>
        <span>Women only</span>
        <span>from <b>${r["price"]}</b> / person</span>
      </div>
      <div class="hero__actions reveal" style="margin-top:1.6rem"><a href={{enquire}} class="btn btn--gold">Reserve your place</a></div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="article reveal">
        <nav class="breadcrumb"><a href="index.html">Home</a> / <a href="index.html#calendar">2027 retreats</a> / {r["title"]}</nav>
        <p class="article__lead">{r["lead"]}</p>
{body}
      </div>
    </div>
  </section>

  <section class="section section--cream pillars">
    <div class="container">
      <div class="section__head reveal"><p class="eyebrow">The theme</p><h2 class="section__title">{r["theme"]}</h2></div>
      <div class="pillars__grid">
{pillars}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="gallery__grid reveal">
{gallery}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section__head reveal"><p class="eyebrow">Day by day</p><h2 class="section__title">Your {r["days"]} day retreat</h2></div>
      <div class="days">
{chr(10).join(days_html)}
      </div>
    </div>
  </section>

  <section class="section section--cream">
    <div class="container">
      <div class="incl reveal">
        <div class="section__head section__head--left"><p class="eyebrow">All taken care of</p><h2 class="section__title">What's included</h2></div>
        <ul class="incl__grid">
{incl}
        </ul>
        <p style="margin-top:1.2rem;color:var(--ink-soft)">From <strong>${r["price"]} per person sharing</strong>; single room supplement available. International flights, visas and travel insurance are not included. Places are limited and held on a first come basis.{extra}</p>
      </div>
    </div>
  </section>

  <section class="cta-band">
    <div class="container reveal"><h2>{r["cta"][0]}</h2><p>{r["cta"][1]}</p><a href={{enquire}} class="btn btn--gold">Reserve your place</a></div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section__head reveal"><p class="eyebrow">Next on the calendar</p><h2 class="section__title">More 2027 retreats</h2></div>
      <div class="related__grid reveal">
{rel}
        <a class="feat" href="index.html#calendar"><div class="feat__img" style="background-image:url('assets/img/cal-apr.jpg')"></div><div class="feat__body"><h3>The full 2027 calendar</h3><p>Themed retreats to rest, reconnect and rise.</p></div></a>
      </div>
    </div>
  </section>

</Base>
'''

if __name__ == "__main__":
    for i, r in enumerate(R):
        p = f"src/pages/{r['slug']}.astro"
        open(p, "w").write(page(r, i))
        print("wrote", p)
